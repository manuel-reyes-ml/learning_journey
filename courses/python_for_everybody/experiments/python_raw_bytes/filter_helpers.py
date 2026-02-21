
from bmp_handler import read_bmp, write_bmp
import copy

def apply_grayscale(width, height, pixels):
    # Remember: Never modify the riginal list if you filter
    # depends on neighbors (like blur/edges).
    # For grayscale it's fine, but copy.deepcopy is a safe habit!
    new_pixels = copy.deepcopy(pixels)
    # =============================================================================
    # COPYING LISTS QUICK REFERENCE
    # =============================================================================
    #
    # Simple list (no nesting):
    #     copy = original.copy()
    #     copy = list(original)
    #     copy = original[:]
    #
    # Nested list (like pixels):
    #     from copy import deepcopy
    #     copy = deepcopy(original)  # Simple but slow
    #
    #     # Or: List comprehension (faster)
    #     copy = [[pixel.copy() for pixel in row] for row in pixels]
    #     copy = [[[b, g, r] for b, g, r in row] for row in pixels]
    #
    # Creating NEW structure (fastest for filters):
    #     new = [[None] * width for _ in range(height)]
    #     # Then fill with new values
    #
    # =============================================================================
    
    for y in range(height):
        for x in range(width):
            b, g, r = pixels[y][x]
            
            # --- YOUR GRAYSCALE MATCH GOES HERE ---
            gray_val = int(0.299 * r + 0.587 * g + 0.114 * b)
            
            new_pixels[y][x] = [gray_val, gray_val, gray_val]
    
    return new_pixels


# --- Main Execution ---
input_file = "input.bmp"
output_file = "output_gray.bmp"

# 1. Read the image
width, height, pixels, header = read_bmp(input_file)

# 2. Apply your filter
filtered_pixels = apply_grayscale(width, height, pixels)

# 3. Save the new image
write_bmp(output_file, width, height, filtered_pixels, header)
print("Image filtered successfully")