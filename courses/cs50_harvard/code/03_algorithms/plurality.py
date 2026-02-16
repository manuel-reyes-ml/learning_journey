"""
"""

from __future__ import annotations
from collections import defaultdict
from typing import Final, Iterator
import argparse
import itertools
import string
import logging
import sys


# =============================================================================
# Module Configuration
# =============================================================================

#Exports
__all__ = [
    "validate_candidates",
    "validate_voter_count",
    "assign_votes",
    "count_winners",
    "CANDIDATES_MIN",
    "CANDIDATES_MAX",
    "VALID_CANDIDATES_LENGTH",
]

# Program constants
CANDIDATES_MIN: Final[int] = 2
CANDIDATES_MAX: Final[int] = 9

# Pre-converting ranges to integer tuples for O(1) lookups in validation
VALID_CANDIDATES_LENGTH: Final[tuple[int, ...]] = tuple(range(CANDIDATES_MIN, CANDIDATES_MAX + 1))

# Exit codes (Unix standard)
EXIT_SUCCESS: int = 0
EXIT_FAILURE: int = 1
EXIT_KEYBOARD_INTERRUPT: int = 130

class ColoredFormatter(logging.Formatter): # Inherits from Python's built-in Formatter!
    """Custom formatter that adds colors based on log level."""
    
    # Color codes for each level
    COLORS: Final[dict[int, str]] = {
        logging.DEBUG:    "\033[90m",   # Gray
        logging.INFO:     "\033[92m",   # Green
        logging.WARNING:  "\033[93m",   # Yellow
        logging.ERROR:    "\033[91m",   # Red
        logging.CRITICAL: "\033[1;91m", # Bold Red
    }
    RESET = "\033[0m"
    
    # Override the parent´s format method
    def format(self, record) -> str:
        # Step 1: Get the color for this log level
        color = self.COLORS.get(record.levelno, self.RESET)
        
        # Format the message normally first
        # This produces: "14:30:45 : INFO : Your message here"
        message = super(). format(record) # Call PARENT´s format!
        
        # Step 3: Wrap with color codes
        return f"{color}{message}{self.RESET}"

# Set up Logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Create handler with colored formatter
handler = logging.StreamHandler()
handler.setFormatter(ColoredFormatter(
    fmt='%(asctime)s : %(levelname)s : %(message)s',
    datefmt='%H:%M:%S',
))
logger.addHandler(handler)

# **The flow when you call `logger.info("Hello")`:**
# logger.info("Hello")
#        ↓
# handler receives the log record
#        ↓
# handler.formatter.format(record) is called
#        ↓
# ColoredFormatter.format() runs:
#    1. Gets color for INFO level → "\033[92m" (green)
#    2. Calls super().format(record) → "14:30:45 : INFO : Hello"
#    3. Returns "\033[92m14:30:45 : INFO : Hello\033[0m"
#        ↓
# Green text appears in terminal!

# =============================================================================
# Core Functions
# =============================================================================

def validate_candidates(candidates: list[str], length_prefix: tuple[int, ...] = VALID_CANDIDATES_LENGTH) -> list[str]:
    """
    """
    if len(candidates) not in length_prefix:
        raise ValueError(
            f"List must be between {min(length_prefix)} and {max(length_prefix)} candidates"
        )
    
    # Set is an unordered collection of unique items
    if len(candidates) != len(set(candidates)):
        raise ValueError("Candidate names must be unique")
    
    return candidates


def _validate_candidate_arg(candidate: str) -> str:
    """
    """
    if not candidate:
        raise argparse.ArgumentTypeError("Candidate name cannot be empty")
    
    clean_candidate = candidate.strip(string.punctuation).title()
    
    if not clean_candidate.replace(" ", "").isalpha():
        raise argparse.ArgumentTypeError(f"Candidate name must be alphabetic: '{candidate}'")

    return clean_candidate.strip()


def validate_voter_count(voters: str | int | None = None) -> int:
    """
    """
    if isinstance(voters, int):
        return voters
    
    if voters is None:
        voters = input("Enter number of voters: ").strip()
    
    if not voters:
        raise ValueError("Voters cannot be empty")
    
    try:
        voters_int = int(voters)
    except (ValueError, TypeError) as e:
        raise ValueError("Number of voters must be numeric") from e
    
    return voters_int


def _validate_votes(voters_int: int | None = None, votes: list[str] | None = None) -> Iterator[str]:
    """
    """
    if votes is None:
        if voters_int is None:
            raise ValueError("voters_int required for interative mode")
        
        for i in range(voters_int):
            vote = input(f"Vote {i + 1}: ").strip()
            
            if not vote or not vote.isalpha():
                logger.warning("Invalid vote...")
                continue
            
            yield vote.title()  # Transform: 'john' -> 'John'
    
    if isinstance(votes, list):
        for vote in votes:
            if not vote or not vote.strip().isalpha():
                continue
            
            yield vote.strip().title()
            

def assign_votes(
    clean_candidates: list[str],
    voters_int: int | None = None,
    votes: list[str] | None = None,
) -> defaultdict[str, int]:
    """
    """
    votes_dict = defaultdict(int)
    votes_iter = _validate_votes(voters_int, votes)
    
    try:
        first = next(votes_iter)
    except StopIteration:
        raise ValueError("No valid votes found!")
    
    for vote in itertools.chain([first], votes_iter):
        if vote not in clean_candidates:
            logger.warning("Invalid vote...")
            continue
        votes_dict[vote] += 1
    
    # If no valid votes, dictionary is empty
    if not votes_dict: 
        raise ValueError("All votes were invalid. No count was processed")
    
    return votes_dict


def count_winners(votes_dict: defaultdict[str, int]) -> Iterator[tuple[str, int]]:
    """
    """
    max_count = max(votes_dict.values())
            
    for vote, count in votes_dict.items():
        if count == max_count:
            yield vote, count
            

# =============================================================================
# CLI Entry Point
# =============================================================================
      
def main(argv: list[str] | None = None) -> int:
    """
    """
    parser = argparse.ArgumentParser(
        description="Count votes per candidates and print out winner(s)"
    )
    parser.add_argument(
        "candidates",
        type=_validate_candidate_arg,  # argparser applies type= to each single string, not the whole list
        nargs="+",  # One or more arguments required
        help=f"Enter candidate names list. Min {min(VALID_CANDIDATES_LENGTH)}, Max {max(VALID_CANDIDATES_LENGTH)}",
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose (debug) output",
    )
    
    args = parser.parse_args(argv)
    
    if args.verbose:
        logger.setLevel(logging.DEBUG)
        logger.debug("Verbose mode enabled")
        
    try:
        candidates = validate_candidates(args.candidates)
        voters_int = validate_voter_count()
        votes_dict = assign_votes(candidates,voters_int)
    
    except KeyboardInterrupt:
        logger.info("\nInterrupted by user. Exiting.")
        return EXIT_KEYBOARD_INTERRUPT
    
    except ValueError as e:
        logger.error(f"Processing Error: {e}")
        return EXIT_FAILURE

    except Exception as e:
        logger.exception(f"Unexpected Error: {e}")  # logger.exception logs the traceback    
        return EXIT_FAILURE
    
    for vote, count in count_winners(votes_dict):
        logger.info(f"{vote} {count}")  # logging mssg accepts string, not direct variable
    
    return EXIT_SUCCESS


if __name__ == "__main__":
    sys.exit(main())