"""
"""

from __future__ import annotations
from typing import Final, Iterator
import itertools
import argparse
import logging
import string
import sys
import re


# =============================================================================
# Module Configuration
# =============================================================================

__all__ = [
    "calculate_variables",
    "coleman_liau",
    "RATE",
    "CLI_COEF_L",
    "CLI_COEF_S",
    "CLI_INTERCEPT",
    "PATTERN_SENTENCE",
    "DEFAULT_TEXT",
]

# Coleman-Liau index (Readability test) coefficients
RATE: Final[int] = 100
CLI_COEF_L: Final[float] = 0.0588
CLI_COEF_S: Final[float] = 0.296
CLI_INTERCEPT: Final[float] = 15.8
ROUND_DIGITS: Final[int] = 2

# Grade boundaries
GRADE_MIN: Final[int] = 1
GRADE_MAX: Final[int] = 16

# REGEX Pattern to match
PATTERN_SENTENCE = re.compile(r'[^.!?]+[.!?]')

DEFAULT_TEXT: Final[str] = """
Congratulations! Today is your day. You're off to Great Places! You're off and away!
"""

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

def _validate_sentences(full_text: str, pattern: re.Pattern[str] = PATTERN_SENTENCE) -> Iterator[str]:
    """
    """ 
    for match in pattern.finditer(full_text): 
        yield str(match.group()).strip()


def _count_strings(sentences: Iterator[str]) -> tuple[int, int, int]:
    """
    """
    sentence_count: int = 0
    word_count: int = 0
    letter_count: int = 0
        
    for sentence in sentences:
        sentence_count += 1
        for word in sentence.split():
            # Strip punctuation from word edges
            # string.puntuaction = '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'
            clean_word = word.strip(string.punctuation)
            
            if clean_word:
                word_count += 1
                letter_count += sum(1 for char in clean_word if char.isalpha())
    
    if word_count == 0:
        raise ValueError("Text contains numeric characters (numbers)")
    
    return sentence_count, word_count, letter_count


def calculate_variables(full_text: str, rate: int = RATE) -> tuple[float, float]:
    """
    """
    logger.debug("Validating text......")
    
    if not full_text:
        raise ValueError("Text is empty")
    
    sentences = _validate_sentences(full_text)
    
    try:
        first = next(sentences)
        sentence_iter = itertools.chain([first], sentences)
        sentence_count, word_count, letter_count = _count_strings(sentence_iter)
    
    except StopIteration:
        raise ValueError("Puntuaction missing. No sentence found")
    
    except (ValueError, ZeroDivisionError) as e:
        raise ValueError(f"Processing Error: {e}") from e
    
    ## PEP 8 discourages single uppercase letters. Use descriptive names
    # Average number of letters per 100 words in the text
    letters_avg: float = (letter_count / word_count) * rate  
    # average number of sentences per 100 words in the text
    sentences_avg: float = (sentence_count / word_count) * rate
    
    logger.debug(f"Sentences: {sentence_count}, Words: {word_count}, Letters: {letter_count}")
    
    return letters_avg, sentences_avg    
            
            
def coleman_liau(
    letters_avg: float,
    sentences_avg: float,
    cli_coef_l: float = CLI_COEF_L,
    cli_coef_s: float = CLI_COEF_S,
    cli_intercept: float = CLI_INTERCEPT,
    grade_min: int = GRADE_MIN,
    grade_max: int = GRADE_MAX,
    round_digits: int = ROUND_DIGITS
) -> str:
    """
    """
    logger.debug("Calculating grade......")
    
    index = (cli_coef_l * letters_avg) - (cli_coef_s * sentences_avg) - cli_intercept
    
    if index < grade_min:
        grade = f"Before Grade {grade_min}"
    elif index > grade_max:
        grade = f"Grade {grade_max}+"
    else:
        grade = f"Grade {round(index)}"
    
    logger.debug(f"Coleman-Liau index is: {round(index, round_digits)}")
    
    return grade
    

# =============================================================================
# CLI Entry Point
# =============================================================================

def main(argv: list[str] | None = None) -> int:
    """
    """
    parser = argparse.ArgumentParser(
        description="Calculate readability level based on Coleman-Liau index"
    )
    parser.add_argument(
        "text",  # Positional argument requires at least 1 argument
        type=str,
        nargs = "*",  # zero or more arguments (words), if zero goes to default
        default=None, # If DEFAULT_TEXT used here, it will be joined as characters by .join()
        help="Enter text with no numeric characters, use alphabetic characteres"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true"  # Store True if flag present ('-v', '--verbose')
    )
    
    args = parser.parse_args(argv)
    
    if args.verbose:
        logger.setLevel(logging.DEBUG)
        logger.debug("Verbose mode enabled")
    
    # Use default=None as a flag to assign text in correct way
    if args.text:
        full_text = " ".join(args.text)
    else:
        full_text = DEFAULT_TEXT
        
    try:
        letters_avg, sentences_avg = calculate_variables(full_text)
        grade = coleman_liau(letters_avg, sentences_avg)
        logger.info(grade)
    
    except KeyboardInterrupt:
        logger.info("\nInterrupted by user. Exiting.")
        return EXIT_KEYBOARD_INTERRUPT
    
    except ValueError as e:
        logger.error(f"Error: {e}")  # Combines WHERE + WHAT
        return EXIT_FAILURE
    
    except Exception as e:
        logger.exception(f"Unexpected error: {e}")  # logger.exception logs the traceback
        return EXIT_FAILURE
    
    return EXIT_SUCCESS


if __name__ == "__main__":
    sys.exit(main())
    