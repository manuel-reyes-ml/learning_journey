"""Structured logging configuration for the llm_api_smoke_test package.

Wires structlog *under* stdlib ``logging`` so every log entry — whether
emitted via ``structlog.get_logger()`` or via ``logging.getLogger()`` —
flows through the same processor chain and the same handlers.  Same
architecture as :mod:`speller.structured_logger`; reusing it here means
both packages emit identically shaped NDJSON, queryable with the same
``jq`` / DuckDB queries.

Why structlog-on-stdlib (not standalone)?
-----------------------------------------
Every LLM SDK in the roadmap (``anthropic``, ``google-genai``,
``langchain``, ``langgraph``, ``httpx``, ``openai``) emits logs via the
stdlib ``logging`` module.  Running structlog standalone would leave
those vendor logs unformatted or lost.  Running under stdlib captures
them into the same NDJSON file as your own code.

Three handlers per call to :func:`configure_structured_logging`
---------------------------------------------------------------
1. Console handler — pretty ``key=value`` via
   :class:`structlog.dev.ConsoleRenderer`.
2. File handler — compact NDJSON via
   :class:`structlog.processors.JSONRenderer`.  Queryable by ``jq``,
   DuckDB's ``read_json_auto``, Datadog, ELK, CloudWatch Logs Insights.
3. Indented JSON file handler — same payload as #2 with ``indent=2``
   for grep-and-read debugging.

Roadmap relevance
-----------------
- DataVault:   ``bind_contextvars(query_id=..., model=...)`` per LLM call.
- PolicyPulse: ``bind_contextvars(request_id=..., user_id=...)`` per RAG turn.
- AFC:         ``bind_contextvars(symbol=..., strategy=...)`` per backtest.

References
----------
.. [1] structlog — Standard Library Integration
   https://www.structlog.org/en/stable/standard-library.html
"""

# =============================================================================
# IMPORTS
# =============================================================================

from __future__ import annotations

import logging
import structlog
import sys

from dataclasses import dataclass
from logging.handlers import RotatingFileHandler
from pathlib import Path

from platformdirs import PlatformDirs
from structlog.types import EventDict, Processor, WrappedLogger
from typing import Any, Final, NamedTuple, TextIO

# =============================================================================
# EXPORTS
# =============================================================================

__all__ = ["configure_structured_logging", "get_structured_logger"]


# =============================================================================
# MODULE CONFIGURATION
# =============================================================================
# =====================================================
# Constants
# =====================================================

# What platformdirs does?
# Given an app name, it returns the right place to write files on the current OS.
# The library knows about:
#   - Linux: XDG Base Directory Specification (~/.local/share, ~/.config, ~/.cache, ~/.local/state)
#   - macOS: Apple's guidance (~/Library/Application Support, ~/Library/Caches, ~/Library/Logs)
#   - Windows: AppData\Local and AppData\Roaming via CSIDL APIs
#   - Android: App-private storage conventions
#   - AWS:
#
# Module-level singleton - configured once, used everywhere
_PLATFORM_DIRS: Final[PlatformDirs] = PlatformDirs(
    appname="llm-api-smoke-test",
    appauthor="manuelreyes",  # Used on windows only; harmless on Unix
    ensure_exists=True,  # Create dirs on first access
)

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


# =====================================================
# Dataclass Frozen Constants
# =====================================================

class LogFilesPath(NamedTuple):
    """Resolved paths for the structured-logging output files.

    Two on-disk files are produced so the compact (machine-parseable)
    and indented (human-readable) views can coexist without one
    overwriting the other.

    Attributes
    ----------
    struct_path : Path
        Compact NDJSON output — one JSON object per line, no
        whitespace.  Consumed by ``jq``, DuckDB, Datadog, ELK,
        CloudWatch.
    struct_indent_path : Path
        Indented JSON (``indent=2``) variant.  Same payload as
        ``struct_path`` but formatted for grep-and-read debugging.
    """
    
    struct_path: Path
    struct_indent_path: Path


