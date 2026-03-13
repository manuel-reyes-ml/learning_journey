"""
"""

# =============================================================================
# IMPORTS
# =============================================================================

from __future__ import annotations
from logging.handlers import RotatingFileHandler
from dataclasses import dataclass, field
from typing import Final, Pattern, NamedTuple, overload
from enum import IntEnum, StrEnum, unique
from pathlib import Path
import argparse
import logging
import random
import sys
import re


# =============================================================================
# MODULE CONFIGURATION
# =============================================================================

# =====================================================
# Exports
# =====================================================

# Controls: from 'module' import *
__all__ = []


# =====================================================
# Module Level Constants
# =====================================================

# For random selection and generations build up
ALLELES: Final[list[str]] = ['A', 'B', 'O']
DEFAULT_GEN_COUNT: Final[int] = 3

alleles_available: str = ", ".join(ALLELES)

# For final output format
INDENT_LENGTH: Final[int] = 4


# =====================================================
# Type Aliases
# =====================================================

type SeedTypes = str | int | float | None


# =====================================================
# Random Generator
# =====================================================

# Production pattern: seed at the top
random.seed()  # Uses system entropy - different each run


# =====================================================
# Dataclasses
# ===================================================== 

@dataclass(frozen=True, slots=True)
class FileHandlerConfig:
    """
    """
    LEVEL_DEFAULT: Final[int] = logging.INFO
    ENCODING: Final[str] = "utf-8"
    BACKUP_COUNT: Final[int] = 3
    FILE_MB: Final[int] = 5      # megabytes
    MEGABYTE: Final[int] = 1024  # kilobytes
    KILOBYTE: Final[int] = 1024  # bytes
    
    @property
    def max_log_bytes(self) -> int:
        """
        """
        return self.FILE_MB * self.MEGABYTE * self.KILOBYTE


@dataclass(frozen=True, slots=True)
class FileDirectories:
    """
    """
    CUR_DIR: Final[Path] = Path(__file__).resolve().parent
    LOG_DIR: Final[Path] = CUR_DIR / "py_log"
    
    def create_log_fname(self) -> str:
        """
        """
        return f"{self.CUR_DIR.name}.log"
    
    @property
    def log_file(self) -> Path:
        """
        """
        return self.LOG_DIR / self.create_log_fname()
    

@dataclass
class Person:
    """
    """
    # Here, lambda is a zero-argument function that, when called,
    # creates and returns a fresh [None, None] list.
    # Each person always has two elements: Person (parents) or None slots
    parents: list[Person | None] = field(default_factory=lambda: [None, None])
    alleles: list[str] = field(default_factory=list)  # on each call creates emtpy list[]
    
    # ❌ DANGEROUS — every Person shares the SAME list object
    # parents: list[Person | None] = [None, None]

    # If you mutated one person's parents, every person's parents would change
    # because they all point to the same list in memory. This is the mutable default
    # argument trap — same pattern used in BMP filter work.

    # default_factory solves this by requiring a callable (a function). 
    # Every time a new Person is created, dataclasses calls that function
    # to produce a brand-new, independent list:
    #   Person A gets created → calls lambda → fresh [None, None]
    #   Person B gets created → calls lambda → different fresh [None, None]
    #   Person C gets created → calls lambda → another fresh [None, None]
    

# =====================================================
# Dataclass Instantiation
# =====================================================

fhandler_config = FileHandlerConfig()
file_dirs = FileDirectories()


# =====================================================
# Other Class Configuration
# =====================================================

class NumberPattern:
    """
    """
    INT_PATTERN: re.Pattern = re.compile(r"^-?\d+$")
    FLOAT_PATTERN: re.Pattern = re.compile(r"^-?\d+\.?\d*$")
    

# Exit codes (Unix standard)
@unique  # Ensure no duplicate values
class ExitCode(IntEnum):
    """
    Process exit codes following Unix conventions.

    Attributes
    ----------
    SUCCESS : int
        Normal termination (0).
    FAILURE : int
        General error (1).
    KEYBOARD_INTERRUPT : int
        Terminated by Ctrl+C (130).
    """
    SUCCESS = 0
    FAILURE = 1
    KEYBOARD_INTERRUPT = 130
    
    
@unique
class ValidatorName(StrEnum):
    """
    """
    SEED = "Seed"
    GENERATION = "Generations"


# =====================================================
# Logging Configuration
# =====================================================

