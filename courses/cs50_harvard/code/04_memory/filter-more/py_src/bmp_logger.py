"""
Logging configuration for the py_src package.

Provides a single ``setup_logging()`` function that configures
the package-level logger with colored console output. Uses
``ColoredFormatter`` from ``bmp_config`` to apply ANSI color
codes based on log severity level.

Notes
-----
The logger is scoped to the ``py_src`` package namespace,
meaning all child loggers (e.g., ``py_src.bmp_io``,
``py_src.bmp_filters``) inherit this configuration
automatically via Python's logger hierarchy.
"""

# =============================================================================
# IMPORTS
# =============================================================================

from __future__ import annotations
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Final
import logging
import sys

try:
    from .bmp_config import ColoredFormatter, CUR_DIR, LOGS_DIR
except ImportError as e:
    sys.exit(f"Error: Cannot find relative modules.\nDetails: {e}")
    

# =============================================================================
# MODULE CONFIGURATION
# =============================================================================

# Exports
__all__ = ["setup_logging"]

# Program Constants
LEVEL_DEFAULT = logging.INFO
LOG_FILE_NAME: Final[str] = "bmp_filter.log"
MAX_LOG_BYTES: Final[int] = 5 * 1024 * 1024   # 5 MBD per file
BACKUP_COUNT: Final[int] = 3                  # Keep 3 rotated backups
FORMATTER_CLASS: Final[type[logging.Formatter]] = ColoredFormatter


# =============================================================================
# CORE FUNCTIONS
# =============================================================================

def setup_logging(
    formatter_class: type[logging.Formatter] | None = FORMATTER_CLASS,
    cur_dir: Path = CUR_DIR,
    logs_dir: Path = LOGS_DIR,
    level: int =LEVEL_DEFAULT,
    log_to_file: bool = True,
    console_verbose: bool = False,
    max_bytes: int = MAX_LOG_BYTES,
    log_fname: str = LOG_FILE_NAME,
    backup_count: int = BACKUP_COUNT,
) -> None:
    """
    Configure the package-level logger with colored console output.

    Sets up a ``StreamHandler`` on ``sys.stdout`` with the specified
    formatter class and log level. Scoped to the ``py_src`` package
    logger so all child module loggers inherit the configuration.

    Parameters
    ----------
    formatter_class : type[logging.Formatter] or None, optional
        Formatter class to use for console output. Defaults to
        ``ColoredFormatter``, which applies ANSI color codes by
        log level. Cannot be None.
    cur_dir : Path, optional
        Directory whose ``.name`` attribute determines the logger
        namespace (default is the ``py_src/`` directory).
    level : int, optional
        Logging level threshold (default ``logging.INFO``). Use
        ``logging.DEBUG`` for verbose output.

    Raises
    ------
    ValueError
        If ``formatter_class`` is None.

    Notes
    -----
    Safe to call multiple times — clears existing handlers before
    attaching a new one to prevent duplicate log output. Sets
    ``propagate = False`` to prevent messages from bubbling up
    to Python's root logger.

    Examples
    --------
    >>> setup_logging()  # INFO level with colors
    >>> setup_logging(level=logging.DEBUG)  # verbose mode
    """
    if not formatter_class:
        raise ValueError("formatter_class cannot be empty")
    
    level = logging.DEBUG if console_verbose else level
    
    # 1. Grab the top-level logger for your package
    # cur_dir.name gives the current directory in string "py_src"
    package_logger = logging.getLogger(cur_dir.name)
    package_logger.setLevel(logging.DEBUG)  # Let handlers decide their own level
    
    # 2. Prevent duplicate handlers if this function is called multiple times
    if package_logger.hasHandlers():
        package_logger.handlers.clear()
        
    # 3. Console handler, colored, respected the 'level' parameter
    console_handler = logging.StreamHandler(sys.stderr)
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter_class(
        fmt='%(asctime)s : %(levelname)s : %(message)s',
        datefmt='%H:%M:%S',
    ))
    package_logger.addHandler(console_handler)
    
    if console_verbose:
        logging.debug("Verbose mode enabled (debug output)")
    
    # 4. File handler - plain text, always captures DEBUG
    if log_to_file:
        # parents=True: create any missing parent directories
        # exist_ok=True: no error if directory already exists
        logs_dir.mkdir(parents=True, exist_ok=True)
        log_file = logs_dir / log_fname
        
        file_handler = RotatingFileHandler(
            filename=log_file,
            maxBytes=max_bytes,
            backupCount=backup_count,
            encoding="utf-8",
        )
        file_handler.setLevel(logging.DEBUG)
        # %(name)s shows module name (py_src.bmp_io)
        file_handler.setFormatter(logging.Formatter(
            fmt='%(asctime)s : %(name)s : %(levelname)s : %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S',
        ))
        package_logger.addHandler(file_handler)
    
    # 5. Prevent logs from bubbling up to Python's default root logger
    # (prevents duplicate printing in some environments)
    package_logger.propagate = False
