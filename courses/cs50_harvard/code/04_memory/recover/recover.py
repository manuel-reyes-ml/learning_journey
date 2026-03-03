"""
"""

# =============================================================================
# IMPORTS
# =============================================================================

from __future__ import annotations  # Must be at the beginning of the file
from typing import Final, NamedTuple, TypedDict
from dataclasses import dataclass
from enum import IntEnum, unique
from pathlib import Path
import argparse
import logging
import struct
import sys


# =============================================================================
# MODULE CONFIGURATION
# =============================================================================

# =====================================================
# Exports
# =====================================================

__all__ = [
    # Core functions
    "validate_infile",
    "generate_outfile",
    "recover_jpeg",
    # Types (needed by consumers of recover_jpeg's return value)
    "JPEGRecoverResult",
    "ImageVariables",
    "ExitCode",
    # Configuration (useful for custom workflows)
    "FileDirectories",
    "FileName",
    "ImageData",
]


# =====================================================
# Type Aliases
# =====================================================

type ImagesReport = dict[str, ImageVariables]


# =====================================================
# Dataclass Frozen Constants
# ===================================================== 

# Directories
@dataclass(frozen=True, slots=True)
class FileDirectories:
    """
    """
    CUR_DIR: Final[Path] = Path(__file__).resolve().parent
    INPUT_DIR: Final[Path] = CUR_DIR / "memory_card"
    OUT_DIR: Final[Path] = CUR_DIR / "recovered"

# File information
@dataclass(frozen=True, slots=True)
class FileName:
    """
    """
    INFILE_EXT: str = ".raw"
    OUTFILE_EXT: str = ".jpeg"
    OUT_FNAME: str = f"image_"  # complete during file writing


# =====================================================
# Dataclass Instantiation
# =====================================================

# Following PEP 8 standars, name of an instance should be lowercase,
# unless it is a global constant itself.
file_directories = FileDirectories()
filename = FileName()


# =====================================================
# Other Class Configuration
# =====================================================

# JPEG Image information
class ImageData(IntEnum):
    """
    """
    BLOCK_SIZE = 512
    BITS_MASK = 0xf0
    KB_PER_BYTE = 1024
    MIN_BLOCK_SIZE = 4
    BYTE_0 = 0xff
    BYTE_1 = 0xd8
    BYTE_2 = 0xff
    BYTE_3 = 0xe0
    
# Exit codes (Unix standard)
@unique  # Ensure no duplicate values
class ExitCode(IntEnum):
    """
    """
    SUCCESS = 0
    FAILURE = 1
    KEYBOARD_INTERRUPT = 130
    
class ByteSignature(NamedTuple):
    """
    """
    byte_0: int
    byte_1: int
    byte_2: int
    byte_3: int

# TypedDict makes a fix structure for a Dictionary,
# for Type checker to warn later on the program.
class ImageVariables(TypedDict):
    """
    """
    kb_size: float

class JPEGRecoverResult(TypedDict):
    """
    """
    images_recovered: int
    images_details: ImagesReport  # Nested dictionary
    output_file: Path | None
    

# =====================================================
# Logging Configuration
# =====================================================

# Inherits from Python´s built-in Formatter
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
        logging.DEBUG:     "\033[90m",   # Gray
        logging.INFO:      "\033[92m",   # Green
        logging.WARNING:   "\033[93m",   # Yellow
        logging.ERROR:     "\033[91m",   # Red
        logging.CRITICAL:  "\033[1;91m", # Bold Red
    }
    RESET: Final[str] = "\033[0m"
    
    # Override the parent´s format method
    def format(self, record) -> str:
        # Step 1: Get the color for this log level 
        color = self.COLORS.get(record.levelno, self.RESET)
        
        # Step 2: Format the message normally first
        # This produces: "14:30:45 : INFO : Your message here"
        message = super().format(record)  # Call PARENT's format!
        
        # Step 3: Wrap with color codes
        return f"{color}{message}{self.RESET}"
    

# Set up logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Create handler with colored formatter
console_handler = logging.StreamHandler()
console_handler.setFormatter(ColoredFormatter(
    fmt='%(asctime)s : %(levelname)s : %(message)s',
    datefmt='%H:%M:%S',
))
logger.addHandler(console_handler)


# =============================================================================
# INTERNAL HELPER FUNCTIONS
# =============================================================================

