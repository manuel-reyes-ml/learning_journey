"""Configure structlog on top of stdlib logging so every log shares one pipeline.

Our events (structlog) and third-party events (stdlib ``logging``) end up in the
same handlers, are shaped by the same processors, and are written in the same
formats: aligned colors on the console, JSON lines in the optional log file.
With ``LOG_FORMAT=json`` (containers), the console writes JSON lines too.

See Also
--------
learning_journey.cli.run : Binds ``run_id`` and logs each command's outcome.

Notes
-----
How a log event travels::

    log.info("table_loaded", rows=10)          logging.getLogger("duckdb").warning("...")
            |  (our code, structlog)                     |  (third-party code, stdlib)
            v                                            |
    structlog processors                                 |
    (filter_by_level -> SHARED -> wrap_for_formatter)    |
            |                                            |
            +--------------> stdlib logging <------------+
                     (root logger: levels, handlers)
                    +-----------+------------+
                    v                        v
            console handler (stderr)    file handler (--log-file, opt-in)
            ProcessorFormatter:         ProcessorFormatter:
              ConsoleRenderer             callsite -> dict traceback -> JSON
              (aligned colors for         (one JSON object per line,
               people), or the JSON        for machines)
               chain if LOG_FORMAT=json

``wrap_for_formatter`` hands our event dict to stdlib *unrendered*, and each
handler's ``ProcessorFormatter`` renders it its own way. Third-party records skip
structlog's chain, so ``foreign_pre_chain`` runs the same SHARED processors on
them first. That gives every line the same shape, whichever library wrote it.

Call `configure_logging` once, from an entry point (a script's ``main()``). Never
call it at import time or from library code: libraries only *emit* logs; the
application decides where they go.

The module is named ``logging_setup`` rather than ``logging`` because a file
called ``logging.py`` can shadow the stdlib module when something is run from
inside its folder.
"""

from __future__ import annotations

import logging
import logging.config
import os
import sys
from pathlib import Path
from typing import TYPE_CHECKING, Any, Final, Literal

import structlog
from structlog.typing import EventDict, Processor, WrappedLogger

if TYPE_CHECKING:
    from logging.config import _DictConfigArgs

__all__ = [
    "REDACTED",
    "LogFormat",
    "configure_logging",
    "get_logger",
    "redact_sensitive",
]


#: How the console handler renders events: text for people, or JSON lines for
#: machines (containers, log collectors).
LogFormat = Literal["console", "json"]

#: Environment variable read when `configure_logging` gets no ``log_format``.
LOG_FORMAT_ENV: Final[str] = "LOG_FORMAT"

#: Root of our logger namespace. Name loggers ``learning_journey.<area>.<name>``.
APP_LOGGER: Final[str] = "learning_journey"

#: Replacement value written in place of a sensitive field.
REDACTED: Final[str] = "[REDACTED]"

