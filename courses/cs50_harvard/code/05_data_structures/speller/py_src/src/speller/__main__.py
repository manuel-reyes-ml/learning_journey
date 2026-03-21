"""
"""

# =============================================================================
# IMPORTS
# =============================================================================

from __future__ import annotations

from argparse import ArgumentParser
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
    from pathlib import Path
    import argparse
    import logging
    
    from speller.dictionaries import HashTableDictionary
    from speller.config import ExitCode, file_dirs
    from speller.logger import configure_logging
    from speller.speller import run_speller
    
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
# INTERNAL HELPER FUNCTIONS
# =============================================================================
    
def _build_parser() -> argparse.ArgumentParser:
    """
    """
    parser = ArgumentParser(
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
    
    # -- Positional arguments --
    # nargs='?' makes dictionary optional
    # When user provides 1 positional arg -> it goes to 'text' (not dictionary)
    # When user provides 2 positional args -> first is dictionary, second is text
    parser.add_argument(
        "dictionary",
        nargs="?",
        default=str(file_dirs.DICT_DIR / "large"),
        help=(
            "Path to dictionary file. One word per line. "
            "Default: dictionaries/large"
        ),
    )
    
    parser.add_argument(
        "text",
        help="Path to text file to spell-check (required).",
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
    
    return parser


def _validate_paths(
    dict_path: Path,
    text_path: Path,
) -> ExitCode | None:
    """
    """
    if not dict_path.exists():
        logger.error("Dictionary file not found: %s", dict_path)
        return ExitCode.FILE_NOT_FOUND
    
    if not text_path.exists():
        logger.error("Text file not found: %s", text_path)
        return ExitCode.FILE_NOT_FOUND
    
    return None


# =============================================================================
# MAIN FUNCTION
# =============================================================================

def main() -> int:
    """
    """
    # -- Step 1: Parse arguments --
    parser = _build_parser()
    args = parser.parse_args()
    
    # __ Step 2: Configure logging FIRST --
    # Must happen before any logger.info/debug calls.
    # --verbose flag controls console log level.
    # --no-log-file disable the rotating file handler.
    configure_logging(
        console_verbose=args.verbose,
        log_to_file=not args.no_log_file,
        custom_console=True,
    )
    
    logger.debug("Arguments parsed: %s", args)
    
    # -- Step 3: Convert and validate paths --
    dict_path = Path(args.dictionary)
    text_path = Path(args.text)
    
    validation_error = _validate_paths(dict_path, text_path)
    if validation_error is not None:
        return validation_error
    
    # -- Step 4: Create concrete dictionary -- 
    # THIS IS THE COMPOSITION ROOT — the one place that picks
    # the concrete implementation. Everything downstream depends
    # on DictionaryProtocol (the abstraction), not this class.
    #
    # To swap implementations:
    #   dictionary = DatabaseDictionary(conn_string)  # Stage 2
    #   dictionary = MockDictionary()                 # testing
    dictionary = HashTableDictionary()
    
    logger.info(
        "Spell checking '%s' with dictionary '%s'",
        text_path.name,
        dict_path.name,
    )
    
    # -- Step 5: RUn spell checker --
    # run_speller() accepts DictionaryProtocol - it doesn´t know
    # or care tjhat we passed a HashTableDictionary.
    try:
        result = run_speller(
            dictionary=dictionary,
            text_path=text_path,
            dict_path=dict_path,
        )
    except SystemExit as e:
        # run_speller raises SystemExit if dictionary fails to load
        logger.error("Speller failed: %s", e)
        return ExitCode.LOAD_FAILED
    
    # -- Step 6: Display results --
    # format_report() returns a string — main() decides to print it.
    # In a web app (Stage 1 Streamlit), you'd display it differently.
    # In tests, you'd just check result.words_misspelled.
    print(result.format_report())
    
    logger.debug("Spell check completed successfully")
    
    # -- Step 7: Return exit code --
    return ExitCode.SUCCESS


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