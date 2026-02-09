"""
Credit Card Validator
=====================

A command-line utility to validate credit card numbers using the Luhn algorithm
and identify the card provider (Visa, MasterCard, Amex) based on IIN prefixes.

Usage
-----
Run the script directly from the command line:

    $ python validator.py 4123456789123456
    $ python validator.py -v 340000000000000 5100000000000000
"""
from __future__ import annotations
import argparse
import logging
import sys
from typing import TypedDict, Final  # TypeDict is Pro way to handle dictionaries that have predictable structure

# =============================================================================
# Module Configuration
# =============================================================================

# Using Final prevents accidental reassignment
# Signals a type checker (MyPy) Value Constraint: always same value(s) and Type Constraint: always same type (int, str, etc.)
AMEX_LENGTH: Final[int] = 15
MASTERCARD_LENGTH: Final[int] = 16
VISA_LENGTH_SHORT: Final[int] = 13
VISA_LENGTH_LONG: Final[int] = 16 

# Ranges and Start Digits
#  In Python type hinting, tuples are treated differently that lists:
#   Lists(list[str]): Lists are assumed to be variable length by default.
#   Tuples: are usually used for fixed-size structures(like coordinates '(x, y)'), so Python
#   expects you to define every single slot.
#   tuple[str] -> a tuple with exactly 1 string ("A",)
#   tuple[str, str] -> a tuple with exactly 2 strings ("A", "B")
#   tuple[str, ...] -> a tuple with any number of strings (), ("A",), ("A", "B", "C")
AMEX_STARTS: Final[tuple[str, ...]] = ("34", "37")  # 
MASTERCARD_RANGE: Final[range] = range(51, 56)  # 51 to 55 inclusive
VISA_START: Final[str] = "4" 

# Pre-converting ranges to string tuples for O(1) lookups in startswith
MASTERCAD_PREFIXES = tuple(str(x) for x in MASTERCARD_RANGE)

# Exit Codes
EXIT_SUCCESS: int = 0
EXIT_KEYBOARD_INTERRUPT: int = 130
EXIT_FAILURE: int = 1

# Define the structure for the inner dictionary
class CardSpecs(TypedDict):
    """
    Defines the structural requirements for a credit card provider.

    Attributes
    ----------
    Length : list[int]
        A list of valid lengths for the card number.
    Start : tuple[str, ...]
        A tuple of valid starting digit sequences (prefixes).
    """
    Length: list[int]
    Start: tuple[str, ...]  # Optimized, startswith accepts tuples natively

# Type Hint: Keys are strings, Values are CardSpecs objects
# If you try to add a key like "Color": "Blue", the IDE will not let you
CARD_SPECS: dict[str, CardSpecs] = {
        "AMEX": {
            "Length": [AMEX_LENGTH],
            "Start": AMEX_STARTS
        }, 
        "MASTERCAD": {
            "Length": [MASTERCARD_LENGTH], 
            "Start": MASTERCAD_PREFIXES # TODO, test in VS code
        },
        "VISA": {
            "Length": [VISA_LENGTH_LONG, VISA_LENGTH_SHORT], 
            "Start": (VISA_START,) # Single item tuple
        },
}

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s : %(levelname)s : %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger(__name__)


# =============================================================================
# Core Functions
# =============================================================================

def validate_luhn(card_number: str) -> bool:
    """
    Validates a credit card number using the Luhn checksum algorithm.

    The Luhn algorithm (or Modulo 10) validates identification numbers by
    creating a checksum digit. It detects accidental errors like typos.

    Parameters
    ----------
    card_number : str
        The credit card number as a string of digits.

    Returns
    -------
    bool
        True if the checksum is valid (modulo 10 is 0), False otherwise.

    Examples
    --------
    >>> validate_luhn("49927398716")
    True
    >>> validate_luhn("49927398717")
    False
    """
    # 1. Reverse string of digits and convert to integers 
    # digits = list(map(int, card_number[::-1]))  # map applies function to each item in iterable
    digits = [int(d) for d in card_number[::-1]]  # Using list comprehension for faster approach
   
    checksum = 0
    
    # 2. Iterate: Double every second digit (index, 1, 3, 5...)
    for i, digit in enumerate(digits):
        # Only apply t0 every other number in the list
        if i % 2 == 1:
            doubled = digit * 2
            # Optimization: Subtracting 9 is faster/equivalent to adding digits for numbers < 19
            if doubled > 9:
                doubled -= 9
            checksum += doubled
        else:
            checksum += digit
    
    return checksum % 10 == 0


