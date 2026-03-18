"""
"""

# =============================================================================
# IMPORTS
# =============================================================================

from __future__ import annotations
from logging.handlers import RotatingFileHandler
from pathlib import Path
import logging
import sys

try:
    from speller.config import (
        file_dirs,
        fhandler_config,
        FileDirectories,
        FileHandlerConfig,
        ColoredFormatter,
    )
except ImportError as e:
    sys.exit(f"Error: Cannot find relative modules.\nDetails: {e}")
    

# =============================================================================
# EXPORTS
# =============================================================================

__all__ = ["config_logging"]


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

def config_logging(
    console_verbose: bool = False,
    log_to_file: bool = True,
    custom_console: bool = True,
    file_dirs: FileDirectories = file_dirs,
    fhandler_config: FileHandlerConfig = fhandler_config,
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
        
        package_logger.addHandler(file_handler)
        
    # 5. Prevent logs from bubbling up to Python's default root logger
    # (prevents duplicate printing in some environments).
    package_logger.propagate = False