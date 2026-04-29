""" """

# =============================================================================
# IMPORTS
# =============================================================================

from __future__ import annotations

from logging.handlers import RotatingFileHandler
from typing import Final, Any
import logging
import sys

import structlog
from structlog.types import Processor, WrappedLogger, EventDict

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

_KEY_ORDER: Final[list[str]] = ["timestamp", "level", "logger", "event"]


# =============================================================================
# INTERNAL HELPER FUNCTIONS
# =============================================================================


def _reorder_keys(preferred_order: list[str]) -> Processor:
    """Processor factory: move specified keys to the front of the event_dict.

    Preserves insertion order for any keys not in preferred_order.
    Apply BEFORE the renderer in the ProcessorFormatter's processors list.

    Parameters
    ----------
    preferred_order : list of str
        Keys to pull to the front, in the desired order.
        Example: ``["timestamp", "level", "logger", "event"]``.

    Returns
    -------
    Processor
        A callable compatible with structlog's processor protocol.
    """

    def processor(
        logger: WrappedLogger, method_name: str, event_dict: EventDict
    ) -> EventDict:
        ordered: dict[str, Any] = {}
        for key in preferred_order:
            if key in event_dict:
                ordered[key] = event_dict.pop(key)
        ordered.update(event_dict)
        return ordered

    return processor


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
                _reorder_keys(_KEY_ORDER),
                structlog.dev.ConsoleRenderer(colors=custom_console),
            ],
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
                _reorder_keys(_KEY_ORDER),
                structlog.processors.JSONRenderer(),
            ],
        )
    )
    return file_handler


def _setup_fhandler_indent(
    file_dirs: FileDirectories = file_dirs,
    fhandler_config: FileHandlerConfig = fhandler_config,
) -> RotatingFileHandler:
    """ """
    file_handler_indent = RotatingFileHandler(
        filename=file_dirs.log_file.slog_indent_path,
        maxBytes=fhandler_config.max_log_bytes,
        backupCount=fhandler_config.BACKUP_COUNT,
        encoding=fhandler_config.ENCODING,
    )
    file_handler_indent.setLevel(logging.DEBUG)
    file_handler_indent.setFormatter(
        structlog.stdlib.ProcessorFormatter(
            # Runs ONLY on non-structlog (stdlib) log records
            foreign_pre_chain=_SHARED_PROCESSORS,
            # Runs on ALL records before rendering
            processors=[
                structlog.stdlib.ProcessorFormatter.remove_processors_meta,
                _reorder_keys(_KEY_ORDER),
                structlog.processors.JSONRenderer(
                    indent=2
                ),  # indent JSON output to improve readability
            ],
        )
    )
    return file_handler_indent


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

    # ─── 5. File handlers — NDJSON, always captures DEBUG ────────────
    if log_to_file:
        # parents=True: create any missing parent directories
        # exist_ok=True: no error if directory already exists
        file_dirs.LOG_DIR.mkdir(parents=True, exist_ok=True)
        file_handler = _setup_fhandler()
        package_logger.addHandler(file_handler)

        # Generate JSON log with indentation = 2 for human readability
        file_handler_indent = _setup_fhandler_indent()
        package_logger.addHandler(file_handler_indent)

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


# =============================================================================
# END-TO-END PROCESSING FLOW — REFERENCE GUIDE
# =============================================================================
#
# Two API paths converge on ONE set of handlers. This guide traces both paths
# step-by-step so you can debug, extend, or reason about any log call.
#
# Setup assumed for all examples below:
#   - configure_structured_logging() has been called once at startup
#   - bind_contextvars(file="austen.txt", run_id=42) was called previously
#   - Two handlers attached to the "speller" package logger:
#       • console → ProcessorFormatter + ConsoleRenderer
#       • file    → ProcessorFormatter + JSONRenderer
#
# =============================================================================


# =====================================================
# THE THREE OBJECTS AT PLAY
# =====================================================
#
# Every structlog log call involves THREE distinct objects. Once you see
# these as separate, the configure() parameters stop feeling magical.
#
# ┌──────────────────────────────┐
# │  1. BoundLogger              │  ← the object YOUR code calls .info() on
# │     (wrapper_class)          │    holds bind() context
# └──────────────┬───────────────┘
#                │ runs the processor chain on .info()
#                ▼
# ┌──────────────────────────────┐
# │  2. Processor chain          │  ← transforms event_dict step by step
# │     (processors list)        │    (add timestamp, log level, etc.)
# └──────────────┬───────────────┘
#                │ final processor hands result to...
#                ▼
# ┌──────────────────────────────┐
# │  3. Underlying logger        │  ← the object that actually writes output
# │     (produced by             │    in our setup: a stdlib logging.Logger
# │      logger_factory)         │
# └──────────────────────────────┘
#
# configure() wires these three together. After that, your application code
# never touches the wiring — it only calls log.info(), log.bind(), etc.


