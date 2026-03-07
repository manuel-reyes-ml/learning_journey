"""
BMP configuration module for image filter processing.

Provides centralized type definitions, constants, data structures,
and logging configuration used across all modules in the py_src
package. Follows a single-source-of-truth pattern where all shared
types, paths, and BMP-specific constants are defined here and
imported by other modules.

Notes
-----
Uses ``from __future__ import annotations`` to enable lazy evaluation
of type hints, allowing forward references (e.g., ``PixelRow``
referencing ``Pixel`` before ``Pixel`` is defined).
"""

# =============================================================================
# IMPORTS
# =============================================================================

from __future__ import annotations
from dataclasses import dataclass
from enum import IntEnum, unique
from pathlib import Path
import logging
from typing import (
    Final,
    Callable,
    NamedTuple,
    Literal,
)


# =============================================================================
# EXPORTS
# =============================================================================

__all__ = [
    "ColoredFormatter",
    "FilterName",
    "ImageData",
    "FilterFunc",
    "DictFuncs",
    "FilterInfo",
    "RegisterOut",
    "ImageSize",
    "BmpData",
    "PixelRow",
    "Pixel",
    "ExitCode",
    "BrightDarkFilter",
    "ALL_FILTERS",
    "CUR_DIR",
    "LOGS_DIR",
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
type PixelRow = list[Pixel]
type ImageData = list[PixelRow]
type HeaderBytes = bytes
type FilterFunc = Callable[[ImageData], ImageData]
type DictFuncs = dict[str, FilterInfo]
type RegisterOut = Callable[[FilterFunc], FilterFunc]

# Keeps type checker aware of valid filter name (production-grade type safety)
type FilterName = Literal["grayscale", "reflect", "blur", "edges", "brighten", "darken"]


# =====================================================
# Constants
# =====================================================

ALL_FILTERS: Final[str] = "all"

# parent = parents[0] = bmp_config.py directory -> py_src/
# parents[1] = project root directory -> filter-more/
CUR_DIR: Final[Path] = Path(__file__).resolve().parent
BASE_DIR: Final[Path] = CUR_DIR.parent
LOGS_DIR: Final[Path] = CUR_DIR / "logs"


# =====================================================
# Dataclass Frozen Constants
# ===================================================== 
# frozen dataclass (since constants might need runtime protection)

# Directories
# slots=True prevents dynamic attribute creation and,
# reduces memory footprint.
@dataclass(frozen=True, slots=True)
class BmpDirectories:
    """
    Immutable directory and file extension configuration for BMP I/O.

    Centralizes all filesystem paths and naming conventions used
    for reading input images and writing filtered output files.

    Attributes
    ----------
    FILE_EXT : str
        Standard BMP file extension.
    INPUT_DIR : Path
        Default directory for source BMP images.
    OUT_DIR : Path
        Default directory for filtered output images.
    OUT_FNAME : str
        Default suffix appended to output file names.

    Examples
    --------
    >>> dirs = BmpDirectories()
    >>> dirs.INPUT_DIR
    PosixPath('.../filter-more/images')
    >>> dirs.FILE_EXT
    '.bmp'
    """
    FILE_EXT: str = ".bmp"
    INPUT_DIR: Path = BASE_DIR / "images"
    OUT_DIR: Path = CUR_DIR / "filtered_imgs"
    OUT_FNAME: str = f"_filtered{FILE_EXT}"

#BMP file constants
# Final[] Type Hint only-tells type checkers "don't reassign" (IDE, mypy)
# frozen=True Makes instance immutable at runtime 
@dataclass(frozen=True, slots=True)
class BmpConstants:
    """
    Immutable BMP file format constants.

    Defines the binary structure parameters required for reading
    and writing 24-bit BMP files, including header sizes, byte
    signatures, and pixel encoding details.

    Attributes
    ----------
    HEADER_SIZE : int
        Size of the BMP file header in bytes (always 14).
    SIGNATURE : bytes
        Magic bytes identifying a valid BMP file (``b"BM"``).
    PAD_HEX : bytes
        Null byte used for row padding alignment.
    PIXEL_SIZE : int
        Number of bytes per pixel (3 for 24-bit BGR).
    BPP : int
        Bits per pixel (24 for 3-channel BGR).

    Examples
    --------
    >>> consts = BmpConstants()
    >>> consts.SIGNATURE
    b'BM'
    >>> consts.BPP
    24
    """
    HEADER_SIZE: Final[int] = 14
    SIGNATURE: Final[bytes] = b"BM"
    PAD_HEX: Final[bytes] = b"\x00"
    PIXEL_SIZE: Final[int] = 3
    BPP: Final[int] = 24  # bits per pixel (3 bytes RGB)


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

@dataclass
class FilterInfo:
    """
    Metadata container for a registered image filter.

    Bundles a filter function with its display name and
    human-readable description. Stored as values in the
    ``FILTERS`` dispatch dictionary and accessed by the
    CLI help system and ``process_filter()`` dispatch.

    Attributes
    ----------
    func : FilterFunc
        The callable filter function.
    name : str
        Display name used as the dictionary key and in logs.
    description : str
        Short label shown in ``--filter-help`` output.
    """
    func: FilterFunc
    name: str
    description: str

# Exit codes (Unix standard)
@unique  # Ensures no duplicate values
class ExitCode(IntEnum):
    """
    Unix-standard exit codes for CLI process termination.

    Provides semantically named exit codes that follow Unix
    conventions, used as return values from ``main()``.

    Attributes
    ----------
    SUCCESS : int
        Normal termination (0).
    FAILURE : int
        General error (1).
    KEYBOARD_INTERRUPT : int
        Terminated by Ctrl+C signal (130).
    """
    SUCCESS = 0
    FAILURE = 1
    KEYBOARD_INTERRUPT = 130
   # BADUSE = 1  Error!

class BrightDarkFilter(IntEnum):
    """
    Pixel brightness adjustment constants.

    Defines the default offset values passed to
    ``create_brightness_filter()`` for the standard
    brighten and darken filter variants.

    Attributes
    ----------
    BRIGHT : int
        Positive offset for brightness increase (50).
    DARK : int
        Negative offset for brightness decrease (-50).
    """
    BRIGHT = 50
    DARK = -50

# Image size variables configuration
class ImageSize(NamedTuple):
    """
    Image dimensions as a named, immutable pair.

    Provides named access to height and width instead of
    positional tuple indexing, improving readability across
    filter and I/O operations.

    Attributes
    ----------
    height : int
        Number of pixel rows in the image.
    width : int
        Number of pixels per row.

    Examples
    --------
    >>> size = ImageSize(height=480, width=640)
    >>> size.height
    480
    >>> h, w = size  # unpacking still works
    """
    height: int
    width: int

# NamedTuple for named access patterns. (BmpData.width)
# BMP read result
class BmpData(NamedTuple):
    """
    Complete result of reading a BMP file.

    Bundles the image dimensions, pixel data, and original
    file headers into a single immutable container returned
    by ``read_bmp()``. Headers are preserved for lossless
    write-back via ``write_bmp()``.

    Attributes
    ----------
    size : ImageSize
        Nested NamedTuple containing image height and width.
    pixels : ImageData
        2D grid of ``Pixel`` objects (list of rows, each row
        a list of ``Pixel``).
    full_header : HeaderBytes
        Concatenated BMP file header and DIB header bytes,
        used for reconstructing the output file.

    Examples
    --------
    >>> bmp = read_bmp(Path("image.bmp"))
    >>> bmp.size.width
    640
    >>> bmp.pixels[0][0].r
    255
    """
    size: ImageSize   # Nested NamedTuple class
    pixels: ImageData
    full_header: HeaderBytes

# Pixel configuration for BMP (b,g,r)
class Pixel(NamedTuple):
    """
    Single pixel in BGR color order.

    Represents one pixel as stored in the BMP file format,
    where blue comes first, followed by green, then red.
    Immutable by design — filters create new ``Pixel``
    instances rather than mutating existing ones.

    Attributes
    ----------
    b : int
        Blue channel value (0–255).
    g : int
        Green channel value (0–255).
    r : int
        Red channel value (0–255).

    Examples
    --------
    >>> px = Pixel(100, 150, 200)
    >>> px.r
    200
    >>> b, g, r = px  # positional unpacking
    """
    b: int
    g: int
    r: int
    

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
    RESET: Final[str] = "\033[0m"
    
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