"""
"""

from __future__ import annotations
from typing import Final
import logging


# =============================================================================
# Exports
# =============================================================================

__all__ = [
    "ColoredFormatter",
    "BMP_HEADER_SIZE",
    "BMP_SIGNATURE",
    "PAD_HEX",
    "PIXEL_SIZE",
    "BPP",
]


# =============================================================================
# Constants
# =============================================================================

BMP_HEADER_SIZE: Final[int] = 14
BMP_SIGNATURE: Final[bytes] = b"BM"
PAD_HEX: Final[bytes] = b"\x00"
PIXEL_SIZE: Final[int] = 3
BPP: Final[int] = 24  # bits per pixel (3 bytes RGB)


# =============================================================================
# Configuration Classes
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
    RESET: Final[str] = f"\033[0m"
    
    # Override the parent's format method
    def format(self, record) -> str:
        # Step 1: Get the color for this log level
        color = self.COLORS.get(record.levelno, self.RESET)
        
        # Step 2: Format the message normally first
        # This produces: "14:30:45 : INFO : Your message here"
        message = super().format(record)  # super() -> Call Parent's format()
        
        # Step 3: Wrap with color codes
        return f"{color}{message}{self.RESET}"