# =====================================================
# PATH A — structlog.get_logger() call
# =====================================================
#
# User code:
#
#   log = structlog.stdlib.get_logger("speller.benchmarks")
#   log.info("dictionary_loaded", word_count=143091, backend="hash")
#
# ─── STEP A1: get_logger() resolves the bound logger ──────────────────
#
# structlog asks the logger_factory (stdlib.LoggerFactory) to produce the
# underlying logger:
#     logging.getLogger("speller.benchmarks")  →  logging.Logger instance
#
# That logging.Logger is wrapped inside a wrapper_class (stdlib.BoundLogger).
# With cache_logger_on_first_use=True, this wrapped logger is cached in a
# proxy so subsequent .info() calls skip re-assembly.
#
# Returned to you: `log` — a stdlib.BoundLogger
#
# ─── STEP A2: .info() builds the initial event_dict ───────────────────
#
# The first argument becomes "event"; all kwargs become fields:
#
#     event_dict = {
#         "event": "dictionary_loaded",
#         "word_count": 143091,
#         "backend": "hash",
#     }
#
# ─── STEP A3: Processor chain runs in order ───────────────────────────
#
# Each processor receives (logger, method_name, event_dict) and returns
# a (possibly modified) event_dict passed to the next processor.
#
# Processor 1: contextvars.merge_contextvars
#   Pulls in any previously bound contextvars.
#     event_dict += {"file": "austen.txt", "run_id": 42}
#
# Processor 2: stdlib.add_logger_name
#   Reads the wrapped logger's name and adds it.
#     event_dict += {"logger": "speller.benchmarks"}
#
# Processor 3: stdlib.add_log_level
#   Adds the method name ("info", "debug", ...) as the level.
#     event_dict += {"level": "info"}
#
# Processor 4: TimeStamper(fmt="iso")
#   Adds ISO-8601 timestamp.
#     event_dict += {"timestamp": "2026-04-21T14:30:45.123Z"}
#
# Processor 5: StackInfoRenderer()
#   No-op here (no stack_info=True was passed). Would format a stack
#   trace into the event_dict if requested.
#
# Processor 6: format_exc_info
#   No-op here (no exception in context). Would serialize exc_info into
#   a structured "exception" field if called via log.exception().
#
# Processor 7: stdlib.ProcessorFormatter.wrap_for_formatter  ← THE HAND-OFF
#   This is NOT a renderer. It wraps the event_dict so it can ride inside
#   a stdlib LogRecord.msg field. Must be last in the chain — anything
#   after it would receive the wrapped object and crash or drop data.
#
# Final event_dict at this point:
#     {
#         "event": "dictionary_loaded",
#         "word_count": 143091,
#         "backend": "hash",
#         "file": "austen.txt",
#         "run_id": 42,
#         "logger": "speller.benchmarks",
#         "level": "info",
#         "timestamp": "2026-04-21T14:30:45.123Z",
#     }
#
# ─── STEP A4: Control passes to stdlib logging ────────────────────────
#
# The underlying logging.Logger (from A1) receives a LogRecord where
# msg = wrapped event_dict. structlog's job ends here.
#
# The LogRecord propagates UP the logger hierarchy via stdlib rules:
#     speller.benchmarks  →  speller  →  root
#
# Every handler attached along the way processes the record.
#
# ─── STEP A5: Each handler's ProcessorFormatter renders the event ─────
#
# Because this record originated in structlog, ProcessorFormatter's
# foreign_pre_chain is SKIPPED. Only the `processors` list runs.
#
# Console handler:
#     processors=[
#         remove_processors_meta,      # strip _record, _from_structlog
#         ConsoleRenderer(colors=True),
#     ]
#     →  "2026-04-21T14:30:45Z [info     ] dictionary_loaded
#         [speller.benchmarks] backend=hash file=austen.txt
#         run_id=42 word_count=143091"
#
# File handler:
#     processors=[
#         remove_processors_meta,
#         JSONRenderer(),
#     ]
#     →  {"event": "dictionary_loaded", "word_count": 143091,
#         "backend": "hash", "file": "austen.txt", "run_id": 42,
#         "logger": "speller.benchmarks", "level": "info",
#         "timestamp": "2026-04-21T14:30:45.123Z"}


