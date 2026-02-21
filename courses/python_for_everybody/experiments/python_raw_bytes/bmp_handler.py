import struct

def read_bmp(filename):
    """Reads a 24-bit uncompressed BMP and returns a 2D list of pixels"""
    
    # 'rb' read binary mode. Returns bytes, not str(string)
    with open(filename, "rb") as f:
        # 1. Read the 14-byte BMP header
        # Returns a bytes object: b'BM\x36\x00\x0c\x00...'
        bmp_header = f.read(14)
        # All BMP files start with "BM"(for "bitmap")
        if bmp_header[0:2] != b"BM":
            raise ValueError("Not a valid BMP file. Must start witn 'BM'.")
        
        # Extract the offset (where pixel data starts) from bytes 10-13
        # struct.unpack: convert raw bytes to Python value
        pixel_offset = struct.unpack('<I', bmp_header[10:14])[0]
        
        # 2. Read the DIB Header
        # We read everything between the BMP header and the pixel offset
        # Pixel-offset in the BPM headers tells us exactly where pixel data starts
        # pixel_offset = 54 -- dib_header_size = 54 - 14(BMP header size)
        ## Visual Example ===========================================================
        # **Standard 24-bit BMP:**
        # Offset 0:   BMP Header (14 bytes)
        # Offset 14:  DIB Header (40 bytes)
        # Offset 54:  Pixel Data ← pixel_offset = 54

        # **8-bit BMP with color table:**
        # Offset 0:    BMP Header (14 bytes)
        # Offset 14:   DIB Header (40 bytes)
        # Offset 54:   Color Table (256 × 4 = 1024 bytes)
        # Offset 1078: Pixel Data ← pixel_offset = 1078
        dib_header_size = pixel_offset - 14
        dib_header = f.read(dib_header_size)
        
        # Extract Width (bytes 4-7 in DIB) and Height (bytes 8-11 in DIB)
        width = struct.unpack('<i', dib_header[4:8])[0]
        height = struct.unpack('<i', dib_header[8:12])[0]
        
        # Check if it's 24-bit (bytes 14-15 in DIB)
        bpp = struct.unpack('<H', dib_header[14:16])[0]
        if bpp != 24:
            raise ValueError("This boilerplate only supports 24-bit BMPs.")
        
        # Calculate how many padding bytes are at the end of each row
        padding = (4 - (width * 3) % 4) % 4
        
        pixels = []
        # Loop through every row
        for _ in range(abs(height)):
            row = []
            # loop through every pixel in the row
            for _ in range(width):
                # Unpack 3 bytes as Blue, Green, Red
                b, g, r = struct.unpack('<BBB', f.read(3))
                row.append([b, g, r])
            
            f.read(padding)
            pixels.append(row)
        
    # We return the original headers so we can easily glue them back
    # onto the new file without having to recalculate file sizes.
    full_header = bmp_header + dib_header
    return width, height, pixels, full_header

