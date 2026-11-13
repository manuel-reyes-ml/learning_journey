""" """

from __future__ import annotations

import logging
import logging.config
import os
import sys
from pathlib import Path
from typing import Any, Final

import structlog
from structlog.typing import EventDict, Processor, WrappedLogger

#: Root of our logger namespace. Name loggers ``learning_journey.<area>.<name>``.
APP_LOGGER: Final[str] = "learning_journey"

#: Replacement value written in place of a sensitive field.
REDACTED: Final[str] = "[REDACTED]"

# Keys whose values must never reach a log, compared case-insensitively.
# This is a key-based safety net, not a full PII scanner: it complements value-level
# checks (regex guardrails), it does not replace them.
_SENSITIVE_KEYS: Final[frozenset] = frozenset(
    {
        "password",
        "passwd",
        "secret",
        "token",
        "api_key",
        "authorization",
        "ssn",
        "tin",
        "account_number",
        "routing_number",
    }
)

_VERBOSITY_TO_LEVEL: Final[dict[int, int]] = {0: logging.WARNING, 1: logging.INFO, 2: logging.DEBUG}


def redact_sensitive(_logger: WrappedLogger, _method: str, event_dict: EventDict) -> EventDict:
    """Mask the values of sensitive keys on every event.

    A structlog processor. It sits in the shared chain, so it runs for our events
    and for third-party records alike; no call site has to remember to mask.

    Parameters
    ----------
    _logger : WrappedLogger
        The wrapped logger. Required by the processor protocol; unused.
    _method : str
        The name of the log method called (``"info"``, ``"error"``, ...).
        Required by the processor protocol; unused.
    event_dict : EventDict
        The event being processed. Modified in place.

    Returns
    -------
    EventDict
        The same event, with the value of every key in the sensitive-key set
        (compared case-insensitively) replaced by `REDACTED`.

    Examples
    --------
    >>> redact_sensitive(None, "info", {"event": "login", "SSN": "123-45-6789"})
    {'event': 'login', 'SSN': '[REDACTED]'}
    """
    for key in event_dict:
        if key.lower() in _SENSITIVE_KEYS:
            event_dict[key] = REDACTED
    return event_dict


# numpydoc ignore=PR02 below: the linter cannot see the __init__ inherited from logging.Filter.
class OnlyThirdyParty(logging.Filter):  # numpydoc ignore=PR02
    """Keep log records from other packages and drop our own.

    Attached to the console handler at default verbosity. Rich already shows the
    user everything our own code has to say, so printing our log lines as well
    would show every message twice. Warnings from libraries are different:
    nothing else would tell the user about them.

    Parameters
    ----------
    name : str, optional
        Inherited from `logging.Filter`; not used by this filter. Default is ``""``.
    """

    def filter(self, record: logging.LogRecord) -> bool:
        """Decide whether a record reaches the handler.

        Parameters
        ----------
        record : logging.LogRecord
            The record about to be emitted.

        Returns
        -------
        bool
            False if the record's logger is `APP_LOGGER` or one of its children,
            True otherwise.
        """
        name = record.name
        return not (name == APP_LOGGER or name.startswith(f"{APP_LOGGER}."))


def _shared_processors() -> list[Processor]:
    """Build the processors applied to every event, structlog or stdlib.

    Returns
    -------
    list[Processor]
        Context merge, logger name, level, ``extra=`` fields, UTC timestamp,
        stack info and, last, `redact_sensitive`, so nothing added afterwards
        can skip the mask.
    """
    # Shared processors run on every log entry regardless of origin:
    #   - structlog.get_logger().info(...)     → native structlog path
    #   - logging.getLogger(__name__).info(...) → stdlib path via ProcessorFormatter
    #
    # Order matters. Each processor receives the event_dict and returns
    # a (possibly modified) event_dict passed to the next processor.
    #
    # 1. merge_contextvars  → pull in any bind_contextvars() values
    # 2. add_logger_name    → add "logger" field (e.g. "learning_journey.recon_toy")
    # 3. add_log_level      → add "level" field ("info", "error", ...)
    # 4. TimeStamper("iso") → add "timestamp" field in ISO-8601
    # 5. StackInfoRenderer  → format stack_info if present
    # 6. format_exc_info    → serialize exc_info tuples into "exception" field
    return [
        structlog.contextvars.merge_contextvars,  # run_id, command, ... bound once per run
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.ExtraAdder(),  # third-party `extra={...}` becomes fields
        structlog.processors.TimeStamper(fmt="iso", utc=True),
        structlog.processors.StackInfoRenderer(),
        redact_sensitive,  # our own processor
    ]


def _console_renderer(*, colors: bool) -> Processor:
    """Build the renderer for the human-readable console stream.

    Parameters
    ----------
    colors : bool
        True for ANSI colors and Rich tracebacks (interactive terminal); False
        for plain text and plain tracebacks (CI, pipes, ``NO_COLOR``).

    Returns
    -------
    Processor
        A configured `structlog.dev.ConsoleRenderer`.

    Notes
    -----
    Tracebacks never show local variables: they can hold participant data.
    """
    exception_formatter = (
        structlog.dev.RichTracebackFormatter(show_locals=False)
        if colors
        else structlog.dev.plain_traceback
    )
    return structlog.dev.ConsoleRenderer(colors=colors, exception_formatter=exception_formatter)


