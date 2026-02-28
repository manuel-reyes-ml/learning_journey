"""
"""

# =============================================================================
# IMPORTS
# =============================================================================

from __future__ import annotations  # Must be at the beginning of the file
from typing import Iterator, Final, cast
from pathlib import Path
import argparse
import logging
import string
import sys

try:
    from .bmp_logger import setup_logging
    from .bmp_io import read_bmp, write_bmp
    from .bmp_config import (
        DictDispatch,
        FilterName,
        ImageData,
        ExitCode,
        ALL_FILTERS,
        CUR_DIR,
        bmp_dirs,
    )
    from .bmp_filters import (
        grayscale,
        reflect,
        edges,
        blur,
    )
    
except ImportError as e:
    sys.exit(f"Error: Cannot find relative modules.\nDetails: {e}")


# =============================================================================
# MODULE CONFIGURATION
# =============================================================================

# Exports
__all__ = [
    "validate_infile",
    "validate_outfile",
    "process_filter",
]

# Program Constants
# Path.name gives the full name of a file or directory
MODULE_NAME: Final[str] = f"{CUR_DIR.name}.bmp_main"

# Keys = function names (strings)
# Values = functions (NOT called — no parentheses!)
FUNCS: DictDispatch = {     # Creating Dictionary Dispatch for faster func iteration
    "grayscale": grayscale,
    "reflect": reflect,
    "edges": edges,
    "blur": blur,
} 

# Set up Logging
setup_logging()  # Uses logging.INFO by default!
# When running this module Python assigns string '__main__' to '__name__',
# so we need to assign the module name directly so this logger is assigned
# to the 'py_src' logger hierarchy we created in bmp_logger.py.
logger = logging.getLogger(MODULE_NAME)


# =============================================================================
# INTERNAL HELPER FUNCTIONS
# =============================================================================

def _validate_filter(
    filter_name: str | None = None,
    funcs: DictDispatch = FUNCS,
    all_filters: str = ALL_FILTERS,
) -> str:
    """
    """
    if not filter_name:
        raise argparse.ArgumentTypeError("Filter cannot be empty")
    
    clean_filter = filter_name.strip().strip(string.punctuation).lower()
    
    if not clean_filter.isalpha():
        raise argparse.ArgumentTypeError("Filter must be alphabetic")
    
    if clean_filter != all_filters:
        if not clean_filter in funcs:
            raise argparse.ArgumentTypeError(
                f"'{clean_filter}' is not part of current filters: {list(funcs.keys())}"
            )
        
    return clean_filter


def _validate_filters(filters: list[FilterName] | None = None) -> Iterator[str]:
    """
    """
    if not filters:
        raise ValueError("Filters cannot be empty")
    
    # Set is an unordered collection of UNIQUE items
    if len(filters) != len(set(filters)):
        raise ValueError("Filters must not contain duplicates")
    
    logger.debug("Filters list has been validated......")
    
    for filter_name in filters:
        yield _validate_filter(filter_name)


# =============================================================================
# CORE FUNCTIONS
# =============================================================================

def validate_infile(
    fname: str | None = None,
    input_dir: str | None = None,
    file_ext: str = bmp_dirs.FILE_EXT,
    image_dir: Path = bmp_dirs.INPUT_DIR,
) -> Path:
    """
    """
    if not fname:
        raise ValueError("Input file name cannot be empty")
    
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
                logger.info(f"File name updated successfully to {new_in_file.name}")
                
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
    out_dir: Path = bmp_dirs.OUT_DIR,
    file_ext: str = bmp_dirs.FILE_EXT,
) -> Path:
    """
    """
    if not fname:
        if not in_file or not filter_name:
            raise ValueError("File name cannot be empty")
        
        # path.stem gives filename without extention (image)
        fname = f"{in_file.stem}_{filter_name}{file_ext}"
        
    out_file = out_dir / fname
    
    if out_file.suffix != file_ext:
        out_file = out_file.with_suffix(file_ext)
        
    # parents=True: create any missing parent directories
    # exist_ok=True: no error if directory already exists
    out_dir.mkdir(parents=True, exist_ok=True)
        
    logger.debug(f"Saving output file in directory '{out_file}'")
    return out_file


