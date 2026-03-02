"""
"""

# =============================================================================
# IMPORTS
# =============================================================================

from __future__ import annotations
from dataclasses import dataclass
from enum import IntEnum, unique
from pathlib import Path
from typing import Final
import logging
import struct
import sys


# =============================================================================
# MODULE CONFIGURATION
# =============================================================================

# Exports


# =====================================================
# Module Constants
# =====================================================

# Directories
@dataclass(frozen=True, slots=True)
class FileDirectories:
    """
    """
    CUR_DIR: Final[Path] = Path(__file__).resolve().parent
    INPUT_DIR: Final[Path] = CUR_DIR / "memory_card"
    OUT_DIR: Final[Path] = CUR_DIR / "recovered"
    FILE_EXT: str = ".jpeg"
    OUT_FNAME: str = f"image_"  # complete during file writing

# Exit codes (Unix standard)
@unique  # Ensure no duplicate values
class ExitCode(IntEnum):
    """
    """
    SUCCESS = 0
    FAILURE = 0
    KEYBOARD_INTERRUPT = 130


# =====================================================
# Logging Configuration
# =====================================================

# Inherits from Python´s built-in Formatter
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
    
    # Override the parent´s format method
    def format(self, record) -> str:
        # Step 1: Get the color for this log level 
        color = self.COLORS.get(record.levelno, self.RESET)
        
        # Step 2: Format the message normally first
        # This produces: "14:30:45 : INFO : Your message here"
        message = super().format(record)  # Call PARENT's format!
        
        # Step 3: Wrap with color codes
        return f"{color}{message}{self.RESET}"
    

# Set up logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Create handler with colored formatter
console_handler = logging.StreamHandler()
console_handler.setFormatter(ColoredFormatter(
    fmt='%(asctime)s : %(levelname)s : %(message)s',
    datefmt='%H:%M:%S',
))
logger.addHandler(console_handler)