# Inherits from Python´s built-in Formatter
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
        logging.DEBUG:     "\033[90m",   # Gray
        logging.INFO:      "\033[92m",   # Green
        logging.WARNING:   "\033[93m",   # Yellow
        logging.ERROR:     "\033[91m",   # Red
        logging.CRITICAL:  "\033[1;91m", # Bold Red
    }
    RESET: Final[str] = "\033[0m"
    
    # Override the parent's format method
    def format(self, record) -> str:
        # Step 1: Get the color for this log level
        color = self.COLORS.get(record.levelno, self.RESET)
        
        # Step 2: Format the message normally first
        # This produces: "14:30:45 : INFO : Your message here"
        # super() calls PARENT's format() method
        message = super().format(record) 
        
        # Step 3: Wrap with color codes
        return f"{color}{message}{self.RESET}"
    

# Set up logging
# Move configuration into a setup function called by main()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)  # Let handlers decide their own level!


# =============================================================================
# INTERNAL HELPER FUNCTIONS
# =============================================================================

def _validate_number(
    number: int | float,
    *,
    func_name: str | None = None,
) -> int | float:
    """
    """
    func_name = func_name if func_name else "Number"
    
    if number <= 0:
        raise argparse.ArgumentTypeError(f"{func_name} must be positive")
    return number


def validate_generations(
    generations: str | None = None,
    func_name = ValidatorName.GENERATION,
) -> int:
    """
    """
    if not generations:
        raise argparse.ArgumentTypeError("Generations cannot be empty")
    
    if not generations.strip().isdigit():
        raise argparse.ArgumentTypeError(f"Generations must be numeric. Got {generations!r}")

    _validate_number(int(generations), func_name=func_name)
    return int(generations.strip())


def validate_seed(
    seed: SeedTypes = None,
    func_name = ValidatorName.SEED,
    match_number: type[NumberPattern] = NumberPattern,
) -> SeedTypes:
    """
    """                 
    if isinstance(seed, str):
        if match_number.INT_PATTERN.match(seed.strip()):
            return _validate_number(int(seed.strip()), func_name=func_name)
        
        elif match_number.FLOAT_PATTERN.match(seed.strip()):
            return _validate_number(float(seed.strip()), func_name=func_name)
        
        else:
            return seed.strip()
        
    elif isinstance(seed, (int, float)):
        return _validate_number(seed, func_name=func_name)
    else:
        return None
            

def config_logging(
    log_to_file: bool = True,
    console_verbose: bool = False,
    file_dirs: FileDirectories = file_dirs,
    fhandler_config: FileHandlerConfig = fhandler_config,
    formatter_class: type[logging.Formatter] = ColoredFormatter,
) -> None:
    """
    """
    # Prevent duplicate handlers if this function is
    # called multiple times (e.g. pytest).
    if logger.hasHandlers():
        logger.handlers.clear()
        
    level = logging.DEBUG if console_verbose else fhandler_config.LEVEL_DEFAULT
        
    console_handler = logging.StreamHandler(sys.stderr)
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter_class(
        fmt='%(asctime)s : %(levelname)s : %(message)s',
        datefmt='%H:%M:%S',
    ))
    
    if log_to_file:
        # parents=True: create any missing parent directories
        # exist_ok=True: no error if directory already exists
        file_dirs.LOG_DIR.mkdir(parents=True, exist_ok=True)
    
        file_handler = RotatingFileHandler(
            filename=file_dirs.log_file,
            maxBytes=fhandler_config.max_log_bytes,
            backupCount=fhandler_config.BACKUP_COUNT,
            encoding=fhandler_config.ENCODING,
        )
        file_handler.setLevel(logging.DEBUG)
        # %(name)s shows module name (inheritance)
        file_handler.setFormatter(logging.Formatter(
            fmt='%(asctime)s : %(levelname)s : %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S',
        ))
        logger.addHandler(file_handler)
    

def random_allele(alleles: list[str] = ALLELES) -> str:
    """
    """
    # Picks one random element from the sequence
    return random.choice(alleles)


# =============================================================================
# CORE FUNCTIONS
# =============================================================================

