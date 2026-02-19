"""
"""

from __future__ import annotations
from typing import Final
from pathlib import Path
import argparse
import struct
import logging
import sys


# =============================================================================
# Module Configuration
# =============================================================================

# Exports
__all__ = [
    "validate_input_file",
    "validate_output_file",
    "change_volume",
    "HEADER_SIZE",
    "SAMPLE_SIZE",
    "BIT_FORMAT",
    "FILE_EXT",
    "DATA_DIR",
]

# Program Constants
HEADER_SIZE: Final[int] = 44
SAMPLE_SIZE: Final[int] = 2
BIT_FORMAT: Final[str] = '<h'
FILE_EXT: Final[str] = ".wav"
OUT_FNAME: Final[str] = "output.wav"
DATA_DIR: Final[Path] = Path(__name__).resolve().parent / "data"


# Exit codes (Unix standard)
EXIT_SUCCESS: Final[int] = 0
EXIT_FAILURE: Final[int] = 1
EXIT_KEYBOARD_INTERRUPT: Final[int] = 130

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
        logging.DEBUG:     "\033[90m",   # Greay
        logging.INFO:      "\033[92m",   # Green
        logging.WARNING:   "\033[93m",   # Yellow
        logging.ERROR:     "\033[91m",   # Red
        logging.CRITICAL:  "\033[1;91m", # Bold Red
    }
    RESET: Final[str] = "\033[0m"
    
    # Overried the parent's format method
    def format(self, record) -> str:
        # Step 1: Get the color for this log level
        color = self.COLORS.get(record.levelno, self.RESET)
        
        # Step 2: Format the message normally first
        # This produces: "14:30:45 : INFO : Your message here"
        message = super().format(record) # Call PARENT's format!
        
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

def validate_input_file(
    fname: str | None = None,
    input_dir: str | None = None,
    file_ext: str = FILE_EXT,
    data_dir: Path = DATA_DIR,
) -> Path:
    """
    Validate file names from arguments
    """
    if not fname:
        raise ValueError("File name cannot be empty")
    
    # Convert the string into a Path object
    if input_dir:
        input_file = Path(input_dir).expanduser().resolve() / fname
    else:
        logger.debug("Not directory entered by user, searching in default directories....")
        input_file = Path(fname).resolve() if Path(fname).exists() else data_dir / fname
    
    logger.debug(f"Searching input file in '{input_file}'....")
    if input_file.is_file():
        
        # Check 1: File with the correct extension?
        # .suffix gets the extension (e.g. .Wav)
        if input_file.suffix == file_ext:
            return input_file
        
        # Check 2: It is already a WAV file (but maybe uppercase like .WaV)?
        elif input_file.suffix.lower() == file_ext:
            # .with_suffix automatically replaces the old extension with the new one
            return input_file.with_suffix(file_ext)
        
        # Check 3: Does it have not extension at all?
        elif input_file.suffix == "":
            return input_file.with_suffix(file_ext)
        
        # Check 4: It has an extension, but it´s  the wrong find (like .mp3)
        else:
            raise FileExistsError(f"{fname} is not a valid WAV file")
    else:
        raise FileNotFoundError(f"{fname} doesn't exists in directory '{input_file}'")

    # ==============================================================================
    # PATHLIB METHOD QUICK REFERENCE
    # How pathlib distinguishes between files, directories, and non-existent paths:
    # 
    # Assume for these examples: 
    # - "input.wav" is a real file that currently exists on the hard drive.
    # - "Music" is a real folder that currently exists on the hard drive.
    # - "fake.wav" is just a string in memory; it does not exist on the drive yet.
    #
    # | Method      | What it checks                         | input.wav | Music | fake.wav |
    # |-------------|----------------------------------------|-----------|-------|----------|
    # | .is_file()  | Is it a file AND does it exist?        | True      | False | False    |
    # | .is_dir()   | Is it a folder AND does it exist?      | False     | True  | False    |
    # | .exists()   | Does it exist at all (file OR folder)? | True      | True  | False    |
    # ==============================================================================


def validate_output_file(
    input_file: Path | None = None,
    fname: str = OUT_FNAME,
    file_ext: str = FILE_EXT,
) -> Path:
    """
    """
    if not input_file:
        raise FileNotFoundError("File path cannot be empty")
    
    logger.debug("Input file found......")
    file_path = input_file.parent
    
    output_file = file_path / fname
    
    if output_file.suffix != file_ext:
        output_file = output_file.with_suffix(file_ext)
    
    logger.debug(f"Saving output file in same directory '{output_file}'")
    return output_file