# =====================================================
# PATH B — stdlib logging.getLogger() call
# =====================================================
#
# User code — note: EXISTING code in dictionaries.py, speller.py, etc.
#                   never changes to use this new logging system:
#
#   logger = logging.getLogger(__name__)                # "speller.dictionaries"
#   logger.info("Loaded %s words from '%s'", 143091, "large")
#
# ─── STEP B1: getLogger() returns the stdlib logger directly ──────────
#
# No structlog wrapping happens here. You get a plain logging.Logger.
# But crucially — this is the SAME logging.Logger instance that
# stdlib.LoggerFactory would produce for the same name.  Path A and
# Path B share the same underlying logger hierarchy.
#
# ─── STEP B2: .info() creates a LogRecord the stdlib way ──────────────
#
# stdlib logging builds a logging.LogRecord:
#     record.name     = "speller.dictionaries"
#     record.levelno  = logging.INFO
#     record.msg      = "Loaded %s words from '%s'"  (plain str)
#     record.args     = (143091, "large")            (for %-formatting)
#
# NO event_dict exists yet. NO processors have run yet.
#
# ─── STEP B3: Record propagates up the logger hierarchy ───────────────
#
# Same propagation as Path A:
#     speller.dictionaries  →  speller  →  root
#
# Every handler on each ancestor logger receives the record.
#
# ─── STEP B4: Each handler's ProcessorFormatter renders the event ─────
#
# Because this record did NOT originate in structlog, ProcessorFormatter
# runs foreign_pre_chain FIRST to manufacture an event_dict comparable
# to what structlog would have produced.
#
# ProcessorFormatter begins by constructing a skeleton event_dict:
#     {
#         "event": "Loaded 143091 words from 'large'",
#         # ^ stdlib's %-formatting has been applied to msg + args
#         "_record": <LogRecord ...>,      # internal bookkeeping
#         "_from_structlog": False,        # internal bookkeeping
#     }
#
# Then foreign_pre_chain runs — which, in our config, is _SHARED_PROCESSORS.
# This is the SAME list used in structlog.configure(), minus the
# wrap_for_formatter terminator (which wouldn't make sense at the handler
# stage anyway).
#
# Processor 1: contextvars.merge_contextvars
#     event_dict += {"file": "austen.txt", "run_id": 42}
#   ★ THE MAGIC — stdlib calls ALSO inherit bound context, because
#     merge_contextvars reads Python's contextvars module directly.
#
# Processor 2: stdlib.add_logger_name
#     event_dict += {"logger": "speller.dictionaries"}
#
# Processor 3: stdlib.add_log_level
#     event_dict += {"level": "info"}
#
# Processor 4: TimeStamper(fmt="iso")
#     event_dict += {"timestamp": "2026-04-21T14:30:45.456Z"}
#
# Processors 5 & 6: StackInfoRenderer + format_exc_info
#     No-ops here (no stack_info or exc_info).
#
# ─── STEP B5: Main processors list runs on all records ────────────────
#
# After foreign_pre_chain (stdlib only) OR wrap_for_formatter (structlog
# only), BOTH paths converge and run the handler's main `processors`
# list:
#
# Processor:  ProcessorFormatter.remove_processors_meta
#   Strips _record and _from_structlog from event_dict so they don't
#   appear in the final output.
#
# Processor:  ConsoleRenderer() or JSONRenderer()  (the real renderer)
#   Console output:
#     "2026-04-21T14:30:45Z [info     ] Loaded 143091 words from 'large'
#      [speller.dictionaries] file=austen.txt run_id=42"
#
#   File output:
#     {"event": "Loaded 143091 words from 'large'",
#      "file": "austen.txt", "run_id": 42,
#      "logger": "speller.dictionaries", "level": "info",
#      "timestamp": "2026-04-21T14:30:45.456Z"}


# =====================================================
# VISUAL: Both paths converging
# =====================================================
#
#   ┌─────── Path A (structlog) ────────┐      ┌──── Path B (stdlib) ────┐
#   │                                    │      │                          │
#   │  log.info("evt", k=v)              │      │  logger.info("msg %s",x)│
#   │        │                           │      │        │                 │
#   │        ▼                           │      │        ▼                 │
#   │  BoundLogger builds event_dict    │      │  LogRecord created       │
#   │        │                           │      │  (no event_dict yet)    │
#   │        ▼                           │      │        │                 │
#   │  _SHARED_PROCESSORS runs           │      │        │                 │
#   │  (from configure's processors=)   │      │        │                 │
#   │        │                           │      │        │                 │
#   │        ▼                           │      │        │                 │
#   │  wrap_for_formatter                │      │        │                 │
#   │  (packages event_dict for stdlib) │      │        │                 │
#   │        │                           │      │        │                 │
#   └────────┼───────────────────────────┘      └────────┼─────────────────┘
#            │                                            │
#            ▼                                            ▼
#       logging.Logger.info(wrapped_event_dict)   logging.Logger.info(msg, *args)
#                  │                                      │
#                  │   (both now stdlib LogRecords)       │
#                  │                                      │
#                  └────────┬─────────────────────────────┘
#                           │
#                           ▼
#                  Record propagates up hierarchy:
#                  speller.<module>  →  speller  →  root
#                           │
#                           ▼
#                  Each handler's ProcessorFormatter runs
#                           │
#                ┌──────────┴──────────┐
#                │                     │
#                ▼                     ▼
#        _from_structlog=True    _from_structlog=False
#        skip foreign_pre_chain  run foreign_pre_chain
#                │               (_SHARED_PROCESSORS)
#                │                     │
#                └──────────┬──────────┘
#                           ▼
#                  remove_processors_meta
#                           │
#                           ▼
#                  ConsoleRenderer OR JSONRenderer
#                           │
#                  ┌────────┴────────┐
#                  ▼                 ▼
#             stderr (pretty)   logs/speller_structured.log (NDJSON)


