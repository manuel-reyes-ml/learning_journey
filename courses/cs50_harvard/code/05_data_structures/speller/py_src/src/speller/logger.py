"""Logging configuration for the speller package.

Provides :func:`configure_logging`, the single entry point that
attaches all handlers to the ``"speller"`` root logger.  Every module
in the package calls ``logging.getLogger(__name__)`` to get a child
logger; this module is the only place that attaches handlers and sets
levels.

Two-handler strategy
--------------------
Console handler (``StreamHandler``)
    Colored output via :class:`ColoredFormatter`.  Level controlled
    by ``--verbose`` flag at runtime.

File handler (``RotatingFileHandler``)
    Plain text.  Always captures ``DEBUG`` level.  Rotates at
    ``FILE_MB`` megabytes with ``BACKUP_COUNT`` backups.

Library logging pattern
-----------------------
:data:`logging.NullHandler` added in ``__init__.py`` follows the
standard Python library convention: a library must never configure
logging on import.  Only the *application* entry point
(``__main__.py``) calls :func:`configure_logging` to activate real
handlers.  This prevents log pollution when the package is imported
by other programs.

Roadmap relevance
-----------------
Identical structure reused across every future project: one
:func:`configure_logging`, one root logger per package, child loggers
per module via ``__name__``.

References
----------
.. [1] Python Docs — Logging HOWTO
   https://docs.python.org/3/howto/logging.html
.. [2] Python Docs — RotatingFileHandler
   https://docs.python.org/3/library/logging.handlers.html
"""

# =============================================================================
# IMPORTS
# =============================================================================

from __future__ import annotations

import logging
import sys
from logging.handlers import RotatingFileHandler
from typing import Final, override

from speller.config import (
    FileDirectories,
    FileHandlerConfig,
    fhandler_config,
    file_dirs,
)

# No ImportError sys.exit() on regular module so the
# error propagates to the caller (__main__.py).


# =============================================================================
# EXPORTS
# =============================================================================

__all__ = ["ColoredFormatter", "configure_logging"]


# =============================================================================
# CUSTOM FORMATTER CLASS
# =============================================================================


# Inherits from Python's built-in Formatter
class ColoredFormatter(logging.Formatter):
    """
    Custom logging formatter that adds ANSI color codes based on log level.

    Inherits from Python's built-in logging.Formatter and overrides the
    format method to wrap log messages in terminal color codes.

    Attributes
    ----------
    COLORS : dict of {int: str}
        Mapping of logging level constants to ANSI color codes.
    RESET : str
        ANSI code to reset terminal color to default.

    Examples
    --------
    >>> handler = logging.StreamHandler()
    >>> handler.setFormatter(ColoredFormatter(
    ...     fmt='%(levelname)s : %(message)s'
    ... ))
    >>> logger.addHandler(handler)
    >>> logger.info("This appears in green")
    >>> logger.error("This appears in red")
    """

    # Color codes for each level
    COLORS: Final[dict[int, str]] = {
        logging.DEBUG: "\033[90m",  # Gray
        logging.INFO: "\033[92m",  # Green
        logging.WARNING: "\033[93m",  # Yellow
        logging.ERROR: "\033[91m",  # Red
        logging.CRITICAL: "\033[1;91m",  # Bold Red
    }
    RESET: Final[str] = "\033[0m"

    # Override the parent's format method
    # Apply override decorator to a subclass method that overrides a base class method.
    # Static type checkers will warn if the base class is modified such that the overridden method
    # no longer exists — avoiding accidentally turning a method override into dead code.
    @override
    def format(self, record: logging.LogRecord) -> str:
        """Format a log record with ANSI color codes for the record's level.

        Overrides :meth:`logging.Formatter.format`.  Calls the parent
        implementation first to produce the fully formatted message string
        (timestamp, level name, message body), then wraps the result in
        the ANSI escape sequence for the record's log level.

        Parameters
        ----------
        record : logging.LogRecord
            The log record to format.  Provided automatically by the
            logging framework — callers never pass this directly.

        Returns
        -------
        str
            The formatted message string wrapped in ANSI color codes,
            followed by :attr:`RESET` to prevent color bleed into
            subsequent terminal output.

        Notes
        -----
        ``super().format(record)`` is called before color wrapping so
        that exception tracebacks appended by the parent formatter are
        also wrapped in the level's color, matching the message style.
        """
        # Step 1: Get the color for this log level
        color = self.COLORS.get(record.levelno, self.RESET)

        # Step 2: Format the message normally first
        # This produces: "14:30:45 : INFO : Your message here"
        # super() calls PARENT's format() methdod
        message = super().format(record)

        # Step 3: Wrap with color codes
        return f"{color}{message}{self.RESET}"


# =============================================================================
# INTERNAL HELPER FUNCTIONS
# =============================================================================


