"""
Here is exactly how WAV files work under the hood and how you can manipulate them in Python.

1. How Digital Audio Works
Sound is just a continuous wave of physical pressure in the air. To store this wave on a computer, we take "snapshots" of the wave's height at specific intervals.

    - Sample Rate: How many snapshots we take per second (typically 44,100 times a second for CD-quality audio).

    - Sample / Amplitude: The actual "height" of the wave at that exact moment.

To change the volume, all you have to do is take the height of each snapshot and multiply it by a factor.

    - Factor 2.0 = Twice as loud (taller wave).

    - Factor 0.5 = Half as loud (shorter wave).

2. The Structure of a WAV File
A standard 16-bit PCM WAV file is divided into two strict sections:

    1. The Header (The first 44 bytes): This is the metadata. It tells the audio player "I am a WAV file, I have 2 channels (stereo), and my sample rate is 44100." 
    When changing the volume, you must not touch these 44 bytes. You just copy them directly to the new file.

    2. The Data (Byte 45 to the end): This is the actual audio. Every 2 bytes (16 bits) represents one audio sample.

3. The "Clipping" Danger
Because standard WAV files use 16-bit signed integers to store these samples, the maximum and minimum values a sample can hold are 32,767 and -32,768.

If a sample's value is 20,000 and you multiply it by 2.0 (volume up), you get 40,000. This is physically too big for 16 bits. 
The computer will "wrap around" into negative numbers, causing horrific, screeching distortion called clipping. You must clamp your values to the max/min limits!
"""

# To read raw bytes as integers in Python, we use the built-in 'struct' library. 

import struct  # All details about struct library are included at the end of this file
import sys

def change_volume(input_file, output_file, factor):
    # Standard WAV header is exactly 44 bytes
    HEADER_SIZE = 44
    
    try:
        #Open files in "rb" (read binary) and "wb" (write binary) modes
        # Use context manager ('with...') to make sure connector to file is close after with block
        with open(input_file, "rb") as infile, open(output_file, "wb") as outfile:
            
            # 1. Read the exact 44-byte header and immediately write it to the new file
            header = infile.read(HEADER_SIZE)
            outfile.write(header)
            
            # 2. Loop through the rest of the file, 2 bytes at a time
            while True:
                sample_bytes = infile.read(2)
                
                # If we didn't get any bytes, we reached the end of the file
                if not sample_bytes:
                    break
                
                # When you read a file in binary("rb"), Python doesn't see "numbers", it sees raw
                # hex bytes like '\xff\x10'.
                
                # 3. Unpack the 2 raw bytes into a Python integer
                # '<h' tells Python: "This is a Little-Endian, 16-bit signed integer (short)"
                # struct.unpack grabs those bytes and translates them into a human-readable math number(like -543)
                sample = struct.unpack('<h', sample_bytes)[0]
                
                # 4. Change the volume (multiply by factor)
                new_sample = int(sample * factor)
                
                # 5. Prevent Clipping (Clamp values to 16-bit limits)
                new_sample = new_sample if new_sample <= 32767 else 32767
                new_sample = new_sample if new_sample >= -32768 else -32768
                
                # 6. Pack the new integer back into 2 raw bytes and write it
                # struct.pack translates your match back into the raw machine bytes the WAV file expects
                new_sample_bytes = struct.pack('<h', new_sample)
                outfile.write(new_sample_bytes)
                
            print(f"Success: Updated volume by factor of {factor} in {output_file}")
    
    except FileNotFoundError:
        print("Error: Input file not found.")
        

if __name__ == "__main__":
    # Multiplies volume by 0.5 (half as loud)
    sys.exit(
        change_volume("input.wav", "output.wav", 3)
    )


# ==============================================================================
# UNDERSTANDING THE 'struct' LIBRARY IN PYTHON
# ==============================================================================
# What it is:
# The 'struct' module acts as a translator between Python's flexible data types 
# and raw, C-style machine memory (binary).
#
# Why we need it:
# In Python, an integer is just a number; it doesn't have a strict "byte size" 
# and handles its own memory. However, binary files (like WAV audio, BMP images) 
# require strict, exact byte layouts. For example, a 16-bit WAV file demands 
# that every single audio sample is exactly 2 bytes long. 'struct' bridges this 
# gap by forcing Python data into these strict byte blocks.
#
# The Two Main Functions:
# 1. struct.pack():   Translates Python values -> Raw Bytes
#                     (e.g., taking the number 1500 and packing it into 2 bytes)
# 2. struct.unpack(): Translates Raw Bytes -> Python values
#                     (e.g., reading '\xff\x10' and converting it to an integer)
#
# Format Strings (The Translation Rules):
# 'struct' uses specific characters to know how to translate the bytes:
#   'c' : char (1 byte)
#   'h' : short integer (2 bytes) <--- What we use for 16-bit WAV audio
#   'i' : standard integer (4 bytes)
#   'f' : float (4 bytes)
#   '<' : Little-Endian byte order (reads the least significant byte first)
# ==============================================================================

# --- Understanding struct.unpack('<h', sample_bytes)[0] ---
#
# 1. The Format String ('<h'):
#    - '<' (Little-Endian): Tells Python the byte order. WAV files store the 
#      least significant byte first. Without this, the audio would be static.
#    - 'h' (short): Tells Python to interpret the 2 bytes as a 16-bit signed 
#      integer, which exactly matches standard WAV audio samples.
#
# 2. The Return Value (Tuple):
#    - struct.unpack always returns a tuple, because it is designed to unpack 
#      multiple values at once (e.g., '<hhh' would return 3 integers). 
#    - Even though we only ask for one value, it returns it like this: (453,)
#
# 3. The Index ([0]):
#    - Since we cannot do math on a tuple (e.g., (453,) * 0.5 will crash), 
#      we use [0] to extract the very first item from the tuple. 
#    - This gives us the plain integer (453) so we can safely multiply it 
#      by our volume factor.