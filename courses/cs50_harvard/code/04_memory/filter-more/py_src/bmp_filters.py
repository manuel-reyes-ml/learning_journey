"""
BMP image filter functions.

Implements six pixel-level image filters for 24-bit BMP images:
grayscale conversion, horizontal reflection, box blur, Sobel
edge detection, brightness increase, and brightness decrease.
Each filter accepts an ``ImageData`` grid and returns a new
grid without mutating the original.

Notes
-----
All filters operate on BGR-ordered ``Pixel`` NamedTuples and
produce new ``Pixel`` instances rather than mutating in place,
consistent with the immutability of NamedTuple objects.

The four core filters use ``@register_filter`` decorator syntax.
Factory-created filters (brighten, darken) use the equivalent
manual call form since no ``def`` statement exists to decorate.
"""

# =============================================================================
# IMPORTS
# =============================================================================

from __future__ import annotations
from functools import wraps
from typing import Any
import enum
import logging
import math
import time
import sys

try:
    # PEP 8 recommends absolute imports for clarity
    from py_src.bmp_config import (
        Pixel,
        PixelRow,
        ImageData,
        ImageSize,
        DictFuncs,
        FilterInfo,
        RegisterOut,
        FilterFunc,
        BrightDarkFilter,
    )
except ImportError as e:
    # sys.exit() raises SystemExit internally, don´t need 'raise...'
    sys.exit(f"Error: Cannot find relative modules.\nDetails: {e}")


# =============================================================================
# MODULE CONFIGURATION
# =============================================================================

# =====================================================
# Exports
# =====================================================

__all__ = [
    "grayscale",
    "reflect",
    "blur",
    "edges",
    "darken",
    "brighten",
    "create_brightness_filter",
]


# =====================================================
# Module Level Constants
# ===================================================== 

# Registry dictionary (global)
FILTERS: DictFuncs = {}


# =====================================================
# Logging Set Up
# =====================================================

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


# A decorator factory is just a function that takes custom parameters 
# and generates a decorator.
def register_filter(name: str, description: str = "") -> RegisterOut:
    """
    Decorator factory that registers a filter in the dispatch table.

    Returns a decorator that wraps a filter function by storing
    it as a ``FilterInfo`` entry in the ``FILTERS`` dictionary.
    The function itself is returned unchanged — registration is
    a side effect, not a transformation.

    Parameters
    ----------
    name : str
        Key under which the filter is stored in ``FILTERS``.
    description : str, optional
        Short human-readable label for CLI help output. If
        empty, falls back to the function's ``__doc__`` attribute.

    Returns
    -------
    RegisterOut
        A decorator that accepts a ``FilterFunc`` and returns
        it unchanged after registration.

    Examples
    --------
    Decorator syntax (for ``def`` statements)::

        @register_filter("blur", "Apply blur filter")
        def blur(pixels): ...

    Manual call (for factory-created functions)::

        brighten = register_filter("brighten", "Increase brightness")(
            create_brightness_filter(50, "brighten")
        )
    """
    def decorator(func: FilterFunc, filters: DictFuncs = FILTERS) -> FilterFunc:
        filters[name] = FilterInfo(
            func,
            name,
            # __doc__ gives the docstring of a function
            description=description or func.__doc__ or ""
        )
        return func  # Return unchanged function
        # func goes in, func comes out. The function's __name__, __doc__, __qualname__
        # are all intact because you never created a replacement. Nothing to fix,
        # so @wraps would do nothing useful.
    return decorator


def timer(func: FilterFunc) -> FilterFunc:
    """Measure and print execution time."""
    @wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        logger.debug(f"{func.__name__} took {elapsed:.6f}s")
        return result
    # Without @wraps(func) on wrapper, the decorated function's __name__ becomes
    # "wrapper", __doc__ becomes None, and tracebacks are useless. @wraps copies
    # the original's identity onto the replacement.
    return wrapper

# The simple rule: If your decorator has def wrapper (or any inner function) that
# gets returned instead of the original, you need @wraps. If it returns the original
# function unchanged, you don't.


# =============================================================================
# CORE FUNCTIONS
# =============================================================================

# Just add decorator factory to grab function metadata and
# generates function to auto-registers!
# Decorator apply **bottom-up** (closest to 'def' goes first)
@register_filter("grayscale", "Convert to grayscale using luminosity")
@timer
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


@register_filter("reflect", "Invert pixels horizontally")
@timer
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


@register_filter("blur", "Apply blur filter to image")
@timer
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


@register_filter("edges", "Identify object edges in image")
@timer
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