def process_filter(
    pixels: ImageData | None = None,
    filters: list[FilterName] | None = None,
    funcs: DictDispatch = FUNCS,
) -> Iterator[tuple[ImageData, str]]:
    """
    """
    if not filters:
        raise ValueError("Filter(s) list cannot be emtpy")
    
    # Explicit check for ImageData (list of lists)
    # This distinguishes between "caller forgot to pass data",
    # and "data exists but is empty".
    if pixels is None:
        raise ValueError("Pixels argument is required")
    
    if len(pixels) == 0:
        raise ValueError("Pixels cannot be empty")
    
    try:
        for clean_filter in _validate_filters(filters):
            logger.warning(f"Applying [{clean_filter}] filter....")
            # funcs[clean_filter](pixels):  Dictionary dispatch!
            # Applies filter function following clean_filter("blur", "reflect", etc.)
            yield funcs[clean_filter](pixels), clean_filter
        
    except (
        argparse.ArgumentTypeError,
        ValueError,
    ) as e:
        raise ValueError(f"Validation Error: {e}") from e
    

# =============================================================================
# CLI ENTRY POINT
# =============================================================================

def main(argv: list[str] | None = None) -> ExitCode:
    """
    """
    parser = argparse.ArgumentParser(
        description=f"Apply one, some or all filters to an image. Options: {list(FUNCS.keys())}"
    )
    parser.add_argument(
        "-i", "--input-file",
        type=str,
        help=f"Enter file name of input {bmp_dirs.FILE_EXT} file",
    )
    parser.add_argument(
        "-o", "--output-file",
        type=str,
        help=f"Enter file name of output {bmp_dirs.FILE_EXT} file",
    )
    parser.add_argument(
        "filter",   # Positional argument make entry required
        type=_validate_filter,
        nargs="+",  # One or more arguments are required
        help=(
            f"Enter filters to apply to the image. Use 'all' for all filters: {list(FUNCS.keys())}"
        )
    )
    parser.add_argument(
        "-d", "--directory",
        type=str,
        help=(
            f"Enter directory path to search for {bmp_dirs.FILE_EXT} file. Default is images/ directory"
        )
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose (debu) output"
    )
    
    args = parser.parse_args(argv)
    
    if args.verbose:
        setup_logging(level=logging.DEBUG)
        logger.debug("Verbose mode enabled")
    
    # Arv(args) returns a list when 'nargs=' is used
    if args.filter[0].strip().strip(string.punctuation).lower() == ALL_FILTERS:
        # cast() tells the type checker to treat a value as a specific type.
        # At runtime, filters is still the exact same list[str] object,
        # cast() just silenced the type checker. It´s purely a hint.
        filters = cast(list[FilterName], list(FUNCS.keys())) 
    else:
        filters: list[FilterName] = args.filter
        
    try:
        # Step 1: Input file validation and read BMP file
        in_file = validate_infile(args.input_file, args.directory)
        bmp_data = read_bmp(in_file)
        
        # Step 2: Apply filter using a generator
        for new_pixels, clean_filter in process_filter(bmp_data.pixels, filters):
            
            # Step 3: Generate output file and write BMP
            out_file = validate_outfile(
                args.output_file, 
                in_file, 
                clean_filter,
            )
            
            write_bmp(
                out_file,
                bmp_data.size.width,
                new_pixels,
                bmp_data.full_header,
            )
        logger.info("=== Program Finished. Enjoy your filtered images :) ===\n")
            
    except KeyboardInterrupt:
        logger.warning("\nInterrupted by user. Exiting.")
        return ExitCode.KEYBOARD_INTERRUPT
        
    except (FileExistsError, FileNotFoundError) as e:
        logger.error(f"Error in file: {e}")
        return ExitCode.FAILURE
        
    except ValueError as e:
        logger.error(f"Error in processing: {e}")
        return ExitCode.FAILURE
    
    except Exception as e:  # Catches every other exception in program
        # Appears as logging.error, provides Python's traceback info
        logger.exception(f"Unexpected Error: {e}")
        return ExitCode.FAILURE
    
    return ExitCode.SUCCESS


if __name__ == "__main__":
    sys.exit(main()) 