@dataclass(frozen=True, slots=True)
class FileDirectories:
    """Resolved filesystem paths for the package's writable directories.

    Uses :class:`platformdirs.PlatformDirs` to put logs in
    OS-appropriate user locations (``~/Library/Logs/llm-api-smoke-test``
    on macOS, ``%APPDATA%\\llm-api-smoke-test\\Logs`` on Windows,
    ``~/.local/state/llm-api-smoke-test/log`` on Linux) rather than
    inside the project tree.  The package therefore works identically
    when installed editable, from a wheel, or from a frozen
    distribution — no read-only ``site-packages`` failures.

    ``frozen=True`` prevents accidental reassignment; ``slots=True``
    reduces memory footprint.

    Attributes
    ----------
    LOG_DIR : Path
        Per-user log directory resolved by ``platformdirs``.
        Writable on every supported OS.
    CUR_DIR : Path
        Absolute path to the ``llm_api_smoke_test/`` source directory.
        Used purely as a naming anchor by :meth:`create_log_fname` —
        not for resolving any other path.
    """
    
    # --- Writable, per-user paths (resolved by platformdirs) --------
    LOG_DIR: Final[Path] = _PLATFORM_DIRS.user_log_path
    
    # `CUR_DIR` is no longer needed by path resolution, but keep it
    # for the existing `create_log_fname()` method which uses
    # `self.CUR_DIR.name` for the log filename. It's now purely a
    # naming helper, not a path anchor.
    CUR_DIR: Final[Path] = Path(__file__).resolve().parent  # llm_api_smoke_test/
    
    def create_log_fname(self) -> tuple[str, str]:
        """Build the two log filenames from the package directory name.

        Uses ``CUR_DIR.name`` (``"llm_api_smoke_test"``) so the filenames
        stay in sync with any future package rename without manual
        updates.

        Returns
        -------
        tuple of (str, str)
            Two filenames in order:

            - ``llm_api_smoke_test.log``        — compact NDJSON.
            - ``llm_api_smoke_test_indent.log`` — indented JSON.
        """
        s_log = f"{self.CUR_DIR.name}.log"
        s_indent_log = f"{self.CUR_DIR.name}_indent.log"
        return s_log, s_indent_log
    
    @property  # Access function's return as an attribute
    def log_file(self) -> LogFilesPath:
        """Full resolved paths to the two rotating log files.

        Combines :attr:`LOG_DIR` with the result of
        :meth:`create_log_fname` for each file.

        Returns
        -------
        LogFilesPath
            NamedTuple of absolute paths — one for the compact NDJSON
            log, one for the indented variant.
        """
        s_log, s_indent_log = self.create_log_fname()
        
        s_log_path = self.LOG_DIR / s_log
        s_indent_log_path = self.LOG_DIR / s_indent_log
        
        return LogFilesPath(s_log_path, s_indent_log_path)


@dataclass(frozen=True, slots=True)
class FileHandlerConfig:
    """
    Immutable configuration for the rotating log file handler.

    All fields are frozen (read-only) constants that control log file
    size, rotation, and encoding. Use the ``max_log_bytes`` property
    to get the computed byte limit.

    Attributes
    ----------
    LEVEL_DEFAULT : int
        Default logging level for console output (``logging.INFO``).
    ENCODING : str
        Character encoding for log files.
    BACKUP_COUNT : int
        Number of rotated backup log files to retain.
    FILE_MB : int
        Maximum log file size in megabytes.
    MEGABYTE : int
        Bytes per kilobyte (1024).
    KILOBYTE : int
        Bytes per unit (1024).
    """
    
    LEVEL_DEFAULT: Final[int] = logging.INFO
    ENCODING: Final[str] = "utf-8"
    BACKUP_COUNT: Final[int] = 3
    FILE_MB: Final[int] = 5
    MEGABYTE: Final[int] = 1024
    KILOBYTE: Final[int] = 1024
    
    def negative_value(self, var: str) -> Exception:
        """Build a :class:`ValueError` for an invalid configuration field.

        Centralises the error message format so all ``__post_init__``
        validation checks produce consistent messages.

        Parameters
        ----------
        var : str
            Name of the offending field (e.g. ``"BACKUP_COUNT"``).

        Returns
        -------
        ValueError
            Ready-to-raise exception with a descriptive message.
        """
        return ValueError(f"{var} must be positive (>0)")
    
    # The position of __post_init__ in source code doesn't matter-
    # Python's calls it automatically after the generated __init__
    # finishes (in dataclasses).
    def __post_init__(self) -> None:
        """Validate that all numeric configuration fields are positive.

        Called automatically by the dataclass machinery after ``__init__``
        completes.  Raises :exc:`ValueError` (via :meth:`negative_value`)
        for any field that is zero or negative, because a log handler
        configured with non-positive values will fail silently at runtime.

        Raises
        ------
        ValueError
            If any of ``BACKUP_COUNT``, ``FILE_MB``, ``MEGABYTE``, or
            ``KILOBYTE`` is less than or equal to zero.

        Notes
        -----
        ``frozen=True`` dataclasses still support ``__post_init__`` —
        the freeze constraint applies to attribute *assignment after*
        init, not to the init process itself.  All validation here runs
        before the instance is returned to the caller.
        """
        if self.BACKUP_COUNT <= 0:
            raise self.negative_value("BACKUP_COUNT")
        if self.FILE_MB <= 0:
            raise self.negative_value("FILE_MB")
        if self.MEGABYTE <= 0:
            raise self.negative_value("MEGABYTE")
        if self.KILOBYTE <= 0:
            raise self.negative_value("KILOBYTE")
        
    @property  # Access function's return as an attribute
    def max_log_bytes(self) -> int:
        """Maximum log file size in bytes.

        Converts :attr:`FILE_MB` from megabytes to bytes using the
        standard definition: 1 MB = 1 024 × 1 024 bytes.  This is the
        value passed to :class:`~logging.handlers.RotatingFileHandler`
        as ``maxBytes``.

        Returns
        -------
        int
            Maximum size in bytes (default: 5 × 1 024 × 1 024 = 5 242 880).
        """
        return self.FILE_MB * self.MEGABYTE * self.KILOBYTE


