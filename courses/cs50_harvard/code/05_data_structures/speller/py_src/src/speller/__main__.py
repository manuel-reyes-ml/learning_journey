"""CLI entry point for the speller package.

Runs when the user executes::

    $ python -m speller [dictionary] text
    $ speller [dictionary] text          (via pyproject.toml scripts)

This module is the COMPOSITION ROOT — the single place that:
1. Parses CLI arguments
2. Configures logging (before any speller logic runs)
3. Creates concrete implementations (HashTableDictionary)
4. Injects them into the orchestrator (run_speller)
5. Handles display and exit codes

No other module imports from __main__.py. This module imports
from everything else. It's the top of the dependency chain.

Dependency Chain (complete picture)
------------------------------------
    config.py            ← constants, enums (bottom — no internal imports)
    protocols.py         ← DictionaryProtocol (bottom — no internal imports)
    benchmarks.py        ← timer, timed, BenchmarkResult (imports nothing internal)
    logger.py            ← config_logging, ColoredFormatter (imports config)
    dictionary.py        ← HashTableDictionary (imports config)
    text_processor.py    ← extract_words (imports config)
    speller.py           ← run_speller, SpellerResult (imports protocols, benchmarks, text_processor)
    __main__.py          ← THIS FILE (imports everything — composition root)

CS50 CLI Behavior
------------------
Matches speller.c usage::

    Usage: ./speller [DICTIONARY] text

    argc == 2:  dictionary defaults to dictionaries/large, argv[1] is text
    argc == 3:  argv[1] is dictionary, argv[2] is text
    otherwise:  print usage and exit with code 1
"""

# =============================================================================
# IMPORTS
# =============================================================================

from __future__ import annotations

import sys 


# =====================================================
# Impor Guard
# =====================================================

# __main__.py is the FRONT DOOR — if imports fail, give a friendly
# error message and exit. This is the ONE place where sys.exit()
# on ImportError is correct, because the user explicitly ran the
# program and expects it to either work or explain why it can't.
#
# Every other module lets ImportError propagate upward to here.
try:
    from dataclasses import replace
    from pathlib import Path
    import argparse
    import logging
    import string
    
    from speller.benchmarks import BenchmarkResult
    from speller.config import ExitCode,  SpellerArgs, file_dirs, default_fnames
    from speller.load_dictionary import load_dictionary
    from speller.logger import configure_logging
    from speller.register import dicts
    from speller.speller import run_speller, REPORT, SpellerResult
    
except ImportError as e:
    sys.exit(f"Error missing speller module.\nDetails: {e}")
    

# =============================================================================
# LOGGER SETUP
# =============================================================================

# Logger is created here but NOT configured yet.
# config_logging() is called INSIDE main() after argparse determines
# the verbosity level. This ensures --verbose flag controls log output
logger = logging.getLogger(__name__)



# =============================================================================
# CONSTANTS
# =============================================================================

ops_list: str = ", ".join(dicts.keys())


# =============================================================================
# INTERNAL HELPER FUNCTIONS
# =============================================================================

def _validate_ops(ops_names: list[str]) -> list[str]:
    """Validate and normalise requested backend operation names.
 
    Strips whitespace and punctuation from each name, lower-cases it,
    and checks it against the live :data:`~speller.register.dicts`
    registry.  Expands the special value ``"all"`` into every
    registered key.
 
    Parameters
    ----------
    ops_names : list of str
        Raw operation names from the ``-o`` / ``--operations`` argument.
 
    Returns
    -------
    list of str
        Cleaned, validated operation names ready for iteration.
        Order matches the input (or the registry insertion order for
        ``"all"``).
 
    Raises
    ------
    KeyError
        If any name (after cleaning) is not in :data:`dicts` and is
        not the literal string ``"all"``.  The error message lists all
        available operations.
 
    Examples
    --------
    >>> _validate_ops(["hash"])
    [\'hash\']
    >>> _validate_ops(["all"])
    [\'hash\', \'list\', \'sorted\']   # depends on registered backends
    >>> _validate_ops(["unknown"])
    KeyError: "Unknown operation \'unknown\'. Available: hash, list, sorted"
    """
    clean_names = [
        name.strip().strip(string.punctuation).lower()
        for name in ops_names
    ]
    
    for name in clean_names:
        # This validates against the actual registry,
        # which is the single source of truth.
        if name not in dicts and (name != "all"):
            raise KeyError(
                f"Unknown operation '{name}'. Available: {ops_list}"
            )

        if name == "all":
            clean_names = [name for name, _ in dicts.items()]
    
    return clean_names


