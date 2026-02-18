"""
Ranked-Choice Voting System (Borda Count) - Determine winner using weighted rankings.

A command-line tool that implements a Borda count voting system where voters
rank candidates by preference. Points are awarded based on ranking position,
and the candidate with the most total points wins.

How Borda Count Works
---------------------
1. Voters rank candidates (1st, 2nd, 3rd choice)
2. Points awarded per rank: rank1=3, rank2=2, rank3=1
3. Points are summed across all voters
4. Candidate with highest total points wins

Usage
-----
    python runoff.py Alice Bob Charlie
    python runoff.py --verbose Alice Bob Charlie David
    python runoff.py "John Smith" "Jane Doe" "Bob Jones"

Examples
--------
    $ python runoff.py Alice Bob Charlie
    Enter number of voters: 2
    
    
    rank1: Alice
    rank2: Bob
    rank3: Charlie
    
    
    rank1: Bob
    rank2: Alice
    rank3: Charlie
    
    14:30:45 : INFO : Alice, Points: 7

    $ python runoff.py -v Alice Bob Charlie
    14:31:00 : DEBUG : Verbose mode enabled
    14:31:00 : DEBUG : Candidates are validated......
    14:31:05 : DEBUG : 'number of voters' is validated......
    14:31:20 : DEBUG : Votes assigned to candidates......
    14:31:20 : DEBUG : Candidates: {'Alice': 7, 'Bob': 5, 'Charlie': 3}....
    14:31:20 : INFO : Alice, Points: 7

Notes
-----
- Candidate names are case-insensitive and normalized to Title Case
- Invalid votes (non-alphabetic, empty) are skipped with warnings
- Requires minimum 3 candidates, maximum 9
- Each voter must rank exactly 3 candidates
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
     Validate the candidate list for count and uniqueness.

    Ensures the number of candidates falls within acceptable bounds
    and that all candidate names are unique.

    Parameters
    ----------
    candidates : list of str
        List of candidate names to validate.
    candidates_min : int, optional
        Minimum number of candidates allowed. Default is 3.
    candidates_max : int, optional
        Maximum number of candidates allowed. Default is 9.

    Returns
    -------
    list of str
        The validated candidate list, unchanged.

    Raises
    ------
    ValueError
        If candidate count is outside valid range or names are not unique.

    Examples
    --------
    >>> validate_candidates(["Alice", "Bob", "Charlie"])
    ['Alice', 'Bob', 'Charlie']
    >>> validate_candidates(["Alice", "Bob"])
    Traceback (most recent call last):
    ...
    ValueError: List must be between 3 and 9 candidates
    >>> validate_candidates(["Alice", "Alice", "Bob"])
    Traceback (most recent call last):
    ...
    ValueError: Candidate names must be unique
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
    Argparse type validator for individual candidate names.

    Validates and normalizes a single candidate name from CLI input.
    Strips punctuation, converts to Title Case, and ensures alphabetic content.

    Parameters
    ----------
    candidate : str
        Raw candidate name from command line.

    Returns
    -------
    str
        Cleaned and normalized candidate name.

    Raises
    ------
    argparse.ArgumentTypeError
        If candidate is empty or contains non-alphabetic characters.

    Notes
    -----
    This is a private function used by argparse's type parameter.
    It is called once per candidate argument, not on the full list.

    Examples
    --------
    >>> _validate_single_candidate("alice")
    'Alice'
    >>> _validate_single_candidate("  Bob!  ")
    'Bob'
    >>> _validate_single_candidate("John Smith")
    'John Smith'
    >>> _validate_single_candidate("Alice123")
    Traceback (most recent call last):
    ...
    argparse.ArgumentTypeError: Candidate name must be alphabetic: 'Alice123'
    """
    if not candidate:
        raise argparse.ArgumentTypeError("Candidate name cannot be empty")
    
    clean_candidate = candidate.strip(string.punctuation).title()
    
    if not clean_candidate.replace(" ", "").isalpha():
        raise argparse.ArgumentTypeError(f"Candidate name must be alphabetic: '{candidate}'")
    
    return clean_candidate.strip()