def create_family(generations: int = DEFAULT_GEN_COUNT) -> Person:
    """
    """
    if generations <= 0:
        raise ValueError("Generations must be positive")
    
    # ------------------------------------------------------------------ #
    # STEP 1: Create a new person — every recursive call starts here.
    # Whether this person is a grandparent or a child, they all begin
    # as a blank Person. The if/else below decides HOW to fill them in.
    # ------------------------------------------------------------------ #
    person = Person()
    
    # ------------------------------------------------------------------ #
    # STEP 2: Decide — are we at the oldest generation yet?
    #
    # Think of "generations" as a countdown:
    #   create_family(3) → child      (has parents)
    #   create_family(2) → parent     (has parents)
    #   create_family(1) → grandparent (NO parents — BASE CASE)
    #
    # When generations == 1, we've reached the oldest generation.
    # This is the BASE CASE — the recursion STOPS here.
    # ------------------------------------------------------------------ #
    if generations == 1:
        # -------------------------------------------------------------- #
        # BASE CASE: Oldest generation (grandparents)
        #
        # - No parents exist for them → stays [None, None] from default
        # - Alleles are assigned randomly — this is where randomness
        #   ENTERS the family tree. All other generations inherit FROM
        #   these random starting points.
        # -------------------------------------------------------------- #
        person.alleles = [random_allele(), random_allele()]
        
    else:
        # -------------------------------------------------------------- #
        # RECURSIVE CASE: This person has parents
        #
        # KEY INSIGHT: We must build the parents BEFORE we can assign
        # this person's alleles, because their alleles are INHERITED
        # from the parents. So parents must exist first.
        #
        # "generations - 1" is what makes recursion work — each call
        # gets a SMALLER number, guaranteeing we eventually hit the
        # base case (generations == 1). Without this shrinkage,
        # the function would call itself forever → RecursionError.
        # -------------------------------------------------------------- #
        
        
        # Create parent_0 — this single call triggers a FULL chain:
        # If generations=3, this calls create_family(2), which calls
        # create_family(1) twice for grandparents. By the time this
        # line finishes, parent_0 is FULLY BUILT with their own
        # parents and alleles already assigned.
        parent_0 = create_family(generations - 1)
        
        # Create parent_1 — same chain, independent branch.
        # This is why we get 2 parents, 4 grandparents, 8 great-grands.
        # Each level DOUBLES because every person creates TWO parents.
        parent_1 = create_family(generations -1)

        # -------------------------------------------------------------- #
        # Link parents to this person — Python equivalent of C's:
        #   p->parents[0] = parent0;
        #   p->parents[1] = parent1;
        # -------------------------------------------------------------- #
        person.parents = [parent_0, parent_1]
        
        # -------------------------------------------------------------- #
        # Inherit alleles — each parent randomly passes ONE of their
        # two alleles to this child.
        #
        # _random_allele(parent_0.alleles) looks at e.g. ['A', 'O']
        # and picks either 'A' or 'O' with equal probability.
        #
        # alleles[0] always comes from parent_0
        # alleles[1] always comes from parent_1
        # -------------------------------------------------------------- #
        person.alleles = [
            random_allele(parent_0.alleles),
            random_allele(parent_1.alleles),
        ]
    
    # ------------------------------------------------------------------ #
    # STEP 3: Return the fully built person.
    #
    # For the base case: returns a grandparent with random alleles.
    # For the recursive case: returns a person with parents linked
    #   and alleles inherited.
    #
    # This returned value is what gets assigned to "parent_0" or
    # "parent_1" in the CALLER's frame — that's how the tree
    # connects itself together.
    # ------------------------------------------------------------------ #
    return person


