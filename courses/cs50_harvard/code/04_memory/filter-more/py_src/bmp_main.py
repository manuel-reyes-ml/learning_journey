"""
"""

from __future__ import annotations
from typing import Iterator
from pathlib import Path
import argparse
import logging
import string
import sys

try:
    from .bmp_config import (
        ColoredFormatter,
        DictDispatch,
        DIRS,
        EXIT,
    )
    from .bmp_filters import(
        grayscale,
        reflect,
        edges,
        blur,
    )
    from .bmp_io import read_bmp, write_bmp
    
except ImportError as e:
    sys.exit(f"Error: Cannot find relative modules.\nDetails: {e}")


# =============================================================================
# Module Configuration
# =============================================================================

# Exports


# Program Constants
# parents=True: create any missing parent directories
# exist_ok=True: no error if directory already exists
DIRS.OUT_DIR.mkdir(parents=True, exist_ok=True)

# Keys = function names (strings)
# Values = functions (NOT called — no parentheses!)
FUNCS: DictDispatch = {     # Creating Dictionary Dispatch for faster func iteration
    "grayscale": grayscale,
    "reflect": reflect,
    "edges": edges,
    "blur": blur,
} 

# Set up Logging
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
# Internal Helper Functions
# =============================================================================

def _validate_filter(filter: str | None = None, funcs: DictDispatch = FUNCS) -> str:
    """
    """
    if not filter:
        raise argparse.ArgumentTypeError("Filter cannot be empty")
    
    clean_filter = filter.strip().strip(string.punctuation).lower()
    
    if not clean_filter.isalpha():
        raise argparse.ArgumentTypeError("Filter must be alphabetic")
    
    if not clean_filter in funcs:
        raise argparse.ArgumentTypeError(
            f"{filter} is not part or current functions: {funcs.keys()}"
        )
    
    return clean_filter


def _validate_filters(filters: list[str] | None = None) -> Iterator[str]:
    """
    """
    if not filters:
        raise ValueError("Filters cannot be empty")
    
    # Set is an unordered collection of UNIQUE items
    if len(filters) != len(set(filters)):
        raise ValueError("Filters must not contain duplicates")
    
    for filter in filters:
        yield _validate_filter(filter)


# =============================================================================
# Core Functions
# =============================================================================

def validate_infile(
    fname: str | None = None,
    input_dir: str | None = None,
    file_ext: str = DIRS.FILE_EXT,
    image_dir: Path = DIRS.INPUT_DIR,
) -> Path:
    """
    """
    if not fname:
        raise ValueError("File name cannot be empty")
    
    # Convert string into a Path object
    if input_dir:
        in_file = Path(input_dir).expanduser().resolve() / fname
    else:
        logger.debug("Not directory entered by user, searching in default directory....")
        in_file = Path(fname).resolve() if Path(fname).exists() else image_dir / fname
        
    logger.debug(f"Searching input file in '{in_file}'....")
    
    if in_file.is_file():
        
        # Check 1: File with the correction extension?
        # .suffix gets the extension (e.g. .Bmp)
        if in_file.suffix == file_ext:
            return in_file
        
        # Check 2: It is already a BMP file (but maybe uppercase like .BmP or no extension)?
        elif in_file.suffix.lower() == file_ext or in_file.suffix == "":
            consent = input(
                f"Would you like me to correct extension to {in_file.name} (yes/no): "
            ).strip().lower()
            
            if consent in ["yes", "y"]:
                new_in_file = in_file.with_suffix(file_ext)
                in_file.rename(new_in_file)
                logger.info(f"File name updated successfully to {in_file.name}")
                
                return new_in_file
            
            else:
                logger.warning(f"File name is unchanged {in_file.name}")
            
                return in_file
        
        else:
            raise FileExistsError(f"{fname} is not a valid BMP file")
    else:
        raise FileNotFoundError(f"{fname} doesn't exists in directory '{in_file}'")
    
    