# =====================================================
# WHY _SHARED_PROCESSORS APPEARS IN TWO PLACES
# =====================================================
#
# Look at configure_structured_logging() and you'll see _SHARED_PROCESSORS
# referenced in TWO spots:
#
#   1. structlog.configure(processors=[*_SHARED_PROCESSORS, ...])
#      → runs on Path A events (structlog-originated)
#
#   2. ProcessorFormatter(foreign_pre_chain=_SHARED_PROCESSORS, ...)
#      → runs on Path B events (stdlib-originated)
#
# Using the SAME list in both places is intentional. It guarantees that a
# log event emitted via stdlib has the same enriched fields as a log event
# emitted via structlog — timestamps, log levels, bound context, exception
# formatting. Consistent output regardless of which API was used.
#
# If the lists diverged, you'd get inconsistent output:
#   - stdlib calls might be missing timestamps
#   - structlog calls might not inherit bound context
#   - Different log levels might be formatted differently
#
# The DRY constant prevents that drift.


# =====================================================
# WHAT CHANGES WHEN YOU CALL log.exception()
# =====================================================
#
# Inside an except block:
#
#   try:
#       ...
#   except ValueError as e:
#       log.exception("dictionary_load_failed", path=str(p))
#
# This triggers the two no-op processors from before:
#
# Processor 5: StackInfoRenderer()
#   If stack_info=True was passed, formats the stack into a "stack" field.
#
# Processor 6: format_exc_info
#   Reads the current exc_info tuple from sys.exc_info() and serializes:
#     event_dict += {
#         "exception": "Traceback (most recent call last):\n...",
#         # or as a structured list if ExceptionDictTransformer is used
#     }
#
# The "exc_info" key is replaced by the rendered "exception" string. In
# the NDJSON output, this means tracebacks become queryable JSON fields
# instead of multi-line text blobs — much easier to ship to Datadog/ELK.


# =====================================================
# WHAT CHANGES WHEN YOU CALL log.bind()
# =====================================================
#
#   request_log = log.bind(request_id="abc-123")
#   request_log.info("llm_call", tokens=1500)
#
# .bind() does NOT bind to contextvars (merge_contextvars won't see it).
# Instead it returns a NEW BoundLogger whose private context dict contains
# {"request_id": "abc-123"}.
#
# When request_log.info() is called, the initial event_dict includes the
# bound context BEFORE the processor chain runs:
#
#     event_dict = {
#         "event": "llm_call",
#         "tokens": 1500,
#         "request_id": "abc-123",   # ← from .bind()
#     }
#
# Differences from bind_contextvars:
#   .bind()              .bind_contextvars()
#   ─────────────────    ─────────────────────────────────
#   Logger-local          Context-local (thread/async-scope)
#   Only this logger      Any logger in this context
#   Returns new logger    Mutates global contextvars state
#   Stdlib calls: NO      Stdlib calls: YES (via foreign_pre_chain)
#
# Rule of thumb:
#   - Per-request/per-batch context that MUST reach stdlib code too:
#     → bind_contextvars (what configure_structured_logging enables)
#   - Per-logger local context that only affects THIS logger's calls:
#     → .bind()


# =====================================================
# DEBUGGING: "Why doesn't my field show up?"
# =====================================================
#
# Symptom                         | Likely cause
# ────────────────────────────────┼─────────────────────────────────────
# Field missing from stdlib       | foreign_pre_chain doesn't include the
# log calls only                  | processor that adds it. Check that
#                                 | _SHARED_PROCESSORS is in both places.
# ────────────────────────────────┼─────────────────────────────────────
# Field missing from structlog    | Processor is in foreign_pre_chain only,
# log calls only                  | not in configure's processors. Move it
#                                 | to _SHARED_PROCESSORS.
# ────────────────────────────────┼─────────────────────────────────────
# bind_contextvars values absent  | merge_contextvars missing from the
#                                 | chain, or clear_contextvars() was
#                                 | called too early.
# ────────────────────────────────┼─────────────────────────────────────
# _record / _from_structlog in    | remove_processors_meta missing from
# output                          | ProcessorFormatter.processors.
# ────────────────────────────────┼─────────────────────────────────────
# Double output (two lines per    | package_logger.propagate=True AND
# log call)                       | root logger has handlers attached.
#                                 | Set propagate=False or clear root.
# ────────────────────────────────┼─────────────────────────────────────
# New reconfigure has no effect   | cache_logger_on_first_use=True
#                                 | cached the pre-reconfigure state.
#                                 | Set to False, OR reconfigure BEFORE
#                                 | the first log call.


# =====================================================
# MENTAL MODEL SUMMARY (one paragraph)
# =====================================================
#
# structlog.configure() wires the LEFT HALF of the pipeline — everything
# that happens BEFORE stdlib logging gets involved. The ProcessorFormatter
# on each handler wires the RIGHT HALF — everything that happens AFTER
# stdlib logging has a LogRecord in hand. The two halves share the
# _SHARED_PROCESSORS list as common ground to produce consistent output
# regardless of which API the emitting code used. wrap_for_formatter is
# the bridge connecting the two halves for structlog calls; foreign_pre_chain
# is the bridge for stdlib calls. Both paths converge on the same handlers
# and the same final renderer.


