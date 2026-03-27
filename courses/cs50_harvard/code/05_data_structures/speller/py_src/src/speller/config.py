"""
"""

# =============================================================================
# IMPORTS
# =============================================================================

from __future__ import annotations

from enum import IntEnum, StrEnum, unique
from collections import namedtuple
from typing import Final, TypedDict, Required, NotRequired
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
    "default_fnames",
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
DICT_FNAMES = namedtuple("DICT_FNAMES", ["large", "small"])


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
    FAILURE = 4
    KEYBOARD_INTERRUPT = 130
    

@unique
class DefaultDirs(StrEnum):
    """
    """
    DICT = "dictionaries"
    KEYS = "keys"
    TXT = "texts"
    LOG = "logs"
    MISS = "misspelled"


class DefaultFileNames(TypedDict, total=False):
    """
    """
    dictionaries: Required[DICT_FNAMES]  # Must be present
    keys: NotRequired[tuple[str, ...]]   # Optional

default_fnames: DefaultFileNames = {
    "dictionaries": DICT_FNAMES("large", "small"),
}


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
    MISS_DIR: Final[Path] = ROOT_DIR / DefaultDirs.MISS
    
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