# Extracting parser construction into its own function means tests can parse
# arguments without running the full program.
def _build_parser() -> argparse.ArgumentParser:
    """Build and return the argument parser.

    Separated from main() for two reasons:
    1. Single responsibility: parsing logic is isolated and testable
    2. Testability: tests can call _build_parser().parse_args([...])
       without running main()

    CS50 CLI behavior to match::

        Usage: ./speller [DICTIONARY] text

        - 1 argument:  text file only (dictionary defaults to large)
        - 2 arguments: dictionary file + text file
        - 0 or 3+ arguments: usage error

    Returns
    -------
    argparse.ArgumentParser
        Configured parser ready to parse sys.argv.

    Notes
    -----
    Why ``nargs='?'`` for dictionary?
        The ``?`` means "zero or one argument." If provided, it's used.
        If omitted, the ``default`` value is used. This replicates C's
        ``(argc == 3) ? argv[1] : DICTIONARY`` ternary pattern.

    Why ``type=str`` (not ``type=Path``)?
        argparse returns strings by default. We convert to Path inside
        main() where we also validate existence. Keeping argparse simple
        and doing validation separately follows single responsibility.
    """
    # Without RawDescriptionHelpFormatter, argparse reformats your epilog text
    # — collapsing newlines and wrapping. It preserves your formatting so the
    # examples display cleanly.
    parser = argparse.ArgumentParser(
        prog="speller",
        description="Spell-check a text file against a dictionary",
        epilog=(
            "Examples:\n"
            "   %(prog)s texts/cat.txt\n"
            "   %(prog)s dictionaries/small texts/cat.txt\n"
            "   %(prog)s --verbose texts/austen.txt"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        "text",  # positional argument required
        nargs="?",  # was required - now optional (zero or one)
        default=None,
        help="Path to text file to spell-check. Omit when using --dir.",
    )
    
    # -- Positional arguments --
    # nargs='?' makes dictionary optional, returns a single str.
    # nargs='*', nargs='+', nargs='N' return lists.
    # When user provides 1 positional arg -> it goes to 'text' (not dictionary)
    # When user provides 2 positional args -> first is dictionary, second is text
    parser.add_argument(
        "dictionary",
        nargs="?",  # zero or one
        default=str(
            file_dirs.DICT_DIR / default_fnames["dictionaries"].large  # "large"
        ),
        help=(
            "Path to dictionary file. One word per line. "
            "Default: dictionaries/large"
        ),
    )
    
    # -- Keyword arguments --
    parser.add_argument(
        "--ops",
        nargs="+",  # one or more
        default=["hash"],
        metavar="OPERATIONS",
        help=f"Data structure(s) to use. Default: hash. Available: {ops_list}",
    )
    
    parser.add_argument(
        "--dir",
        type=Path,
        default=None,
        metavar="DIRECTORY",
        help=(
            "Process all .txt files in this directory. "
            "When provided, 'text' argument is optional. "
            " Example: --dir texts/"
        ),
    )
    
    # -- Optional flags --
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        default=False,
        help="Enable verbose output (DEBUG-level logging).",
    )
    
    parser.add_argument(
        "--no-log-file",
        action="store_true",
        default=False,
        help="Disable file logging (console only).",
    )
    
    parser.add_argument(
        "--show-misspelled",
        action="store_true",
        default=False,
        help="Show all misspelled words from input txt file.",
    )
    
    return parser


