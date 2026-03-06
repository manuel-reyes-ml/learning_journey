"""
CLI entry point and orchestration for BMP image filtering.

Provides argument parsing, file validation, and filter
orchestration for the BMP filter pipeline. Coordinates the
read → filter → write workflow through ``main()``, which
serves as both the CLI entry point and the package's public
API via ``py_src.main()``.

Examples
--------
Command-line usage::

    $ python -m py_src blur -i image.bmp
    $ python -m py_src grayscale edges -i photo.bmp -v
    $ python -m py_src all -i image.bmp -d ~/pictures/
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
    from .bmp_io import read_bmp, write_bmp
    from .bmp_logger import setup_logging
    from .bmp_config import (
        FilterName,
        DictFuncs,
        ImageData,
        ExitCode,
        ALL_FILTERS,
        CUR_DIR,
        bmp_dirs,
    )
    from .bmp_filters import FILTERS
    
except ImportError as e:
    sys.exit(f"Error: Cannot find relative modules.\nDetails: {e}")


# =============================================================================
# MODULE CONFIGURATION
# =============================================================================

# =====================================================
# Exports
# =====================================================

__all__ = [
    "validate_infile",
    "validate_outfile",
    "process_filter",
]


# =====================================================
# Module Level Constants & Variables
# =====================================================

# Path.name gives the full name of a file or directory
MODULE_NAME: Final[str] = f"{CUR_DIR.name}.bmp_main"
funcs_available: str = ", ".join(FILTERS.keys())


# =====================================================
# Logging Set Up
# =====================================================

setup_logging()  # Uses logging.INFO by default!

# When running this module Python assigns string '__main__' to '__name__',
# so we need to assign the module name directly so this logger is assigned
# to the 'py_src' logger hierarchy we created in bmp_logger.py.
logger = logging.getLogger(MODULE_NAME)


# =============================================================================
# INTERNAL HELPER FUNCTIONS
# =============================================================================

def _get_filter_help(funcs_data: DictFuncs = FILTERS) -> str:
    """
    """
    lines: list[str] = ["\nAvailable Filters:\n"]
    
    for _, info in funcs_data.items():
        lines.append(f"     {info.name:<12} {info.description}")
    
    return "\n".join(lines) + "\n"
        

def _validate_filter(
    filter_name: str | None = None,
    funcs: DictFuncs = FILTERS,
    all_filters: str = ALL_FILTERS,
    funcs_available: str = funcs_available,
) -> str:
    """
    Validate and normalize a single filter name string.

    Strips whitespace and punctuation, converts to lowercase,
    then verifies the filter exists in the dispatch table or
    is the special ``"all"`` keyword.

    Parameters
    ----------
    filter_name : str or None, optional
        Raw filter name from user input. Cannot be None or empty.
    funcs : DictDispatch, optional
        Filter dispatch table to validate against (default ``FUNCS``).
    all_filters : str, optional
        Special keyword that selects all filters (default ``"all"``).

    Returns
    -------
    str
        Cleaned, lowercase filter name.

    Raises
    ------
    argparse.ArgumentTypeError
        If ``filter_name`` is empty, non-alphabetic, or not a
        recognized filter name.
    """
    if not filter_name:
        raise argparse.ArgumentTypeError("Filter cannot be empty")
    
    clean_filter = filter_name.strip().strip(string.punctuation).lower()
    
    if not clean_filter.isalpha():
        raise argparse.ArgumentTypeError("Filter must be alphabetic")
    
    if clean_filter != all_filters:
        if not clean_filter in funcs:
            raise argparse.ArgumentTypeError("'{clean_filter}' is not part "
                                             f"of current filters: {funcs_available}")
        
    return clean_filter


def _validate_filters(filters: list[FilterName] | None = None) -> Iterator[str]:
    """
    Validate a list of filter names and yield each cleaned name.

    Checks for duplicates in the filter list, then yields each
    filter name through ``_validate_filter()`` for individual
    validation.

    Parameters
    ----------
    filters : list of FilterName or None, optional
        List of filter name strings to validate. Cannot be
        None or empty.

    Yields
    ------
    str
        Each validated and cleaned filter name.

    Raises
    ------
    ValueError
        If ``filters`` is None, empty, or contains duplicates.
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
    Locate and validate an input BMP file.

    Resolves the file path from the given filename and optional
    directory, then verifies the file exists and has the correct
    BMP extension. Offers to correct mismatched extensions
    interactively.

    Parameters
    ----------
    fname : str or None, optional
        Name of the input BMP file. Cannot be None or empty.
    input_dir : str or None, optional
        Directory to search for the file. If None, searches the
        current working directory first, then the default images
        directory.
    file_ext : str, optional
        Expected file extension (default ``".bmp"``).
    image_dir : Path, optional
        Fallback directory for BMP images (default ``images/``).

    Returns
    -------
    Path
        Resolved, validated path to the input BMP file.

    Raises
    ------
    ValueError
        If ``fname`` is None or empty.
    FileNotFoundError
        If the file does not exist at the resolved path.
    FileExistsError
        If the file exists but has an invalid extension.
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
            consent = input("Would you like me to correct extension to "
                                 f" {in_file.name} (yes/no): ").strip().lower()
            
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
    Build and validate an output file path for a filtered image.

    Constructs the output filename from the input file stem and
    filter name if no explicit filename is provided. Ensures the
    output directory exists and the file has the correct extension.

    Parameters
    ----------
    fname : str or None, optional
        Explicit output filename. If None, auto-generates from
        ``in_file`` stem and ``filter_name``.
    in_file : Path or None, optional
        Path to the input file, used for auto-generating the
        output filename. Required if ``fname`` is None.
    filter_name : str or None, optional
        Name of the applied filter, appended to the output
        filename. Required if ``fname`` is None.
    out_dir : Path, optional
        Directory for output files (default ``filtered_imgs/``).
    file_ext : str, optional
        Required file extension (default ``".bmp"``).

    Returns
    -------
    Path
        Validated output file path with correct extension.

    Raises
    ------
    ValueError
        If ``fname`` is None and either ``in_file`` or
        ``filter_name`` is also None.

    Examples
    --------
    >>> validate_outfile(in_file=Path("tower.bmp"), filter_name="blur")
    PosixPath('.../filtered_imgs/tower_blur.bmp')
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
    funcs_data: DictFuncs = FILTERS,
) -> Iterator[tuple[ImageData, str]]:
    """
    Apply one or more filters to an image via dictionary dispatch.

    Validates the filter list, then lazily applies each filter
    function from the dispatch table to the pixel data. Yields
    results one at a time to support streaming write operations.

    Parameters
    ----------
    pixels : ImageData or None, optional
        2D grid of ``Pixel`` objects to filter. Cannot be None
        or empty.
    filters : list of FilterName or None, optional
        Filter names to apply sequentially. Cannot be None or
        empty.
    funcs : DictDispatch, optional
        Filter dispatch table mapping names to functions
        (default ``FUNCS``).

    Yields
    ------
    tuple of (ImageData, str)
        Each yield produces the filtered pixel grid and the
        name of the filter that was applied.

    Raises
    ------
    ValueError
        If ``pixels`` is None or empty, ``filters`` is None or
        empty, or a filter name fails validation.

    Notes
    -----
    Each filter is applied independently to the original pixel
    data, not chained. This means applying ``["blur", "edges"]``
    produces two separate outputs, not a blurred-then-edged image.
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
            logger.warning(f"Applying {clean_filter} filter....")
            # funcs_data[clean_filter].func(pixels):  Dictionary dispatch!, 
            # need to unpack the FilterInfo class.
            # Applies filter function following clean_filter("blur", "reflect", etc.)
            yield funcs_data[clean_filter].func(pixels), clean_filter
        
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
    Parse CLI arguments and run the BMP filter pipeline.

    Orchestrates the complete read → filter → write workflow:
    validates input/output paths, reads the BMP file, applies
    each requested filter, and writes the results.

    Parameters
    ----------
    argv : list of str or None, optional
        Command-line arguments to parse. If None, reads from
        ``sys.argv`` (standard CLI behavior). Pass a list for
        programmatic or test invocation.

    Returns
    -------
    ExitCode
        ``SUCCESS`` (0) on normal completion, ``FAILURE`` (1)
        on any handled error, or ``KEYBOARD_INTERRUPT`` (130)
        if terminated by Ctrl+C.

    Examples
    --------
    CLI usage::

        $ python -m py_src blur -i image.bmp
        $ python -m py_src all -i image.bmp -v

    Programmatic usage::

        >>> from py_src.bmp_main import main
        >>> exit_code = main(["blur", "-i", "image.bmp"])
    """
    parser = argparse.ArgumentParser(
        description="Apply one, some or all filters to an image."
                    f"Options: {funcs_available}"
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
        nargs="*",  # Zero or more arguments
        help="Enter filters to apply to the image. "
             f"Use 'all' for all filters: {funcs_available}",
    )
    parser.add_argument(
        "-d", "--directory",
        type=str,
        help=f"Enter directory path to search for {bmp_dirs.FILE_EXT} file. "
              "Default is images/ directory",
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose (debu) output",
    )
    parser.add_argument(
        "--no-log-file",
        action="store_true",
        help="Disable file logging (console only)",
    )
    parser.add_argument(
        "--filter-help",
        action="store_true",
        help="Show all available filters with descriptions",
    )
    
    args = parser.parse_args(argv)
    
    if args.filter_help:
        print(_get_filter_help())
        return ExitCode.SUCCESS
    
    if not args.filter:
        parser.error("At least one filter is required (or use --filter-help)")
    
    setup_logging(
        console_verbose=args.verbose,
        log_to_file=not args.no_log_file,
    )
    
    if args.verbose:
        logger.debug("Verbose mode enabled (console debug output)")
    
    # Arv(args) returns a list when 'nargs=' is used
    if args.filter[0].strip().strip(string.punctuation).lower() == ALL_FILTERS:
        # cast() tells the type checker to treat a value as a specific type.
        # At runtime, filters is still the exact same list[str] object,
        # cast() just silenced the type checker. It´s purely a hint.
        filters = cast(list[FilterName], list(FILTERS.keys())) 
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

# Run using 'python py_src', since a __main__.py file is implemented as start point