def validate_outfile(
    fname: str | None = None,
    in_file: Path | None = None,
    filter_name: str | None = None,
    out_dir: Path = DIRS.OUT_DIR,
    file_ext: str = DIRS.FILE_EXT,
) -> Path:
    """
    """
    if not fname:
        if not in_file or not filter_name:
            raise ValueError("File name cannot be empty")
        
        fname = f"{in_file.stem}_{filter_name}{file_ext}"
        
    out_file = out_dir / fname
    
    if out_file.suffix != file_ext:
        out_file = out_file.with_suffix(file_ext)
    
    logger.debug(f"Saving output file in directory '{out_file}'")
    return out_file


def process_filter(
    pixels: list | None = None,
    filters: list[str] | None = None,
    funcs: DictDispatch = FUNCS,
) -> Iterator[tuple[list, str]]:
    """
    """
    if not filters:
        raise ValueError("Filter(s) list cannot be emtpy")
    
    if not pixels:
        raise ValueError("Pixels cannot be empty")
    
    try:
        for clean_filter in _validate_filters(filters):
            # funcs[clean_filter](pixels):  Dictionary dispatch!
            # Applies filter function following clean_filter("blur", "reflect", etc.)
            yield funcs[clean_filter](pixels), clean_filter
        
    except (
        argparse.ArgumentTypeError,
        ValueError,
    ) as e:
        raise ValueError(f"Validation Error: {e}") from e
    

# =============================================================================
# CLI Entry Point
# =============================================================================

def main(argv: list[str] | None = None) -> int:
    """
    """
    parser = argparse.ArgumentParser(
        description=f"Apply one, some or all filters to an image. Options: {FUNCS.keys()}"
    )
    parser.add_argument(
        "-i", "--input-file",
        type=str,
        help=f"Enter file name of input {DIRS.FILE_EXT} file",
    )
    parser.add_argument(
        "-o", "--output-file",
        type=str,
        help=f"Enter file name of output {DIRS.FILE_EXT} file",
    )
    parser.add_argument(
        "-f", "--filter",
        type=_validate_filter,
        nargs="+",
        help=(
            f"Enter filters to apply to the image. Use 'all' for all filters: {FUNCS.keys()}"
        )
    )
    parser.add_argument(
        "-d", "--directory",
        type=str,
        help=(
            f"Enter directory path to search for {DIRS.FILE_EXT} file. Default is images/ directory"
        )
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose (debu) output"
    )
    
    args = parser.parse_args(argv)
    
    if args.verbose:
        logger.setLevel(logging.DEBUG)
        logger.debug("Verbose mode enabled")
    
    if str(args.filter).strip().lower() == "all":
        filters = list(FUNCS.keys())
    else:
        filters = args.filter
        
    try:
        # Step 1: Input and read BMP file
        in_file = validate_infile(args.input_file, args.directory)
        width, height, pixels, full_header = read_bmp(in_file)
        
        # Step 2: Apply filter using a generator
        for new_pixels, clean_filter in process_filter(pixels, filters):
            
            # Step 3: Generate output file and write BMP
            out_file = validate_outfile(
                args.output_file, 
                in_file, 
                clean_filter,
            )
            
            write_bmp(out_file, width, new_pixels, full_header)
            
    except KeyboardInterrupt:
        logger.warning("\nInterrupted by user. Exiting.")
        return EXIT.KEYBOARD_INTERRUPT
        
    except (FileExistsError, FileNotFoundError) as e:
        logger.error(f"Error in file: {e}")
        return EXIT.FAILURE
        
    except ValueError as e:
        logger.error(f"Error in processing: {e}")
        return EXIT.FAILURE
    
    except Exception as e:  # Catches every other exception in program
        # Appears as logging.error, provides Python's traceback info
        logger.exception(f"Unexpected Error: {e}")
        return EXIT.FAILURE
    
    return EXIT.SUCCESS


if __name__ == "__main__":
    sys.exit(main()) 