def _validate_paths(
    raw_path: Path,
    *,
    path_name: str = "path",
) -> ExitCode | None:
    """Validate that required files exist before processing.

    Separated from main() because validation is a distinct concern
    from argument parsing and program execution. This function is
    also independently testable.

    Parameters
    ----------
    dict_path : Path
        Path to the dictionary file.
    text_path : Path
        Path to the text file.

    Returns
    -------
    ExitCode or None
        ExitCode if validation fails, None if all paths are valid.

    Notes
    -----
    Why return ExitCode instead of raising?
        main() handles the exit logic. This function just reports
        what it found. Separation of detection (here) from action
        (main) keeps both functions simple.

    Why check BEFORE calling run_speller()?
        run_speller() has its own error handling, but catching missing
        files here gives cleaner error messages. Fail fast — don't
        load a 143K-word dictionary only to discover the text file
        is missing.
    """
    if not raw_path.exists():
        logger.error("%s file not found: %s", path_name.title(), raw_path)
        return ExitCode.FILE_NOT_FOUND
    
    return None  # None means "all good"


# argparse.Namespace is the object that parser.parse_args() returns. It's
# essentially a simple container that holds your parsed CLI arguments as
# dot-access attributes.
#
# The tradeoff is that argparse.Namespace attribute access is typed as Any — Pyright can't verify
# that args.text actually exists, because argparse builds the namespace dynamically at runtime.
# That's just an argparse limitation, not something you did wrong.
def _resolve_text_paths(args: SpellerArgs) -> list[Path]:
    """
    """
    paths: list[Path] = []
    seen: set[Path] = set()
    
    # Single file from positional arg (existing behavior, unchanged)
    if args.text:  # Pyright knows args has dynamic attributes
        p = Path(args.text)
        if p.exists() and p not in seen:
            paths.append(p)
            seen.add(p)
            
    # Directory glob - same pattern as black/ruff/mypy
    if args.directory:
        dir_path = Path(args.directory)
        if not dir_path.is_dir():
            logger.error("--dir path is not a directory: %s", dir_path)
            return []
        for txt_file in sorted(dir_path.glob("*.txt")):  # sorted = deterministic order
            if txt_file not in seen:
                paths.append(txt_file)
                seen.add(txt_file)
                
    return paths       


def _print_reports(reports: REPORT, infile_name: str) -> None:
    """Write the misspelled-words file (if requested) and print the report.
 
    If ``reports.misspelled`` is not ``None``, creates the misspelled
    words output directory and writes the word list to a file named
    ``misspelled_<infile_name>``.  Always prints ``reports.main`` to
    ``stdout``.
 
    Parameters
    ----------
    reports : REPORT
        Named tuple from :meth:`~speller.speller.SpellerResult.format_report`.
        ``reports.main`` is the CS50-format summary string.
        ``reports.misspelled`` is a newline-joined word list, or
        ``None`` if ``--show-misspelled`` was not requested.
    infile_name : str
        Base name of the checked text file (e.g. ``"austen.txt"``).
        Used to construct the output filename.
 
    Notes
    -----
    Directory creation uses ``mkdir(parents=True, exist_ok=True)`` so
    the call is idempotent — no error if the directory already exists.
    """
    if reports.misspelled:
        file_dirs.MISS_DIR.mkdir(parents=True, exist_ok=True)
        out_file = file_dirs.MISS_DIR / f"misspelled_{infile_name}"
        out_file.write_text(reports.misspelled, encoding="utf-8")
        logger.info("Misspelled words saved to '%s'", out_file)
    
    print(reports.main)
    

# =============================================================================
# MAIN FUNCTION
# =============================================================================

