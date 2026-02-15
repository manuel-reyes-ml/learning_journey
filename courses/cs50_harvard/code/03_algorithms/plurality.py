"""
"""

from __future__ import annotations
from collections import Counter, defaultdict
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

# Program constants
CANDIDATES_MAX: Final[int] = 9
CANDIDATES_MIN: Final[int] = 2
RANGE_CANDIDATES: Final[range] = range(2, 10)  # 2 to 9 inclusive

# Pre-converting ranges to integer tuples for O(1) lookups in validation
LENGTH_PREFIX: Final[tuple[int, ...]] = tuple(x for x in RANGE_CANDIDATES)

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

def candidates_validation(candidates: list[str], length_prefix: tuple[int, ...] = LENGTH_PREFIX) -> list[str]:
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


def _validate_candidate_args(candidate: str) -> str:
    """
    """
    if not candidate:
        raise argparse.ArgumentTypeError("Candidate name cannot be empty")
    
    clean_candidate = candidate.strip(string.punctuation).title()
    
    if not clean_candidate.replace(" ", "").isalpha():
        raise argparse.ArgumentTypeError(f"Candidate name must be alphabetic: '{candidate}'")

    return clean_candidate.strip()


def number_voters_validation(voters: str | int | None = None) -> int:
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


def _vote_validation(voters_int: int, votes: list[str] | None = None) -> Iterator[str]:
    """
    """
    if votes is None:
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
            

def assign_votes(voters_int: int, clean_candidates: list[str]) -> defaultdict[str, int]:
    """
    """
    votes_dict = defaultdict(int)
    votes = _vote_validation(voters_int)
    
    try:
        first = next(votes)
    except StopIteration:
        raise ValueError("No valid votes found!")
    
    for vote in itertools.chain([first], votes):
        if vote not in clean_candidates:
            logger.info("Invalid vote...")
            continue
        votes_dict[vote] += 1
    
    if all(counter_value == 0 for counter_value in votes_dict.values()):
        raise ValueError("All votes were invalid. No count was processed")
    
    return votes_dict


def count_winners(votes_dict: defaultdict[str, int]) -> Iterator[tuple[str, int]]:
    """
    """
    votes_counter = Counter(votes_dict)
    max_count = max(votes_counter.values())
            
    for vote, count in votes_counter.items():
        if count == max_count:
            yield vote, count
            

def main(argv: list[str] | None = None) -> int:
    """
    """
    parser = argparse.ArgumentParser(
        description="Count votes per candidates and print out winner(s)"
    )
    parser.add_argument(
        "candidates",
        type=_validate_candidate_args,  # argparser applies type= to each single string, not the whole list
        nargs="*",
        help=f"Enter candidate names list. Min {min(LENGTH_PREFIX)}, Max {max(LENGTH_PREFIX)}",
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
        candidates = candidates_validation(args.candidates)
        voters_int = number_voters_validation()
        votes_dict = assign_votes(voters_int, candidates)
    
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