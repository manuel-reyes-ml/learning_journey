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
        logger.error("Tet file not found: %s", text_path)
        return ExitCode.FILE_NOT_FOUND
    
    return None


# =============================================================================
# MAIN FUNCTION
# =============================================================================