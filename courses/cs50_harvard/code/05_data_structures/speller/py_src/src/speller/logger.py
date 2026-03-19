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

__all__ = ["configure_logging"]


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
        logging.DEBUG:     "\033[90m",   # Gray
        logging.INFO:      "\033[92m",   # Green
        logging.WARNING:   "\033[93m",   # Yellow
        logging.ERROR:     "\033[91m",   # Red
        logging.CRITICAL:  "\033[1;91m", # Bold Red
    }
    RESET: Final[str] = "\033[0m"
    
    # Override the parent's format method
    def format(self, record: logging.LogRecord) -> str:
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
    """
    """
    console_handler = logging.StreamHandler(sys.stderr)
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter(
        fmt='%(asctime)s : %(levelname)s : %(message)s',
        datefmt='%H:%M:%S',
    ))
    return console_handler


def _setup_fhandler(
    file_dirs: FileDirectories = file_dirs,
    fhandler_config: FileHandlerConfig = fhandler_config,
) -> RotatingFileHandler:
    """
    """
    file_handler = RotatingFileHandler(
        filename=file_dirs.log_file,
        maxBytes=fhandler_config.max_log_bytes,
        backupCount=fhandler_config.BACKUP_COUNT,
        encoding=fhandler_config.ENCODING,
    ) 
    file_handler.setLevel(logging.DEBUG)
    
    # %(name)s shows module name (speller.main)
    file_handler.setFormatter(logging.Formatter(
        fmt='%(asctime)s : %(name)s : %(levelname)s : %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
    ))
    return file_handler


# =============================================================================
# CORE FUNCTIONS
# =============================================================================

def configure_logging(
    console_verbose: bool = False,
    log_to_file: bool = True,
    custom_console: bool = True,
    custom_formatter: type[logging.Formatter] = ColoredFormatter,
) -> None:
    """
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
        
    # 5. Prevent logs from bubbling up to Python's default root logger
    # (prevents duplicate printing in some environments).
    package_logger.propagate = False