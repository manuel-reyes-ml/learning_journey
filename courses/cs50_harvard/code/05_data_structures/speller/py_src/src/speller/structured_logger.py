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
    #
    # That's why actual renderers don't appear in this list — rendering happens downstream
    # at the handler. The handlers, not structlog.configure(), decide console-pretty vs JSON.
    # This is exactly what lets you have two handlers with different renderers.
    structlog.configure(
        processors=[
            *_SHARED_PROCESSORS,  # unpacks your 6 shared processors:
            #   1. contextvars.merge_contextvars  → adds any bound context
            #   2. stdlib.add_logger_name          → adds "logger": "speller.foo"
            #   3. stdlib.add_log_level            → adds "level": "info"
            #   4. TimeStamper(fmt="iso")          → adds "timestamp": "2026-04-21T..."
            #   5. StackInfoRenderer()             → formats stack_info if present
            #   6. format_exc_info                 → serializes exceptions
            
            # MUST be last, Hands off to stdlib logging instead of rendering.
            # This is not a renderer. It's a bridge. It takes the enriched event_dict and
            # wraps it in a format that a stdlib logging.LogRecord can carry as its msg field.
            # Then the ProcessorFormatter attached to each handler unwraps it on the other side
            # and applies the real renderer (your ConsoleRenderer or JSONRenderer).
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,  # the 7th processor
        ],
        
        # stdlib.BoundLogger knows logging's method names (info/debug/...)
        # and delegates to the wrapped logging.Logger.
        # What it is: The class of the object returned by structlog.get_logger(). When your code
        # does log.info("event", k=v), it's calling .info() on an instance of this class.
        # Why this specific one?: structlog.stdlib.BoundLogger is purpose-built to play nicely
        # with stdlib logging.
        #   - It has hardcoded .debug(), .info(), .warning(), .error(), .critical(), .exception()
        #     methods that mirror logging.Logger.
        #   - It knows how to pass exc_info, stack_info, and stacklevel through to the underlying
        #     logging.Logger correctly.
        #   - It supports %s-style positional args via PositionalArgumentsFormatter (not strictly
        #     used here but wired up).
        wrapper_class=structlog.stdlib.BoundLogger,

        # stdlib.LoggerFactory creates a logging.Logger when structlog
        # needs one. Auto-deduces the caller's module name.
        # What it is: A factory (a callable) that produces the underlying logger object.
        # Why this specific one: When structlog.get_logger("speller.dictionaries") is called, this
        # factory runs logging.getLogger("speller.dictionaries") internally and returns that
        # logging.Logger instance. That logger is then wrapped in a stdlib.BoundLogger (parameter 2)
        # and returned to you.
        #
        # Why LoggerFactory() not LoggerFactory: It's an instantiated factory, not the class itself.
        # configure() calls the factory — logger_factory() — and you want the result of 
        # LoggerFactory()(...) which returns a logging.Logger.
        logger_factory=structlog.stdlib.LoggerFactory(),
        
        # Cache the bound logger after the first call. Safe because
        # we reconfigure idempotently via handler clearing below.
        # What it is: A performance optimization. Default is False.
        # What True does: After the first call, the assembled bound logger is cached inside the
        # proxy. Subsequent calls skip the assembly step.
        # The trade-off:
        #   - True → faster in hot loops (e.g. your for word in extract_words(...) check loop in
        #     Stage 2+ when you're logging per-iteration), but reconfiguration after the first log
        #     call has no effect on already-cached loggers.
        #   - False → every log call re-assembles, slightly slower, but reconfiguration always
        #     takes effect.
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


# =============================================================================
# REFERENCE GUIDES
# =============================================================================
 
# How the pieces connect
# ──────────────────────
#
#   structlog.get_logger().info("evt", k=v)      logging.getLogger().info("msg")
#              │                                             │
#              │ (structlog path)                            │ (stdlib path)
#              ▼                                             ▼
#     _SHARED_PROCESSORS                            logging.LogRecord created
#     (merge_contextvars, add_log_level,                    │
#      TimeStamper, ...)                                    │
#              │                                             │
#              ▼                                             │
#     ProcessorFormatter.wrap_for_formatter                  │
#              │                                             │
#              └──────────────┬──────────────────────────────┘
#                             │
#                             ▼
#                  ProcessorFormatter on handler
#                  ├── foreign_pre_chain (stdlib only):
#                  │       _SHARED_PROCESSORS
#                  └── processors (both):
#                          remove_processors_meta
#                          ConsoleRenderer or JSONRenderer
#                             │
#                             ▼
#              ┌──────────────┴──────────────┐
#              │                             │
#       Console handler                File handler
#       ConsoleRenderer                JSONRenderer
#              │                             │
#              ▼                             ▼
#   2026-04-21T14:30:45Z        {"timestamp": "2026-04-21T...",
#   [info  ] dictionary_loaded   "level": "info",
#            backend=hash         "logger": "speller.load_dictionary",
#            word_count=143091    "event": "dictionary_loaded",
#                                 "backend": "hash",
#                                 "word_count": 143091}
#
 
# =====================================================
# Processor Contract
# =====================================================
#
# A structlog processor is ANY callable with signature:
#     (logger, method_name, event_dict) -> event_dict
#
# The chain runs left-to-right. Each processor reads/adds/removes
# keys in event_dict and returns it. The LAST processor (the
# renderer) returns a str/bytes that gets handed to the wrapped
# logger's output method.
#
# Example — writing your own processor:
#
#     def add_version(logger, method_name, event_dict):
#         event_dict["app_version"] = "1.0.0"
#         return event_dict
#
# Then add it anywhere in _SHARED_PROCESSORS. Every log event
# will now include {"app_version": "1.0.0"}.
 
 
# =====================================================
# Context Variables — the killer feature
# =====================================================
#
# structlog.contextvars.bind_contextvars() stores keys in Python's
# contextvars module.  Every subsequent log call in this execution
# context automatically includes those keys via merge_contextvars.
#
#     structlog.contextvars.bind_contextvars(file="austen.txt", run_id=42)
#
#     # In some_function() called downstream — no need to pass file/run_id:
#     log.info("words_extracted", count=125203)
#
#     # Output includes ALL bound context:
#     # {"event": "words_extracted", "count": 125203,
#     #  "file": "austen.txt", "run_id": 42, ...}
#
#     structlog.contextvars.clear_contextvars()  # reset for next iteration
#
# Safe across threading AND asyncio boundaries — uses the same
# contextvars primitive that asyncio tasks use for coroutine-local
# state.  Stage 2+ RAG pipelines and Stage 4+ LangGraph agents
# will rely on this for request-scoped logging.