# The if __name__ block and pyproject.toml script call main() with no arguments,which
# defaults to None, which triggers sys.argv reading. Your tests pass explicit lists.
def main(argv: list[str] | None = None) -> ExitCode:
    """Entry point for the speller CLI.

    Parameters
    ----------
    argv : list[str] or None
        Command-line arguments. If None, reads from sys.argv.
        Pass explicitly for testing:
            main(["texts/cat.txt"])
            main(["--verbose", "dictionaries/small", "texts/cat.txt"])
    
    Orchestrates the full program lifecycle:
    1. Parse arguments
    2. Configure logging (respects --verbose and --no-log-file)
    3. Validate file paths
    4. Create dictionary (concrete implementation chosen HERE)
    5. Run spell checker (dependency injection via Protocol)
    6. Display results
    7. Return exit code

    Returns
    -------
    int
        Exit code (0 for success, non-zero for errors).
        Used by sys.exit() and by shell scripts checking $?.

    Notes
    -----
    Why return int instead of calling sys.exit() directly?
        Returning an int makes main() testable:
            assert main() == ExitCode.SUCCESS
        If main() called sys.exit() internally, tests would need
        to catch SystemExit exceptions — messy and fragile.

        sys.exit() is called ONE place: the if __name__ block at
        the bottom. main() just returns the code.
    """
    # -- Step 1: Parse arguments --
    parser = _build_parser()
    raw: argparse.Namespace = parser.parse_args(argv)
    args = SpellerArgs(
        text=raw.text,
        dictionary=raw.dictionary,
        operations=raw.ops, 
        directory=raw.dir,
        verbose=raw.verbose,
        no_log_file=raw.no_log_file,
        show_misspelled=raw.show_misspelled,
    )
    
    # __ Step 2: Configure logging FIRST --
    # Must happen before any logger.info/debug calls.
    # --verbose flag controls console log level.
    # --no-log-file disable the rotating file handler.
    configure_logging(
        console_verbose=args.verbose,
        log_to_file=not args.no_log_file,
        custom_console=True,
    )
    
    if args.verbose:
        logger.debug("Verbose mode enabled (console debug output)")
    
    logger.debug("Arguments parsed: %s", args)
    
    # -- Step 3: Convert and validate paths --
    dict_path = Path(args.dictionary)
    path_validation = _validate_paths(dict_path, path_name="dictionary")
    if path_validation is not None:
        return path_validation
    
    text_paths: list[Path] = _resolve_text_paths(args)
    # If no files in directory provided
    if not text_paths:
        logger.error("No text files found. Provide a file or --dir path.")
        return ExitCode.FILE_NOT_FOUND
    
    success = False
    try:
        # _validate_ops() returns a list of valid ops
        for operation in _validate_ops(args.operations):
            data = dicts[operation]
            
            # -- Step 4: Create concrete dictionary -- 
            # THIS IS THE COMPOSITION ROOT — the one place that picks
            # the concrete implementation. Everything downstream depends
            # on DictionaryProtocol (the abstraction), not this class.
            #
            # To swap implementations:
            #   dictionary = DatabaseDictionary(conn_string)  # Stage 2
            #   dictionary = MockDictionary()                 # testing
            
            # Load dictionary ONCE for this backend
            loaded_dict, load_result = load_dictionary(dictionary=data.dict_class(), dict_path=dict_path)
            
            # -- Step 5: Run spell checker --
            # run_speller() accepts DictionaryProtocol - it doesn´t know
            # or care that we passed a HashTableDictionary.
            logger.debug("Running Speller with '%s'", data.name)
            
            # Now iterate over all text files - no dictionary reload
            for text_path in text_paths:
                path_validation: ExitCode | None = _validate_paths(text_path, path_name="text")
                if path_validation is not None:
                    logger.warning("Skipping '%s': not found", text_path)
                    continue    # skip bad files, don't abort the batch
                
                logger.info(
                    "Spell checking '%s' with dictionary '%s', in %s",
                    text_path.name,
                    dict_path.name,
                    type(loaded_dict).__name__,
                )
                
                benchmarks: dict[str, BenchmarkResult] = {}
                benchmarks["load"] = load_result
                
                # Initial results[] (ops_name, description empty)
                # data.results[str]: Type hints = ... fail, because in Python we cannot annotate
                # a subscript assignment. PEP 526 only allows annotations on: 
                #   - Simple names: x: int = 5
                #   - Attribute access: self.x: int = 5
                data.results[text_path.name] = run_speller(
                    dictionary=loaded_dict, 
                    text_path=text_path,
                    benchmarks=benchmarks,
                )
                result: SpellerResult | None = data.results[text_path.name]
                if result is None:
                    continue
                
                # "Update" by creating a NEW frozen instance (original unchanged)
                # replace() doesn't mutate — it copies all fields into a new frozen instance with the
                # specified fields overridden. The original object is untouched. This is the idiomatic
                # pattern for "updating" immutable data in Python.
                result = replace(
                    result,
                    ops_name=data.name,
                    description=data.description,
                )
            
                # Show for the FIRST operation only (avoid duplicate files)
                show_misspelled = (
                    args.show_misspelled 
                    and (operation == _validate_ops(args.operations)[0])
                )
        
                # -- Step 6: Display results --
                # format_report() returns a string — main() decides to print it.
                # In a web app (Stage 1 Streamlit), you'd display it differently.
                # In tests, you'd just check result.words_misspelled.
                reports: REPORT = result.format_report(log_misspelled=show_misspelled)
                _print_reports(reports, text_path.name)
        
        # -- Step 7: Return exit code --
        success = True
        return ExitCode.SUCCESS

    except KeyboardInterrupt:
        logger.warning("Interrupted by user. Exiting.")
        return ExitCode.KEYBOARD_INTERRUPT
    
    except SystemExit as e:
        # run_speller raises SystemExit if dictionary fails to load
        logger.error("Speller failed: %s", e)
        return ExitCode.LOAD_FAILED
    
    except (KeyError, TypeError) as e:
        logger.error("Operation argument failed: %s", e)
        return ExitCode.USAGE_ERROR
    
    except Exception as e:  # Catches every other exception in program
        # Appears as logging.error, provides Python's traceback info
        logger.exception("Unexpected Error: %s", e)
        return ExitCode.FAILURE
    
    # Why %s over f-string in logging? The f-string is evaluated immediately even if the log level
    # is disabled. The %s format is only evaluated if the message actually gets logged. This is a
    # performance pattern that matters in hot loops (Stage 2 ETL, Stage 3 training).
    
    finally:   # Always runs (error or no erros)
        if success:
            logger.info("Program completed.\n")
            logger.debug("Spell check completed successfully\n")
        else:
            logger.warning("Program terminated with errors.\n")
    
   