def _setup_chandler(
    *,
    level: int,
    formatter: type[logging.Formatter],
) -> logging.StreamHandler:
    """Create and configure a console (stream) logging handler.

    Writes to ``sys.stderr`` so log output and program output
    (``stdout``) remain on separate streams and can be redirected
    independently.

    Parameters
    ----------
    level : int
        Minimum log level for this handler (e.g. ``logging.INFO``).
        Derived from the ``--verbose`` flag in ``__main__.py``.
    formatter : type[logging.Formatter]
        Formatter class to instantiate.  Pass plain
        ``logging.Formatter`` in tests to suppress ANSI color codes
        from captured output.

    Returns
    -------
    logging.StreamHandler
        Fully configured handler ready to add to a logger.
    """
    console_handler = logging.StreamHandler(sys.stderr)
    console_handler.setLevel(level)
    console_handler.setFormatter(
        formatter(
            fmt="%(asctime)s : %(levelname)s : %(message)s",
            datefmt="%H:%M:%S",
        )
    )
    return console_handler


def _setup_fhandler(
    file_dirs: FileDirectories = file_dirs,
    fhandler_config: FileHandlerConfig = fhandler_config,
) -> RotatingFileHandler:
    """Create and configure a rotating file logging handler.

    Always captures ``DEBUG`` level regardless of console verbosity so
    full diagnostic information is available on disk even when the
    console shows only ``INFO``.  Rotates at
    :attr:`~speller.config.FileHandlerConfig.max_log_bytes` and keeps
    :attr:`~speller.config.FileHandlerConfig.BACKUP_COUNT` backups.

    Parameters
    ----------
    file_dirs : FileDirectories, optional
        Provides the log file path.  Defaults to the module-level
        singleton from ``config.py``.
    fhandler_config : FileHandlerConfig, optional
        Provides size and rotation settings.  Defaults to the
        module-level singleton from ``config.py``.

    Returns
    -------
    RotatingFileHandler
        Fully configured handler ready to add to a logger.

    Notes
    -----
    The log directory is created by :func:`configure_logging` before
    this function is called.  Directory creation is a side effect and
    belongs at the call site, not inside a handler factory.
    """
    file_handler = RotatingFileHandler(
        filename=file_dirs.log_file.flog_path,
        maxBytes=fhandler_config.max_log_bytes,
        backupCount=fhandler_config.BACKUP_COUNT,
        encoding=fhandler_config.ENCODING,
    )
    file_handler.setLevel(logging.DEBUG)

    # %(name)s shows module name (speller.main)
    file_handler.setFormatter(
        logging.Formatter(
            fmt="%(asctime)s : %(name)s : %(levelname)s : %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
    )
    return file_handler


# =============================================================================
# CORE FUNCTIONS
# =============================================================================


def configure_logging(
    *,
    console_verbose: bool = False,
    log_to_file: bool = True,
    custom_console: bool = True,
    custom_formatter: type[logging.Formatter] = ColoredFormatter,
) -> None:
    """Configure all handlers for the package root logger.

    Must be called once at program startup (inside ``main()`` in
    ``__main__.py``) before any log messages are emitted.  Safe to
    call multiple times — existing handlers are cleared first to
    prevent duplicate output.

    Parameters
    ----------
    console_verbose : bool, optional
        ``True`` sets the console handler to ``DEBUG`` so all messages
        appear in the terminal.  ``False`` (default) shows ``INFO``
        and above.  Controlled by the ``--verbose`` CLI flag.
    log_to_file : bool, optional
        ``True`` (default) attaches a :class:`RotatingFileHandler`
        writing ``DEBUG``-level logs to disk.  ``False`` disables file
        logging.  Controlled by the ``--no-log-file`` CLI flag.
    custom_console : bool, optional
        ``True`` (default) uses :class:`ColoredFormatter` for the
        console handler.  Set ``False`` in tests to suppress ANSI codes.
    custom_formatter : type[logging.Formatter], optional
        Formatter class to use when ``custom_console=True``.  Defaults
        to :class:`ColoredFormatter`.  Injectable for testing.

    Notes
    -----
    Logger hierarchy::

        speller                 ← root package logger (configured here)
        ├── speller.benchmarks
        ├── speller.config
        ├── speller.dictionaries
        ├── speller.register
        ├── speller.speller
        └── speller.text_processor

    Child loggers propagate messages upward to ``speller``, which
    dispatches them to the console and file handlers.
    ``propagate = False`` on the root logger prevents messages reaching
    Python's global root logger and being printed twice.
    """
    # 1. Grab the top-level logger for the package
    # CUR_DIR.name gives the current directory in string "speller"
    package_logger = logging.getLogger(file_dirs.CUR_DIR.name)
    package_logger.setLevel(logging.DEBUG)  # Let handlers decide their own level

    # 2. Prevent duplicate handlers if this function is called multiple times
    if package_logger.hasHandlers():
        package_logger.handlers.clear()

    # 3. Console handler, colored(optional), respected the 'level' parameter
    level = logging.DEBUG if console_verbose else fhandler_config.LEVEL_DEFAULT
    formatter = custom_formatter if custom_console else logging.Formatter

    console_handler = _setup_chandler(level=level, formatter=formatter)
    package_logger.addHandler(console_handler)

    # 4. File handler - plain text, always captures DEBUG
    if log_to_file:
        # parents=True: create any missing parent directories
        # exist_ok=True: no error if directory already exists
        file_dirs.LOG_DIR.mkdir(parents=True, exist_ok=True)

        file_handler = _setup_fhandler()
        package_logger.addHandler(file_handler)

    # 5. When 'False' - prevents logs from bubbling up to Python's default root logger
    # (prevents duplicate printing in some environments).
    package_logger.propagate = True