def _file_processor() -> list[Processor]:
    """Build the formatter chain that writes JSON lines to the log file.

    Returns
    -------
    list[Processor]
        Call-site fields, metadata removal, a structured traceback and the
        JSON renderer, in that order.

    Notes
    -----
    * ``CallsiteParameterAdder`` reads module, function and line from the
      ``LogRecord``, so it must run before ``remove_processors_meta`` deletes
      the ``_record`` key.
    * The traceback becomes a JSON field, so one error is one line in the file.
      ``show_locals=False`` is set explicitly because it defaults to True.
    * ``default=str`` writes ``Path``, ``Decimal``, ``datetime`` and similar
      values as plain strings instead of ``repr()`` noise such as
      ``PosixPath('...')``.
    """
    callsite = structlog.processors.CallsiteParameter
    return [
        structlog.processors.CallsiteParameterAdder(
            {callsite.MODULE, callsite.FUNC_NAME, callsite.LINENO}
        ),
        # The 'remove_processors_meta' processor strips '_record' and '_from_structlog'
        # keys before rendering so they don't appear in output.
        structlog.stdlib.ProcessorFormatter.remove_processors_meta,
        structlog.processors.ExceptionRenderer(
            structlog.tracebacks.ExceptionDictTransformer(show_locals=False)
        ),
        structlog.processors.JSONRenderer(defaul=str),
    ]


def configure_logging(
    *,
    verbosity: int = 0,
    log_file: Path | None = None,
    cache_loggers: bool = True,
) -> None:
    """Configure structlog and stdlib logging for one process run.

    Parameters
    ----------
    verbosity : int, optional
        Console detail. 0 shows only third-party WARNING and above, because Rich
        speaks for our own code. 1 (``-v``) shows all INFO and above; 2 or more
        (``-vv``) shows all DEBUG and above. Default is 0.
    log_file : Path or None, optional
        If given, also append every DEBUG-and-above event to this file as JSON
        lines; parent folders are created. Default is None: nothing is written
        to disk.
    cache_loggers : bool, optional
        Cache each logger's configuration on first use. Keep True in
        production (faster). Tests that reconfigure structlog, for example with
        `structlog.testing.capture_logs`, pass False; otherwise loggers already
        used keep the old configuration. Default is True.

    See Also
    --------
    learning_journey.cli.add_observability_args : Adds the matching CLI flags.

    Notes
    -----
    Safe to call more than once: `logging.config.dictConfig` closes and replaces
    the previous handlers instead of stacking new ones on top.

    Settings worth knowing in the configuration below:

    * ``disable_existing_loggers=False`` keeps loggers that libraries created at
      import time working. The default (True) silently mutes them.
    * Console logs go to stderr, never stdout, because they are diagnostics.
    * The root level is the lowest level any handler needs; each handler then
      applies its own threshold.
    * ``logging.captureWarnings(True)`` turns ``warnings.warn(...)`` calls into
      ``py.warnings`` log records, so they reach the same handlers.
    * ``filter_by_level`` runs first in structlog's chain and drops events no
      handler wants before any processing work. stdlib levels are the single
      source of truth for filtering.

    Examples
    --------
    >>> from pathlib import Path
    >>> configure_logging(verbosity=1, log_file=Path("logs/run.jsonl"))  # doctest: +SKIP
    """
    console_level = _VERBOSITY_TO_LEVEL.get(verbosity, logging.DEBUG)
    colors = sys.stderr.isatty() and not os.environ.get("NO_COLOR")
    shared = _shared_processors()

    handlers: dict[str, dict[str, Any]] = {
        "console": {
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
            "level": console_level,
            "formatter": "console",
            "filters": ["only_third_party"] if verbosity == 0 else [],
        },
    }
    if log_file is not None:
        log_file = log_file.expanduser().resolve()
        log_file.parent.mkdir(parents=True, exist_ok=True)
        handlers["file"] = {
            "class": "logging.FileHandler",
            "filename": str(log_file),
            "mode": "a",  # append: each run adds lines, the run_id tells runs apart
            "encoding": "utf-8",
            "delay": True,  # create the file only when the first record arrives
            "level": logging.DEBUG,
            "formatter": "json",
        }

    logging.config.dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "filters": {"only_third_party": {"()": OnlyThirdyParty}},
            "formatters": {
                "console": {
                    "()": structlog.stdlib.ProcessorFormatter,
                    "foreign_pre_chain": shared,
                    "processors": [
                        structlog.stdlib.ProcessorFormatter.remove_processors_meta,
                        _console_renderer(colors=colors),
                    ],
                },
                "json": {
                    "()": structlog.stdlib.ProcessorFormatter,
                    "foreign_pre_chain": shared,
                    "processor": _file_processor(),
                },
            },
            "handlers": handlers,
            "root": {
                "level": logging.DEBUG if log_file else console_level,
                "handler": list(handlers),
            },
        }
    )
    logging.captureWarnings(True)

    structlog.configure(
        processors=[
            structlog.stdlib.filter_by_level,
            *shared,  # unpack list of Processors list
            # Must be last: hand the event dict to stdlib unrendered.
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        ],
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=cache_loggers,
    )
