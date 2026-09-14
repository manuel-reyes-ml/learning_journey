#!/usr/bin/env python3
"""
Spam Confidence Analyzer - Production-Grade Single-File Script

Extracts X-DSPAM-Confidence values from email files and computes statistics.

This script demonstrates production-grade Python practices within a single file:
- CLI with argparse (not input())
- Structured logging (not print())
- Proper exit codes with sys.exit()
- Custom exceptions for domain-specific errors
- Dataclass for structured results
- Comprehensive type hints
- Configuration as constants
- Defensive error handling

Original Author: Manuel Reyes
Enhanced: January 2026 for production-grade standards

Usage:
    python read_count_production.py data/mbox-short.txt
    python read_count_production.py data/mbox-short.txt --verbose
    python read_count_production.py --help
"""
from __future__ import annotations # Enables postponed evaluation of type annotations

import argparse  # For command-line argument parsing
import logging   # For structured logging: timestamps, levels, etc.
import re        # For regular expressions: pattern matching to extract digits
import sys
from collections.abc import Generator
from dataclasses import dataclass
from enum import IntEnum
from pathlib import Path
from statistics import mean, stdev


# =============================================================================
# CONFIGURATION CONSTANTS
# =============================================================================
# Using constants makes the code configurable without hardcoding values
# throughout the codebase. In larger projects, these would come from a
# config file or environment variables.

# Get the directory where this script lives (works regardless of where you run from)
SCRIPT_DIR: Path = Path(__file__).resolve().parent

HEADER_PATTERN: str = "X-DSPAM-Confidence:"
NUMBER_REGEX: str = r"[-+]?\d*\.\d+"
DEFAULT_FILE: str = "mbox-short.txt"
DEFAULT_DATA_DIR: Path = SCRIPT_DIR / "data"  # Relative to script, not cwd
LOG_FORMAT: str = "%(asctime)s | %(levelname)-8s | %(message)s"
LOG_DATE_FORMAT: str = "%Y-%m-%d %H:%M:%S"


# =============================================================================
# EXIT CODES
# =============================================================================
# Standard exit codes enable shell scripts and CI/CD pipelines to detect
# success/failure programmatically. Using IntEnum provides readable names.

class ExitCode(IntEnum):
    """Standard exit codes for the application.
    
    Following Unix conventions:
    - 0 = success
    - 1-127 = various error conditions
    - 130 = terminated by Ctrl+C (128 + SIGINT signal number 2)
    """
    SUCCESS = 0
    FILE_NOT_FOUND = 1
    NO_DATA_FOUND = 2
    FILE_READ_ERROR = 3
    INVALID_ARGUMENT = 4
    USER_INTERRUPT = 130


# =============================================================================
# CUSTOM EXCEPTIONS
# =============================================================================
# Domain-specific exceptions provide clearer error messages and allow
# targeted error handling. They're more Pythonic than returning error codes.

class SpamAnalyzerError(Exception):
    """Base exception for all spam analyzer errors."""
    pass


class NoDataFoundError(SpamAnalyzerError):
    """Raised when no X-DSPAM-Confidence headers are found."""
    
    def __init__(self, file_path: Path) -> None:
        self.file_path = file_path
        super().__init__(
            f"No '{HEADER_PATTERN}' headers found in '{file_path}'. "
            "Ensure the file contains valid email headers."
        )


class FileReadError(SpamAnalyzerError):
    """Raised when a file cannot be read."""
    
    def __init__(self, file_path: Path, original_error: Exception) -> None:
        self.file_path = file_path
        self.original_error = original_error
        super().__init__(f"Cannot read file '{file_path}': {original_error}")


# =============================================================================
# DATA STRUCTURES
# =============================================================================
# Using a dataclass instead of a tuple provides:
# - Type safety and IDE autocompletion
# - Self-documenting structure
# - Automatic __repr__ for debugging
# - Immutability with frozen=True