# Keys whose values must never reach a log, compared case-insensitively.
# This is a key-based safety net, not a full PII scanner: it complements value-level
# checks (regex guardrails), it does not replace them.
_SENSITIVE_KEYS: Final[frozenset[str]] = frozenset(
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


# numpydoc ignore=PR02 below: the linter cannot see the __init__ inherited from logging.Filter.
class OnlyThirdParty(logging.Filter):  # numpydoc ignore=PR02
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
    # 1. merge_contextvars  -> pull in any bind_contextvars() values (run_id, command)
    # 2. add_logger_name    -> add "logger" field (e.g. "learning_journey.scripts.load_market_seed")
    # 3. add_log_level      -> add "level" field ("info", "error", ...)
    # 4. ExtraAdder         -> turn a stdlib call's extra={...} into fields
    # 5. TimeStamper("iso") -> add "timestamp" field in ISO-8601, UTC
    # 6. StackInfoRenderer  -> format stack_info if present
    # 7. redact_sensitive   -> mask sensitive keys; last, so nothing added after it skips the mask
    #
    # Exceptions are NOT formatted here: each handler renders them its own way
    # (a Rich traceback on the console, a JSON field in the file):
    #   8. format_exc_info    → serialize exc_info tuples into "exception" field - one text string
    return [
        structlog.contextvars.merge_contextvars,  # run_id, command, ... bound once per run
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.ExtraAdder(),  # third-party `extra={...}` becomes fields
        structlog.processors.TimeStamper(fmt="iso", utc=True),
        structlog.processors.StackInfoRenderer(),
        redact_sensitive,  # our own processor; last, so nothing added after it skips the mask
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
        structlog.processors.JSONRenderer(default=str),
    ]


def _resolve_log_format(log_format: LogFormat | None) -> LogFormat:
    """Pick the console format: the argument, else ``LOG_FORMAT``, else console.

    Parameters
    ----------
    log_format : LogFormat or None
        The format passed to `configure_logging`. If not None it wins, so tests
        and callers never depend on the environment.

    Returns
    -------
    LogFormat
        ``"console"`` or ``"json"``.

    Raises
    ------
    ValueError
        If ``LOG_FORMAT`` is set to anything other than ``console`` or ``json``
        (case and surrounding spaces are ignored).

    Notes
    -----
    A typo such as ``LOG_FORMAT=jsn`` fails at startup instead of silently
    falling back to text, which would leave a log collector with unparseable
    lines and no warning.
    """
    if log_format is not None:
        return log_format
    value = os.environ.get(LOG_FORMAT_ENV, "console").strip().lower()
    match value:
        case "console":
            return "console"
        case "json":
            return "json"

    raise ValueError(f"{LOG_FORMAT_ENV} must be 'console' or 'json', got {value!r}")


# (log_format=...) is a new parameter, either "console" or "json". When the code passes it,
# it wins; otherwise the LOG_FORMAT environment variable decides, and the default is "console".
# That way tests never depend on your shell.
def configure_logging(
    *,
    verbosity: int = 0,
    log_file: Path | None = None,
    log_format: LogFormat | None = None,
    cache_loggers: bool = True,
) -> None:
    """Configure structlog and stdlib logging for one process run.

    Parameters
    ----------
    verbosity : int, optional
        Console detail. 0 shows only third-party WARNING and above, because Rich
        speaks for our own code. 1 (``-v``) shows all INFO and above; 2 or more
        (``-vv``) shows all DEBUG and above. Default is 0. In JSON format the
        console starts at INFO instead (see Notes).
    log_file : Path or None, optional
        If given, also append every DEBUG-and-above event to this file as JSON
        lines; parent folders are created. Default is None: nothing is written
        to disk.
    log_format : {"console", "json"} or None, optional
        How the console handler renders events. ``"console"``: aligned text for
        people. ``"json"``: one JSON object per line, for containers and log
        collectors. Default is None, which reads the ``LOG_FORMAT`` environment
        variable and falls back to ``"console"``.
    cache_loggers : bool, optional
        Cache each logger's configuration on first use. Keep True in
        production (faster). Tests that reconfigure structlog, for example with
        `structlog.testing.capture_logs`, pass False; otherwise loggers already
        used keep the old configuration. Default is True.

    Raises
    ------
    ValueError
        If ``log_format`` is None and ``LOG_FORMAT`` holds an unknown value.

    See Also
    --------
    learning_journey.cli.add_observability_args : Adds the matching CLI flags.

    Notes
    -----
    Safe to call more than once: `logging.config.dictConfig` closes and replaces
    the previous handlers instead of stacking new ones on top.

    In JSON format the console stream *is* the record (a container has no log
    file), so two console rules change:

    * Our own events are kept: the third-party-only filter is not applied.
    * The console starts at INFO even at verbosity 0; ``-vv`` still adds DEBUG.

    Settings worth knowing in the configuration below:

    * ``disable_existing_loggers=False`` keeps loggers that libraries created at
      import time working. The default (True) silently mutes them.
    * Console logs go to stderr, never stdout, because they are diagnostics.
      Docker collects stderr too, so JSON mode needs no other stream.
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

    In a container, set the format once in the Dockerfile instead::

        ENV LOG_FORMAT=json
    """
    # Optional JSON formatted stdout when env var is passed (for Docker, CI, etc)
    json_console = _resolve_log_format(log_format) == "json"
    console_level = _VERBOSITY_TO_LEVEL.get(verbosity, logging.DEBUG)

    # For console's json output always generate at least INFO level
    if json_console:
        console_level = min(console_level, logging.INFO)

    # isatty() returns True only when stderr is a real terminal. In CI, a pipe
    # or a redirect to a file it's False, so colors are switched off there and
    # the output isn't full of escape codes.
    colors = sys.stderr.isatty() and not os.environ.get("NO_COLOR")
    shared = _shared_processors()

    handlers: dict[str, dict[str, Any]] = {
        "console": {
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
            "level": console_level,
            "formatter": "json" if json_console else "console",
            "filters": ["only_third_party"] if verbosity == 0 and not json_console else [],
        },
    }
    # Why not RotatingFileHandler? A short CLI run that appends grows the file slowly.
    # Rotation becomes unsafe if two runs write to the same file at once, and your
    # roadmap leaves rotation to the environment (logrotate or Docker). If you add
    # logrotate later, switch to WatchedFileHandler.
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

    # dictConfig wants a recipe it can build from, not the finished object, chose for two reasons:
    #   - It's safe to call more than once. dictConfig closes and replaces the root logger's old
    #     handlers. In the hand-built style, a second call without cleanup adds a second handler,
    #     so every line prints twice.
    #   - The whole setup is one data structure. You can read all handlers, levels and formatters
    #     in one place, and later move them into a settings file. # TODO move to a settings file?
    # "()" in dictConfig means “call this to build the object”. All the other keys in that dict are
    # passed to it as keyword arguments, so {"()": ProcessorFormatter, "processors": [...]} runs
    # ProcessorFormatter(processors=[...]). That's also why the "processor" typo didn't fail at
    # setup: it's a real (old) argument of ProcessorFormatter.
    config: _DictConfigArgs = {
        "version": 1,
        "disable_existing_loggers": False,
        "filters": {"only_third_party": {"()": OnlyThirdParty}},
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
                "processors": _file_processor(),
            },
        },
        "handlers": handlers,
        "root": {
            "level": logging.DEBUG if log_file else console_level,
            "handlers": list(handlers),
        },
    }
    # dictConfig doesn't check its keys, so typos fail silently.
    # The type stubs that mypy and Pyright use describe dictConfig's settings as
    # a typed dict called _DictConfigArgs. Annotate your config with it.
    logging.config.dictConfig(config)
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


def get_logger(name: str | None = None) -> structlog.stdlib.BoundLogger:
    """Return a structlog logger that writes through the stdlib pipeline.

    Parameters
    ----------
    name : str or None, optional
        Logger name. Package modules pass ``__name__``; scripts pass
        ``"learning_journey.scripts.<command>"``, because ``__name__`` is
        ``"__main__"`` there. Default is None: structlog uses the calling
        module's name.

    Returns
    -------
    structlog.stdlib.BoundLogger
        A lazy logger; it picks up the configuration on first use, so it is safe
        to create at import time, before `configure_logging` runs.

    Notes
    -----
    ``None`` must not be passed through to structlog: ``get_logger(None)``
    returns the root logger.

    Examples
    --------
    >>> log = get_logger("learning_journey.scripts.load_market_seed")
    >>> log.info("table_loaded", table="bars_daily", rows=2)  # doctest: +SKIP
    """
    if name is None:
        return structlog.stdlib.get_logger()
    return structlog.stdlib.get_logger(name)
