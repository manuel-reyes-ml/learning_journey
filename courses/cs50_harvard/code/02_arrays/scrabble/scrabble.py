"""
Scrabble Point Calculator - Determine the winner between players based on word scores.

A command-line tool that calculates Scrabble points for words submitted by
players and determines the winner based on standard Scrabble letter values.

Usage
-----
    python scrabble.py WORD1 WORD2
    python scrabble.py --verbose CAT DOG
    python scrabble.py -v QUEEN ZEBRA

Examples
--------
    $ python scrabble.py CAT DOG
    12:30:45 : INFO : Scores: {'player_1': 5, 'player_2': 5}
    12:30:45 : INFO : It's a tie!

    $ python scrabble.py QUEEN ZEBRA
    12:31:00 : INFO : Scores: {'player_1': 14, 'player_2': 16}
    12:31:00 : INFO : Winner is player_2, points: 16

    $ python scrabble.py -v CAT DOG
    12:32:15 : DEBUG : Verbose mode enabled
    12:32:15 : DEBUG : Received 2 words: ['CAT', 'DOG']
    12:32:15 : DEBUG : Validating Scrabble word(s)......
    12:32:15 : DEBUG : Calculating points for ['player_1', 'player_2']......
    12:32:15 : DEBUG : Analyzing winner......
    12:32:15 : INFO : Scores: {'player_1': 5, 'player_2': 5}
    12:32:15 : INFO : It's a tie!
"""

from __future__ import annotations
from typing import Final
from collections import Counter
import argparse
import logging
import sys


# =============================================================================
# Module Configuration
# =============================================================================

__all__ = [
    "validate_input",
    "calculate_points",
    "POINTS",
]

# Number of words allowble to enter the program at a time
PLAYERS: Final[int] = 2
PLAYER_PREFIX: Final[str] = "player"

# Exit codes (Unix standard)
EXIT_SUCCESS: int = 0
EXIT_FAILURE: int = 1
EXIT_KEYBOARD_INTERRUPT: int = 130

# Point specs to define winner player
POINTS: Final[dict[str, int]] = {
    "A": 1, "B": 3, "C": 3,
    "D": 2, "E": 1, "F": 4,
    "G": 2, "H": 4, "I": 1,
    "J": 8, "K": 5, "L": 1,
    "M": 3, "N": 1, "O": 1,
    "P": 3, "Q": 10, "R": 1,
    "S": 1, "T": 1, "U": 1,
    "V": 4, "W": 4, "X": 8,
    "Y": 4, "Z": 10,
}

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

def validate_input(words: list[str], players: int = PLAYERS) -> list[str]:
    """
    Validate and normalize player words for Scrabble scoring.

    Ensures the correct number of words are provided and that each word
    contains only alphabetic characters. Words are stripped of whitespace
    and converted to uppercase for consistent scoring.

    Parameters
    ----------
    words : list of str
        Raw word strings submitted by players.
    players : int, optional
        Expected number of words (one per player). Default is PLAYERS (2).

    Returns
    -------
    list of str
        Validated words, stripped and uppercased.

    Raises
    ------
    ValueError
        If the word list is empty, contains the wrong number of words,
        or any word contains non-alphabetic characters.

    Examples
    --------
    >>> validate_input(["cat", "dog"])
    ['CAT', 'DOG']
    >>> validate_input(["  HELLO  ", "world"])
    ['HELLO', 'WORLD']
    >>> validate_input(["abc123", "dog"])
    Traceback (most recent call last):
    ...
    ValueError: Words must contain only letters
    """
    logger.debug("Validating Scrabble word(s)......")
    
    # Validate once at the entry point (DRY!)
    if not words:
        raise ValueError("List of strings cannot be empty")
    
    if len(words) != players:
        raise ValueError(f"Expected {players} words, got {len(words)}'")
   
    word_list = [word.strip().upper() for word in words]
    
    # True if one word is not alphabetic (contains digits)
    if not all(word.isalpha() for word in word_list):
        raise ValueError("Words must contain only letters")
    
    return word_list