@dataclass(frozen=True)
class AnalysisResult:
    """Immutable container for analysis results.
    
    Attributes:
        mean: Arithmetic mean of confidence values.
        count: Total number of values analyzed.
        minimum: Lowest confidence value found.
        maximum: Highest confidence value found.
        std_dev: Standard deviation (0.0 if count < 2).
        file_path: Path to the analyzed file.
    """
    mean: float
    count: int
    minimum: float
    maximum: float
    std_dev: float
    file_path: Path

    def format_report(self, precision: int = 6) -> str:
        """Format results as a human-readable report.
        
        Args:
            precision: Decimal places for floating-point values.
        
        Returns:
            Formatted multi-line string with analysis results.
        """
        width = 50
        return (
            f"\n{'=' * width}\n"
            f"  ANALYSIS RESULTS: {self.file_path.name}\n"
            f"{'=' * width}\n"
            f"  Lines analyzed:     {self.count:,}\n"
            f"  Mean confidence:    {self.mean:.{precision}f}\n"
            f"  Minimum:            {self.minimum:.{precision}f}\n"
            f"  Maximum:            {self.maximum:.{precision}f}\n"
            f"  Standard Deviation: {self.std_dev:.{precision}f}\n"
            f"{'=' * width}\n"
        )


# =============================================================================
# LOGGING SETUP
# =============================================================================
# Using the logging module instead of print() provides:
# - Log levels (DEBUG, INFO, WARNING, ERROR)
# - Timestamps for debugging
# - Easy output redirection
# - Can be disabled without removing code

def setup_logging(verbose: bool = False) -> logging.Logger:
    """Configure and return the application logger.
    
    Args:
        verbose: If True, set level to DEBUG; otherwise INFO.
    
    Returns:
        Configured logger instance.
    """
    logger = logging.getLogger("spam_analyzer")
    
    # Avoid adding multiple handlers if called repeatedly
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stderr)
        handler.setFormatter(logging.Formatter(LOG_FORMAT, LOG_DATE_FORMAT))
        logger.addHandler(handler)
    
    logger.setLevel(logging.DEBUG if verbose else logging.INFO)
    return logger


# Module-level logger (configured in main)
logger = logging.getLogger("spam_analyzer")


# =============================================================================
# CORE FUNCTIONS
# =============================================================================

def extract_confidence_values(file_path: Path) -> Generator[float, None, None]:
    """Extract floating-point confidence values from email headers.
    
    Generator function that yields values one at a time for memory efficiency
    when processing large files.
    
    Args:
        file_path: Path to the email/mbox file to analyze.
    
    Yields:
        Confidence values (floats) from matching header lines.
    
    Raises:
        FileNotFoundError: If file_path does not exist.
        FileReadError: If file cannot be read (permissions, encoding).
    
    Example:
        >>> values = list(extract_confidence_values(Path("mbox.txt")))
        >>> print(f"Found {len(values)} values")
    """
    logger.debug("Starting extraction from: %s", file_path)
    
    if not file_path.exists():
        logger.error("File not found: %s", file_path)
        raise FileNotFoundError(file_path)
    
    # Compile regex once for efficiency (not on every iteration)
    pattern = re.compile(NUMBER_REGEX)
    values_found = 0
    
    try:
        # Use encoding and errors parameters for robustness
        with file_path.open("r", encoding="utf-8", errors="replace") as file_handle:
            for line_number, line in enumerate(file_handle, start=1):
                if not line.startswith(HEADER_PATTERN):
                    continue
                
                match = pattern.search(line)
                if match:
                    value = float(match.group())
                    values_found += 1
                    logger.debug("Line %d: extracted %.6f", line_number, value)
                    yield value
                else:
                    logger.warning(
                        "Line %d: header found but no value: %s",
                        line_number,
                        line.strip()
                    )
    
    except PermissionError as e:
        logger.error("Permission denied: %s", file_path)
        raise FileReadError(file_path, e) from e
    except OSError as e:
        logger.error("Error reading file: %s - %s", file_path, e)
        raise FileReadError(file_path, e) from e
    
    logger.debug("Extraction complete: %d values found", values_found)