def identify_card_provider(card_number: str, specs: dict[str, CardSpecs]) -> str:
    """
    Identifies the card issuer based on IIN prefixes and validates length.

    Parameters
    ----------
    card_number : str
        The valid credit card number to identify.
    specs : dict[str, CardSpecs]
        A dictionary containing provider specifications (prefixes and lengths).

    Returns
    -------
    str
        The name of the card provider (e.g., "VISA", "AMEX").

    Raises
    ------
    ValueError
        If the card number does not match any known provider prefix or
        if the length is invalid for the matched provider.

    Examples
    --------
    >>> specs = CARDS_SPECS
    >>> identify_card_provider("4123456789123", specs)
    'VISA'
    """
    for name, data in specs.items():
        # Optimization: startswith accepts a tuple of strings directly
        if card_number.startswith(data["Start"]):
            logger.debug(f"Prefix match found for {name}")
        
            if len(card_number) not in data["Length"]:
                msg = f"Invalid length for {name}. Expected {data['Length']}, got {len(card_number)}"
                raise ValueError(msg)
            
            return name
    
    raise ValueError("Unknown card provider (Prefix mismatch)")


def process_card(card_number: str) -> None:
    """
    Orchestrates the validation pipeline for a single card number.

    This function cleans the input, runs the Luhn check, identifies the
    provider, and logs the final result.

    Parameters
    ----------
    card_number : str
        The raw input string (can contain whitespace).

    Returns
    -------
    None
        This function does not return a value; it logs results to stdout/stderr.
    """
    clean_number = card_number.strip()
    
    if not clean_number.isdigit():
        logger.error(f"'{clean_number}' contains non-numeric characters.")
        return
    
    logger.debug(f"Analyzing card: {clean_number}")
    
    try:
        # Step 1: Luhn Check
        if not validate_luhn(clean_number):
            logger.error(f"INVALID Checksum (Luhn) for '{clean_number}'")
            return
        
        # Step 2: Provider Identification
        provider = identify_card_provider(clean_number, CARD_SPECS)
        logger.info(f"VALID {provider} detected: {clean_number}")
    
    except ValueError as e:
        logger.error(f"Validation Error for '{clean_number}': {e}")
        

# =============================================================================
# CLI Entry Point
# =============================================================================

def main(argv: list[str] | None = None) -> int:
    """
    The main entry point for the command-line interface.

    Parameters
    ----------
    argv : list[str] | None, optional
        A list of command-line arguments. Defaults to sys.argv[1:].

    Returns
    -------
    int
        Exit status code. 0 for success, 1 for failure and 130 for interruption.
    """
    parser = argparse.ArgumentParser(
        description="Validate real credit card number"
    )
    parser.add_argument(
        "card_numbers",
        metavar="N",  # Use when variable name is long "card_number" -> Now the positional name is "N" in --help/-h
        type=str,
        nargs="+",  # One or more arguments
        help="Enter credit card number(s). If many, separated by space"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",  # Store True if Flag present ('-v', '--verbose'), False if not entered
        help="Enable verbose (debug) output"
    )
    
    args = parser.parse_args(argv)
    
    if args.verbose:
        logger.setLevel(logging.DEBUG)
        logger.debug("Verbose mode enabled")
    
    # Wrap main execution to catch interruptions gracefully
    try:
        for number in args.card_numbers:
            process_card(number)
    
    except KeyboardInterrupt:
        logger.info("\nInterrupted by User. Exiting.")
        return EXIT_KEYBOARD_INTERRUPT
    
    except Exception as e:
        logger.exception(f"Unexpected crash: {e}") # Defaults to 'ERROR' level, but it always include traceback
        return EXIT_FAILURE
    
    return EXIT_SUCCESS

if __name__ == "__main__":
    sys.exit(main())