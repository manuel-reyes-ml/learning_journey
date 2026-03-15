"""
"""

# =============================================================================
# IMPORTS
# =============================================================================

from __future__ import annotations
from typing import Any, Final, Callable, overload
from logging.handlers import RotatingFileHandler
from functools import update_wrapper, wraps
from enum import IntEnum, StrEnum, unique
from dataclasses import dataclass, field
from pathlib import Path
import argparse
import logging
import random
import time
import sys
import re  # Python's built-in library for working with regex


# =============================================================================
# MODULE CONFIGURATION
# =============================================================================

# =====================================================
# Exports
# =====================================================

# Controls: from 'module' import *
__all__ = [
    # Core functions
    "create_family",
    "print_family",
    # Types
    "ValidatorName",
    "ExitCode",
    # Configuration (useful for custom workflows)
    "FileHandlerConfig",
    "FileDirectories",
    "GenBuildConstants",
    "NumberPattern",
    "Person",
    #Module-level constants
    "INDENT_LENGTH",
]


# =====================================================
# Module Level Constants
# =====================================================

# For final output format
INDENT_LENGTH: Final[int] = 4


# =====================================================
# Type Aliases
# =====================================================

type SeedTypes = str | int | float | None
# When using isinstance(var, None):
#   None isn't a type-it's a value. Its type is
#   NoneType(from types library, Python 3.10+).

#   type(None) is more used in production code,
#   since doesn't require an import.


# =====================================================
# Random Generator
# =====================================================

# Production pattern: seed at the top
random.seed()  # Uses system entropy - different each run

# seed() accepts any hashable value, including 0,
# negatives, strings, and even none.


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
    
    
# For random selection and generations build up
@dataclass(frozen=True, slots=True)
class GenBuildConstants:
    """
    """
    # For dataclass 'frozen' need to use hashable structure
    # [str, ...] -> any number of strings values
    ALLELES: Final[tuple[str, ...]] = ('A', 'B', 'O')
    DEFAULT_GEN_COUNT: Final[int] = 3

    def __post_init__(self) -> None:
        if self.DEFAULT_GEN_COUNT <= 0:
            raise ValueError("Generations must be positive (>0)")
        
    @property
    def alleles_available(self) -> str:
        """
        """
        return ", ".join(self.ALLELES)


@dataclass
class Person:
    """
    """
    # Here, lambda is a zero-argument function that, when called,
    # creates and returns a fresh [None, None] list.
    # Each person always has two elements: Person (parents) or None slots
    parents: list[Person | None] = field(default_factory=lambda: [None, None])
    alleles: tuple[str, ...] = field(default_factory=tuple)  # on each call creates emtpy tuple()
    
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

try:
    gen_constants = GenBuildConstants()
except ValueError as e:
    sys.exit(f"Error: Invalid generation setting: {e}\n")


# =====================================================
# Other Class Configuration
# =====================================================

# With NamedTuple, the fields on the class itself are
# descriptors (_tuplegetter), not the actual values.
class NumberPattern:
    """
    """
    INT_PATTERN: re.Pattern = re.compile(r"^-?\d+$")
    FLOAT_PATTERN: re.Pattern = re.compile(r"""
        ^       # Start of the string
        -?      # negative sign (optional)
        \d+     # one or more digits
        \.      # decimal point (literal)
        \d*     # zero or more decimal digits
        $       # no more values at end of string
    """, re.VERBOSE)
    # re.VERBOSE is the Production standard for complex regex
    # With regular class no need to instantiate to access values
    
    # re.compile() pre-compiles a pattern into a reusable Pattern object.
    # This is faster when you use the same pattern multiple times (loops).
    #
    # ┌──────────────────────────────────────────────────────────────────┐
    # │  WITHOUT compile (recompiles every iteration):                   │
    # │                                                                  │
    # │  for row in million_rows:                                        │
    # │      re.search(r"\d{3}-\d{4}", row)  ← compiles EACH time      │
    # │                                                                  │
    # │  WITH compile (compile once, use many times):                    │
    # │                                                                  │
    # │  phone_pattern = re.compile(r"\d{3}-\d{4}")  ← compile ONCE    │
    # │  for row in million_rows:                                        │
    # │      phone_pattern.search(row)  ← uses cached pattern           │
    # └──────────────────────────────────────────────────────────────────┘

