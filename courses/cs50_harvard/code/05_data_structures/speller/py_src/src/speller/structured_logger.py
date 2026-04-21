"""
"""

# =============================================================================
# IMPORTS
# =============================================================================

from __future__ import annotations

from logging.handlers import RotatingFileHandler
from typing import Final
import logging
import sys

import structlog
from structlog.types import Processor

from speller.config import (
    file_dirs,
    fhandler_config,
    FileDirectories,
    FileHandlerConfig,
)

# No ImportError sys.exit() on regular module so the
# error propagates to the caller (__main__.py).


# =============================================================================
# EXPORTS
# =============================================================================

__all__ = []


# =============================================================================
# MODULE CONFIGURATION
# =============================================================================
# =====================================================
# Shared Processor Chain
# =====================================================

# Shared processors run on every log entry regardless of origin:
#   - structlog.get_logger().info(...)     → native structlog path
#   - logging.getLogger(__name__).info(...) → stdlib path via ProcessorFormatter
#
# Order matters. Each processor receives the event_dict and returns
# a (possibly modified) event_dict passed to the next processor.
#
# 1. merge_contextvars  → pull in any bind_contextvars() values
# 2. add_logger_name    → add "logger" field (e.g. "speller.dictionaries")
# 3. add_log_level      → add "level" field ("info", "error", ...)
# 4. TimeStamper("iso") → add "timestamp" field in ISO-8601
# 5. StackInfoRenderer  → format stack_info if present
# 6. format_exc_info    → serialize exc_info tuples into "exception" field
_SHARED_PROCESSORS: Final[list[Processor]] = [
    structlog.contextvars.merge_contextvars,
    structlog.stdlib.add_logger_name,
    structlog.stdlib.add_log_level,
    structlog.processors.TimeStamper(fmt="iso"),
    structlog.processors.StackInfoRenderer(),
    structlog.processors.format_exc_info,
]


# =============================================================================
# INTERNAL HELPER FUNCTIONS
# =============================================================================

def _setup_chandler(
    *,
    level: int,
    custom_console: bool = True,
) -> logging.StreamHandler:
    """Create and configure a structlog-aware console (stream) handler.
 
    Writes to ``sys.stderr`` so log output and program output
    (``stdout``) remain on separate streams and can be redirected
    independently — matches :mod:`speller.logger`.
 
    Uses :class:`structlog.dev.ConsoleRenderer` as the final renderer
    for pretty, aligned, colored ``key=value`` output optimised for
    developers.  Stack traces are pretty-printed with syntax
    highlighting when :class:`structlog.dev.RichTracebackFormatter`
    is available.
 
    Parameters
    ----------
    level : int
        Minimum log level for this handler (e.g. ``logging.INFO``).
        Derived from the ``--verbose`` flag in ``__main__.py``.
    custom_console : bool, optional
        ``True`` (default) enables ANSI colors.  Set ``False`` in
        tests to suppress colors from captured output.
 
    Returns
    -------
    logging.StreamHandler
        Fully configured handler ready to attach to a logger.
 
    Notes
    -----
    Why ``ProcessorFormatter`` instead of a regular ``Formatter``?
        ``ProcessorFormatter`` is a :class:`logging.Formatter`
        subclass that runs structlog's processor pipeline on
        :class:`~logging.LogRecord` objects.  This means stdlib
        ``logging.getLogger(__name__).info(...)`` calls flow through
        the SAME processor chain as native ``structlog.get_logger()``
        calls — consistent output regardless of origin.
 
    Why ``foreign_pre_chain`` equals the shared processors?
        ``foreign_pre_chain`` only runs on non-structlog entries
        (stdlib logs).  Setting it to ``_SHARED_PROCESSORS`` ensures
        stdlib logs get timestamps, log levels, and bound context
        just like structlog logs.  The ``remove_processors_meta``
        processor strips ``_record`` and ``_from_structlog`` keys
        before rendering so they don't appear in output.
    """
    console_handler = logging.StreamHandler(sys.stderr)
    console_handler.setLevel(level)
    console_handler.setFormatter(
        structlog.stdlib.ProcessorFormatter(
            # Runs ONLY on non-structlog (stdlib) log records
            foreign_pre_chain=_SHARED_PROCESSORS,
            # Runs on ALL records (structlog + stdlib) before rendering
            processors=[
                structlog.stdlib.ProcessorFormatter.remove_processors_meta,
                structlog.dev.ConsoleRenderer(colors=custom_console),
            ]
        )
    )
    return console_handler