def print_family(
    person: Person | None,
    *,
    generation: int = 0,
    indent_length: int = INDENT_LENGTH,
) -> None:
    """
    """
    # ------------------------------------------------------------------ #
    # BASE CASE: If person is None, there's nothing to print.
    #
    # This happens when we try to print the parents of the oldest
    # generation — their parents are [None, None]. Without this check,
    # we'd crash trying to access None.alleles.
    #
    # Compare to create_family's base case:
    #   create_family stops when generations == 1  (countdown hits bottom)
    #   print_family stops when person is None     (tree has no more nodes)
    # Different triggers, same purpose — STOP the recursion.
    # ------------------------------------------------------------------ #
    if person is None:
        return
    
    # ------------------------------------------------------------------ #
    # STEP 1: Build the indentation string.
    #
    # Each generation level indents further to show depth visually:
    #   Generation 0 (child):       no indent      ""
    #   Generation 1 (parent):      4 spaces       "    "
    #   Generation 2 (grandparent): 8 spaces        "        "
    #
    # This is just string multiplication — " " * 4 = "    "
    # Same logic as the C version's for-loop printing spaces.
    # ------------------------------------------------------------------ #
    indent = " " * (generation * indent_length)
    
    # ------------------------------------------------------------------ #
    # STEP 2: Determine the label based on generation number.
    #
    # Generation 0 → "Child"
    # Generation 1 → "Parent"
    # Generation 2 → "Grandparent"
    # Generation 3 → "Great-Grandparent"
    # Generation 4 → "Great-Great-Grandparent"
    #
    # For generation 3+, we prepend "Great-" for each level beyond 2.
    # The count of "Great-" prefixes is (generation - 2).
    #   generation 3 → 1 "Great-"  → "Great-Grandparent"
    #   generation 4 → 2 "Great-"  → "Great-Great-Grandparent"
    # ------------------------------------------------------------------ #
    if generation == 0:
        label = "Child"
    elif generation == 1:
        label = "Parent"
    else:
        # "Great-" repeated (generation - 2) times, then "Grandparent"
        # String multiplication again: "Great-" * 1 = "Great-"
        #                              "Great-" * 2 = "Great-Great-"
        label = "Great-" * (generation-2) + "Grandparent"
    
    # ------------------------------------------------------------------ #
    # STEP 3: Print this person's info.
    #
    # Combines: indentation + label + generation number + both alleles.
    # person.alleles[0] and [1] are single chars like 'A', 'O', 'B'.
    # Printing them side by side gives "AO", "BB", "OA", etc.
    # ------------------------------------------------------------------ #
    print(
        f"{indent}{label} (Generation {generation}): "
        f"blood type {person.alleles[0]}{person.alleles[1]}"
    )
    
    # ------------------------------------------------------------------ #
    # STEP 4: Recurse into both parents.
    #
    # This is the RECURSIVE CASE — we print parent_0 first, then
    # parent_1. Each call increases generation by 1, which:
    #   - Adds more indentation (deeper = further right)
    #   - Changes the label (Parent → Grandparent → Great-...)
    #
    # Compare to create_family's recursion:
    #   create_family passes (generations - 1)  → counting DOWN
    #   print_family passes (generation + 1)    → counting UP
    #
    # Why opposite directions?
    #   create_family counts DOWN to know when to STOP building.
    #   print_family counts UP to know how deep we ARE for display.
    #
    # When we reach a grandparent whose parents are [None, None],
    # these calls hit the base case (person is None) and return
    # immediately — no crash, no infinite loop.
    # ------------------------------------------------------------------ #
    print_family(person.parents[0], generation=generation + 1)
    print_family(person.parents[1], generation=generation + 1)
    

# =============================================================================
# CLI ENTRY POINT
# =============================================================================

def main(argv: list[str] | None = None) -> ExitCode:
    """
    """
    parser = argparse.ArgumentParser(
        description="Create family tree selecting random alleles from parent to child"
                    f"Oldest generation gets random alleles from Constant: {alleles_available}"
    )
    parser.add_argument(
        "-g","--generations",
        type=validate_generations,
        default=DEFAULT_GEN_COUNT,
        help="Enter generations as a positive number. "
             f"Default is {DEFAULT_GEN_COUNT}",
    )
    parser.add_argument(
        "-s", "--seed",
        type=validate_seed,
        help="Enter seed as a positive number or "
             "string to set a deterministic pattern",
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose (debug) output",
    )
    parser.add_argument(
        "--no-log-file",
        action="store_true",
        help="Disable file logging (console only)",
    )
    
    args = parser.parse_args(argv)
    
    config_logging(
        console_verbose=args.verbose,
        log_to_file=not args.no_log_file,
    )
    
    if args.verbose:
        logger.debug("Verbose mode enabled (console debug output)")
        
    if args.seed:
        random.seed(args.seed)
        
    try:
        person = create_family(args.generations)
        print_family(person, generation=0)
    
    except KeyboardInterrupt:
        logger.warning("\nInterrupted by user. Exiting.")
        return ExitCode.KEYBOARD_INTERRUPT
    
    except ValueError as e:
        logger.error(f"Process Error: {e}")
        return ExitCode.FAILURE
    
    except Exception as e:
        # Behaves like .error but includes TraceBack info
        logger.exception(f"Unexpected Error: {e}")
        return ExitCode.FAILURE
    
    return ExitCode.SUCCESS



if __name__ == "__main__":
    sys.exit(main())