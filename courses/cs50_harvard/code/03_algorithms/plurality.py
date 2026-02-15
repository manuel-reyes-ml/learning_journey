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

# Set up Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s : %(levelname)s : %(message)s',
    datefmt='%H:%M:%S',
)
logger = logging.getLogger(__name__)


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
                logger.info("Invalid vote...")
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
            logger.info("Invalid vote...")
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