# Core functions from 're' module (more info at the end)
#   re.search(pattern, string)    # Find first match anywhere in string
#   re.match(pattern, string)     # Match only at the beginning
#   re.findall(pattern, string)   # Return ALL matches as a list
#   re.sub(pattern, repl, string) # Replace matches with new text
#   re.split(pattern, string)     # Split string at each match
 
 
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
    
# unique checks values regardless or
# Enum type: InEnum, StrEnum, Enum.    
@unique
class ValidatorName(StrEnum):
    """
    """
    SEED = "Seed"
    GENERATION = "Generations"
# Duplicate values get caught at class definition time.


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
# DECORATORS
# =============================================================================

# Sometimes you want a decorator that's a CLASS, not a function.
# @wraps doesn't work as neatly here — use update_wrapper.
class CountCalls:
    """
    """
    def __init__(self, func: Callable) -> None:
        update_wrapper(self, func)  # Copy func´s metadata to self
        self.func = func
        self.count = 0
        
    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        self.count += 1
        return self.func(*args, **kwargs)
    
    # If someone imports and uses random_allele across multiple create_family
    # calls (e.g., in tests), the count accumulates across ALL calls.
    def reset_count(self) -> None:
        """Reset the call counter (useful for testing)."""
        self.count = 0

# @wraps(func) is actually syntactic sugar for update_wrapper().
# They do the same thing, but update_wrapper gives you more control.
#
# @wraps(func)  ←→  update_wrapper(wrapper, wrapped=func)
#
# You would use update_wrapper directly when:
# 1. You're not using a decorator pattern (e.g., factory functions)
# 2. You need to customize WHICH attributes get copied
# 3. You're building a class-based decorator


def timer(func: Callable) -> Callable:
    """
    """
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        logger.debug(f"{func.__name__} took {elapsed:.6f}s")
        return result 
    # Without @wraps(func) on wrapper, the decorated function's __name__ becomes
    # "wrapper", __doc__ becomes None, and tracebacks are useless. @wraps copies
    # the original's identity onto the replacement.
    return wrapper    

# The simple rule: If your decorator has def wrapper (or any inner function) that
# gets returned instead of the original, you need @wraps. If it returns the original
# function unchanged, you don't.


# =============================================================================
# INTERNAL HELPER FUNCTIONS
# =============================================================================

# Use overload when return Type depends on input Type for type checker!
@overload
def _validate_number(number:int, *, func_name: str | None = None) -> int: ...

@overload
def _validate_number(number: float, *, func_name: str | None = None) -> float: ...

def _validate_number(
    number: int | float,
    *,
    func_name: str | None = None,
) -> int | float:
    """
    """
    func_name = func_name if func_name else "Number"
    
    if number <= 0:
        raise argparse.ArgumentTypeError(
            f"{func_name} must be positive. Got {number!r}"
        )
    return number


def validate_generations(
    generations: str | int | None = None,
    func_name = ValidatorName.GENERATION,
) -> int:
    """
    """
    if generations is None or generations == "":
        raise argparse.ArgumentTypeError("Generations cannot be empty")
        
    if isinstance(generations, str):
        if not generations.strip().isdigit():
            raise argparse.ArgumentTypeError(
                f"Generations must be a positive integer. Got {generations!r}"
            )
        # Validate integer in case is zero(0)
        return _validate_number(int(generations.strip()), func_name=func_name)
        
    return _validate_number(generations, func_name=func_name)


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
    logger.addHandler(console_handler)
    
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
            # %(name)s would show module name (inheritance)
            fmt='%(asctime)s : %(levelname)s : %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S',
        ))
        logger.addHandler(file_handler)
    