# =====================================================
# REFERENCES
# =====================================================
# structlog — Configuration:
#   https://www.structlog.org/en/stable/configuration.html
# structlog — Standard Library Logging:
#   https://www.structlog.org/en/stable/standard-library.html
# structlog — Processors:
#   https://www.structlog.org/en/stable/processors.html
# structlog — Context Variables:
#   https://www.structlog.org/en/stable/contextvars.html
# Python Docs — logging.LogRecord:
#   https://docs.python.org/3/library/logging.html#logrecord-objects


# =============================================================================
# ADDENDUM — STANDALONE STRUCTLOG SETUP AND USAGE
# =============================================================================
#
# This addendum documents the OTHER mode of structlog — standalone, with no
# stdlib logging.Logger involved at all.  We do NOT use this mode in the
# speller; the production-standard choice is structlog-on-stdlib (the main
# reference guide above).  This section exists so you know:
#
#   1. How standalone structlog differs from what we actually run
#   2. When standalone is the right choice (rare)
#   3. How to recognise standalone config in other codebases you read
#
# Rule of thumb: if you're ever unsure which mode a codebase is in, check
# the LAST processor and the logger_factory.  Two markers settle it:
#
#   ┌──────────────────────────────────────────────────────────────────┐
#   │  Marker                        │ Standalone      │ Stdlib-wrap  │
#   │────────────────────────────────┼─────────────────┼──────────────│
#   │  Last processor                │ A renderer      │ wrap_for_   │
#   │                                │ (Console/JSON)  │ formatter    │
#   │  logger_factory                │ PrintLogger-    │ stdlib.      │
#   │                                │ Factory,        │ LoggerFactory│
#   │                                │ WriteLogger-    │              │
#   │                                │ Factory         │              │
#   │  wrapper_class                 │ make_filtering_ │ stdlib.      │
#   │                                │ bound_logger or │ BoundLogger  │
#   │                                │ BoundLogger     │              │
#   │  logging.getLogger() calls     │ Separate,       │ Same         │
#   │  elsewhere in codebase         │ uncaptured path │ hierarchy    │
#   └──────────────────────────────────────────────────────────────────┘
#
# =============================================================================


# =====================================================
# WHAT STANDALONE STRUCTLOG ACTUALLY IS
# =====================================================
#
# In standalone mode, structlog owns the ENTIRE pipeline:
#
#   ┌──────────────────────┐
#   │  1. BoundLogger      │  ← generic structlog.BoundLogger
#   │     (wrapper_class)  │     or make_filtering_bound_logger()
#   └──────────┬───────────┘
#              │
#              ▼
#   ┌──────────────────────┐
#   │  2. Processor chain  │  ← ends with a REAL renderer
#   │                      │     (ConsoleRenderer or JSONRenderer)
#   └──────────┬───────────┘
#              │ final processor returns a str (or bytes)
#              ▼
#   ┌──────────────────────┐
#   │  3. PrintLogger or   │  ← writes the str directly to a file/stream
#   │     WriteLogger      │     no logging.Logger, no handlers,
#   │                      │     no LogRecord, no hierarchy
#   └──────────────────────┘
#
# The key difference from structlog-on-stdlib:
#   - No logging.Logger is ever created
#   - No LogRecord is ever created
#   - No handler/formatter/propagation machinery exists
#   - structlog's own PrintLogger/WriteLogger does the I/O directly
#
# That means ROTATION, MULTIPLE HANDLERS, PROPAGATION, SHARING WITH
# THIRD-PARTY LIBRARY LOGS — none of that exists out of the box.  You'd
# have to re-implement any of those features yourself.


# =====================================================
# MINIMAL STANDALONE CONFIG — DEV MODE
# =====================================================
#
# The simplest useful standalone setup: colored output to the terminal,
# no file logging.  This is what structlog's default looks like when you
# just call get_logger() without calling configure() first.
#
#   import logging
#   import structlog
#
#   structlog.configure(
#       processors=[
#           # 1. Merge any contextvars-bound key/values
#           structlog.contextvars.merge_contextvars,
#           # 2. Add "level": "info" / "error" / ...
#           structlog.processors.add_log_level,
#           # 3. Handle stack_info=True if passed
#           structlog.processors.StackInfoRenderer(),
#           # 4. Switch the exception formatter for pretty tracebacks
#           structlog.dev.set_exc_info,
#           # 5. Add "timestamp": "2026-04-22T..."
#           structlog.processors.TimeStamper(fmt="iso"),
#           # 6. FINAL RENDERER — turns event_dict into a colored string.
#           #    THIS IS THE LINE THAT DIFFERS FROM STRUCTLOG-ON-STDLIB.
#           #    Here the renderer runs INSIDE structlog.
#           #    In stdlib-wrap mode, a handler's ProcessorFormatter would
#           #    do the rendering instead.
#           structlog.dev.ConsoleRenderer(),
#       ],
#       # Filter by level BEFORE the chain runs — fastest option.
#       # make_filtering_bound_logger uses logging's level NAMES but
#       # does NOT actually use the stdlib logging module.
#       wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
#       # Plain dict for context storage (OrderedDict is the default).
#       context_class=dict,
#       # PrintLogger writes directly to sys.stdout (or any TextIO).
#       # No handlers, no LogRecord, no hierarchy.
#       logger_factory=structlog.PrintLoggerFactory(),
#       # Build the bound logger once at first use and cache it.
#       # Safe because we only configure once at startup.
#       cache_logger_on_first_use=True,
#   )
#
#   log = structlog.get_logger()
#   log.info("dictionary_loaded", word_count=143091, backend="hash")
#   # → 2026-04-22T14:28:50Z [info  ] dictionary_loaded
#   #   backend=hash word_count=143091


