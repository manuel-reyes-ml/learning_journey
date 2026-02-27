"""
"""

# =============================================================================
# IMPORTS
# =============================================================================

from __future__ import annotations
from typing import Final, Callable, TypedDict, NamedTuple
from dataclasses import dataclass
from enum import IntEnum, unique
from pathlib import Path
import logging


# =============================================================================
# EXPORTS
# =============================================================================

__all__ = [
    "ColoredFormatter",
    "DictDispatch",
    "FilterFunc",
    "ImageData",
    "BmpData",
    "PixelRow",
    "Pixel",
    "ExitCode",
    "ALL_FILTERS",
    "CUR_DIR",
    "bmp_dirs",
    "bmp_constants",
]


# =============================================================================
# CONSTANTS CONFIGURATION
# =============================================================================

# =====================================================
# Type Aliases
# =====================================================

# TypeAlias statement: Improves readability for function Type Hint
#   - Syntax: Callable[[INPUT_TYPES], RETURN_TYPE]
#       - Input parameters in a list
#       - Function that takes a list, returns a list
#       - def process(pixels: list) -> list
type Pixel = list[int]
type PixelRow = list[Pixel]
type ImageData = list[PixelRow]
type HeaderBytes = bytes
type FilterFunc = Callable[[ImageData], ImageData]


# =====================================================
# Constants
# =====================================================

ALL_FILTERS: Final[str] = "all"

# parent = parents[0] = bmp_config.py directory -> py_src/
# parents[1] = project root directory -> filter-more/
CUR_DIR: Final[Path] = Path(__file__).resolve().parent
BASE_DIR: Final[Path] = CUR_DIR.parent


# =====================================================
# Dataclass Frozen Constants
# ===================================================== 
# frozen dataclass (since variables might need runtime protection)

# Directories
@dataclass(frozen=True)
class BmpDirectories:
    """
    """
    FILE_EXT: str = ".bmp"
    INPUT_DIR: Path = BASE_DIR / "images"
    OUT_DIR: Path = CUR_DIR / "filtered_imgs"
    OUT_FNAME: str = f"_filtered{FILE_EXT}"

#BMP file constants
# Final[] Type Hint only-tells type checkers "don't reassign" (IDE, mypy)
# frozen=True Makes instance immutable at runtime 
@dataclass(frozen=True)
class BmpConstants:
    """
    """
    HEADER_SIZE: Final[int] = 14
    SIGNATURE: Final[bytes] = b"BM"
    PAD_HEX: Final[bytes] = b"\x00"
    PIXEL_SIZE: Final[int] = 3
    BPP: Final[int] = 24  # bits per pixel (3 bytes RGB)

# Exit codes (Unix standard)
@unique  # Ensures no duplicate values
class ExitCode(IntEnum):
    """
    """
    SUCCESS = 0
    FAILURE = 1
    KEYBOARD_INTERRUPT = 130
   # BADUSE = 1  Error!

# =====================================================
# Dataclass Instantiation
# =====================================================

# Following PEP 8 standars, name of an instance should be lowercase,
# unless it is a global constant itself.
bmp_dirs = BmpDirectories()
bmp_constants = BmpConstants()


# =============================================================================
# OTHER CLASS CONFIGURATION
# =============================================================================

# Dictionary Dispatch for filters function iteration
class DictDispatch(TypedDict):
    """
    """
    grayscale: FilterFunc
    reflect: FilterFunc
    blur: FilterFunc
    edges: FilterFunc

# NamedTuple for named access patterns. (BmpData.width)
# BMP read result
class BmpData(NamedTuple):
    """
    """
    width: int
    height: int
    pixels: ImageData
    full_header: HeaderBytes


# =============================================================================
# LOGGING CONFIGURATION
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
    

# =============================================================================
# CALLABLE, TYPE ALIAS & DICTIONARY DISPATCH
# =============================================================================
#
# CALLABLE - Type hint for functions:
#     Callable[[input_types], return_type]
#
#     Callable[[], None]           # No params, no return
#     Callable[[str], int]         # str → int
#     Callable[[int, int], float]  # (int, int) → float
#     Callable[[list], list]       # list → list
#
# TYPE ALIAS - Name for a type:
#     FilterFunc = Callable[[list], list]
#     Pixel = list[int]
#     ImageData = list[list[Pixel]]
#
# DICTIONARY DISPATCH - Map names to functions:
#     FUNCS: dict[str, Callable] = {
#         "name1": func1,
#         "name2": func2,
#     }
#
#     # Get and call
#     FUNCS["name1"](args)
#
#     # With validation
#     if name in FUNCS:
#         return FUNCS[name](args)
#     raise ValueError(f"Unknown: {name}")
#
# =============================================================================
# =============================================================================
# FUNCTION DISPATCH QUICK REFERENCE
# =============================================================================
#
# Dictionary dispatch (most common):
#     FUNCS = {"name": func, ...}
#     result = FUNCS[name](args)
#
# getattr() for class methods:
#     func = getattr(self, method_name)
#     result = func(args)
#
# Decorator registry:
#     REGISTRY = {}
#     def register(func):
#         REGISTRY[func.__name__] = func
#         return func
#
#     @register
#     def my_func(): ...
#
# With validation:
#     if name not in FUNCS:
#         raise ValueError(f"Unknown: {name}")
#     FUNCS[name](args)
#
# =============================================================================