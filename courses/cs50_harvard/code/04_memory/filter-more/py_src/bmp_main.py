"""
"""

from __future__ import annotations
from typing import Callable, Iterator
from pathlib import Path
import argparse
import logging
import string
import sys

from bmp_config import (
    ColoredFormatter, 
    FUNCS,
    DIRS,
)
from bmp_io import read_bmp, write_bmp
from bmp_filters import (
    grayscale,
    reflect,
    blur,
    edges,
)


# =============================================================================
# Module Configuration
# =============================================================================

# Exports


# Program Constants
# parents=True: create any missing parent directories
# exist_ok=True: no error if directory already exists
DIRS.OUT_DIR.mkdir(parents=True, exist_ok=True)

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

def _validate_filter(filter: str | None = None, funcs: dict[str, Callable] = FUNCS) -> str:
    """
    """
    if not filter:
        raise argparse.ArgumentTypeError("Filter cannot be empty")
    
    filter = filter.strip()
    clean_filter = filter.strip(string.punctuation).lower()
    
    if not clean_filter.isalpha():
        raise argparse.ArgumentTypeError("Filter must be alphabetic")
    
    if not clean_filter in funcs:
        raise argparse.ArgumentTypeError(
            f"{filter} is not part or current functions: {funcs.keys()}"
        )
    
    return clean_filter


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
    out_dir: Path = DIRS.OUT_DIR,
    file_ext: str = DIRS.FILE_EXT,
    default_name: str = DIRS.OUT_FNAME,
) -> Path:
    """
    """
    if not fname:
        if not in_file:
            raise ValueError("File name cannot be empty")
        
        fname = f"{in_file.stem}{default_name}"
        
    out_file = out_dir / fname
    
    if out_file.suffix != file_ext:
        out_file = out_file.with_suffix(file_ext)
    
    logger.debug(f"Saving output file in directory '{out_file}'")
    return out_file


def process_filter(
    pixels: list | None = None,
    filters: list[str] | None = None,
    funcs: dict[str, Callable] = FUNCS,
) -> Iterator[list]:
    """
    """
    if not filters:
        raise ValueError("Filter(s) list cannot be emtpy")
    
    if not pixels:
        raise ValueError("Pixels cannot be empty")
    
    try:
        clean_filters = [
            _validate_filter(filter) 
            for filter in filters
        ]
        
        for filter in clean_filters:
            new_pixels = funcs[filter](pixels)  # Dictionary dispatch!
            yield new_pixels
        
    except (
        argparse.ArgumentTypeError,
        ValueError,
    ) as e:
        raise ValueError(f"Validation Error: {e}") from e
    
    
    
    