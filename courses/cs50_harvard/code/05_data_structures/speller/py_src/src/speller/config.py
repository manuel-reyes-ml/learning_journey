"""
"""

# =============================================================================
# IMPORTS
# =============================================================================

from __future__ import annotations
from enum import IntEnum, StrEnum, unique
from typing import Final, TypedDict
from dataclasses import dataclass
from pathlib import Path
import logging
import sys


# =============================================================================
# EXPORTS
# =============================================================================

__all__ = [
    # Constants
    "MAX_WORD_LENGTH",
    "default_fnames",
    # Configuration
    "ExitCode",
    "file_dirs",
    "fhandler_config",
    "ColoredFormatter",
    # Class
    "FileDirectories",
    "FileHandlerConfig",
]


# =============================================================================
# CONSTANTS CONFIGURATION
# =============================================================================
# =====================================================
# Constants
# =====================================================

MAX_WORD_LENGTH: Final[int] = 45
default_fnames: DefaultFileNames = {
    "dictionaries": ("large", "small"),
    "keys": ("aca.txt", "austen.txt"),
}


# =====================================================
# Class Constants Configuration
# =====================================================

@unique
class ExitCode(IntEnum):
    """
    """
    SUCCESS = 0
    USAGE_ERROR = 1
    FILE_NOT_FOUND = 2
    LOAD_FAILED = 3
    

@unique
class DefaultDirs(StrEnum):
    """
    """
    DICT = "dictionaries"
    KEYS = "keys"
    TXT = "texts"
    LOG = "logs"


class DefaultFileNames(TypedDict):
    """
    """
    dictionaries: tuple[str, ...]
    keys: tuple[str, ...]
    

# =====================================================
# Dataclass Frozen Constants
# ===================================================== 

# frozen=True makes instances immutable.
# slots=True prevents dynamic attribute creation and
# reduces memory fooprint.
# Together they create a truly locked-down data container.
@dataclass(frozen=True, slots=True)
class FileDirectories:
    """
    """
    CUR_DIR: Final[Path] = Path(__file__).resolve().parent  # speller/
    ROOT_DIR: Final[Path] = CUR_DIR.parents[1]  # py_src/
    
    DICT_DIR: Final[Path] = ROOT_DIR / DefaultDirs.DICT
    KEYS_DIR: Final[Path] = ROOT_DIR / DefaultDirs.KEYS
    TXT_DIR: Final[Path] = ROOT_DIR / DefaultDirs.TXT
    LOG_DIR: Final[Path] = ROOT_DIR / DefaultDirs.LOG
    
    def create_log_fname(self) -> str:
        """
        """
        return f"{self.CUR_DIR.name}.log"
    
    @property
    def log_file(self) -> Path:
        """
        """
        return self.LOG_DIR / self.create_log_fname()


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
        """
        """
        return ValueError(f"{var} must be positive (> 0)")
    
    # The position of __post_init__ in source code doesn't matter-
    # Python's calls it automatically after the generated __init__
    # finishes (in dataclasses).
    def __post_init__(self) -> None:
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
        """
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


# =====================================================
# Logging Configuration
# =====================================================

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
    def format(self, record) -> str:
        # Step 1: Get the color for this log level
        color = self.COLORS.get(record.levelno, self.RESET)
        
        # Step 2: Format the message normally first
        # This produces: "14:30:45 : INFO : Your message here"
        # super() calls PARENT's format() methdod
        message = super().format(record)
        
        # Step 3: Wrap with color codes
        return f"{color}{message}{self.RESET}"