def calculate_points(
    word_list: list[str],
    points: dict[str, int] = POINTS, 
    player_prefix: str = PLAYER_PREFIX,
) -> dict[str, int]:
    """
    Calculate Scrabble points for each player's word.

    Iterates through each word and sums the point values for each letter
    based on standard Scrabble scoring. Letters not found in the points
    dictionary are assigned zero points.

    Parameters
    ----------
    word_list : list of str
        Validated uppercase words, one per player.
    points : dict of {str: int}, optional
        Letter-to-point mapping. Default is POINTS (standard Scrabble values).
    player_prefix : str, optional
        Prefix for player keys in the result dict. Default is "player".

    Returns
    -------
    dict of {str: int}
        Player identifiers mapped to their total scores.
        Keys are formatted as "{player_prefix}_{n}" where n starts at 1.

    Examples
    --------
    >>> calculate_points(["CAT", "DOG"])
    {'player_1': 5, 'player_2': 5}
    >>> calculate_points(["QUEEN", "ZEBRA"])
    {'player_1': 14, 'player_2': 16}
    >>> calculate_points(["ZZ"], player_prefix="team")
    {'team_1': 20}
    """
    results = {}
    for i, word in enumerate(word_list):
        # Use sum() to make list comprehensive(iterator)
        player_points = sum(points.get(letter, 0) for letter in word)
        results[f"{player_prefix}_{i + 1}"] = player_points
    
    logger.debug(f"Calculating points for {list(results.keys())}......")
    return results


def determine_winner(scores: dict[str, int]) -> str:
    """
    Determine the winner from player scores.

    Identifies the player(s) with the highest score. If multiple players
    share the highest score, declares a tie.

    Parameters
    ----------
    scores : dict of {str: int}
        Player identifiers mapped to their total scores.

    Returns
    -------
    str
        Result message indicating the winner and their score,
        or a tie announcement if scores are equal.

    Examples
    --------
    >>> determine_winner({"player_1": 10, "player_2": 8})
    'Winner is player_1, points: 10'
    >>> determine_winner({"player_1": 5, "player_2": 5})
    "It's a tie!"
    >>> determine_winner({"player_1": 3, "player_2": 7, "player_3": 7})
    "It's a tie!"
    """
    logger.debug("Analyzing winner......")
    
    ## OPTION 1: Use conditions to define winner or Tie ====================
    max_score = max(scores.values())
    winners = [player for player, score in scores.items() if score == max_score]
    
    if len(winners) > 1:
        return "It's a tie!"
    return f"Winner is {winners[0]}, points: {max_score}"
    
    ## OPTION 2: Set to store unique values ================================
    # Set -> unordered collection of unique elements
    # if len(set(scores.values())) > 1:
    #    winner = Counter(scores).most_common(1)
         
    ## OPTION 3: Use iterator to preserve memory ===========================
    # When you have a massive dictionary (millions of items), an iterator
    # is the best approach to stop when a difference is found.
    # values = iter(counters.values())
    # first = next(values)
    # if any(first != value for value in values):


# =============================================================================
# CLI Entry Point
# =============================================================================

def main(argv: list[str] | None = None) -> int:
    """
    Main entry point for the Scrabble point calculator CLI.

    Parses command-line arguments, validates input words, calculates
    points for each player, and logs the winner.

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
        description=f"Calculate Scrabble point for {PLAYERS} players / words"
    )
    parser.add_argument(
        "words",
        type=str,
        nargs=PLAYERS,
        help=f"Enter {PLAYERS} words to calculate points"    
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
        
    logger.debug(f"Received {PLAYERS} words: {args.words}")
        
    try:
        word_list = validate_input(args.words)
        scores = calculate_points(word_list)
        winner = determine_winner(scores)
    
    except KeyboardInterrupt:
        logger.info("\nInterrupted by User. Exiting.")
        return EXIT_KEYBOARD_INTERRUPT
    
    except ValueError as e:
        logger.error(f"Processing Error for {args.words}: {e}")
        return EXIT_FAILURE
    
    except Exception as e:
        logger.exception(f"Unexpected crash: {e}")  # Defaults to 'ERROR' level, but it always include traceback
        return EXIT_FAILURE
    
    logger.info(f"Scores: {scores}")
    logger.info(winner)
    return EXIT_SUCCESS

if __name__ == "__main__":
    sys.exit(main())