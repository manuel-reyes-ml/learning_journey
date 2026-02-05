"""
Mario Script - Use Height value from user to build a pyramid.

Usage:
    python mario.py [HEIGHT]
    python mario.py --verbose
"""

from __future__ import annotations
from typing import Optional

import argparse
import logging
import sys

# Set up logging
logging.basicConfig(
    level=logging.INFO, # Only save messages with level INFO or higher
    format='%(asctime)s : %(levelname)s : %(message)s', # Format the log message
)
logger = logging.getLogger(__name__)

def input_height_validation(height: Optional[str] = None) -> int:
    """
    Get the height of the pyramid from the user.
    
    Args:
        height (str): The height of the pyramid.
    Returns:
        The height (int) of the pyramid.
    Raises:
        ValueError: If the input is not a number or is not between 1 and 8.
    """
    if not height:
        height = input("Please enter Height: ").strip()
    
    try: 
        height = int(height)
    except TypeError as e:
        raise f"Invalid input '{height}': {e}"
    else:
        if height < 1 or height > 8:
            raise ValueError(f"Invalid input '{height}': Height must be between 1 and 8")
        return height
    

def print_pyramid(height: int) -> None:
    """
    Print the pyramid of hashes based on the height.
    
    Args:
        height (int): The height of the pyramid.
    Returns:
        None
    Raises:
        None
    """
    for i in range(height):
        
        for j in range(height - i - 1):
            print(" ", end="")
        
        for k in range(i + 1):
            print("#", end="")
        
        print("  ", end="")
        
        for l in range(i + 1):
            print("#", end="")
            
        print("\n", end="")


def main(argv: list[str] | None = None) -> int:
    """
    Main entry point for the build pyramid script.
    
    Args:
        argv (list[str] | None, optional): Command line arguments. Defaults to None.
    Returns:
        int: Return code (0 on success, 1 on failure, 130 on keyboard interrupt).
    Raises:
        TypeError: If trying to cover str to int.
        ValueError: If digit is not between 1 and 8.
    """
    parser = argparse.ArgumentParser(
        description="Get block height from user and build pyramid"
    )
    parser.add_argument(
        "height",
        nargs='?',
        help="Enter height number between 1 and 8"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose (debug) output"
    )
    
    args = parser.parse_args(argv)
    
    if args.verbose:
        logger.setLevel(logging.DEBUG)
    
    logger.info(f"Building pyramid of height: {args.height}")
    
    try:
        height = input_height_validation(args.height)
    except TypeError as e:
        logger.error(f"Invalid input. {args.height} is not a numerical value: {e}")
        return 1
    except ValueError as e:
        logger.error(f"Invalid input '{args.height}'. Value must be between 1 and 8: {e}")
        return 1
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return 1
    except KeyboardInterrupt:
        logger.info("Interrupted by User. Exiting")
        return 130
    else:
        print_pyramid(height)
        return 0
    
if __name__ == "__main__":
    sys.exit(main())