"""
"""

from __future__ import annotations
from collections import defaultdict
from typing import Final, Iterator
import itertools
import argparse
import logging
import string
import sys


# =============================================================================
# Module Configuration
# =============================================================================

# Exports
__all__ = [
    "validate_candidates",
    "validate_voter_count",
    "assign_votes",
    "count_winners",
    "CANDIDATES_MIN",
    "CANDIDATES_MAX",
    "RANK_SPECS",
    "MAX_RANK",
]

# Program constants
CANDIDATES_MIN: Final[int] = 3
CANDIDATES_MAX: Final[int] = 9
RANK_NUMBER: Final[int] = 3

# Rank and points structure for iteration in function
# RANK_POINTS = {"rank1": 3, "rank2": 2, "rank3": 1}
RANK_SPECS: Final[dict[str, int]] = {
    f"rank{i + 1}": RANK_NUMBER - i   # dict comprehension (same as list's)
    for i in range(RANK_NUMBER)
}

# Identify max rank format -> 'rank1'
MAX_RANK: Final[str] = list(RANK_SPECS.keys())[0]

# Exit codes (Unix standard)
EXIT_SUCCESS: Final[int] = 0
EXIT_FAILURE: Final[int] = 1
EXIT_KEYBOARD_INTERRUPT: Final[int] = 130

# Inherits from Python's built-in Formatter
class ColoredFormatter(logging.Formatter):
    """
    Custom logging formatter that adds ANSI color codes based on log level.

    Inherits from Python's built-in logging.Formatter and overrides the
    format method to wrap log messages in terminal color codes.

    Attributes
    ----------
    COLORS : dict of {int: str}
        Mapping of logging level constants to ANSI color codes.
    RESET : str
        ANSI code to reset terminal color to default.

    Examples
    --------
    >>> handler = logging.StreamHandler()
    >>> handler.setFormatter(ColoredFormatter(
    ...     fmt='%(levelname)s : %(message)s'
    ... ))
    >>> logger.addHandler(handler)
    >>> logger.info("This appears in green")
    >>> logger.error("This appears in red")
    """
    # Color codes for each level
    COLORS: Final[dict[int, str]] = {
        logging.DEBUG:    "\033[90m",   # Gray
        logging.INFO:     "\033[92m",   # Green
        logging.WARNING:  "\033[93m",   # Yellow
        logging.ERROR:    "\033[91m",   # Red
        logging.CRITICAL: "\033[1;91m", # Bold Red
    }
    RESET: Final[str] = "\033[0m"
    
    # Override the parent's format method
    def format(self, record) -> str:
        # Step 1: Get the color for this log level
        color = self.COLORS.get(record.levelno, self.RESET)
        
        # Step 2: Format the message normally first
        # This produces: "14:30:45 : INFO : Your message here"
        message = super().format(record) # Call PARENT's format!
        
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


# =============================================================================
# Core Functions
# =============================================================================

def validate_candidates(
    candidates: list[str], 
    candidates_min: int = CANDIDATES_MIN,
    candidates_max: int = CANDIDATES_MAX,
    ) -> list[str]:
    """
    """
    if not (candidates_min <= len(candidates) <= candidates_max):
        raise ValueError(
            f"List must be between {candidates_min} and {candidates_max} candidates"
        )
    
    # Set is an unordered collection of unique items
    if len(candidates) != len(set(candidates)):
        raise ValueError("Candidate names must be unique")
    
    logger.debug("Candidates are validated......")
    return candidates


def _validate_single_candidate(candidate: str) -> str:
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
    
    logger.debug("'number of voters' is validated......")
    return voters_int


def _validate_votes(
    voters_int: int | None = None,
    votes: list[list[str]] | None = None,
    max_rank: str = MAX_RANK,
    rank_specs: dict[str, int] = RANK_SPECS,
) -> Iterator[tuple[str, int]]:
    """
    """
    if votes is None:
        if voters_int is None:
            raise ValueError("voters_int required for interactive mode")
        
        for _ in range(voters_int):
            print("\n")
            for rank, points in rank_specs.items():
                vote = input(f"{rank}: ").strip()
                
                if not vote or not vote.isalpha():
                    logger.warning("Invalid vote...")
                    continue
                
                # Gives rank1 more weight into the calculation
                points = (points + 1) if rank == max_rank else points
                
                yield vote.title(), points
        
        return  # Explicitly returns after 'if votes is None' block
    
    # When votes are manually passed as list of lists            
    if isinstance(votes, list):
        for voter in votes:
            if len(voter) > len(rank_specs.keys()):
                raise ValueError(f"Only {len(rank_specs.keys())} allow, got {len(voter)}")
            
            for i, vote in enumerate(voter):
                if not vote or not vote.strip().isalpha():
                    continue
                
                points = rank_specs.get(f"rank{i + 1}", 0)
                points = (points + 1) if i == 0 else points
                
                yield vote.strip().title(), points
                

def assign_votes(
    clean_candidates: list[str],
    voters_int: int | None = None,
    votes: list[list[str]] | None = None,
) -> defaultdict[str, int]:
    """
    """
    votes_dict = defaultdict(int)
    votes_iter = _validate_votes(voters_int, votes)
    
    try:
        first = next(votes_iter)
    except StopIteration:
        raise ValueError("No valid votes found!")
    
    for vote, points in itertools.chain([first], votes_iter):
        if vote not in clean_candidates:
            logger.warning("Invalid vote...")
            continue
        votes_dict[vote] += points
    
    # if no valid votes, dictionary is empty
    if not votes_dict:
        raise ValueError("All votes were invalid. No count was processed")
    
    logger.debug("Votes assigned to candidates......")
    return votes_dict


def count_winners(votes_dict: defaultdict[str, int]) -> tuple[str, int]:
    """
    """
    sorted_items = sorted(
        votes_dict.items(), 
        key=lambda item: item[1],
        reverse=True,
    )
    
    logger.debug(f"Candidates: {dict(sorted_items)}....")
    return sorted_items[0]


# =============================================================================
# CLI Entry Point
# =============================================================================

def main(argv: list[str] | None = None) -> int:
    """
    """
    parser = argparse.ArgumentParser(
        description="Count votes per candidates and per ranking and print out winner"
    )
    parser.add_argument(
        "candidates",
        type=_validate_single_candidate,  # argparser applies type= to each single string, not the whole list
        nargs="+",  # One or more arguments required
        help=f"Enter candidate names list. Min {CANDIDATES_MIN}, Max {CANDIDATES_MAX}"
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
        candidates = validate_candidates(args.candidates)
        voters_int = validate_voter_count()
        votes_dict = assign_votes(candidates, voters_int)
        
    except KeyboardInterrupt:
        logger.warning("\nInterrupted by user. Exiting.")
        return EXIT_KEYBOARD_INTERRUPT
    
    except ValueError as e:
        logger.error(f"Processing Error: {e}")
        return EXIT_FAILURE
    
    except Exception as e:
        logger.exception(f"Unexpected Error: {e}")
        return EXIT_FAILURE
    
    winner, points = count_winners(votes_dict)
    logger.info(f"{winner}, Points: {points}")
    return EXIT_SUCCESS


if __name__ == "__main__":
    sys.exit(main())
    