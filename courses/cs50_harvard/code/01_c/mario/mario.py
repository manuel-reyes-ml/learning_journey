"""
Mario Pyramid Builder - Generate ASCII pyramids of specified height.

A command-line tool that creates double-sided pyramids using hash symbols,
inspired by the classic Super Mario Bros pyramid structures.

Usage
-----
    python mario.py [HEIGHT]
    python mario.py --verbose
    python mario.py  # Interactive mode

Examples
--------
    $ python mario.py 4
       #  #
      ##  ##
     ###  ###
    ####  ####

    $ python mario.py --verbose 3
    2025-02-05 10:30:15 : DEBUG : Verbose mode enabled
    2025-02-05 10:30:15 : INFO : Building pyramid of height: 3
      #  #
     ##  ##
    ###  ###
"""

from __future__ import annotations
import argparse
import logging
import sys

# =============================================================================
# Module Configuration
# =============================================================================

# Module level constants
MIN_HEIGHT: int = 1
MAX_HEIGHT: int = 8

# Exit codes (Unix standard)
EXIT_SUCCESS: int = 0
EXIT_ERROR: int = 1
EXIT_KEYBOARD_INTERRUP: int = 130 # Standard SIGINT exit code

# Logging configuration
logging.basicConfig(
    level=logging.INFO, # Only save messages with level INFO or higher
    format='%(asctime)s : %(levelname)s : %(message)s', # Format the log message
)
logger = logging.getLogger(__name__)


# =============================================================================
# Core Functions
# =============================================================================

def input_height_validation(height: str | None = None) -> int:
    """
     Validate and return the pyramid height from user input.

    Prompts the user interactively if height is not provided. Validates
    that the input is a positive integer within the acceptable range.

    Parameters
    ----------
    height : str or None, optional
        The height as a string to validate. If None, prompts the user
        for input interactively.

    Returns
    -------
    int
        Validated height between MIN_HEIGHT and MAX_HEIGHT inclusive.

    Raises
    ------
    ValueError
        If height cannot be converted to an integer or falls outside
        the valid range [MIN_HEIGHT, MAX_HEIGHT].

    Examples
    --------
    >>> validate_height("5")
    5
    >>> validate_height("0")
    Traceback (most recent call last):
    ...
    ValueError: Height 0 outside valid range [1-8]
    """
    if not height:
        height = input("Please enter Height: ").strip()
    
    try: 
        height_int = int(height)
    except ValueError as e: # Catches int("abc"), int("3.5")
        raise ValueError(f"'{height}' is not a valid integer") from e # To trace back to original error
    else:
        if not MIN_HEIGHT <= height_int <= MAX_HEIGHT: # Python´s chain comparison is more readable
            raise ValueError(
                f"Height {height_int} outside valid range [{MIN_HEIGHT}-{MAX_HEIGHT}]"
            )
        
        return height_int
    

def print_pyramid(height: int) -> str:
    """
    Build an ASCII pyramid string of the specified height.

    Creates a double-sided pyramid where each row contains hash symbols
    separated by two spaces, with leading spaces for right-alignment.

    Parameters
    ----------
    height : int
        The number of rows in the pyramid. Must be a positive integer.

    Returns
    -------
    str
        The complete pyramid as a multi-line string.

    Examples
    --------
    >>> print(build_pyramid(2))
     #  #
    ##  ##
    >>> print(build_pyramid(3))
      #  #
     ##  ##
    ###  ###
    """
    lines = []
    
    for row in range(height):
        spaces = " " * (height - row - 1)
        blocks = "#" * (row + 1)
        lines.append(f"{spaces}{blocks}  {blocks}")
        
    return "\n".join(lines) 
    # it is testable: 'assert build_pyramid(2) == " #  #\n##  ##"


# =============================================================================
# CLI Entry Point
# =============================================================================

def main(argv: list[str] | None = None) -> int:
    """
      Main entry point for the pyramid builder CLI.

    Parses command-line arguments, validates input, and outputs
    the generated pyramid to stdout.

    Parameters
    ----------
    argv : list of str or None, optional
        Command-line arguments. If None, uses sys.argv.

    Returns
    -------
    int
        Exit code: 0 on success, 1 on validation error,
        130 on keyboard interrupt.
    """
    parser = argparse.ArgumentParser(
        description="Build an ASCII pyramid of specified height"
    )
    parser.add_argument(
        "height",
        nargs='?',
        help=f"Enter height number between {MIN_HEIGHT} and {MAX_HEIGHT}"
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
        height = input_height_validation(args.height)
        logger.info(f"Building pyramid of height: {height}") # Log AFTER validation
    
    except KeyboardInterrupt: # Must specific first
        logger.info("Interrupted by User. Exiting")
        return EXIT_KEYBOARD_INTERRUP
    
    except ValueError as e:
        logger.error(f"Height validation failed: {e}") # Combines WHERE + WHAT
        return EXIT_ERROR
    
    except Exception as e: # General catch-all last
        logger.exception(f"Unexpected error: {e}") # logger.exception logs the traceback
        return EXIT_ERROR
    
    else:
        print(print_pyramid(height))
        return EXIT_SUCCESS
    
if __name__ == "__main__":
    sys.exit(main())