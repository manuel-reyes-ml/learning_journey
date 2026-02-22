"""
"""

from __future__ import annotations
from pathlib import Path
from typing import Final
import logging
import struct
import sys


# =============================================================================
# Module Configuration
# =============================================================================

# Exports
__all__ = [
    "read_bmp",
    "write_bmp",
]

# Program Constants
BMP_HEADER_SIZE: Final[int] = 14
BMP_SIGNATURE: Final[bytes] = b"BM"
PAD_HEX: Final[bytes] = b"\x00"
PIXEL_SIZE: Final[int] = 3
BPP: Final[int] = 24  # bits per pixel (3 bytes RGB)

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
    
    
# Set up logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
    
# Create handler with colored formatter
handler = logging.StreamHandler()
handler.setFormatter(ColoredFormatter(
    fmt='%(asctime)s : %(levelname)s : %(message)s',
    datefmt='%H:%M:%S',
))
logger.addHandler(handler)


# =============================================================================
# Core Functions
# =============================================================================

def _padding_calculator(width: int) -> int:
    """
    """
    return (4 - (width * 3) % 4) % 4


def read_bmp(
    in_file: Path | None = None,
    bmp_signature: bytes = BMP_SIGNATURE,
    bmp_header_size: int = BMP_HEADER_SIZE,
    pixel_size: int = PIXEL_SIZE,
    bpp_bmp: int = BPP,
) -> tuple[int, int, list, bytes]:
    """
    """
    if not in_file:
        raise ValueError("Input file cannot be empty.")
    
    with open(in_file, "rb") as f:
        # =====================================================
        # STEP 1: Read and validate BMP Header (14 bytes)
        # =====================================================
        bmp_header = f.read(bmp_header_size)
        
        # Check for "BM" signature
        if bmp_header[0:2] != bmp_signature:
            raise ValueError(f"Not a valid BMP file. Must start with '{bmp_signature}'.")
        
        # Extract pixel data offset (bytes 10-13)
        # '<I' = little-endian unsigned 32-bit integer
        pixel_offset = struct.unpack('<I', bmp_header[10:14])[0]
        
        # =====================================================
        # STEP 2: Read DIB Header
        # =====================================================
        dib_header_size = pixel_offset - bmp_header_size
        dib_header = f.read(dib_header_size)
        
        # Extract dimensions
        # '<i' = little-endian SIGNED 32-bit (height can be negative)
        width = struct.unpack('<i', dib_header[4:8])[0]
        height = struct.unpack('<i', dib_header[8:12])[0]
        
        # Extract bits per pixel (bytes 14-15 in DIB)
        # '<H' = little-endian unsigned 16-bit
        bpp = struct.unpack('<H', dib_header[14:15])[0]
        
        if bpp != bpp_bmp:
            raise ValueError(f"Only {bpp_bmp}-bit BMPs supported. Got {bpp}-bit.")
        
        # =====================================================
        # STEP 3: Calculate row padding
        # =====================================================
        # BMP rows must be multiplies of 4 bytes
        padding = _padding_calculator(width)
        
        # =====================================================
        # STEP 4: Read pixel data
        # =====================================================
        pixels = []
        
        for _ in range(abs(height)):
            row = []
            for _ in range(width):
                # Read 3 bytes as BGR
                # '<BBB' = three unsigned bytes
                b, g, r = struct.unpack('<BBB', f.read(pixel_size))
                row.append([b, g, r])
                
            # Skip padding bytes at the end of the row
            f.read(padding)
            pixels.append(row)
            
    # Return headers for easy writing later
    full_header = bmp_header + dib_header
    
    return width, height, pixels, full_header


def write_bmp(
    out_file: Path | None = None,
    width: int | None = None,
    pixels: list | None = None,
    header: bytes | None = None,
    pad_hex: bytes = PAD_HEX,
) -> None:
    """
    """
    if not out_file:
        raise ValueError("Output file cannot be empty")
    
    if not width:
        raise ValueError("Width cannot be empty")
    
    if not pixels:
        raise ValueError("Pixels cannot be empty")
    
    if not header:
        raise ValueError("Header cannot be empty")
    
    padding = _padding_calculator(width)
    
    with open(out_file, "wb") as f:
        # Write original header
        f.write(header)
        
        # Write pixel data
        for row in pixels:
            for pixel in row:
                b, g, r = pixel
                f.write(struct.pack('<BBB', b, g, r))
                
            # Write padding
            f.write(pad_hex * padding)
        