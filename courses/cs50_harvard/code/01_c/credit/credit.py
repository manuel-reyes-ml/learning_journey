"""
"""
from __future__ import annotations
from typing import TypedDict  # Pro way to handle dictionaries that have predictable structure
import logging

import argparse
import sys

AMEX_LENGTH: int = 15
MASTERCARD_LENGTH: int = 16
VISA_LENGTH_SHORT: int = 13
VISA_LENGTH_LONG: int = 16 

AMEX_START_1: int = 34
AMEX_START_2: int = 37
MASTERCARD_START_MIN: int = 51
MASTERCARD_START_MAX: int = 55
VISA_START: int = 4 

EXIT_SUCCESS: int = 0
EXIT_KEYBOARD_INTERRUPT: int = 1
EXIT_ERROR: int = 1

# Define the structure for the inner dictionary
class CardSpecs(TypedDict):
    Length: list[int]
    Start: list[int]

# Type Hint: Keys are strings, Values are CardSpecs objects
# If you try to add a key like "Color": "Blue", the IDE will not let you
cards_specs: dict[str, CardSpecs] = {
        "AMEX": {
            "Length": [AMEX_LENGTH],
            "Start": [AMEX_START_1, AMEX_START_2]
        }, 
        "MASTERCAD": {
            "Length": [MASTERCARD_LENGTH], 
            "Start": list(range(MASTERCARD_START_MIN, MASTERCARD_START_MAX)) # TODO, test in VS code
        },
        "VISA": {
            "Length": [VISA_LENGTH_LONG, VISA_LENGTH_SHORT], 
            "Start": [VISA_START]
        },
}

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s : %(levelname)s : %(message)s',
)
logger = logging.getLogger(__name__)


def number_validation(str_number: str) -> str:
    """
    """
    # Reverse string of digits and re convert to int
    reversed_numbers = list(map(int, str_number[::-1]))
   
    sum = 0
    for i, number in enumerate(reversed_numbers, 1):
        # Only apply t0 every other number in the list
        if i % 2 == 0:
            product = number * 2
            sum += int(product / 10) + (product % 10)
        else:
            sum += number
    
    if sum % 10 != 0:
        raise ValueError(f"INVALID credit card number '{str_number}'")
        
    logger.debug(f"Analyzing credit card number '{str_number}...")
    return str_number
    

def card_type(str_number: str, card_specs: dict[str, CardSpecs]) -> str:
    """
    """
    found_card = False
    
    for name, specs in cards_specs.items():
        # 1. First, check if the card start with the right digits
        # We convert the start numbers to strings to compare easily
        start_digits = [str(digits) for digits in specs["Start"]]
        
        if any(str_number.startswith(prefix) for prefix in start_digits):
            logger.debug("Card type found...")
            found_card = True
        
            if len(str_number) not in specs["Length"]:
                raise ValueError(f"Invalid length for {name}. Expected {specs["Length"]}")
            
            logger.debug("Card length matches...")
            return name
    
    if not found_card:
        raise ValueError("Unknown card type.")


def main(argv: list[str] | None = None) -> int:
    """
    """
    parser = argparse.ArgumentParser(
        description="Validate real credit card number"
    )
    parser.add_argument(
        "card_number",
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
    
    str_numbers: list[str] = list(args.card_number)
    
    for digits in str_numbers:
        str_number = digits.strip()
        
        try:
            number_validation(str_number)
            merchant_name = card_type(str_number, cards_specs)
        
        except KeyboardInterrupt:
            logger.info("Interrupted by User. Exiting")
            return EXIT_KEYBOARD_INTERRUPT
        
        except ValueError as e:
            logger.error(f"Error validating card number: {e}")
            return EXIT_ERROR
        
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return EXIT_ERROR
        
        else:
            logger.info(f"Valid {merchant_name} detected!")
            return EXIT_SUCCESS

if __name__ == "__main__":
    sys.exit(main())