"""
"""

from __future__ import annotations

from pathlib import Path
from turtle import exitonclick
from _pytest.outcomes import Exit
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

class TestValidatePaths:
    """Test _validate_paths() helper function.

    _validate_paths() returns ExitCode on failure, None on success.
    This separation of detection from action makes both the helper
    and main() simpler and independently testable.
    """
    
    def test_valid_path_return_none(
        self, sample_dict_file: Path, sample_text_file: Path
    ) -> None:
        """Both files exist → returns None (success).

        None means "no error" — the absence of a value.
        This is a common Python pattern: return None for success,
        return a specific value for specific failures.
        """
        result_dict = _validate_paths(
            sample_dict_file,
            path_name=sample_dict_file.name
        )
        result_text = _validate_paths(
            sample_text_file,
            path_name=sample_text_file.name
        )
        
        assert result_dict is None
        assert result_text is None
        
    def test_missing_path_returns_exit_code(
        self, sample_text_file: Path
    ) -> None:
        """Missing dictionary → returns FILE_NOT_FOUND."""
        result = _validate_paths(
            Path("nonexisting_dic.txt"),
            path_name=Path("nonexistent_dict.txt").name,
        )
        assert result == ExitCode.FILE_NOT_FOUND
        

# =============================================================================
# MAIN FUNCTION
# =============================================================================

class TestMain:
    """Test the main() entry point.

    main(argv=...) is testable because it accepts an explicit
    argument list instead of reading sys.argv directly. This is
    the pattern we established early in the project.

    Without the argv parameter, every test would need:
        monkeypatch.setattr("sys.argv", ["speller", "texts/cat.txt"])
    — fragile and ugly.
    """
    
    def test_missing_file_returns_error(self) -> None:
        """main() returns FILE_NOT_FOUND for nonexistent text file.

        We pass --no-log-file to avoid creating log directories
        during tests.
        """
        result = main(["--no-log-file", "nonexistent.txt"])
        assert result == ExitCode.FILE_NOT_FOUND
        
    def test_missing_dictionary_returns_error(self) -> None:
        """main() returns FILE_NOT_FOUND for nonexistent dictionary."""
        result = main([
            "--no-log-file",
            "texts/cat.txt",
            "nonexistent_dict.txt",
        ])
        assert result == ExitCode.FILE_NOT_FOUND
        
    @pytest.mark.integration
    def test_successful_run(
        self,
        large_dict_path: Path,
        texts_dir: Path,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        """main() returns SUCCESS for valid inputs.

        capsys is a built-in pytest fixture that captures stdout
        and stderr. After the function runs, capsys.readouterr()
        returns a named tuple with .out and .err attributes.

        This lets us verify:
        1. main() returns the correct exit code
        2. The output contains expected text
        Without capsys, we'd have to redirect stdout manually.
        """
        text_path = texts_dir / "cat.txt"
        if not text_path.exists():
            pytest.skip(f"Text file not found: {text_path}")
            
        result = main([
            "--no-log-file",
            str(text_path),
            str(large_dict_path),
        ])
        
        assert result == ExitCode.SUCCESS
        
        # Verify output was printed
        captured = capsys.readouterr()
        assert "WORDS MISSPELLED:" in captured.out
        assert "WORDS IN DICTIONARY:" in captured.out
        
    @pytest.mark.integration
    def test_cat_txt_output(
        self,
        large_dict_path: Path,
        texts_dir: Path,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        """cat.txt should show 0 misspelled, 6 words in text."""
        text_path = texts_dir / "cat.txt"
        if not text_path.exists():
            pytest.skip(f"Text file not found: {text_path}")
            
        main([
            "--no-log-file",
            str(text_path),
            str(large_dict_path),
        ])
        
        captured = capsys.readouterr()
        # Check for exact values in output
        assert "0" in captured.out
        assert "143091" in captured.out
        assert "6" in captured.out
    
    # captured.out catches the report from print(). captured.err catches all log
    # messages regardless of level — including INFO and DEBUG.
    
    @pytest.mark.integration
    def test_verbose_enables_debug_output(
        self,
        large_dict_path: Path,
        texts_dir: Path,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        """--verbose flag enables DEBUG-level console output."""
        text_path = texts_dir / "cat.txt"
        if not text_path.exists():
            pytest.skip(f"Text file not found: {text_path}")
            
        main([
            "--verbose",
            "--no-log-file",
            str(text_path),
            str(large_dict_path),
        ])
        
        # Debug messages as well as all logging levels go to stderr (via logging StreamHandler)
        captured = capsys.readouterr()
        # Verbose mode should produce debug-level output on stderr
        assert len(captured.err) > 0