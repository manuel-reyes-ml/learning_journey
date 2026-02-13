"""
Readability Calculator - Determine text readability using the Coleman-Liau index.

A command-line tool that analyzes text complexity by counting sentences, words,
and letters, then calculates a grade level using the Coleman-Liau readability
formula. Useful for educators, writers, and content creators.

The Coleman-Liau Index Formula
------------------------------
    CLI = (0.0588 * L) - (0.296 * S) - 15.8

    Where:
        L = average number of letters per 100 words
        S = average number of sentences per 100 words

Usage
-----
    python readability.py "Your text here. Multiple sentences work!"
    python readability.py --verbose "Text to analyze."
    python readability.py  # Uses default sample text

Examples
--------
    $ python readability.py "Hello world. Simple text."
    14:30:45 : INFO : Grade 2

    $ python readability.py "The quick brown fox jumps. Over the lazy dog."
    14:31:00 : INFO : Grade 3

    $ python readability.py -v "Congratulations! Today is your day."
    14:32:15 : DEBUG : Verbose mode enabled
    14:32:15 : DEBUG : Validating text......
    14:32:15 : DEBUG : Sentences: 2, Words: 5, Letters: 29
    14:32:15 : DEBUG : Calculating grade......
    14:32:15 : DEBUG : Coleman-Liau index is: 2.45
    14:32:15 : INFO : Grade 2

    $ python readability.py  # No arguments, uses default text
    14:33:00 : INFO : Grade 3

References
----------
.. [1] Coleman, M., & Liau, T. L. (1975). A computer readability formula
       designed for machine scoring. Journal of Applied Psychology, 60(2), 283.
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
    Extract sentences from text using regex pattern matching.

    Yields individual sentences by matching text segments that end with
    sentence-terminating punctuation (.!?).

    Parameters
    ----------
    full_text : str
        The complete text to parse for sentences.
    pattern : re.Pattern[str], optional
        Compiled regex pattern for sentence matching.
        Default matches sequences ending in period, exclamation, or question mark.

    Yields
    ------
    str
        Individual sentences, stripped of leading/trailing whitespace.

    Notes
    -----
    This is a private helper function. Text without sentence-ending
    punctuation will yield no results, which should be handled by the caller.
    """
    for match in pattern.finditer(full_text): 
        yield str(match.group()).strip()


def _count_strings(sentences: Iterator[str]) -> tuple[int, int, int]:
    """
    Count sentences, words, and letters from an iterator of sentences.

    Processes each sentence to extract word and letter counts. Punctuation
    is stripped from word boundaries to ensure accurate counting of words
    like contractions ("You're") and sentence-final words ("away!").

    Parameters
    ----------
    sentences : Iterator[str]
        An iterator yielding sentence strings to analyze.

    Returns
    -------
    tuple of (int, int, int)
        A tuple containing:
        - sentence_count : Total number of sentences processed
        - word_count : Total number of valid words found
        - letter_count : Total number of alphabetic characters

    Raises
    ------
    ValueError
        If no valid words are found in the text (word_count == 0).

    Notes
    -----
    This is a private helper function. Words are identified by splitting
    on whitespace and stripping edge punctuation using `string.punctuation`.
    Only alphabetic characters contribute to the letter count.
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
    Calculate the L and S variables required for the Coleman-Liau index.

    Parses the input text to count sentences, words, and letters, then
    computes the average letters and sentences per specified rate (default 100)
    words.

    Parameters
    ----------
    full_text : str
        The complete text to analyze for readability.
    rate : int, optional
        The normalization rate for averaging. Default is 100 (per 100 words).

    Returns
    -------
    tuple of (float, float)
        A tuple containing:
        - letters_avg : Average number of letters per `rate` words
        - sentences_avg : Average number of sentences per `rate` words

    Raises
    ------
    ValueError
        If the text is empty, contains no valid sentences (missing punctuation),
        or contains no valid words.

    Examples
    --------
    >>> letters_avg, sentences_avg = calculate_variables("Hello world. Test sentence.")
    >>> isinstance(letters_avg, float) and isinstance(sentences_avg, float)
    True
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
    Calculate the Coleman-Liau readability grade from text statistics.

    Applies the Coleman-Liau formula to determine the U.S. school grade level
    required to understand the text. Results are clamped to a readable range.

    Parameters
    ----------
    letters_avg : float
        Average number of letters per 100 words (L variable).
    sentences_avg : float
        Average number of sentences per 100 words (S variable).
    cli_coef_l : float, optional
        Coefficient for the letters variable. Default is 0.0588.
    cli_coef_s : float, optional
        Coefficient for the sentences variable. Default is 0.296.
    cli_intercept : float, optional
        Constant intercept value. Default is 15.8.
    grade_min : int, optional
        Minimum grade level to report. Default is 1.
    grade_max : int, optional
        Maximum grade level to report. Default is 16.
    round_digits : int, optional
        Decimal places for debug logging. Default is 2.

    Returns
    -------
    str
        Human-readable grade level string:
        - "Before Grade {min}" if index < grade_min
        - "Grade {max}+" if index > grade_max
        - "Grade {n}" where n is the rounded index

    Examples
    --------
    >>> coleman_liau(letters_avg=100.0, sentences_avg=10.0)
    'Grade 3'
    >>> coleman_liau(letters_avg=50.0, sentences_avg=20.0)
    'Before Grade 1'
    >>> coleman_liau(letters_avg=200.0, sentences_avg=5.0)
    'Grade 16+'
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
    Main entry point for the readability calculator CLI.

    Parses command-line arguments, processes the input text (or uses default),
    calculates readability metrics, and logs the resulting grade level.

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
        description="Calculate readability level based on Coleman-Liau index"
    )
    parser.add_argument(
        "text",  # Positional argument requires at least 1 argument
        type=str,
        nargs = "*",  # zero or more arguments (words), if zero goes to default
        default=None, # If DEFAULT_TEXT used here, it will be joined as characters by .join()
        help="Enter text with no numeric characters, use alphabetic characteres",
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
    