"""
"""

from __future__ import annotations
from typing import Final, Iterator
import itertools
import argparse
import logging
import sys
import re


# =============================================================================
# Module Configuration
# =============================================================================

# Coleman-Liau index (Readability test)
RATE: Final[int] = 100

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

def _validate_setences(full_text: str, pattern: re.Pattern[str] = PATTERN_SENTENCE) -> Iterator[str]:
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
        for word in sentence.strip().split():
            if word.isalpha():
                word_count += 1
                for char in word.strip():
                    if char.isalpha():
                        letter_count += 1
    
    if word_count == 0:
        raise ValueError("Text contains numeric characters (numbers)")
    
    return sentence_count, word_count, letter_count


def calculate_variables(full_text: str, rate: int = RATE) -> tuple[float, float]:
    """
    """
    logger.debug("Validating text......")
    
    if not full_text:
        raise ValueError("Text is empty")
    
    sentences = _validate_setences(full_text)
    
    try:
        first = next(sentences)
        sentence_iter = itertools.chain([first], sentences)
        sentence_count, word_count, letter_count = _count_strings(sentence_iter)
    
    except StopIteration:
        raise ValueError("Puntuaction missing. No sentence found")
    
    except (ValueError, ZeroDivisionError) as e:
        raise ValueError (f"Processing Error: {e}") from e
    
    # Average number of letters per 100 words in the text
    L: float = (letter_count / word_count) * rate  
    # average number of sentences per 100 words in the text
    S: float = (sentence_count / word_count) * rate
    
    logger.debug(f"Sentences: {sentence_count}, Words: {word_count}, Letters: {letter_count}")
    
    return L, S    
            
            
def coleman_liau(L: float, S: float) -> str:
    """
    """
    logger.debug("Calculating grade......")
    
    index = (0.0588 * L) - (0.296 * S) - 15.8
    
    if index < 1:
        grade = "Before Grade 1"
    elif index > 16:
        grade = "Grade 16+"
    else:
        grade = f"Grade {round(index)}"
    
    logger.debug(f"Coleman-Liau index is: {round(index, 2)}")
    
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
        default=DEFAULT_TEXT,
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
    
    full_text = " ".join(args.text)
    
    try:
        L, S = calculate_variables(full_text)
        grade = coleman_liau(L, S)
        logger.info(grade)
    
    except KeyboardInterrupt:
        logger.info("\nInterrupted by user. Exiting.")
        return EXIT_KEYBOARD_INTERRUPT
    
    except ValueError as e:
        logger.error(f"Error: {e}")  # Combines WHERE + WHAT
        return EXIT_FAILURE
    
    except Exception as e:
        logger.exception(f"Unexpected error: {e}")  # logger.exception logs the traceback
    
    return EXIT_SUCCESS

if __name__ == "__main__":
    sys.exit(main())
    