def _build_outfile_path(
    out_fname: str | None = None,
    out_dir: Path = file_directories.OUT_DIR,
) -> Path:
    """
    """
    if out_fname == "":
        raise ValueError("out_fname cannot be empty")
    
    if not isinstance(out_fname, str):
        raise TypeError(f"out_fname must a string. Got '{type(out_fname)}'")
    
    if not out_dir.exists():
        out_dir.mkdir(parents=True, exist_ok=True)
    
    return out_dir / out_fname


def _is_jpeg_start(
    buffer: ByteSignature | None = None,
    byte_0: int = ImageData.BYTE_0,
    byte_1: int = ImageData.BYTE_1,
    byte_2: int = ImageData.BYTE_2,
    byte_3: int = ImageData.BYTE_3,
    bits_mask: int = ImageData.BITS_MASK,
) -> bool:
    """
    """
    if not buffer: 
        raise ValueError("Buffer cannot be empty")
    
    return (
        buffer.byte_0 == byte_0 and
        buffer.byte_1 == byte_1 and
        buffer.byte_2 == byte_2 and
        (
            buffer.byte_3 & 
            bits_mask
        ) == byte_3
    )


# =============================================================================
# CORE FUNCTIONS
# =============================================================================

def validate_infile(
    fname: str | None = None,
    input_dir: Path | str | None = None,
    auto_rename: bool = False,
    infile_ext: str = filename.INFILE_EXT,
    default_dir: Path = file_directories.INPUT_DIR,
    ) -> Path:
    """
    """
    if not fname:
        raise ValueError("File name cannot be empty")
    
    if input_dir:
        if not isinstance(input_dir, Path):
            input_dir = Path(input_dir)
        input_dir = input_dir.expanduser().resolve()
        in_file = input_dir / fname
    else: 
        logger.debug("Not directory entered by user, searching in default directory....")
        in_file = Path(fname).resolve() if Path(fname).exists() else default_dir / fname
    
    if in_file.is_file():
        
        # Check 1: File with correct extension?
        # .suffix gets the extension (.raw)
        if in_file.suffix == infile_ext:
            return in_file
        
        # Check 2: It is already a RAW file (but maybe uppercase like .RaW or not extension)?
        elif in_file.suffix.lower() == infile_ext or in_file.suffix == "":
            if auto_rename:
                logger.debug(
                    f"Auto-renaming file {in_file.name} to {in_file.with_suffix(infile_ext).name}"
                )
                new_in_file = in_file.with_suffix(infile_ext)
                in_file.rename(new_in_file)
                # .name returns just file name ('card.raw')
                logger.info(f"File name updated successfully to {new_in_file.name}")
                return new_in_file
            else:
                # Multiple lines using f-strings for readability
                logger.warning(f"File '{in_file.name}' has non-standard extension. "
                               f"Use auto-rename=True to fix.") 
                return in_file
        else:
            raise FileExistsError(f"{fname} is not a valid '{infile_ext}' file")
    else:
        raise FileNotFoundError(f"{fname} doesn't exist in directory '{in_file}'")
# BEFORE — validate_infile does TWO jobs:
# Job 1: Validate a file path (logic)
# Job 2: Ask a human what to do (user interaction)

# PRODUCTION PATTERN — each layer handles its own job:

#  main()           → Handles ALL user interaction (argparse, prompts)
#  validate_infile  → Handles ONLY validation logic
#  recover_jpeg     → Handles ONLY recovery logic

# The "decision" flows DOWN as a parameter, not UP as an input() call


def generate_outfile(
    image_counter: int | str | None = None,
    file_ext: str = filename.OUTFILE_EXT,
    fname: str = filename.OUT_FNAME,
) -> Path:
    """
    """
    # If its any other Type than 'int' or 'str' (eg. None, float)
    if not isinstance(image_counter, (int, str)):
        raise TypeError(f"image_count must be an integer or string. Got '{type(image_counter)}'")
    
    # If its empty
    if image_counter == "":
        raise ValueError("image_counter cannot be empty")
    
    if isinstance(image_counter, str):
        if not image_counter.strip().isdigit(): 
            raise ValueError("image_counter string must only contain digits")   

        image_counter = int(image_counter.strip())

    out_fname = f"{fname}{image_counter:03}{file_ext}"
        
    return _build_outfile_path(out_fname)
    
        
