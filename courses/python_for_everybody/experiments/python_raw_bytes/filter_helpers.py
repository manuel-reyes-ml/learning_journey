
from bmp_handler import read_bmp, write_bmp
import copy

def apply_grayscale(width, height, pixels):
    # Remember: Never modify the riginal list if you filter
    # depends on neighbors (like blur/edges).
    # For grayscale it's fine, but copy.deepcopy is a safe habit!
    new_pixels = copy.deepcopy(pixels)
    
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