# =============================================================================
# DECORATOR EXECUTION ORDER
# =============================================================================
#
# THE @ SYNTAX RULE:
# Python always makes exactly ONE call on whatever expression follows @.
# With @timer, that one call is timer(func).
# With @register_filter(...), the parentheses already made one call,
# so @ makes the SECOND call on the result.
#
# ─────────────────────────────────────────────────────────────────────
# PATTERN 1: DECORATOR FACTORY (register_filter)
# ─────────────────────────────────────────────────────────────────────
#
#   @register_filter("grayscale", "Convert to grayscale")
#   def grayscale(pixels): ...
#
#   Python expands this to:
#     decorator = register_filter("grayscale", "Convert to grayscale")
#     grayscale = decorator(grayscale)
#
#   Call 1 (definition time):
#     register_filter("grayscale", "Convert to grayscale")
#     → outer function body runs
#     → creates 'decorator' function
#     → returns decorator (just a function, not called yet)
#
#   Call 2 (definition time — @ forces this immediately):
#     decorator(grayscale)
#     → inner function body runs NOW
#     → filters["grayscale"] = FilterInfo(...)  ← work done at definition
#     → returns original grayscale unchanged
#
#   Result:
#     grayscale = original function (no middleman)
#     FILTERS dict is populated
#     At call time: grayscale(pixels) runs the original directly
#
# ─────────────────────────────────────────────────────────────────────
# PATTERN 2: WRAPPING DECORATOR (timer)
# ─────────────────────────────────────────────────────────────────────
#
#   @timer
#   def grayscale(pixels): ...
#
#   Python expands this to:
#     grayscale = timer(grayscale)
#
#   Call 1 (definition time):
#     timer(grayscale)
#     → creates 'wrapper' function (code inside is NOT executed)
#     → returns wrapper as a REPLACEMENT for grayscale
#
#   Result:
#     grayscale = wrapper (middleman installed)
#     At call time: grayscale(pixels) actually calls wrapper(pixels)
#       → wrapper measures start time
#       → wrapper calls original grayscale inside
#       → wrapper measures elapsed time
#       → wrapper logs the result
#
# ─────────────────────────────────────────────────────────────────────
# BOTH STACKED (correct order):
# ─────────────────────────────────────────────────────────────────────
#
#   @register_filter("grayscale", "Convert to grayscale")
#   @timer
#   def grayscale(pixels): ...
#
#   Python expands bottom-up:
#     step1 = timer(grayscale)                          # wrapper created
#     step2 = register_filter("grayscale", "...")(step1) # wrapper registered
#     grayscale = step2                                  # wrapper is stored
#
#   Call 1 (definition time — @timer):
#     timer(original_grayscale)
#     → creates wrapper around original
#     → returns wrapper
#
#   Call 2 (definition time — @register_filter):
#     register_filter("grayscale", "...")(wrapper)
#     → stores WRAPPER in FILTERS["grayscale"].func  ← has timing!
#     → returns wrapper unchanged
#
#   Result:
#     grayscale = wrapper (has timer)
#     FILTERS["grayscale"].func = wrapper (has timer)
#     At call time: both the variable AND the dispatch dict
#       go through the timer
#
# ─────────────────────────────────────────────────────────────────────
# WRONG ORDER (timer on top):
# ─────────────────────────────────────────────────────────────────────
#
#   @timer
#   @register_filter("grayscale", "Convert to grayscale")
#   def grayscale(pixels): ...
#
#   Call 1 (definition time — @register_filter):
#     → stores ORIGINAL in FILTERS["grayscale"].func  ← no timer!
#     → returns original
#
#   Call 2 (definition time — @timer):
#     → wraps original with timing
#     → returns wrapper
#
#   Result:
#     grayscale variable = wrapper (has timer)
#     FILTERS["grayscale"].func = original (NO timer!)
#     process_filter dispatches through FILTERS → timer never runs
#
# =============================================================================


# =============================================================================
# FUNCTION FACTORIES
# =============================================================================

# Functions that creates and return other functions
def create_brightness_filter(adjustment: int, name: str) -> FilterFunc:
    """
    Factory that creates a brightness adjustment filter function.

    Returns a closure that adds ``adjustment`` to every pixel
    channel, clamping results to the 0–255 range. The returned
    function's ``__name__``, ``__qualname__``, and ``__doc__``
    are set dynamically so each variant is identifiable in
    tracebacks, logs, and ``help()`` output.

    Parameters
    ----------
    adjustment : int
        Value to add to each BGR channel (-255 to 255).
        Positive values brighten, negative values darken.
    name : str
        Identity for the returned function, used to set
        ``__name__`` and ``__qualname__``.

    Returns
    -------
    FilterFunc
        A filter function with the standard
        ``(ImageData) -> ImageData`` signature.

    Examples
    --------
    >>> brighten = create_brightness_filter(50, "brighten")
    >>> brighten.__name__
    'brighten'
    >>> darken = create_brightness_filter(-50, "darken")
    >>> darken.__doc__[:30]
    'Adjust pixel brightness by -50'
    """
    def adjust_brightness(pixels: ImageData | None = None) -> ImageData:
        if pixels is None:
            raise ValueError("Pixels argument is required")
        
        if len(pixels) == 0:
            raise ValueError("Pixels cannot be empty")
        
        new_pixels: ImageData = []
        
        # adjustment is a free variable (captured by inner function)
        for row in pixels:
            new_row: PixelRow = []
            for pixel in row:
                new_pixel = Pixel(
                    max(0, min(255, pixel.b + adjustment)),
                    max(0, min(255, pixel.g + adjustment)),
                    max(0, min(255, pixel.r + adjustment)),
                )
                new_row.append(new_pixel)
                
            new_pixels.append(new_row)
                
        logger.debug("Filter applied......")
        return new_pixels        
    
    # Python sets __name__ to "adjust_brightness" normally
    # Override function's name to 'brighten' or 'darken' to identify
    # each variant.
    adjust_brightness.__name__ = name
    
    # __qualname__(qualified name) gives the full dotted path showing where
    # a function lives in the nesting hierarchy.
    # <locals> means the function was defined inside another function.
    # __qualname__ showing create_brightness_filter.<locals>.brighten
    # or .darken tells exactly which one failed.
    adjust_brightness.__qualname__ = f"create_brightness_filter.<locals>.{name}"
    
    # __doc__ gives the docstring of a function
    # When creating functions dinamycally a static dosctring would
    # say the same thing for every variant.
    # That´s why is better to set docstring dynamically also
    adjust_brightness.__doc__ = (
        f"Adjust pixel brightness by {adjustment} units.\n\n"
        f"Parameters\n"
        f"----------\n"
        f"pixels : ImageData or None\n"
        f"    2D grid of Pixel objects. Cannot be None or empty.\n\n"
        f"Returns\n"
        f"-------\n"
        f"ImageData\n"
        f"    New pixel grid with each channel clamped to 0-255.\n"
    )
               
    return adjust_brightness