def validate_voter_count(voters: str | int | None = None) -> int:
    """
    Validate and return the number of voters.

    Accepts input as string, integer, or prompts interactively if None.
    Ensures the value is a valid integer.

    Parameters
    ----------
    voters : str, int, or None, optional
        The voter count as string or int. If None, prompts user interactively.

    Returns
    -------
    int
        Validated voter count.

    Raises
    ------
    ValueError
        If voters is empty or cannot be converted to an integer.

    Examples
    --------
    >>> validate_voter_count(5)
    5
    >>> validate_voter_count("10")
    10
    >>> validate_voter_count("")
    Traceback (most recent call last):
    ...
    ValueError: Voters cannot be empty
    >>> validate_voter_count("abc")
    Traceback (most recent call last):
    ...
    ValueError: Number of voters must be numeric
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
    Validate and yield individual votes with their point values.

    Operates in two modes: interactive (prompts for each rank) or batch
    (processes a provided nested list). Invalid votes are skipped with warnings.

    Parameters
    ----------
    voters_int : int or None, optional
        Number of voters for interactive mode. Required if votes is None.
    votes : list of list of str or None, optional
        Pre-defined votes for testing/batch mode. Each inner list represents
        one voter's rankings in order (1st choice, 2nd choice, etc.).
    max_rank : str, optional
        Key identifying the highest rank for bonus points. Default is "rank1".
    rank_specs : dict of {str: int}, optional
        Mapping of rank names to base point values. Default is RANK_SPECS.

    Yields
    ------
    tuple of (str, int)
        Tuples of (candidate_name, points) for each valid vote.

    Raises
    ------
    ValueError
        If votes is None and voters_int is also None, or if a ballot
        contains more ranks than allowed.

    Notes
    -----
    This is a private generator function. The highest rank (rank1) receives
    a +1 bonus point to give it additional weight.

    Point calculation:
        - rank1: 3 + 1 = 4 points
        - rank2: 2 points
        - rank3: 1 point

    Examples
    --------
    >>> list(_validate_votes(votes=[["Alice", "Bob", "Charlie"]]))
    [('Alice', 4), ('Bob', 2), ('Charlie', 1)]
    >>> list(_validate_votes(votes=[["alice", "BOB"]]))
    [('Alice', 4), ('Bob', 2)]
    >>> list(_validate_votes(votes=None, voters_int=None))
    Traceback (most recent call last):
    ...
    ValueError: voters_int required for interactive mode
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
    Collect and tally ranked votes for candidates.

    Processes votes either interactively or from a provided list, summing
    points for each candidate based on their rankings.

    Parameters
    ----------
    clean_candidates : list of str
        List of valid candidate names to accept votes for.
    voters_int : int or None, optional
        Number of voters for interactive mode.
    votes : list of list of str or None, optional
        Pre-defined votes for testing/batch mode.

    Returns
    -------
    defaultdict of {str: int}
        Dictionary mapping candidate names to their total points.
        Only candidates with at least one valid vote are included.

    Raises
    ------
    ValueError
        If no valid votes are found or all votes are invalid.

    Examples
    --------
    >>> votes = [["Alice", "Bob", "Charlie"], ["Bob", "Alice", "Charlie"]]
    >>> dict(assign_votes(["Alice", "Bob", "Charlie"], votes=votes))
    {'Alice': 6, 'Bob': 6, 'Charlie': 2}
    >>> assign_votes(["Alice", "Bob", "Charlie"], votes=[[]])
    Traceback (most recent call last):
    ...
    ValueError: No valid votes found!
    >>> assign_votes(["Alice", "Bob"], votes=[["Charlie", "David", "Eve"]])
    Traceback (most recent call last):
    ...
    ValueError: All votes were invalid. No count was processed
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
    Determine the winner from vote tallies.

    Sorts candidates by total points in descending order and returns
    the candidate with the highest score.

    Parameters
    ----------
    votes_dict : defaultdict of {str: int}
        Dictionary mapping candidate names to total points.

    Returns
    -------
    tuple of (str, int)
        Tuple containing (winner_name, total_points).

    Notes
    -----
    In case of a tie, returns the first candidate encountered with the
    maximum score. The current implementation does not handle ties
    explicitly — consider using a tiebreaker or returning all winners
    if tie handling is required.

    Examples
    --------
    >>> from collections import defaultdict
    >>> votes = defaultdict(int, {"Alice": 10, "Bob": 8, "Charlie": 5})
    >>> count_winners(votes)
    ('Alice', 10)
    >>> votes = defaultdict(int, {"Alice": 7, "Bob": 7, "Charlie": 3})
    >>> count_winners(votes)  # Returns first max (undefined order)
    ('Alice', 7)
    """
    sorted_items = sorted(
        votes_dict.items(), 
        key=lambda item: item[1],
        reverse=True,
    )
    
    logger.debug(f"Candidates: {dict(sorted_items)}....")
    return sorted_items[0]

# =============================================================================
# LAMBDA WITH SORTED() QUICK REFERENCE
# =============================================================================
#
# Pattern:
#     sorted(iterable, key=lambda x: WHAT_TO_SORT_BY, reverse=True/False)
#
# Examples:
#     # Sort tuples by second element
#     sorted([(a, 1), (b, 3), (c, 2)], key=lambda x: x[1])
#     # Result: [(a, 1), (c, 2), (b, 3)]
#
#     # Sort strings by length
#     sorted(["cat", "elephant", "dog"], key=lambda x: len(x))
#     # Result: ["cat", "dog", "elephant"]
#
#     # Sort dicts by a key
#     sorted([{"name": "Bob", "age": 25}, {"name": "Alice", "age": 30}], key=lambda x: x["age"])
#     # Result: [{"name": "Bob", "age": 25}, {"name": "Alice", "age": 30}]
#
#     # Sort by multiple criteria (tuple)
#     sorted(items, key=lambda x: (x["category"], x["price"]))
#     # Sorts by category first, then by price within each category
#
# =============================================================================

# =============================================================================
# CLI Entry Point
# =============================================================================

def main(argv: list[str] | None = None) -> int:
    """
    Main entry point for the ranked-choice voting CLI.

    Parses command-line arguments, validates candidates, collects ranked
    votes, tallies points, and announces the winner.

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
    