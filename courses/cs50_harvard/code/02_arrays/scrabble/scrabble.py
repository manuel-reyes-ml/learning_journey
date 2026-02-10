"""
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
]

# Number of words allowble to enter the program at a time
PLAYERS: Final[int] = 2

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
    """
    if not words:
        raise ValueError(f"List of strings can't be empty")
    elif len(words) != PLAYERS:
        raise ValueError(
            f"Program will process only '{players}' words at a time. Submitted '{len(words)} words'"
        )
   
    word_list = [word.strip().upper() for word in words]
    
    # True if one word is not alphabetic (contains digits)
    if not all(word.isalpha() for word in word_list):
        raise ValueError(f"Strings contain numeric or special characters. Can't process it")
    
    logger.debug("Scrabble word(s) validated...")
    return word_list


def calculate_points(word_list: list[str], points: dict[str, int] = POINTS, players: int = PLAYERS) -> None:
    """
    """
    if not word_list:
        raise ValueError(f"List of strings can't be empty")
    elif len(word_list) != players:
        raise ValueError(
            f"Program will process only '{players}' words at a time. Submitted '{len(word_list)}' words'"
        )
        
    counters = {}
    
    for player in range(players):
        player_points = 0
        for letter in word_list[player]:
            player_points += points.get(letter, 0)
            
        counters[f"player_{player + 1}"] = player_points
    
    logger.debug(f"Points calculated for {list(counters.keys())}...")

    # Set -> unordered collection of unique elements
    # if len(set(counters.values())) > 1:
       #   ... connects with line '97'   
    
    # When you have a massive dictionary (millions of items), an iterator
    # is the best approach to stop when a difference is found.
    values = iter(counters.values())
    first = next(values)
    if any(first != value for value in values):
        winner = Counter(counters).most_common(1)
        logger.info(f"The winner is {winner[0][0]}, points: {winner[0][1]}")
        return
    
    logger.info("It's a tie!")
    return


# =============================================================================
# CLI Entry Point
# =============================================================================

def main(argv: list[str] | None = None) -> int:
    """
    """
    parser = argparse.ArgumentParser(
        description=f"Calculate Scrabble point for {PLAYERS} players / words"
    )
    parser.add_argument(
        "words",
        type=str,
        nargs=PLAYERS,
        help=f"Enter '{PLAYERS}' words to calculate points"    
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
        word_list = validate_input(args.words, PLAYERS)
        calculate_points(word_list, POINTS, PLAYERS)
    
    except KeyboardInterrupt:
        logger.info("\nInterrupted by User. Exiting.")
        return EXIT_KEYBOARD_INTERRUPT
    
    except ValueError as e:
        logger.error(f"Processing Error for {args.words}: {e}")
        return EXIT_FAILURE
    
    except Exception as e:
        logger.exception(f"Unexpected crash: {e}")  # Defaults to 'ERROR' level, but it always include traceback
    
    return EXIT_SUCCESS

if __name__ == "__main__":
    sys.exit(main())
    
            
    