# =============================================================================
# EXECUTION GUARD
# =============================================================================

# This block runs ONLY when the module is executed directly:
#   $ python -m speller texts/cat.txt    → runs this block
#   from speller.__main__ import main    → does NOT run this block
#
# sys.exit() lives HERE and ONLY here — never inside main().
# main() returns an int, this block converts it to a process exit code.
#
# The shell can check the exit code:
#   $ python -m speller texts/cat.txt && echo "success" || echo "failed"
if __name__ == "__main__":
    sys.exit(main())
    
# Execution: __name__ == "__main__" → runs sys.exit(main())
#   $ python -m speller texts/cat.txt

# Import: __name__ == "speller.__main__" → guard block skipped
#   >>> from speller.__main__ import main
#   >>> code = main()  # returns int, no sys.exit


# =============================================================================
# SHORT REFERENCE GUIDES
# =============================================================================
# =====================================================
# CLI Arguments And sys.argv
# =====================================================

# When you call parse_args() with NO arguments:
#   args = parser.parse_args()
# It implicitly reads from sys.argv[1:]
# Same as: args = parser.parse_args(sys.argv[1:])

# When you call parse_args() WITH arguments:
#   args = parser.parse_args(["texts/cat.txt"])
# It uses YOUR list instead of sys.argv