# =====================================================
# STANDALONE CONFIG — PRODUCTION JSON MODE
# =====================================================
#
# For a "12-factor app" style container deployment where you write ONLY
# JSON to stdout and let the platform (Kubernetes, Docker, ECS) collect
# the logs.
#
#   import logging
#   import structlog
#
#   structlog.configure(
#       processors=[
#           structlog.contextvars.merge_contextvars,
#           structlog.processors.add_log_level,
#           structlog.processors.TimeStamper(fmt="iso"),
#           structlog.processors.StackInfoRenderer(),
#           structlog.processors.format_exc_info,
#           # Final renderer — JSON instead of Console.
#           structlog.processors.JSONRenderer(),
#       ],
#       wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
#       context_class=dict,
#       # WriteLogger is slightly faster than PrintLogger. Defaults to
#       # stdout; pass a file object to write elsewhere.
#       logger_factory=structlog.WriteLoggerFactory(),
#       cache_logger_on_first_use=True,
#   )
#
#   log = structlog.get_logger()
#   log.info("dictionary_loaded", word_count=143091, backend="hash")
#   # → {"event": "dictionary_loaded", "word_count": 143091,
#   #    "backend": "hash", "level": "info",
#   #    "timestamp": "2026-04-22T14:28:50.147Z"}
#
# For file output, pass an open file handle to WriteLoggerFactory:
#
#   log_file = open("/var/log/app.log", "a", encoding="utf-8")
#   logger_factory=structlog.WriteLoggerFactory(file=log_file)
#
# ⚠ NO ROTATION.  You'd need external tooling (logrotate on Linux, or
# roll your own) because WriteLogger doesn't implement any file-size or
# time-based rollover.  This is one of the big reasons production
# projects pick the structlog-on-stdlib mode instead — you inherit
# RotatingFileHandler and TimedRotatingFileHandler for free.


# =====================================================
# END-TO-END PROCESSING FLOW — STANDALONE MODE
# =====================================================
#
# Same setup assumptions as the main reference guide:
#   - configure() has been called once at startup
#   - bind_contextvars(file="austen.txt", run_id=42) was called earlier
#
# User code (no change from Path A):
#
#   log = structlog.get_logger()
#   log.info("dictionary_loaded", word_count=143091, backend="hash")
#
# ─── STEP S1: get_logger() returns a proxy ─────────────────────────────
#
# structlog.get_logger() returns a lazy BoundLoggerLazyProxy.  At first
# actual use (.info/.bind/etc), the proxy builds the real bound logger:
#   1. Calls the logger_factory → returns a PrintLogger or WriteLogger
#   2. Wraps it in the wrapper_class (make_filtering_bound_logger result)
#   3. Caches the wrapped logger because cache_logger_on_first_use=True
#
# Notice what's DIFFERENT from stdlib-wrap mode:
#   - No logging.Logger anywhere
#   - No LogRecord anywhere
#   - The "logger at the bottom" is a PrintLogger/WriteLogger whose only
#     job is to call file.write(str) + file.flush()
#
# ─── STEP S2: Level filter runs BEFORE the chain ──────────────────────
#
# make_filtering_bound_logger(logging.INFO) builds a specialized class
# where methods BELOW the configured level are compiled to just
# `return None`.  So log.debug(...) with a level-INFO filter never
# enters the processor chain at all — zero overhead.
#
# log.info(...) with a level-INFO filter continues normally.
#
# ─── STEP S3: BoundLogger builds the initial event_dict ────────────────
#
# Same as Path A:
#     event_dict = {
#         "event": "dictionary_loaded",
#         "word_count": 143091,
#         "backend": "hash",
#     }
#
# ─── STEP S4: Processor chain runs in order ────────────────────────────
#
# Same processors as Path A up through format_exc_info… but the LAST
# processor is different.  Instead of wrap_for_formatter (the stdlib
# bridge), the last processor is a REAL RENDERER that returns a str.
#
# Processor 1: contextvars.merge_contextvars
#     event_dict += {"file": "austen.txt", "run_id": 42}
#
# Processor 2: add_log_level
#     event_dict += {"level": "info"}
#
# Processor 3: TimeStamper(fmt="iso")
#     event_dict += {"timestamp": "2026-04-22T14:28:50.147Z"}
#
# Processor 4: StackInfoRenderer() — no-op here
# Processor 5: format_exc_info — no-op here
#
# Processor 6 (FINAL): JSONRenderer()
#   Receives the fully enriched event_dict and returns a STRING:
#     '{"event": "dictionary_loaded", "word_count": 143091, ...}'
#
#   (Or ConsoleRenderer in dev mode → returns a colored string.)
#
# ─── STEP S5: PrintLogger/WriteLogger writes the string ────────────────
#
# structlog's BoundLogger takes the string returned by the final
# processor and calls the matching method on the underlying logger:
#
#     self._logger.info(rendered_string)
#
# PrintLogger.info just does:
#     print(rendered_string, file=self._file, flush=True)
#
# WriteLogger.info does the same thing slightly faster (no print()
# overhead, direct file.write()+flush() calls).
#
# DONE.  The string is in the file/stream.  No LogRecord was ever made,
# no handler was ever consulted, no hierarchy was ever walked.