def recover_jpeg(
    infile: Path | None = None,
    block_size: int = ImageData.BLOCK_SIZE,
    kb_per_byte: int = ImageData.KB_PER_BYTE,
    min_block_size: int = ImageData.MIN_BLOCK_SIZE,
) -> JPEGRecoverResult:
    """
    """
    if not infile:
        raise ValueError("Input file cannot be empty")
    
    with open(infile, "rb") as inputf:
        
        kbytes: float = 0.0
        image_counter: int = 0
        out_filename = None
        output_dir = None
        out_handler = None
        images_result: ImagesReport = {}
        
        try:
            while True:
                buffer: bytes = inputf.read(block_size)
                
                if not buffer:
                    break
                
                if len(buffer) < min_block_size:  # Guard if buffer is less than signature (4 bytes)
                    break
                
                b0, b1, b2, b3 = struct.unpack("<BBBB", buffer[0:4])
                signature = ByteSignature(b0, b1, b2, b3)
                
                # Check if the block is the start of a new JPEG
                if _is_jpeg_start(signature): 
                    #If we were already writing a file, close it
                    if out_handler:
                        # .tell() returns the current position of the file pointer in bytes
                        kbytes = out_handler.tell() / kb_per_byte
                        out_handler.close()
                        
                        if out_filename:
                            images_result[out_filename.name] = ImageVariables(kb_size=kbytes)
                    
                    # Open a new file to start writing
                    image_counter += 1
                    out_filename = generate_outfile(image_counter)
                    out_handler = open(out_filename, "wb")
                    
                    
                    
                    # Write the start of the image
                    out_handler.write(buffer)
                
                # If it´s not a new JPEG start, but we have a file open, keep writing
                elif out_handler:
                    out_handler.write(buffer)
        
        finally:
            # Ensure the file is closed even if an error occurs (finally always executes)
            # Close the last file if one was open        
            if out_handler:
                kbytes = out_handler.tell() / kb_per_byte
                out_handler.close()
                
                if out_filename:
                    images_result[out_filename.name] = ImageVariables(kb_size=kbytes)
                    output_dir = out_filename.parent
            
    if not images_result:
        raise ValueError(f"{infile.name} is empty")
    
    return {
        "images_recovered": image_counter,
        "images_details": images_result,
        "output_file": output_dir,
    }

    
# =============================================================================
# CLI ENTRY POINT
# =============================================================================

def main(argv: list[str] | None = None)-> ExitCode:
    """
    """
    parser = argparse.ArgumentParser(
        description=f"Recover all images from memory card file, with '{filename.OUTFILE_EXT}' signature"
    )
    parser.add_argument(
        "-i", "--input-file",  # Short and long flag arguments (optional)
        required=True,
        type=str,
        help=f"Enter memory card file, format '{filename.INFILE_EXT}'",
    )
    parser.add_argument(
        "-o", "--output-file",
        type=str,
        help=f"Enter desired prefix for output. Default: '{filename.OUT_FNAME}'",
    )
    parser.add_argument(
        "-d", "--directory",
        type=str,
        help=f"Enter directory path to search for input file. Default: '{file_directories.INPUT_DIR}'"
    )
    parser.add_argument(
        "--auto-rename",
        action="store_true",
        help="Automatically rename input file to standard extension"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose (debug) output",
    )
    
    args = parser.parse_args(argv)
    
    if args.verbose:
        logger.setLevel(logging.DEBUG)
        logger.debug("Verbose mode enabled")
        
    try:
        input_file = validate_infile(
            args.input_file,
            args.directory,
            auto_rename=args.auto_rename)
        
        report: JPEGRecoverResult = recover_jpeg(input_file)
        
    except KeyboardInterrupt:
        logger.warning("\nInterrupted by user. Exiting.")
        return ExitCode.KEYBOARD_INTERRUPT
    
    except (FileExistsError, FileNotFoundError) as e:
        logger.error(f"File Error: {e}")
        return ExitCode.FAILURE
    
    except (ValueError, TypeError, struct.error) as e:
        logger.error(f"Processing Error: {e}")
        return ExitCode.FAILURE
    
    except Exception as e: 
        logger.exception(f"Unexpected Error: {e}")  # Behaves like .error but includes TraceBack info
        return ExitCode.FAILURE
    
    
    # Print out report using logging
    logger.info(f"Recovered {report['images_recovered']} images from file")
    
    for image, size in report["images_details"].items():
        logger.info(f"Name: {image}, Size: {size['kb_size']} KB")
        
    logger.info(f"All images are saved in: '{report['output_file']}'")
    
    return ExitCode.SUCCESS
    
    
if __name__ == "__main__":
    sys.exit(main())