def _validate_factor(factor: str | None = None) -> int:
    """
    """ 
    if not factor:
        raise argparse.ArgumentTypeError("Factor cannot be empty")
    
    try:
        factor_int = int(factor.strip())
    except (ValueError, TypeError) as e:
        raise argparse.ArgumentTypeError("Factor must contain numeric characters only")
    
    return factor_int


def change_volume(
    input_file: Path | None = None,
    output_file: Path | None = None,
    factor: int | None = None,
    bit_format: str = BIT_FORMAT,
    header_size: int = HEADER_SIZE,
    sample_size: int = SAMPLE_SIZE,
) -> None:
    """
    """
    if not input_file or not output_file:
        raise FileNotFoundError("File(s) path cannot be empty")
    
    if not factor:
        raise ValueError("Factor cannt be empty")
    
    #Open files in "rb" (read binary) and "wb" (write binary) modes
    # Use context manager ('with...') to make sure connector to file is close after with block
    logger.debug(f"Opening input and output file to update volume using factor {factor}....")
    with open(input_file, "rb") as infile, open(output_file, "wb") as outfile:
        
        file_empty = True
        # 1. Read the exact 44-byte header and immediately write it to the new file
        header = infile.read(header_size)
        outfile.write(header)

        count_bytes = 0
        
        # 2. Loop through the rest of the file, 2 bytes at a time
        while True:
            sample_bytes = infile.read(sample_size)
                
            # If we didn't get any bytes, we rechaed the end of the file
            if not sample_bytes:
                break
            
            file_empty = False
            count_bytes += 2
             
            # When you read a file in binary("rb"), Python doesn't see "numbers", it sees raw
            # hex bytes like '\xff\x10'.
                
            # 3. Unpack the 2 raw bytes into a Python integer
            # '<h' tells Python: "This is a Little-Endian, 16-bit signed integer (short)"
            # struct.unpack grabs those bytes and translates them into a human-readable math number(like -543)
            sample = struct.unpack(bit_format, sample_bytes)[0]
                
            # 4. Change the volume (multiply by factor)
            new_sample = int(sample * factor)
                
            # 5. Prevent Clipping (Clamp values to 16-bit limits)
            new_sample = new_sample if new_sample <= 32767 else 32767
            new_sample = new_sample if new_sample >= -32768 else -32768
                
            # 6. Pack the new integer back into 2 raw bytes and write it
            # struct.pack translates your  match back into the raw machine bytes the WAV file expects
            new_sample_bytes = struct.pack(bit_format, new_sample)
            outfile.write(new_sample_bytes)
                
        if file_empty:
            raise ValueError(f"File {input_file} is empty")
        logger.debug(f"Input file not empty, updating {count_bytes} bytes......")
        
        logger.info(f"Success: Updated volume by factor of {factor} in {output_file}")
        

# =============================================================================
# CLI Entry Point
# =============================================================================
    
def main(argv: list[str] | None = None) -> int:
    """
    """
    parser = argparse.ArgumentParser(
        description="Change volume of audio file using a factor from user"
    )
    # No need to add 'nargs' since it changes argument´s output automatically to a list, not single strings
    #   -> parser.add_argument("input_file", nargs=1)
    #   -> Returns a list -> ['input.wav']
    parser.add_argument(
        "-input", "--input-file",
        type= str,
        help="Enter file name of input audio file",
    )
    parser.add_argument(
        "-out", "--output-file",
        type=str,
        default=OUT_FNAME,
        help=f"Enter file name of output audio file. Default if 'None': {OUT_FNAME}",
    )
    parser.add_argument(
        "factor",
        type=_validate_factor,
        help="Enter factor number to be used to update volume of audio file",
    )
    parser.add_argument(
        "-dir", "--directory",
        type=str,
        help=f"Enter directory or Path to search for input audio file. Default is current directory or {DATA_DIR}"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose (debug) output"
    )
    
    args = parser.parse_args(argv)
    
    if args.verbose:
        logger.setLevel(logging.DEBUG)
        logger.debug("Verbose mode enabled")
     
    try:
        input_file = validate_input_file(args.input_file, args.directory)
        output_file = validate_output_file(input_file, args.output_file)
        
        change_volume(input_file, output_file, args.factor)
        
    except KeyboardInterrupt:
        logger.warning("\nInterrupted by user. Exiting.")
        return EXIT_KEYBOARD_INTERRUPT
    
    except (FileExistsError, FileNotFoundError) as e:
        logger.error(f"Error in file: {e}")
        return EXIT_FAILURE
    
    except ValueError as e:
        logger.error(f"Error in processing: {e}")
        return EXIT_FAILURE
    
    except Exception as e:
        logger.exception(f"Unexpected Error: {e}")
        return EXIT_FAILURE
        
    return EXIT_SUCCESS


if __name__ == "__main__":
    sys.exit(main())