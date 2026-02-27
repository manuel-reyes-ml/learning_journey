"""
"""

# =============================================================================
# IMPORTS
# =============================================================================

from __future__ import annotations
import logging
import math
import sys

try:
    from .bmp_config import PixelRow, ImageData
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

# Set up Logging
# '__name__' will automatically be name 'py_src.bmp_filters'
logger = logging.getLogger(__name__)


# =============================================================================
# INTERNAL HELPER FUNCTIONS
# =============================================================================

def _width_height_calculator(pixels: ImageData) -> tuple[int, int]:
    """
    """
    # How many rows / main lists (where pixel lists are inside)
    height = len(pixels)
    
    # How many pixel lists are inside each row/main list
    width = len(pixels[0])

    return height, width


# =============================================================================
# CORE FUNCTIONS
# =============================================================================

def grayscale(pixels: ImageData | None = None) -> ImageData:
    """
    """
    if not pixels: 
        raise ValueError("Pixels list cannot be empty")
    
    new_pixels: ImageData = []
    
    for row in pixels:
        new_row: PixelRow = []
        for pixel in row:
            b, g, r = pixel
            # Luminosity formula (human eye is most sensitive to gree)
            gray = int(0.299 * r + 0.587 * g + 0.114 * b)
            new_row.append([gray, gray, gray])
        
        new_pixels.append(new_row)
    
    logger.debug("Filter applied......")
    return new_pixels


def reflect(pixels: ImageData | None = None) -> ImageData:
    """
    """
    if not pixels: 
        raise ValueError("Pixels list cannot be empty")
    
    new_pixels: ImageData = []
    
    for row in pixels:
        # Reverse each row
        new_pixels.append(row[::-1])
    
    logger.debug("Filter applied......")
    return new_pixels


def blur(pixels: ImageData | None = None) -> ImageData:
    """
    """
    if not pixels: 
        raise ValueError("Pixels list cannot be empty")
    
    height, width = _width_height_calculator(pixels)

    # Create a copy to avoid modifying while reading
    new_pixels: ImageData = [[[0, 0, 0] for _ in range(width)] for _ in range(height)]
    
    for y in range(height):
        for x in range(width):
            total_b, total_g, total_r = 0, 0, 0
            count = 0
            
            # Check all 9 positions in 3x3 Grid
            for dy in [-1, 0, 1]:
                for dx in [-1, 0, 1]:
                    ny, nx = y + dy, x + dx
                    
                    # Check bounds
                    if 0 <= ny < height and 0 <= nx < width:
                        b, g, r = pixels[ny][nx]
                        total_b += b
                        total_g += g
                        total_r += r
                        count += 1
            
            # Average
            new_pixels[y][x] = [
                round(total_b / count),
                round(total_g / count),
                round(total_r / count),
            ]
    
    logger.debug("Filter applied......")
    return new_pixels


def edges(pixels: ImageData | None = None) -> ImageData:
    """
    """
    if not pixels: 
        raise ValueError("Pixels list cannot be empty")
    
    height, width = _width_height_calculator(pixels)
    
    # Initialize the new image grid
    new_pixels: ImageData = [[[0, 0, 0] for _ in range(width)] for _ in range(height)]
    
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
    
    for y in range(height):
        for x in range(width):
            gx_b, gx_g, gx_r = 0, 0, 0
            gy_b, gy_g, gy_r = 0, 0, 0
            
            # Check all 9 positions in 3x3 Grid
            for dy in [-1, 0, 1]:
                for dx in [-1, 0, 1]:
                    ny, nx = y + dy, x + dx
                    
                    # If out of bounds, values remain 0 (so we only add if IN bounds)
                    if 0 <= ny < height and 0 <= nx < width:
                        b, g, r = pixels[ny][nx]
                        
                        # Map 'dy' and 'dx' from [-1, 1] to kernel indices [0, 2]
                        weight_x = gx_kernel[dy + 1][dx + 1]
                        weight_y = gy_kernel[dy + 1][dx + 1]
                        
                        # Apply Gx weights
                        gx_b += b * weight_x
                        gx_g += g * weight_x
                        gx_r += r * weight_x
                        
                        # Apply Gy weights
                        gy_b += b * weight_y
                        gy_g += g * weight_y
                        gy_r += r * weight_y
                        
            # Calculate final magnitude: sqrt(Gx^2 + Gy^2)
            mag_b = round(math.sqrt(gx_b**2 + gy_b**2))
            mag_g = round(math.sqrt(gx_g**2 + gy_g**2))
            mag_r = round(math.sqrt(gx_r**2 + gy_r**2))
            
            # Cap values at 255 to ensure valid color values
            new_pixels[y][x] = [
                min(255, mag_b),
                min(255, mag_g),
                min(255, mag_r),
            ]
    
    logger.debug("Filter applied......")
    return new_pixels