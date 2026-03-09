"""
BMP file I/O operations.

Handles binary reading and writing of 24-bit BMP image files,
including header parsing, pixel data extraction, and row padding
calculations. Supports the standard BMP format with BGR pixel
order and 4-byte row alignment.

Notes
-----
BMP files store pixel rows padded to 4-byte boundaries. This
module calculates and applies the correct padding during both
read and write operations. Headers are preserved verbatim from
the input file to ensure lossless round-trip I/O.
"""

# =============================================================================
# IMPORTS
# =============================================================================

from __future__ import annotations
from pathlib import Path
import logging
import struct
import sys

try:
    # PEP 8 recommends absolute imports for clarity
    from py_src.bmp_config import (
        bmp_constants, 
        ImageData,
        ImageSize,
        HeaderBytes,
        BmpData,
        Pixel,
    )
except ImportError as e:
    sys.exit(f"Error: Cannot find relative modules.\nDetails: {e}")


# =============================================================================
# MODULE CONFIGURATION
# =============================================================================

# Exports
__all__ = [
    "read_bmp",
    "write_bmp",
]   
    
# Set up logging
# '__name__' will automatically be name 'py_src.bmp_io'
logger = logging.getLogger(__name__)


# =============================================================================
# INTERNAL HELPER FUNCTIONS
# =============================================================================

def _padding_calculator(width: int) -> int:
    """
    Calculate the number of padding bytes needed per BMP row.

    BMP rows must be aligned to 4-byte boundaries. For 24-bit
    images, each pixel occupies 3 bytes, so padding is added
    at the end of each row to reach the next multiple of 4.

    Parameters
    ----------
    width : int
        Number of pixels per row.

    Returns
    -------
    int
        Number of null bytes (0–3) to append after each row.

    Examples
    --------
    >>> _padding_calculator(1)   # 1 * 3 = 3 bytes → 1 pad
    1
    >>> _padding_calculator(4)   # 4 * 3 = 12 bytes → 0 pad
    0
    >>> _padding_calculator(5)   # 5 * 3 = 15 bytes → 1 pad
    1
    """
    return (4 - (width * 3) % 4) % 4


# =============================================================================
# CORE FUNCTIONS
# =============================================================================

