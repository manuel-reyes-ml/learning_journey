"""
"""

from __future__ import annotations
from typing import Final
import argparse
import logging
import string
import sys


# =============================================================================
# Module Configuration
# =============================================================================

# Cipher Specs
KEY_LENGTH: Final[int] = 26
KEY_CHAR_UNIQUE: Final[bool] = True
DEFAULT_KEY: Final[str] = "NQXPOMAFTRHLZGECYJIUWSKDVB"

# English alphabet lowercase 'abcdefghijklmnopqrstuvwxyz'
ALPHABET : Final[str] = string.ascii_lowercase

# Exit codes (Unix standard)
EXIT_SUCCESS: int = 0
EXIT_FAILURE: int = 1
EXIT_KEYBOARD_INTERRUPT: int = 130

# Set up Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s : %(levelname)s : %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger(__name__)


# =============================================================================
# Core Functions
# =============================================================================

def validate_key(key: str, key_length: int = KEY_LENGTH, key_char_unique: bool = KEY_CHAR_UNIQUE) -> str:
    """
    """
    if not key:
        raise ValueError("Key cannot be empty")
    
    clean_key = key.strip().lower()
    
    if not clean_key.isalpha():
        raise ValueError("Key must contain only alphabetic characters")
    
    if len(clean_key) != key_length:
        raise ValueError(f"Key has {len(clean_key)} characters, {key_length} are required")
    
    if key_char_unique:
        # Set structure is an unordered collection of UNIQUE elements
        if len(set(clean_key)) < key_length:
            raise ValueError("Key must have unique characters")
    
    logger.debug("Key is valid......")
    
    return clean_key


def input_plaintext() -> str:
    """
    """
    plain_text = input("Enter plain text: ").strip().split()
    
    if not plain_text:
        raise ValueError("Text cannot be empty")
    
    clean_text = " ".join(plain_text)
    
    return clean_text


def substitution(clean_key: str, clean_text: str, alphabet: str = ALPHABET) -> str:
    """
    """
    logger.debug("Running substitution algorithm...")
    
    cipher_text_lst = []
    for char in clean_text:
        if char.isalpha():
            
            if char.isupper():
                pos = alphabet.find(char.lower())
                cipher_text_lst.append(clean_key[pos].upper())
            else:
                pos = alphabet.find(char)
                cipher_text_lst.append(clean_key[pos])
                
            continue
        
        cipher_text_lst.append(char)
    
    return "".join(cipher_text_lst)
       
        
# =============================================================================
# CLI Entry Point
# =============================================================================
      
def main(argv: list[str] | None = None) -> int:
    """
    """
    parser = argparse.ArgumentParser(
        description="Encrypt plain text using substitution algorithm"
    )
    parser.add_argument(
        "cipher_key",
        type=str,
        metavar="key",
        nargs="?",  # Zero or One argument
        default=DEFAULT_KEY,
        help= f"Enter Cipher Key. Only alphabetic and unique, 26 characters. Default: '{DEFAULT_KEY}'"
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
        clean_key = validate_key(args.cipher_key)
        clean_text = input_plaintext()
        cipher_text = substitution(clean_key, clean_text)
        logger.info(f"Cipher text: {cipher_text}")
    
    except KeyboardInterrupt:
        logger.info("\nInterrupted by user. Exiting.")
        return EXIT_KEYBOARD_INTERRUPT
    
    except ValueError as e:
        logger.error(f"Processing Error: {e}")
        return EXIT_FAILURE
    
    except Exception as e:
        logger.exception(f"Unexpected error: {e}") # logger.exception logs the traceback
        return EXIT_FAILURE

    return EXIT_SUCCESS


if __name__ == "__main__":
    sys.exit(main())