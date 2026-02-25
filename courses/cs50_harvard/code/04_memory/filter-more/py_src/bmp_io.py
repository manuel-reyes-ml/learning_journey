"""
"""

from __future__ import annotations
from pathlib import Path
import logging
import struct
import sys

try:
    from .bmp_config import (
    ColoredFormatter,
    BMP,
    )
except ImportError as e:
    sys.exit(f"Error: Cannot find relative modules.\nDetails: {e}")


# =============================================================================
# Module Configuration
# =============================================================================

# Exports
__all__ = [
    "read_bmp",
    "write_bmp",
]   
    
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
# Internal Helper Functions
# =============================================================================

def _padding_calculator(width: int) -> int:
    """
    """
    return (4 - (width * 3) % 4) % 4


# =============================================================================
# Core Functions
# =============================================================================

def read_bmp(
    in_file: Path | None = None,
    bmp_signature: bytes = BMP.SIGNATURE,
    bmp_header_size: int = BMP.HEADER_SIZE,
    pixel_size: int = BMP.PIXEL_SIZE,
    bpp_bmp: int = BMP.BPP,
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
        
        logger.debug("File has been located and accessed. Retrieving pixels....")
        
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
        # '<H' = little-endian unsigned 16-bit: Requires 2 bytes
        bpp = struct.unpack('<H', dib_header[14:16])[0]
        
        if bpp != bpp_bmp:
            raise ValueError(f"Only {bpp_bmp}-bit BMPs supported. Got {bpp}-bit.")
        
        logger.info(f"Processing file '{in_file.name}'....")
        
        # =====================================================
        # STEP 3: Calculate row padding
        # =====================================================
        # BMP rows must be multiplies of 4 bytes
        padding = _padding_calculator(width)
        
        # =====================================================
        # STEP 4: Read pixel data
        # =====================================================
        pixels = []
        
        # abs() returns the absolute value
        # is the distance from 0 to the number (always positive)
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
    
    logger.debug("Pixels are retrieved from input file......")
    
    return width, height, pixels, full_header


def write_bmp(
    out_file: Path | None = None,
    width: int | None = None,
    pixels: list | None = None,
    header: bytes | None = None,
    pad_hex: bytes = BMP.PAD_HEX,
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
    
    logger.info(f"File '{out_file.name}' is generated....")