@CountCalls  # random_allele is no longer a function-it's a CountCalls instance.
def random_allele(alleles: tuple[str, ...] = gen_constants.ALLELES) -> str:
    """
    """
    # Picks one random element from the sequence
    return random.choice(alleles)

# Step 1: Decoration happens at definition time
#   Python translates @ syntax into this:
#   random_allele = CountCalls(random_allele)
#                   ^^^^^^^^^^^^^^^^^^^^^^^^^^
#                   Calling the CLASS → triggers __init__

# Step 2: Calling the decorated function triggers __call__
#   random_allele()
#                ^^
#   random_allele is now a CountCalls INSTANCE
#   Putting () after an instance triggers __call__:
#       1. self.count += 1         → count goes from 0 → 1
#       2. self.func("A", "B")     → runs original random_allele
#       3. Returns the result


# =============================================================================
# CORE FUNCTIONS
# =============================================================================

def _build_person(generations: int) -> Person:
    """
    """
    # Guard for programmatic use — CLI validation handles this for end users
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
        person.alleles = (random_allele(), random_allele())
        
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
        parent_0 = _build_person(generations - 1)
        
        # Create parent_1 — same chain, independent branch.
        # This is why we get 2 parents, 4 grandparents, 8 great-grands.
        # Each level DOUBLES because every person creates TWO parents.
        parent_1 = _build_person(generations - 1)

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
        person.alleles = (
            random_allele(parent_0.alleles),
            random_allele(parent_1.alleles),
        )
    
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


def _print_person(person: Person | None, generation: int, indent_length: int) -> None:
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
    match generation:  # Structural pattern matching - more powerful than if/elif
        case 0:
            label = "Child"
        case 1:
            label = "Parent"
        case _:  # Default case (wildcard)
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
    _print_person(
        person.parents[0],
        generation + 1,
        indent_length,
    )
    _print_person(
        person.parents[1],
        generation + 1,
        indent_length,
    )


# =====================================================
# Callers For Recursive Functions
# =====================================================

@timer
def create_family(
    generations: int = gen_constants.DEFAULT_GEN_COUNT,
) -> Person:
    """
    """
    return _build_person(generations)


@timer
def print_family(
    person: Person | None = None,
    *,
    generation: int = 0,
    indent_length: int = INDENT_LENGTH,
) -> None:
    """
    """
    _print_person(person, generation, indent_length)
# No need to define a Callable parameter in func signature to pass builders, since the
# intention is not that a user can pass a function in CLI, but the function runs with
# its predetermined caller behind the scenes.

# =============================================================================
# CLI ENTRY POINT
# =============================================================================

