"""
"""

# =============================================================================
# IMPORTS
# =============================================================================

from __future__ import annotations
from dataclasses import dataclass
from enum import IntEnum, StrEnum, unique
from pathlib import Path
from typing import Final



# =============================================================================
# EXPORTS
# =============================================================================

__all__ = []


# =============================================================================
# CONSTANTS CONFIGURATION
# =============================================================================


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
    
    
    