"""
"""

from __future__ import annotations

from pathlib import Path
import pytest

from speller.config import ExitCode

# Import internal helpers for direct testing.
# Underscore-prefixed functions are "internal" by convention but
# still importable — the underscore is a HINT, not enforcement.
# Testing private functions is acceptable when they contain
# significant logic worth verifying independently.
from speller.__main__ import _build_parser, _validate_paths, main


# =============================================================================
# ARGUMENT PARSER
# =============================================================================

class TestBuildParser:
    """Test _build_parser() argument parsing.

    _build_parser() was extracted from main() specifically for
    testability. We can test argument combinations without
    running the full spell-check pipeline.
    """
    
    def test_text_only(self) -> None:
        """Single argument goes to 'text', dictionary uses default.

        Matches C: argc == 2, argv[1] is the text file.
        """
        parser = _build_parser()
        args = parser.parse_args(["texts/cat.txt"])
        
        assert args.text == "texts/cat.txt" 
        # Dictionary should have the default path
        assert "large" in args.dictionary
        
    def test_dictionary_and_text(self) -> None:
        """Two arguments: first is dictionary, second is text.

        Matches C: argc == 3, argv[1] is dictionary, argv[2] is text.
        """
        parser = _build_parser()
        args = parser.parse_args(["texts/cat.txt", "dictionaries/small"])
        
        assert args.dictionary == "dictionaries/small"
        assert args.text == "texts/cat.txt"
        
    def test_verbose_flag(self) -> None:
        """--verbose flag is parsed as boolean."""
        parser = _build_parser()
        args = parser.parse_args(["--verbose", "texts/cat.txt"])
        
        assert args.verbose is True
        
    def test_verbose_short_flag(self) -> None:
        """-v is the short form of --verbose."""
        parser = _build_parser()
        args = parser.parse_args(["-v", "texts/cat.txt"])
        
        assert args.verbose is True
        
    def test_no_log_file_flag(self) -> None:
        """--no-log-file disables file logging."""
        parser = _build_parser()
        args = parser.parse_args(["--no-log-file", "texts/cat.txt"])
        
        assert args.no_log_file is True
        
    def test_show_misspelled_flag(self) -> None:
        """--show-misspelled enables misspelled word output."""
        parser = _build_parser()
        args = parser.parse_args(["--show-misspelled", "texts/cat.txt"])
        
        assert args.show_misspelled is True
        
    def test_defaults(self) -> None:
        """Default values when no optional flags are provided."""
        parser = _build_parser()
        args = parser.parse_args(["texts/cat.txt"])
        
        assert args.verbose is False
        assert args.no_log_file is False
        assert args.show_misspelled is False
        
    def test_all_flags_combined(self) -> None:
        """All optional flags can be combined."""
        parser = _build_parser()
        args = parser.parse_args([
            "--verbose",
            "--no-log-file",
            "--show-misspelled",
            "texts/cat.txt",
            "dictionaries/small",
        ])
        
        assert args.verbose is True
        assert args.no_log_file is True
        assert args.show_misspelled is True
        assert args.dictionary == "dictionaries/small"
        assert args.text == "texts/cat.txt"
        
    def test_missing_text_argument(self) -> None:
        """No arguments at all should cause SystemExit.

        argparse raises SystemExit(2) for invalid arguments.
        """
        parser = _build_parser()
        with pytest.raises(SystemExit):
            parser.parse_args(["--ops"])
            
            
# =============================================================================
# PATH VALIDATION
# =============================================================================