# The flow:

#   $ python -m speller --verbose texts/cat.txt

#   sys.argv = ["speller/__main__.py", "--verbose", "texts/cat.txt"]
#   sys.argv[1:] = ["--verbose", "texts/cat.txt"]    ← [1:] skips the script name

#   parser.parse_args()       → reads sys.argv[1:] automatically
#   parser.parse_args(None)   → same thing (None = use sys.argv[1:])
#   parser.parse_args([...])  → uses YOUR list instead

# def main(argv: list[str] | None = None) -> ExitCode:
#     args = parser.parse_args(argv)

# ┌─────────────────────────────────────────────────────────────────┐
# │  Caller                        │ argv value   │ parse_args uses │
# │────────────────────────────────│──────────────│─────────────────│
# │  if __name__ == "__main__":    │              │                 │
# │      sys.exit(main())          │ None         │ sys.argv[1:]    │
# │                                │              │ (real CLI args) │
# │────────────────────────────────│──────────────│─────────────────│
# │  pyproject.toml script:        │              │                 │
# │      speller texts/cat.txt     │ None         │ sys.argv[1:]    │
# │                                │              │ (real CLI args) │
# │────────────────────────────────│──────────────│─────────────────│
# │  Test:                         │              │                 │
# │      main(["texts/cat.txt"])   │ ["texts/..."]│ your list       │
# │                                │              │ (controlled)    │
# │────────────────────────────────│──────────────│─────────────────│
# │  Another module:               │              │                 │
# │      main(["--verbose", path]) │ [...]        │ your list       │
# │                                │              │ (programmatic)  │
# └─────────────────────────────────────────────────────────────────┘

# =====================================================
# [project.scripts]: How pyproject.toml connects
# =====================================================

# [project.scripts]
# speller = "speller.__main__:main"

# When the user types `speller texts/cat.txt`, pip's generated script calls `main()`
# directly and handles the exit code — it doesn't go through the `if __name__` block.

## Complete Module Flow
# $ python -m speller --verbose dictionaries/small texts/cat.txt

# 1. Python finds speller/__main__.py
# 2. __init__.py runs → NullHandler set
# 3. ImportError guard → all modules import successfully
# 4. if __name__ == "__main__" → sys.exit(main())
# 5. main() starts:
#      a. _build_parser() → ArgumentParser created
#      b. parse_args() → dictionary="dictionaries/small", text="texts/cat.txt", verbose=True
#      c. config_logging(verbose=True) → DEBUG console + file handlers
#      d. _validate_paths() → both files exist → None (success)
#      e. HashTableDictionary() → concrete instance created
#      f. run_speller(dictionary, text, dict) → SpellerResult returned
#         ├── timer("load") → dictionary.load("dictionaries/small")
#         ├── timer("check") → for word in extract_words("texts/cat.txt"):
#         │                        dictionary.check(word)
#         └── timer("size") → dictionary.size()
#      g. print(result.format_report()) → CS50-format output
#      h. return ExitCode.SUCCESS → 0
# 6. sys.exit(0) → process exits cleanly


# =====================================================
# argparse.NameSpace Object
# =====================================================

# argparse.Namespace is the object that parser.parse_args() returns. It's
# essentially a simple container that holds your parsed CLI arguments as
# dot-access attributes.
#
# The tradeoff is that argparse.Namespace attribute access is typed as Any — Pyright can't verify
# that args.text actually exists, because argparse builds the namespace dynamically at runtime.
# That's just an argparse limitation, not something you did wrong.
#
#   def _resolve_text_paths(args: argparse.Namespace) -> list[Path]: