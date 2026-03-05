"""
BMP image filter functions.

Implements four pixel-level image filters for 24-bit BMP images:
grayscale conversion, horizontal reflection, box blur, and Sobel
edge detection. Each filter accepts an ``ImageData`` grid and
returns a new grid without mutating the original.

Notes
-----
All filters operate on BGR-ordered ``Pixel`` NamedTuples and
produce new ``Pixel`` instances rather than mutating in place,
consistent with the immutability of NamedTuple objects.
"""

# =============================================================================
# IMPORTS
# =============================================================================

from __future__ import annotations
import logging
import math
import sys

try:
    from .bmp_config import (
        Pixel,
        PixelRow,
        ImageData,
        ImageSize,
        DictFuncs,
        FilterFunc,
    )
except ImportError as e:
    # sys.exit() raises SystemExit internally, don´t need 'raise...'
    sys.exit(f"Error: Cannot find relative modules.\nDetails: {e}")


# =============================================================================
# MODULE CONFIGURATION
# =============================================================================

# Exports
__all__ = [
    "grayscale",
    "reflect",
    "blur",
    "edges",
]


# Registry dictionary (global)
FILTERS: DictFuncs = {}

# Set up Logging
# '__name__' will automatically be name 'py_src.bmp_filters'
logger = logging.getLogger(__name__)


# =============================================================================
# INTERNAL HELPER FUNCTIONS
# =============================================================================

def _width_height_calculator(pixels: ImageData) -> ImageSize:
    """
    Extract image dimensions from the pixel grid.

    Derives height from the number of rows and width from
    the length of the first row, assuming a rectangular grid.

    Parameters
    ----------
    pixels : ImageData
        2D grid of ``Pixel`` objects (non-empty).

    Returns
    -------
    ImageSize
        NamedTuple with ``height`` and ``width`` fields.
    """
    # How many rows / main lists (where pixel lists are inside)
    height = len(pixels)
    
    # How many pixel lists are inside each row/main list
    width = len(pixels[0])

    return ImageSize(height, width)

# A decorator is just a function that takes a function and returns a function
def register_filter(func: FilterFunc, filters: DictFuncs = FILTERS ) -> FilterFunc:
    """
    """
    filters[func.__name__] = func
    return func  # Return unchanged function


# =============================================================================
# CORE FUNCTIONS
# =============================================================================

# Just add decorator - function auto-registers!
@register_filter
def grayscale(pixels: ImageData | None = None) -> ImageData:
    """
    Convert an image to grayscale using the luminosity method.

    Applies the ITU-R BT.601 luminosity formula to each pixel,
    weighting RGB channels by human eye sensitivity:
    ``gray = 0.299 * R + 0.587 * G + 0.114 * B``.

    Parameters
    ----------
    pixels : ImageData or None
        2D grid of ``Pixel`` objects to convert. Cannot be
        None or empty.

    Returns
    -------
    ImageData
        New pixel grid where each pixel has equal B, G, R
        values set to the computed grayscale intensity.

    Raises
    ------
    ValueError
        If ``pixels`` is None or an empty list.

    Examples
    --------
    >>> img = [[Pixel(50, 100, 200)]]
    >>> result = grayscale(img)
    >>> result[0][0]
    Pixel(b=126, g=126, r=126)
    """
    # Explicit check for ImageData (list of lists)
    # This distinguishes between "caller forgot to pass data",
    # and "data exists but is empty".
    if pixels is None:
        raise ValueError("Pixels argument is required")
    
    if len(pixels) == 0:
        raise ValueError("Pixels cannot be empty")
    
    new_pixels: ImageData = []
    
    for row in pixels:
        new_row: PixelRow = []
        for pixel in row:
            # Luminosity formula (human eye is most sensitive to gree)
            gray = int(0.299 * pixel.r + 0.587 * pixel.g + 0.114 * pixel.b)
            new_row.append(Pixel(gray, gray, gray))
        
        new_pixels.append(new_row)
    
    logger.debug("Filter applied......")
    return new_pixels


@register_filter
def reflect(pixels: ImageData | None = None) -> ImageData:
    """
    Mirror an image horizontally by reversing each pixel row.

    Produces a left-to-right reflection of the input image.
    Each row's pixel order is reversed while row order is
    preserved.

    Parameters
    ----------
    pixels : ImageData or None
        2D grid of ``Pixel`` objects to reflect. Cannot be
        None or empty.

    Returns
    -------
    ImageData
        New pixel grid with each row reversed.

    Raises
    ------
    ValueError
        If ``pixels`` is None or an empty list.

    Examples
    --------
    >>> img = [[Pixel(1, 2, 3), Pixel(4, 5, 6)]]
    >>> result = reflect(img)
    >>> result[0]
    [Pixel(b=4, g=5, r=6), Pixel(b=1, g=2, r=3)]
    """
    # Explicit check for ImageData (list of lists)
    if pixels is None:
        raise ValueError("Pixels argument is required")
    
    if len(pixels) == 0:
        raise ValueError("Pixels cannot be empty")
    
    new_pixels: ImageData = []
    
    for row in pixels:
        # Reverse each row
        new_pixels.append(row[::-1])
    
    logger.debug("Filter applied......")
    return new_pixels


@register_filter
def blur(pixels: ImageData | None = None) -> ImageData:
    """
    Apply a 3x3 box blur to an image.

    For each pixel, computes the average of all neighboring
    pixels within a 3x3 grid (including the pixel itself).
    Edge and corner pixels use only the available neighbors,
    resulting in a naturally weighted boundary treatment.

    Parameters
    ----------
    pixels : ImageData or None
        2D grid of ``Pixel`` objects to blur. Cannot be
        None or empty.

    Returns
    -------
    ImageData
        New pixel grid with each pixel replaced by the
        rounded average of its 3x3 neighborhood.

    Raises
    ------
    ValueError
        If ``pixels`` is None or an empty list.

    Notes
    -----
    Reads from the original ``pixels`` grid and writes to a
    separate ``new_pixels`` grid to avoid read-after-write
    artifacts during the convolution pass.
    """
    # Explicit check for ImageData (list of lists)
    if pixels is None:
        raise ValueError("Pixels argument is required")
    
    if len(pixels) == 0:
        raise ValueError("Pixels cannot be empty")
    
    size: ImageSize = _width_height_calculator(pixels)

    # Create a copy to avoid modifying while reading
    new_pixels: ImageData = [
        [Pixel(0, 0, 0) for _ in range(size.width)]
        for _ in range(size.height)
    ]
    
    for y in range(size.height):
        for x in range(size.width):
            total_b, total_g, total_r = 0, 0, 0
            count = 0
            
            # Check all 9 positions in 3x3 Grid
            for dy in [-1, 0, 1]:
                for dx in [-1, 0, 1]:
                    ny, nx = y + dy, x + dx
                    
                    # Check bounds
                    if 0 <= ny < size.height and 0 <= nx < size.width:
                        pixel: Pixel = pixels[ny][nx]
                        total_b += pixel.b
                        total_g += pixel.g
                        total_r += pixel.r
                        count += 1
            
            # Average
            new_pixels[y][x] = Pixel(
                round(total_b / count),
                round(total_g / count),
                round(total_r / count),
            )
    
    logger.debug("Filter applied......")
    return new_pixels


@register_filter
def edges(pixels: ImageData | None = None) -> ImageData:
    """
    Detect edges in an image using the Sobel operator.

    Applies two 3x3 Sobel kernels (Gx for horizontal edges,
    Gy for vertical edges) to each color channel independently.
    The final magnitude is computed as ``sqrt(Gx² + Gy²)``
    using ``math.hypot()``, then capped at 255.

    Parameters
    ----------
    pixels : ImageData or None
        2D grid of ``Pixel`` objects to process. Cannot be
        None or empty.

    Returns
    -------
    ImageData
        New pixel grid where bright values indicate strong
        edges and dark values indicate uniform regions.

    Raises
    ------
    ValueError
        If ``pixels`` is None or an empty list.

    Notes
    -----
    Out-of-bounds neighbors are treated as black (value 0),
    consistent with the CS50 specification. The Sobel kernels
    used are:

    Gx::

        [-1  0  1]
        [-2  0  2]
        [-1  0  1]

    Gy::

        [-1 -2 -1]
        [ 0  0  0]
        [ 1  2  1]

    References
    ----------
    .. [1] Sobel, I. and Feldman, G., "A 3x3 Isotropic Gradient
       Operator for Image Processing," 1968.
    """
    # Explicit check for ImageData (list of lists)
    if pixels is None:
        raise ValueError("Pixels argument is required")
    
    if len(pixels) == 0:
        raise ValueError("Pixels cannot be empty")
    
    size: ImageSize = _width_height_calculator(pixels)
    
    # Initialize the new image grid
    new_pixels: ImageData = [
        [Pixel(0, 0, 0) for _ in range(size.width)]
        for _ in range(size.height)
    ]
    
    # Define the Sobel kernels
    gx_kernel = [
        [-1, 0, 1],
        [-2, 0, 2],
        [-1, 0, 1],
    ]
    
    gy_kernel = [
        [-1, -2, -1],
        [0, 0, 0],
        [1, 2, 1],
    ]
    
    for y in range(size.height):
        for x in range(size.width):
            gx_b, gx_g, gx_r = 0, 0, 0
            gy_b, gy_g, gy_r = 0, 0, 0
            
            # Check all 9 positions in 3x3 Grid
            for dy in [-1, 0, 1]:
                for dx in [-1, 0, 1]:
                    ny, nx = y + dy, x + dx
                    
                    # If out of bounds, values remain 0 (so we only add if IN bounds)
                    if 0 <= ny < size.height and 0 <= nx < size.width:
                        pixel: Pixel = pixels[ny][nx]
                        
                        # Map 'dy' and 'dx' from [-1, 1] to kernel indices [0, 2]
                        weight_x = gx_kernel[dy + 1][dx + 1]
                        weight_y = gy_kernel[dy + 1][dx + 1]
                        
                        # Apply Gx weights
                        gx_b += pixel.b * weight_x
                        gx_g += pixel.g * weight_x
                        gx_r += pixel.r * weight_x
                        
                        # Apply Gy weights
                        gy_b += pixel.b * weight_y
                        gy_g += pixel.g * weight_y
                        gy_r += pixel.r * weight_y
                        
            # Calculate final magnitude: 
            # math.hypot = sqrt(Gx^2 + Gy^2)
            mag_b = round(math.hypot(gx_b, gy_b))
            mag_g = round(math.hypot(gx_g, gy_g))
            mag_r = round(math.hypot(gx_r, gy_r))
            
            # Cap values at 255 to ensure valid color values
            new_pixels[y][x] = Pixel(
                min(255, mag_b),
                min(255, mag_g),
                min(255, mag_r),
            )
    
    logger.debug("Filter applied......")
    return new_pixels