def _setup_fhandler(
    file_dirs: FileDirectories = file_dirs,
    fhandler_config: FileHandlerConfig = fhandler_config,
) -> RotatingFileHandler:
    """Create and configure a rotating JSON file handler.
 
    Always captures ``DEBUG`` level regardless of console verbosity
    so full diagnostic information is available on disk even when
    the console shows only ``INFO``.  Reuses the singleton
    :class:`~speller.config.FileHandlerConfig` for size/rotation
    settings — same disk budget as the plain-text handler.
 
    Uses :class:`structlog.processors.JSONRenderer` as the final
    renderer for NDJSON output (one JSON object per line).  This is
    the format expected by ``jq``, DuckDB's ``read_json_auto``, and
    every major log aggregation platform.
 
    Parameters
    ----------
    file_dirs : FileDirectories, optional
        Provides the log file path.  Defaults to the module-level
        singleton from :mod:`speller.config`.
    fhandler_config : FileHandlerConfig, optional
        Provides size and rotation settings.  Defaults to the
        module-level singleton from :mod:`speller.config`.
 
    Returns
    -------
    RotatingFileHandler
        Fully configured handler ready to attach to a logger.
 
    Notes
    -----
    Why a separate log file (``speller_structured.log``)?
        Running ``--structured-logging`` and ``--template-logging``
        on the same batch would otherwise overwrite each other's
        files.  Separate paths let you diff the output of the three
        logging backends directly.
 
    Why ``JSONRenderer()`` rather than the stdlib ``JsonTemplateFormatter``?
        :class:`~speller.template_logger.JsonTemplateFormatter` is
        a hand-rolled renderer for t-string interpolations — it
        extracts values from a single template per call.
        ``JSONRenderer`` serialises the full event dictionary
        including ALL bound context variables in one pass.  That
        matters when downstream code adds fields via
        ``bind_contextvars``: those fields appear automatically in
        every log line without the emitting code knowing about them.
    """
    file_handler = RotatingFileHandler(
        filename=file_dirs.log_file.slog_path,
        maxBytes=fhandler_config.max_log_bytes,
        backupCount=fhandler_config.BACKUP_COUNT,
        encoding=fhandler_config.ENCODING,
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(
        structlog.stdlib.ProcessorFormatter(
            # Runs ONLY on non-structlog (stdlib) log records
            foreign_pre_chain=_SHARED_PROCESSORS,
            # Runs on ALL records before rendering
            processors=[
                structlog.stdlib.ProcessorFormatter.remove_processors_meta,
                structlog.processors.JSONRenderer(),
            ],   
        )
    )
    return file_handler


# =============================================================================
# CORE FUNCTIONS
# =============================================================================

def configure_structured_logging(
    *,
    console_verbose: bool = False,
    log_to_file: bool = True,
    custom_console: bool = True,
) -> None:
    """Configure structlog + stdlib logging for the speller package.
 
    Must be called once at program startup (inside ``main()`` in
    ``__main__.py``) before any log messages are emitted.  Safe to
    call multiple times — existing handlers are cleared first to
    prevent duplicate output.
 
    Parameter signature mirrors :func:`~speller.logger.configure_logging`
    and :func:`~speller.template_logger.configure_template_logging`
    so the composition root can treat all three backends
    interchangeably via the Strategy pattern.
 
    Parameters
    ----------
    console_verbose : bool, optional
        ``True`` sets the console handler to ``DEBUG`` so all messages
        appear in the terminal.  ``False`` (default) shows ``INFO``
        and above.  Controlled by the ``--verbose`` CLI flag.
    log_to_file : bool, optional
        ``True`` (default) attaches a :class:`RotatingFileHandler`
        writing ``DEBUG``-level NDJSON logs to disk.  ``False``
        disables file logging.  Controlled by the ``--no-log-file``
        CLI flag.
    custom_console : bool, optional
        ``True`` (default) enables ANSI colors in the console
        renderer.  Set ``False`` in tests to suppress colors from
        captured output.
 
    Notes
    -----
    Two-phase configuration
        structlog is configured in TWO places that must agree:
 
        1. :func:`structlog.configure` — defines the processor chain
           used by ``structlog.get_logger()`` calls.  Ends with
           ``ProcessorFormatter.wrap_for_formatter``, which hands
           the event_dict off to stdlib logging rather than rendering
           it directly.
        2. :class:`~structlog.stdlib.ProcessorFormatter` on each
           handler — runs ``foreign_pre_chain`` on stdlib entries
           and the final renderer on all entries.
 
        The ``_SHARED_PROCESSORS`` list is reused in both places so
        the output format is identical regardless of which API
        (structlog or stdlib) emitted the log.
 
    Logger hierarchy::
 
        speller                 ← root package logger (configured here)
        ├── speller.benchmarks
        ├── speller.config
        ├── speller.dictionaries
        ├── speller.register
        ├── speller.speller
        └── speller.text_processor
 
        Both ``structlog.get_logger(__name__)`` and
        ``logging.getLogger(__name__)`` resolve to the same underlying
        hierarchy — the structlog logger factory wraps stdlib loggers.
    """
    # ─── 1. Configure structlog itself ──────────────────────────────
    # The final processor (wrap_for_formatter) converts the event_dict
    # into a form that logging.LogRecord.msg can hold. The handler's
    # ProcessorFormatter unwraps it on the way out.
    structlog.configure(
        processors=[
            *_SHARED_PROCESSORS,
            # MUST be last, Hands off to stdlib logging instead of rendering.
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        ],
        # stdlib.BoundLogger knows logging's method names (info/debug/...)
        # and delegates to the wrapped logging.Logger.
        wrapper_class=structlog.stdlib.BoundLogger,
        # stdlib.LoggerFactory creates a logging.Logger when structlog
        # needs one. Auto-deduces the caller's module name.
        logger_factory=structlog.stdlib.LoggerFactory(),
        # Cache the bound logger after the first call. Safe because
        # we reconfigure idempotently via handler clearing below.
        cache_logger_on_first_use=True,
    )
    
    # ─── 2. Grab the top-level package logger ───────────────────────
    # Same package_logger pattern as speller.logger.configure_logging —
    # child loggers (speller.dictionaries, speller.speller, ...)
    # propagate messages upward to this one.
    package_logger = logging.getLogger(file_dirs.CUR_DIR.name)
    package_logger.setLevel(logging.DEBUG)  # Let handlers decide their own level
    
    # ─── 3. Prevent duplicate handlers on re-configuration ──────────
    if package_logger.hasHandlers():
        package_logger.handlers.clear()
        
    # ─── 4. Console handler — pretty key=value, color optional ──────
    level = logging.DEBUG if console_verbose else fhandler_config.LEVEL_DEFAULT
    console_handler = _setup_chandler(level=level, custom_console=custom_console)
    package_logger.addHandler(console_handler)
    
    # ─── 5. File handler — NDJSON, always captures DEBUG ────────────
    if log_to_file:
        # parents=True: create any missing parent directories
        # exist_ok=True: no error if directory already exists
        file_dirs.LOG_DIR.mkdir(parents=True, exist_ok=True)
        file_handler = _setup_fhandler()
        package_logger.addHandler(file_handler)
        
    # ─── 6. Propagation control ─────────────────────────────────────
    # Same choice as speller.logger.configure_logging — propagate to
    # root so parent loggers (if any) see these messages.  Set False
    # if you notice double-printing in specific environments. 
    package_logger.propagate = True
  

def get_structured_logger(name: str | None = None) -> structlog.stdlib.BoundLogger:
    """Return a structlog bound logger with correct type hints.
 
    Thin wrapper around :func:`structlog.stdlib.get_logger` that
    makes the return type statically visible to Pyright.
 
    Parameters
    ----------
    name : str or None, optional
        Logger name.  Conventionally ``__name__`` of the caller.
        If ``None``, structlog auto-deduces the caller's module.
 
    Returns
    -------
    structlog.stdlib.BoundLogger
        Bound logger with ``.info()``, ``.debug()``, ``.bind()``,
        etc.  Accepts keyword arguments as first-class fields::
 
            log = get_structured_logger(__name__)
            log.info("dictionary_loaded", word_count=143091, backend="hash")
 
    Examples
    --------
    In a module that wants structured logging::
 
        from speller.structured_logger import get_structured_logger
        log = get_structured_logger(__name__)
 
        log.info("event_name", key1=value1, key2=value2)
        log.bind(request_id="abc").info("sub_event", another_key=42)
 
    In a module that wants to stay stdlib (most of the package)::
 
        import logging
        logger = logging.getLogger(__name__)  # unchanged
        logger.info("Loaded %s words", count)  # unchanged
 
    Both APIs produce identical output when
    :func:`configure_structured_logging` has been called, because
    they share the same handlers and processor pipeline.
    """
    if name is None:
        return structlog.stdlib.get_logger()
    return structlog.stdlib.get_logger(name)



