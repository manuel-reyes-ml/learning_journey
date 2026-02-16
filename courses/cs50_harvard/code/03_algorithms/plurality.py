"""
Plurality Voting System - Count votes and determine winner(s) by simple majority.

A command-line tool that implements a plurality voting system where each voter
casts one vote for their preferred candidate. The candidate(s) with the most
votes wins. Supports ties when multiple candidates share the highest vote count.

How Plurality Voting Works
--------------------------
1. Register candidates (2-9 allowed)
2. Each voter casts exactly one vote
3. Votes are tallied per candidate
4. Candidate(s) with most votes win(s)

Usage
-----
    python plurality.py Alice Bob Charlie
    python plurality.py --verbose Alice Bob
    python plurality.py "John Smith" "Jane Doe"

Examples
--------
    $ python plurality.py Alice Bob Charlie
    Enter number of voters: 5
    Vote 1: Alice
    Vote 2: Bob
    Vote 3: Alice
    Vote 4: Charlie
    Vote 5: Alice
    14:30:45 : INFO : Alice 3

    $ python plurality.py Alice Bob
    Enter number of voters: 4
    Vote 1: Alice
    Vote 2: Bob
    Vote 3: Alice
    Vote 4: Bob
    14:31:00 : INFO : Alice 2
    14:31:00 : INFO : Bob 2

    $ python plurality.py -v Alice Bob Charlie
    14:32:15 : DEBUG : Verbose mode enabled
    Enter number of voters: 2
    Vote 1: alice
    Vote 2: David
    14:32:20 : WARNING : Invalid vote...
    14:32:20 : INFO : Alice 1

Notes
-----
- Candidate names are case-insensitive and normalized to Title Case
- Invalid votes (non-candidates, empty, numeric) are logged and skipped
- Ties are reported by listing all winners with their vote counts
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
    "ColoredFormatter",
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
    Validate the candidate list for count and uniqueness.

    Ensures the number of candidates falls within acceptable bounds and
    that all candidate names are unique.

    Parameters
    ----------
    candidates : list of str
        List of candidate names to validate.
    length_prefix : tuple of int, optional
        Valid candidate count range. Default is (2, 3, 4, 5, 6, 7, 8, 9).

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
    >>> validate_candidates(["Alice"])
    Traceback (most recent call last):
    ...
    ValueError: List must be between 2 and 9 candidates
    >>> validate_candidates(["Alice", "Alice", "Bob"])
    Traceback (most recent call last):
    ...
    ValueError: Candidate names must be unique
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
    >>> _validate_candidate_arg("alice")
    'Alice'
    >>> _validate_candidate_arg("  Bob!  ")
    'Bob'
    >>> _validate_candidate_arg("John Smith")
    'John Smith'
    >>> _validate_candidate_arg("Alice123")
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
    Ensures the value is a valid positive integer.

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
    
    return voters_int


def _validate_votes(voters_int: int | None = None, votes: list[str] | None = None) -> Iterator[str]:
    """
    Validate and yield individual votes.

    Operates in two modes: interactive (prompts for each vote) or batch
    (processes a provided list). Invalid votes are skipped with a warning.

    Parameters
    ----------
    voters_int : int or None, optional
        Number of voters for interactive mode. Required if votes is None.
    votes : list of str or None, optional
        Pre-defined vote list for testing/batch mode. If provided,
        voters_int is ignored.

    Yields
    ------
    str
        Valid vote strings, normalized to Title Case.

    Raises
    ------
    ValueError
        If votes is None and voters_int is also None.

    Notes
    -----
    This is a private generator function. Invalid votes (empty, non-alphabetic)
    are silently skipped in batch mode, or logged as warnings in interactive mode.

    Examples
    --------
    >>> list(_validate_votes(votes=["alice", "BOB", "charlie"]))
    ['Alice', 'Bob', 'Charlie']
    >>> list(_validate_votes(votes=["alice", "123", "bob"]))
    ['Alice', 'Bob']
    >>> list(_validate_votes(votes=None, voters_int=None))
    Traceback (most recent call last):
    ...
    ValueError: voters_int required for interative mode
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
    Collect and tally votes for candidates.

    Processes votes either interactively or from a provided list, counting
    only valid votes that match registered candidates.

    Parameters
    ----------
    clean_candidates : list of str
        List of valid candidate names to accept votes for.
    voters_int : int or None, optional
        Number of voters for interactive mode.
    votes : list of str or None, optional
        Pre-defined vote list for testing/batch mode.

    Returns
    -------
    defaultdict of {str: int}
        Dictionary mapping candidate names to their vote counts.
        Only candidates with at least one vote are included.

    Raises
    ------
    ValueError
        If no valid votes are found or all votes are invalid.

    Examples
    --------
    >>> assign_votes(["Alice", "Bob"], votes=["Alice", "Alice", "Bob"])
    defaultdict(<class 'int'>, {'Alice': 2, 'Bob': 1})
    >>> assign_votes(["Alice", "Bob"], votes=["Charlie", "David"])
    Traceback (most recent call last):
    ...
    ValueError: All votes were invalid. No count was processed
    >>> assign_votes(["Alice", "Bob"], votes=[])
    Traceback (most recent call last):
    ...
    ValueError: No valid votes found!
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
    Determine the winner(s) from vote tallies.

    Identifies the candidate(s) with the highest vote count. In case of
    a tie, yields all candidates sharing the maximum votes.

    Parameters
    ----------
    votes_dict : defaultdict of {str: int}
        Dictionary mapping candidate names to vote counts.

    Yields
    ------
    tuple of (str, int)
        Tuples of (candidate_name, vote_count) for each winner.

    Examples
    --------
    >>> dict(count_winners(defaultdict(int, {"Alice": 3, "Bob": 2})))
    {'Alice': 3}
    >>> dict(count_winners(defaultdict(int, {"Alice": 3, "Bob": 3, "Charlie": 1})))
    {'Alice': 3, 'Bob': 3}
    >>> list(count_winners(defaultdict(int, {"Alice": 5})))
    [('Alice', 5)]
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
    Main entry point for the plurality voting CLI.

    Parses command-line arguments, validates candidates, collects votes,
    tallies results, and announces the winner(s).

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