def compute_statistics(values: list[float], file_path: Path) -> AnalysisResult:
    """Compute statistical measures from confidence values.
    
    Args:
        values: List of confidence values to analyze.
        file_path: Path to the source file (for result metadata).
    
    Returns:
        AnalysisResult containing all computed statistics.
    
    Raises:
        NoDataFoundError: If values list is empty.
    """
    if not values:
        raise NoDataFoundError(file_path)
    
    count = len(values)
    avg = mean(values)
    minimum = min(values)
    maximum = max(values)
    # Standard deviation requires at least 2 values
    std = stdev(values) if count >= 2 else 0.0
    
    logger.debug(
        "Statistics computed: count=%d, mean=%.6f, std=%.6f",
        count, avg, std
    )
    
    return AnalysisResult(
        mean=avg,
        count=count,
        minimum=minimum,
        maximum=maximum,
        std_dev=std,
        file_path=file_path,
    )


def analyze_file(file_path: Path) -> AnalysisResult:
    """Main analysis function - extracts values and computes statistics.
    
    This is the primary entry point for the analysis logic, combining
    extraction and computation into a single callable.
    
    Args:
        file_path: Path to the file to analyze.
    
    Returns:
        AnalysisResult with all computed statistics.
    
    Raises:
        FileNotFoundError: If file doesn't exist.
        FileReadError: If file can't be read.
        NoDataFoundError: If no matching headers found.
    """
    logger.info("Analyzing file: %s", file_path)
    
    # Convert generator to list (required for multiple passes in statistics)
    values = list(extract_confidence_values(file_path))
    
    result = compute_statistics(values, file_path)
    
    logger.info("Analysis complete: %d values processed", result.count)
    return result


# =============================================================================
# CLI INTERFACE
# =============================================================================
# Using argparse instead of input() makes the script:
# - Automatable in scripts and pipelines
# - Self-documenting with --help
# - Type-safe with automatic validation

def create_argument_parser() -> argparse.ArgumentParser:
    """Create and configure the command-line argument parser.
    
    Returns:
        Configured ArgumentParser instance.
    """
    parser = argparse.ArgumentParser(
        prog="spam_analyzer",
        description=(
            "Analyze X-DSPAM-Confidence headers from email files. "
            "Computes mean, min, max, and standard deviation of confidence values."
        ),
        epilog="Example: %(prog)s data/mbox-short.txt --verbose",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    
    parser.add_argument(
        "file_path",
        type=Path,
        nargs="?",  # Optional - allows default
        default=DEFAULT_DATA_DIR / DEFAULT_FILE,
        help=f"Path to the email/mbox file (default: data/{DEFAULT_FILE})",
    )
    
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose (debug) output",
    )
    
    parser.add_argument(
        "-p", "--precision",
        type=int,
        default=6,
        choices=range(1, 11),
        metavar="N",
        help="Decimal precision for output (1-10, default: 6)",
    )
    
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s 1.0.0",
    )
    
    return parser


# =============================================================================
# MAIN ENTRY POINT
# =============================================================================

def main() -> int:
    """Main entry point for the spam confidence analyzer.
    
    Parses arguments, runs analysis, and handles errors gracefully.
    
    Returns:
        Exit code (0 for success, non-zero for errors).
    """
    # Parse command-line arguments
    parser = create_argument_parser()
    args = parser.parse_args()
    
    # Setup logging based on verbosity flag
    setup_logging(verbose=args.verbose)
    
    logger.debug("Arguments: file_path=%s, verbose=%s", args.file_path, args.verbose)
    
    try:
        # Run the analysis
        result = analyze_file(args.file_path)
        
        # Output results (to stdout, separate from logs on stderr)
        print(result.format_report(precision=args.precision))
        
        return ExitCode.SUCCESS
    
    except FileNotFoundError:
        logger.error("File not found: %s", args.file_path)
        print(f"Error: File '{args.file_path}' not found.", file=sys.stderr)
        return ExitCode.FILE_NOT_FOUND
    
    except FileReadError as e:
        logger.error("Cannot read file: %s", e)
        print(f"Error: {e}", file=sys.stderr)
        return ExitCode.FILE_READ_ERROR
    
    except NoDataFoundError as e:
        logger.error("No data found: %s", e)
        print(f"Error: {e}", file=sys.stderr)
        return ExitCode.NO_DATA_FOUND
    
    except KeyboardInterrupt:
        logger.info("Operation cancelled by user")
        print("\nOperation cancelled.", file=sys.stderr)
        return ExitCode.USER_INTERRUPT


if __name__ == "__main__":
    sys.exit(main())