# =====================================================
# VISUAL: Standalone vs stdlib-wrap (side by side)
# =====================================================
#
#   ┌─── STANDALONE STRUCTLOG ─────┐    ┌─── STRUCTLOG-ON-STDLIB ─────┐
#   │                              │    │                              │
#   │  log.info("evt", k=v)        │    │  log.info("evt", k=v)        │
#   │         │                    │    │         │                    │
#   │         ▼                    │    │         ▼                    │
#   │  BoundLogger                 │    │  stdlib.BoundLogger          │
#   │  (+ level filter)            │    │                              │
#   │         │                    │    │         │                    │
#   │         ▼                    │    │         ▼                    │
#   │  Processor chain runs:       │    │  Processor chain runs:       │
#   │  • merge_contextvars         │    │  • merge_contextvars         │
#   │  • add_log_level             │    │  • add_log_level             │
#   │  • TimeStamper               │    │  • TimeStamper               │
#   │  • StackInfoRenderer         │    │  • StackInfoRenderer         │
#   │  • format_exc_info           │    │  • format_exc_info           │
#   │  • ConsoleRenderer ←RENDERS  │    │  • wrap_for_formatter ←WRAP  │
#   │    (returns str)             │    │    (returns wrapped dict)    │
#   │         │                    │    │         │                    │
#   │         ▼                    │    │         ▼                    │
#   │  PrintLogger.info(str)       │    │  logging.Logger.info(...)    │
#   │         │                    │    │         │                    │
#   │         ▼                    │    │         ▼                    │
#   │  file.write(str) + flush     │    │  LogRecord propagates up     │
#   │                              │    │    hierarchy                 │
#   │  ═══ END ═══                 │    │         │                    │
#   │                              │    │         ▼                    │
#   │                              │    │  Handler.emit()              │
#   │                              │    │         │                    │
#   │                              │    │         ▼                    │
#   │                              │    │  ProcessorFormatter runs     │
#   │                              │    │  (incl. foreign_pre_chain    │
#   │                              │    │   for stdlib-origin records) │
#   │                              │    │         │                    │
#   │                              │    │         ▼                    │
#   │                              │    │  Final renderer              │
#   │                              │    │  (ConsoleRenderer or JSON)   │
#   │                              │    │         │                    │
#   │                              │    │         ▼                    │
#   │                              │    │  Stream/file I/O             │
#   │                              │    │                              │
#   │                              │    │  ═══ END ═══                 │
#   └──────────────────────────────┘    └──────────────────────────────┘


# =====================================================
# WHEN STANDALONE IS THE RIGHT CHOICE
# =====================================================
#
# Standalone mode is CORRECT, not just acceptable, in a few specific
# scenarios.  If you're ever building one of these, use it without guilt:
#
# 1. ── Tiny CLI utilities or scripts ──
#    A 200-line CLI tool that imports no third-party libraries and
#    doesn't need rotation.  Simpler config, one less concept.
#    PrintLoggerFactory → stdout, use a shell redirect for file output.
#
# 2. ── 12-factor containerized apps (JSON to stdout) ──
#    In Docker/Kubernetes/ECS, the platform collects stdout and ships
#    it to the log aggregator.  Rotation is the platform's job, not
#    yours.  WriteLoggerFactory + JSONRenderer is the minimal setup.
#    Some teams prefer this for clarity — no stdlib handler zoo.
#
# 3. ── Doctests and library code ──
#    structlog's own docs note WriteLogger is "very useful for testing
#    and examples since logging is finicky in doctests".  If you're
#    writing reusable library code that should NOT impose a logging
#    config on consumers, standalone mode avoids polluting the root
#    logger.
#
# 4. ── Performance-critical hot paths ──
#    Marginally faster than stdlib-wrap because you skip LogRecord
#    creation and handler dispatch.  Rarely decisive.
#
# DO NOT use standalone when:
#   - You integrate with third-party libraries that log via stdlib
#     (pandas, chromadb, langchain, httpx, SQLAlchemy, FastAPI, requests,
#      openai, google.generativeai — basically all of them)
#   - You want rotation, multiple handlers, or propagation
#   - You're building for the roadmap from Stage 2 onward — vendor logs
#     will flood stdlib, and you want to capture them in your pipeline