# =====================================================
# Dataclass Instantiation
# =====================================================

file_dirs = FileDirectories()

try:
    fhandler_config = FileHandlerConfig()
except ValueError as e:
    sys.exit(f"Error: Invalid FileHandlerConfig setting: {e}")


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
        """Pull the configured keys to the front of ``event_dict``.

        See :func:`_reorder_keys` for the full description.  This is the
        closure that captures ``preferred_order`` and applies the
        reordering on each invocation.
        """
        ordered: dict[str, Any] = {}
        for key in preferred_order:
            if key in event_dict:
                # pop() does two things: returns the value AND
                # removes the key from event_dict. 
                ordered[key] = event_dict.pop(key)
        
        # update() merges one dict into another in place. For each
        # key-value pair in the argument, it writes that pair into
        # the receiving dict:
            # - If the key doesn't exist in the receiver → it's added
            #   at the end (preserving the receiver's insertion order,
            #   then the argument's order).
            # - If the key already exists in the receiver → its value
            #   is overwritten.
        ordered.update(event_dict)  # .update() returns None
        return ordered
    
    return processor


def _setup_chandler(
    *,
    level: int,
    custom_console: bool = True,
) -> logging.StreamHandler[TextIO]:
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
    file_dirs: FileDirectories,
    fhandler_config: FileHandlerConfig
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
        filename=file_dirs.log_file.struct_path,
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
    file_dirs: FileDirectories,
    fhandler_config: FileHandlerConfig,
) -> RotatingFileHandler:
    """Create a rotating file handler that emits indented JSON.

    Twin of :func:`_setup_fhandler`, but configures
    :class:`~structlog.processors.JSONRenderer` with ``indent=2`` so
    the on-disk output is human-readable.  Writes to a separate file
    (``llm_api_smoke_test_indent.log``) to avoid clobbering the
    compact NDJSON used by log aggregators.

    Parameters
    ----------
    file_dirs : FileDirectories
        Provides the log file path.
    fhandler_config : FileHandlerConfig
        Provides size and rotation settings.

    Returns
    -------
    RotatingFileHandler
        Fully configured handler ready to attach to a logger.

    Notes
    -----
    Why two JSON files (compact and indented)?
        Compact NDJSON is what ``jq``, DuckDB, and log aggregators
        expect — one JSON object per line, no whitespace.  Indented
        JSON is what humans want when grepping raw log files during
        development.  Keeping both removes the trade-off.
    """
    file_handler_indent = RotatingFileHandler(
        filename=file_dirs.log_file.struct_indent_path,
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
                structlog.processors.JSONRenderer(indent=2),  # indent JSON output to improve readability
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
    structlog.configure(
        processors=[
            *_SHARED_PROCESSORS,  # unpacks your 6 shared processors
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,  # the 7th processor
        ],
        wrapper_class=structlog.stdlib.BoundLogger,
        logger_factory=structlog.stdlib.LoggerFactory(),
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
        file_handler = _setup_fhandler(file_dirs, fhandler_config)
        package_logger.addHandler(file_handler)
        
        # Generate JSON log with indentation = 2 for human readability
        file_handler_indent = _setup_fhandler_indent(file_dirs, fhandler_config)
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