"""
Substitution Cipher - Encrypt plaintext using a monoalphabetic substitution algorithm.

A command-line tool that encrypts text by replacing each letter with a corresponding
letter from a 26-character cipher key. Non-alphabetic characters (spaces, punctuation,
numbers) are preserved in their original positions.

How Substitution Cipher Works
-----------------------------
Each letter in the plaintext is replaced by the letter at the same position
in the cipher key:

    Alphabet: abcdefghijklmnopqrstuvwxyz
    Key:      NQXPOMAFTRHLZGECYJIUWSKDVB
    
    'a' → 'N', 'b' → 'Q', 'c' → 'X', etc.

Usage
-----
    python substitution.py [KEY]
    python substitution.py --verbose NQXPOMAFTRHLZGECYJIUWSKDVB
    python substitution.py  # Uses default key

Examples
--------
    $ python substitution.py
    Enter plain text: Hello World
    14:30:45 : INFO : Cipher text: Aozze Kesip

    $ python substitution.py ZYXWVUTSRQPONMLKJIHGFEDCBA
    Enter plain text: ABC xyz
    14:31:00 : INFO : Cipher text: ZYX cba

    $ python substitution.py -v
    14:32:15 : DEBUG : Verbose mode enabled
    14:32:15 : DEBUG : Key is valid......
    Enter plain text: Test
    14:32:20 : DEBUG : Running substitution algorithm...
    14:32:20 : INFO : Cipher text: Uoiu

Notes
-----
The cipher key must be exactly 26 unique alphabetic characters representing
the substitution alphabet. Case is preserved during encryption.
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

# Exports
__all__ = [
    "validate_key",
    "get_plaintext",
    "substitution",
    "DEFAULT_KEY",
    "ALPHABET",
]

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
    Validate and normalize a substitution cipher key.

    Ensures the key contains only alphabetic characters, meets the required
    length, and optionally contains only unique characters.

    Parameters
    ----------
    key : str
        The cipher key to validate.
    key_length : int, optional
        Required length of the key. Default is 26 (full alphabet).
    key_char_unique : bool, optional
        If True, requires all characters to be unique. Default is True.

    Returns
    -------
    str
        The validated key, stripped of whitespace and lowercased.

    Raises
    ------
    ValueError
        If key is empty, contains non-alphabetic characters, has incorrect
        length, or contains duplicate characters (when uniqueness required).

    Examples
    --------
    >>> validate_key("NQXPOMAFTRHLZGECYJIUWSKDVB")
    'nqxpomaftrhlzgecyjiuwskdvb'
    >>> validate_key("  ZYXWVUTSRQPONMLKJIHGFEDCBA  ")
    'zyxwvutsrqponmlkjihgfedcba'
    >>> validate_key("ABC")
    Traceback (most recent call last):
    ...
    ValueError: Key has 3 characters, 26 are required
    >>> validate_key("AAXPOMAFTRHLZGECYJIUWSKDVB")
    Traceback (most recent call last):
    ...
    ValueError: Key must have unique characters
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


# When no input to function is expected, use a default parameter to make function testable
def get_plaintext(text: str | None = None) -> str:
    """
    Get and validate plaintext for encryption.

    Prompts the user interactively if text is not provided. Normalizes
    whitespace by collapsing multiple spaces into single spaces.

    Parameters
    ----------
    text : str or None, optional
        The plaintext to validate. If None, prompts user for input.

    Returns
    -------
    str
        The validated and whitespace-normalized plaintext.

    Raises
    ------
    ValueError
        If the text is empty or contains only whitespace.

    Examples
    --------
    >>> get_plaintext("Hello World")
    'Hello World'
    >>> get_plaintext("  Multiple   Spaces  ")
    'Multiple Spaces'
    >>> get_plaintext("")
    Traceback (most recent call last):
    ...
    ValueError: Text cannot be empty
    >>> get_plaintext("   ")
    Traceback (most recent call last):
    ...
    ValueError: Text cannot be empty
    """
    if text is None:
        text = input("Enter plain text: ")
    
    if not text:
        raise ValueError("Text cannot be empty")
    
    clean_text = " ".join(text.strip().split())
    
    return clean_text


def substitution(clean_key: str, clean_text: str, alphabet: str = ALPHABET) -> str:
    """
    Encrypt plaintext using monoalphabetic substitution cipher.

    Each letter in the plaintext is replaced by the corresponding letter
    in the cipher key. Case is preserved, and non-alphabetic characters
    remain unchanged.

    Parameters
    ----------
    clean_key : str
        The 26-character substitution key (lowercase).
    clean_text : str
        The plaintext to encrypt.
    alphabet : str, optional
        The source alphabet for mapping. Default is 'abcdefghijklmnopqrstuvwxyz'.

    Returns
    -------
    str
        The encrypted ciphertext.

    Notes
    -----
    Uses Python's built-in `str.maketrans()` and `str.translate()` for
    efficient character substitution. Two translation tables are created
    to handle both lowercase and uppercase characters.

    Examples
    --------
    >>> key = "nqxpomaftrhlzgecyjiuwskdvb"
    >>> substitution(key, "hello")
    'aozze'
    >>> substitution(key, "Hello World")
    'Aozze Kesip'
    >>> substitution(key, "ABC xyz")
    'NQX dvq'
    >>> substitution(key, "Hello, World!")
    'Aozze, Kesip!'
    >>> substitution(key, "123")
    '123'
    """
    logger.debug("Running substitution algorithm...")
    
    # OPTION 3: Pythonic way, using buil-in tools
    # str.maketrans creates a translation table (mapping) -> dictionary:
    #   - where Keys = ASCII codes of original characteres
    #   - and Values = ASCII codes of replacement characteres
    #   - Length of both strings  need to match, if not ValueError is raised
    lower_table = str.maketrans(alphabet, clean_key)
    upper_table = str.maketrans(alphabet.upper(), clean_key.upper())
    
    # translate does the work to switch the character from original text to new characters from table
    result = clean_text.translate(lower_table)
    result = result.translate(upper_table)
    
    return result
    
    
    # OPTION 2: Using inner function as generator ==================
    # Single responsability: handles one character at a time
    #def substitute_char(char: str) -> str:
    #    """
    #    """
    #    if not char.isalpha():
    #        return char
    #    
    #    pos = alphabet.find(char.lower())
    #    substituted = clean_key[pos]
    #    
    #    return substituted.upper() if char.isupper() else substituted
    
    # Generator expression is more memory-efficient than building a list
    #return "".join(substitute_char(c) for c in clean_text)
    
    # OPTION 1: Using conditionals and list ========================
    #cipher_text_lst = []
    #for char in clean_text:
    #    if char.isalpha():
            
    #        if char.isupper():
    #            pos = alphabet.find(char.lower())
    #            cipher_text_lst.append(clean_key[pos].upper())
    #        else:
    #            pos = alphabet.find(char)
    #            cipher_text_lst.append(clean_key[pos])
    #            
    #   else:
    #        cipher_text_lst.append(char)  # Non-alphabetic preserved
    
    #return "".join(cipher_text_lst)
       
        
# =============================================================================
# CLI Entry Point
# =============================================================================
      
def main(argv: list[str] | None = None) -> int:
    """
    Main entry point for the substitution cipher CLI.

    Parses command-line arguments, validates the cipher key, prompts for
    plaintext, performs encryption, and logs the result.

    Parameters
    ----------
    argv : list of str or None, optional
        Command-line arguments. If None, uses sys.argv.

    Returns
    -------
    int
        Exit code: 0 on success, 1 on validation/processing error,
        130 on keyboard interrupt.
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
        help= f"Enter Cipher Key. Only alphabetic and unique, 26 characters. Default: '{DEFAULT_KEY}'",
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",  # Store True if flag present ('-v', '--verbose')
        help="Enable verbose (debug) output",
    )
    
    args = parser.parse_args(argv)
    
    if args.verbose:
        logger.setLevel(logging.DEBUG)
        logger.debug("Verbose mode enabled")
        
    try:
        clean_key = validate_key(args.cipher_key)
        clean_text = get_plaintext()
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