def main(argv: list[str] | None = None) -> ExitCode:
    """
    """
    parser = argparse.ArgumentParser(
        description="Create family tree selecting random alleles "
                    "from parent to child. Oldest generation gets "
                    f"random alleles from Constant: {gen_constants.alleles_available}"
    )
    parser.add_argument(
        "-g", "--generations",
        type=validate_generations,
        default=gen_constants.DEFAULT_GEN_COUNT,
        help="Enter generations as a positive number. "
             f"Default is {gen_constants.DEFAULT_GEN_COUNT}",
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
        logger.info(f"Seed successfully set to {args.seed!r}")
        random.seed(args.seed)
        
    try:
        person = create_family(args.generations)
        logger.debug(f"Random allele was called {random_allele.count!r} times")
        logger.info(f"{args.generations} Gen Family Tree created successfully....")
        logger.info("Printing family tree now......\n")
        
        print_family(person, generation=0)
        logger.info("Family Tree printed successfully")
        return ExitCode.SUCCESS
    
    except KeyboardInterrupt:
        logger.warning("Interrupted by user. Exiting.")
        return ExitCode.KEYBOARD_INTERRUPT
    
    except ValueError as e:
        logger.error(f"Process Error: {e}")
        return ExitCode.FAILURE
    
    except Exception as e:
        # Behaves like .error but includes TraceBack info
        logger.exception(f"Unexpected Error: {e}")
        return ExitCode.FAILURE
    
    finally:  # Always runs (error or no erros)
        logger.warning("\nProgram terminated. Exiting...\n")


if __name__ == "__main__":
    sys.exit(main())
    
    
    
# ================================================================== #
#                   REGEX (re module) QUICK REFERENCE                  #
# ================================================================== #
#
# re.search(pattern, string)
#   → Returns: Match object | None
#   → Behavior: Finds FIRST match ANYWHERE in string
#   → Example: re.search(r"\d+", "abc 123 def")  → Match '123'
#   → Example: re.search(r"\d+", "no numbers")   → None
#
# re.match(pattern, string)
#   → Returns: Match object | None
#   → Behavior: Matches only at the BEGINNING of string
#   → Example: re.match(r"\d+", "123 abc")   → Match '123'
#   → Example: re.match(r"\d+", "abc 123")   → None
#
# re.fullmatch(pattern, string)
#   → Returns: Match object | None
#   → Behavior: ENTIRE string must match the pattern
#   → Example: re.fullmatch(r"\d+", "123")     → Match '123'
#   → Example: re.fullmatch(r"\d+", "123 abc") → None
#
# re.findall(pattern, string)
#   → Returns: list[str] (all matches) | [] (empty list if none)
#   → Behavior: Finds ALL non-overlapping matches
#   → Example: re.findall(r"\d+", "abc 12 def 345") → ['12', '345']
#   → Example: re.findall(r"\d+", "no numbers")     → []
#
# re.sub(pattern, repl, string)
#   → Returns: str (new string with matches replaced)
#   → Behavior: Replaces ALL matches with replacement text
#   → Example: re.sub(r"\d+", "X", "abc 12 def 345") → 'abc X def X'
#   → Example: re.sub(r"\d+", "X", "no numbers")     → 'no numbers'
#
# re.split(pattern, string)
#   → Returns: list[str] (string split at each match)
#   → Behavior: Splits string wherever the pattern matches
#   → Example: re.split(r"\s+", "hello   world  foo") → ['hello', 'world', 'foo']
#   → Example: re.split(r",", "a,b,c")                → ['a', 'b', 'c']
#
# re.compile(pattern)
#   → Returns: re.Pattern object (pre-compiled regex)
#   → Behavior: Compile once, reuse many times (faster in loops)
#   → Example: pattern = re.compile(r"\d+")
#              pattern.match("123")      → Match '123'
#              pattern.findall("a 1 b 2") → ['1', '2']
#
# ------------------------------------------------------------------ #
#                     MATCH OBJECT METHODS                             #
# ------------------------------------------------------------------ #
#
# match.group()    → Returns the matched string: '123'
# match.start()    → Returns start index of match: 4
# match.end()      → Returns end index of match: 7
# match.span()     → Returns (start, end) tuple: (4, 7)
#
# ------------------------------------------------------------------ #
#                   COMMON PATTERN CHARACTERS                          #
# ------------------------------------------------------------------ #
#
# \d    → Any digit [0-9]
# \D    → Any NON-digit
# \w    → Any word char [a-zA-Z0-9_]
# \W    → Any NON-word char
# \s    → Any whitespace (space, tab, newline)
# \S    → Any NON-whitespace
# .     → Any character except newline
# ^     → Start of string
# $     → End of string
# +     → One or more
# *     → Zero or more
# ?     → Zero or one (optional)
# {n}   → Exactly n times
# {n,m} → Between n and m times
# []    → Character class: [aeiou], [0-9], [A-Za-z]
# |     → OR: (cat|dog)
# ()    → Capture group
# \.    → Literal dot (escaped)
#
# ================================================================== #