# =====================================================
# Create Specific Filters
# =====================================================

# Having the creation and registration here so one module owns filter registration
brighten: FilterFunc = register_filter("brighten", "Increase pixel brightness")(
    timer(create_brightness_filter(BrightDarkFilter.BRIGHT, "brighten"))
)
darken: FilterFunc = register_filter("darken", "Decrease pixel brightness")(
    timer(create_brightness_filter(BrightDarkFilter.DARK, "darken"))
)

# READ THIS INSIDE-OUT (innermost call executes first):

# Step 1 (factory — innermost):
#    create_brightness_filter(BrightDarkFilter.BRIGHT, "brighten")
#    → creates adjust_brightness closure
#    → sets __name__, __qualname__, __doc__ dynamically
#    → returns the raw filter function

# Step 2 (timer — wraps the factory output):
#    timer(raw_filter_function)
#    → creates wrapper with timing logic around the filter
#    → @wraps preserves __name__, __doc__, etc. from the original
#    → returns wrapper (middleman installed)

# Step 3 (register_filter — outermost call):
#    register_filter("brighten", "Increase pixel brightness")
#    → returns the 'decorator' function

# Step 4 (chained call — decorator receives the timed wrapper):
#    decorator(timed_wrapper)
#    → stores TIMED wrapper in FILTERS["brighten"] as a FilterInfo
#    → returns timed wrapper unchanged

# Step 5 (assignment):
#    brighten: FilterFunc = <timed wrapper>

# This mirrors the stacked @ syntax on core filters:
#
#    @register_filter("grayscale", "Convert to grayscale")
#    @timer
#    def grayscale(pixels): ...
#
# Which Python expands bottom-up to:
#    step1 = timer(grayscale)                              # wrap with timing
#    step2 = register_filter("grayscale", "...")(step1)    # register the wrapper
#    grayscale = step2
#
# You can't use @ on factory-created functions because there's no
# def statement to decorate — the function already exists as a
# variable. So you use the manual inside-out call form instead.


# =============================================================================
# INTROSPECTION (Advanced Debugging)
# =============================================================================

def _log_closure_debug(filters: DictFuncs = FILTERS) -> None:
    """One-time diagnostic: log captured closure variables."""
    for filter_info in filters.values():
        func: FilterFunc = filter_info.func
        # Non-closure functions have __closure__ = None
        if func.__closure__:  # Captures free variables (tuple)
            for i, cell in enumerate(func.__closure__):
                # __code__.co_freevars lists the NAMES of captured variables (tuple)
                var = func.__code__.co_freevars[i]
                # Each cell has a .cell_contents attribute with the actual value
                logger.debug(f"{func.__name__} captured: {var} "
                                 f"= {cell.cell_contents!r}")
    
    
#  =============================================================================
#
# A CLOSURE is a function that captures variables from its enclosing
# scope. The captured variables are stored in __closure__ as a tuple
# of "cell" objects.
#
# VISUAL:
# ┌─────────────────────────────────────────────────┐
# │  def make_adder(n):          # Enclosing scope  │
# │      ┌────────────────────┐                     │
# │      │ n = 10  (captured) │ ← "free variable"   │
# │      └────────┬───────────┘                     │
# │               │                                 │
# │      def adder(x):           # Inner function   │
# │          return x + n        # Uses 'n' from    │
# │                              # enclosing scope  │
# │      return adder                               │
# │                                                  │
# │  add10 = make_adder(10)                          │
# │  add10.__closure__[0].cell_contents == 10        │
# └─────────────────────────────────────────────────┘
#
# WHY THIS MATTERS:
# Your create_brightness_filter IS a closure. The 'adjustment'
# parameter is a free variable captured by the inner function.
# Understanding __closure__ lets you inspect what values were
# captured — invaluable for debugging.
#
# =============================================================================