def read_bmp(
    in_file: Path | None = None,
    bmp_signature: bytes = bmp_constants.SIGNATURE,
    bmp_header_size: int = bmp_constants.HEADER_SIZE,
    pixel_size: int = bmp_constants.PIXEL_SIZE,
    bpp_bmp: int = bmp_constants.BPP,
) -> BmpData:
    """
    Read a 24-bit BMP file and extract its pixel data.

    Parses the BMP file header and DIB header to extract image
    dimensions, validates the format, then reads the pixel grid
    row by row (accounting for padding). Returns all data needed
    to reconstruct the file via ``write_bmp()``.

    Parameters
    ----------
    in_file : Path or None
        Path to the input BMP file. Cannot be None.
    bmp_signature : bytes, optional
        Expected magic bytes at file start (default ``b"BM"``).
    bmp_header_size : int, optional
        Size of the BMP file header in bytes (default 14).
    pixel_size : int, optional
        Bytes per pixel (default 3 for BGR).
    bpp_bmp : int, optional
        Expected bits per pixel (default 24).

    Returns
    -------
    BmpData
        NamedTuple containing:
        - ``size``: ``ImageSize`` with height and width.
        - ``pixels``: 2D grid of ``Pixel`` NamedTuples in BGR order.
        - ``full_header``: Concatenated BMP + DIB header bytes.

    Raises
    ------
    ValueError
        If ``in_file`` is None, the file lacks a valid BMP
        signature, or the bit depth is not 24-bit.

    Notes
    -----
    Uses ``struct.unpack`` with little-endian format codes:
    ``'<I'`` for unsigned 32-bit, ``'<i'`` for signed 32-bit,
    ``'<H'`` for unsigned 16-bit, and ``'<BBB'`` for three
    unsigned bytes (one pixel).
    """
    if not in_file:
        raise ValueError("Input file cannot be empty.")
    
    with open(in_file, "rb") as f:
        # =====================================================
        # STEP 1: Read and validate BMP Header (14 bytes)
        # =====================================================
        bmp_header = f.read(bmp_header_size)
        
        # Check for "BM" signature
        # Slicing bytes [0:2] returns a bytes objects
        # Indexing bytes [1] returns an int
        if bmp_header[0:2] != bmp_signature:
            raise ValueError(f"Not a valid BMP file. Must start with {bmp_signature!r}.")
        
        logger.debug("File has been located and accessed. Retrieving pixels....")
        
        # Extract pixel data offset (bytes 10-13)
        # '<I' = little-endian unsigned 32-bit integer
        pixel_offset = struct.unpack('<I', bmp_header[10:14])[0]
        
        # =====================================================
        # STEP 2: Read DIB Header
        # =====================================================
        dib_header_size = pixel_offset - bmp_header_size
        dib_header = f.read(dib_header_size)
        
        # Extract dimensions (don't include padding)
        # '<i' = little-endian SIGNED 32-bit (height can be negative)
        width = struct.unpack('<i', dib_header[4:8])[0]
        height = struct.unpack('<i', dib_header[8:12])[0]
        size = ImageSize(height, width)
        
        # Extract bits per pixel (bytes 14-15 in DIB)
        # '<H' = little-endian unsigned 16-bit: Requires 2 bytes
        bpp = struct.unpack('<H', dib_header[14:16])[0]
        
        if bpp != bpp_bmp:
            raise ValueError(f"Only {bpp_bmp}-bit BMPs supported. Got {bpp}-bit.")
        
        logger.info(f"Processing file {in_file.name!r}....")
        
        # =====================================================
        # STEP 3: Calculate row padding
        # =====================================================
        # BMP rows must be multiplies of 4 bytes
        padding = _padding_calculator(size.width)
        
        # =====================================================
        # STEP 4: Read pixel data
        # =====================================================
        pixels = []
        
        # abs() returns the absolute value, is the difference
        # from 0 to the number (always positive).
        for _ in range(abs(size.height)):
            row = []
            for _ in range(size.width):
                # Read 3 bytes as BGR
                # '<BBB' = three unsigned bytes
                # -unpack returns a plain tuple: tuple[Any, ...] type
                b, g, r = struct.unpack('<BBB', f.read(pixel_size))
                row.append(Pixel(b, g, r))
                
            # Skip padding bytes at the end of the row
            f.read(padding)
            pixels.append(row)
            
    # Return headers for easy writing later
    full_header = bmp_header + dib_header
    
    logger.debug("Pixels are retrieved from input file......")
    
    return BmpData(size, pixels, full_header)


def write_bmp(
    out_file: Path | None = None,
    width: int | None = None,
    pixels: ImageData | None = None,
    header: HeaderBytes | None = None,
    pad_hex: bytes = bmp_constants.PAD_HEX,
) -> None:
    """
    Write pixel data and headers to a BMP file.

    Reconstructs a valid 24-bit BMP file by writing the original
    headers followed by pixel data with correct row padding.

    Parameters
    ----------
    out_file : Path or None
        Destination path for the output BMP file. Cannot be None.
    width : int or None
        Image width in pixels, used to calculate row padding.
        Cannot be None.
    pixels : ImageData or None
        2D grid of ``Pixel`` objects to write. Cannot be None
        or empty.
    header : HeaderBytes or None
        Original BMP + DIB header bytes from ``read_bmp()``.
        Cannot be None.
    pad_hex : bytes, optional
        Byte value used for row padding (default ``b"\\x00"``).

    Raises
    ------
    ValueError
        If any required parameter is None or empty.

    Notes
    -----
    Writes pixels in BGR order using ``struct.pack('<BBB', ...)``,
    matching the BMP file format specification. Row padding is
    appended as null bytes to maintain 4-byte alignment.
    """
    if not out_file:
        raise ValueError("Output file cannot be empty")
    
    if not width:
        raise ValueError("Width cannot be empty")
    
    # Explicit check for ImageData (list of lists)
    if pixels is None:
        raise ValueError("Pixels argument is required")
    
    if len(pixels) == 0:
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
                f.write(struct.pack('<BBB', pixel.b, pixel.g, pixel.r))
                
            # Write padding
            f.write(pad_hex * padding)
    
    logger.info(f"File {out_file.name!r} is generated....")