# =====================================================
# GOTCHA: Mixing modes is BAD
# =====================================================
#
# You can't "also use stdlib logging on the side" while structlog is in
# standalone mode.  The two systems would be fully independent:
#
#   Your structlog log calls  →  WriteLogger → app.log
#   Third-party lib log calls →  stdlib root logger → ??? (unhandled)
#
# So you get pretty JSON for your code and unformatted garbage from
# pandas/ChromaDB leaking to stderr through the default root handler.
#
# This is exactly the failure mode that structlog-on-stdlib fixes.
# If you find yourself tempted to mix — stop and switch modes.


# =====================================================
# QUICK REFERENCE — STANDALONE PRIMITIVES
# =====================================================
#
# ── Logger factories (the "underlying logger" producer) ──────────────
#
#   PrintLoggerFactory(file=sys.stdout)
#     • Wraps file.write() in print() calls.
#     • Slightly slower than WriteLogger.
#     • Supports passing a name positional arg to get_logger()
#       (silently ignored — PrintLogger doesn't use logger names).
#
#   WriteLoggerFactory(file=sys.stdout)
#     • Direct file.write() + flush().
#     • ~30% faster than PrintLoggerFactory in benchmarks.
#     • Added in structlog 22.1.0.
#
#   BytesLoggerFactory(file=sys.stdout.buffer)
#     • For renderers that output bytes (e.g. orjson JSONRenderer).
#     • Skip str → bytes encoding step for raw speed.
#     • Rarely needed unless you've measured the encode overhead.
#
# ── Wrapper classes (the thing .info()/.debug() methods live on) ────
#
#   structlog.BoundLogger
#     • The generic default.  Proxies unknown methods to the wrapped
#       logger via __getattr__.  Works with anything.
#
#   structlog.make_filtering_bound_logger(min_level)
#     • Returns a specialized class where methods below min_level are
#       compiled to `return None`.  Fastest level filter in structlog —
#       drops events BEFORE any processor runs.  No logging module used.
#     • Preferred for standalone mode.  Shown in official docs.
#
#   structlog.stdlib.BoundLogger   ← DO NOT USE IN STANDALONE MODE
#     • This is specifically for stdlib-wrap mode.  Requires the
#       underlying logger to be a logging.Logger.  Will crash if
#       paired with PrintLogger/WriteLogger.
#
# ── Renderers (the final processor; returns str or bytes) ────────────
#
#   structlog.dev.ConsoleRenderer(colors=True, pad_event=30)
#     • Human-readable, aligned, ANSI-colored.
#     • Syntax-highlights tracebacks when rich is installed.
#     • Dev-only.  Don't ship colors to production log aggregators.
#
#   structlog.processors.JSONRenderer()
#     • One JSON object per event.  Production default.
#     • Pair with orjson for 3-5x speed:
#         JSONRenderer(serializer=orjson.dumps)
#
#   structlog.processors.KeyValueRenderer(key_order=[...])
#     • logfmt-style output: event="hi" level=info timestamp=...
#     • Compromise between human-readable and machine-parseable.


# =====================================================
# DECISION SUMMARY FOR OUR ROADMAP
# =====================================================
#
# The speller uses structlog-on-stdlib.  Every Stage 1+ project in the
# roadmap will also use structlog-on-stdlib, for one overriding reason:
# EVERY third-party library in the roadmap logs via stdlib.
#
#   Stage 1:  google.generativeai, chromadb, pydantic, langchain, httpx
#   Stage 2:  apache-airflow, boto3, psycopg2, pinecone, kafka-python
#   Stage 3:  sklearn, xgboost, ray, ollama, torch
#   Stage 4:  langgraph, langchain_mcp, openai-agents
#   Stage 5:  prometheus_client, opentelemetry, fastapi, uvicorn
#
# Running any of these in standalone mode means their logs either
# disappear or flood an unconfigured stderr.  Running them under
# stdlib-wrap mode means their logs automatically get:
#   - ISO timestamps
#   - Request IDs from bind_contextvars
#   - NDJSON output queryable with jq/DuckDB
#   - Routed to the same rotating file handler as your code
#
# That's the compounding value that makes stdlib-wrap the production
# standard — and why the speller's pattern carries forward unchanged.


# =====================================================
# REFERENCES
# =====================================================
# structlog — Getting Started (shows standalone config):
#   https://www.structlog.org/en/stable/getting-started.html
# structlog — Loggers (PrintLogger, WriteLogger, BytesLogger):
#   https://www.structlog.org/en/stable/api.html#loggers
# structlog — make_filtering_bound_logger:
#   https://www.structlog.org/en/stable/api.html#structlog.make_filtering_bound_logger
# structlog — "12 factor app" JSON-to-stdout pattern:
#   https://www.structlog.org/en/stable/standard-library.html
# Better Stack — Comprehensive Python Logging with Structlog:
#   https://betterstack.com/community/guides/logging/structlog/
