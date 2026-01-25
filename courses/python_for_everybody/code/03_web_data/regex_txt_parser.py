"""
Regex Sum Script - Extract and sum all integers from a text file.

Usage:
    python regex_sum.py
    python regex_sum.py --file mydata.txt
    python regex_sum.py --file mydata.txt --data-dir /path/to/data
"""

from __future__ import annotations
from typing import Optional, Iterator

from pathlib import Path

import re
import argparse
import sys

SCRIPT_DIR: Path = Path(__file__).resolve().parent # .resolve() normalizes path (e.g. ./../data -> data)
DEFAULT_DATA_DIR: Path = SCRIPT_DIR / 'data'
NUMBER_PATTERN: str = r'[0-9]+' # 'r' -> raw string = no escape characters
FILE_DEFAULT: str = 'regex_sum_42.txt'


def resolve_input_path(fname: str, data_dir: Optional[Path]) -> Path:
    """
    Resolve a file path:
    - If fname is absolute or exists as given, use it.
    - Else, if data_dir provided, look under data_dir/fname.
    - Else, look under ./data/fname relative to current working directory.

    Args:
        fname (str): Input filename or path.
        data_dir (Optional[Path], optional): Optional data directory to search. Defaults to None.
    Returns:
        Path: Resolved file path.
    Raises:
        FileNotFoundError: If file not found.
    """

    p = Path(fname)
    if p.is_file():
        return p 

    if data_dir is None:
        data_dir = DEFAULT_DATA_DIR
    
    candidate = data_dir / fname
    if candidate.is_file():
        return candidate

    raise FileNotFoundError(f"File not found: {fname} (also tried: {candidate})")


def _extract_and_generate_numbers(path: Path) -> Iterator[int]:
    """
    Extract strings from txt file that match regex pattern 'NUMBER_PATTERN'.
    Convert strings to int and yield it.

    Args:
        path (Path): Path to txt file.
    Yields:
        int: Integer extracted from file.
    """
    pattern = re.compile(NUMBER_PATTERN) # Compile regex pattern for better performance
    with path.open(encoding='utf-8') as f:
        for line in f:
            if line.strip() == '': # Skip empty lines(blank lines in file)
                continue
            for match in pattern.findall(line.strip()):
                yield int(match)


def add_ints(path: Path) -> int:
    """
    Add all integers extracted from file.
    Return sum.

    Args:
        path (Path): Path to txt file.
    Returns:
        int: Sum of all integers extracted from file.
    Raises:
        ValueError: If no integers found in file.
    """
    total_ints = None
    for i in _extract_and_generate_numbers(path):
        total_ints = i if total_ints is None else total_ints + i
    
    if total_ints is not None: # Compares with None to check if it was initialized
        return total_ints
    
    raise ValueError(f"No integers found in file: {path}")


def main(argv: list[str] | None = None) -> int:
    """
    Main entry point for the regex sum script.
    
    Args:
        argv (list[str] | None, optional): Command line arguments. Defaults to None.
    Returns:
        int: Return code (0 on success, 1 on failure, 130 on keyboard interrupt).
    Raises:
        FileNotFoundError: If file not found.
        ValueError: If no integers found in file.
    """
    parser = argparse.ArgumentParser(description=f"Extract numbers from file and add them to get a total.")
    parser.add_argument("--file", default=FILE_DEFAULT, help=f"Input filename or path (default: {FILE_DEFAULT})")
    parser.add_argument("--data-dir", default=None, help="Optional data directory to search")
    args = parser.parse_args(argv)

    data_dir = Path(args.data_dir) if args.data_dir else None

    try:
        path = resolve_input_path(args.file, data_dir)
        total_ints = add_ints(path)
        print(f"\nTotal of integers in file: {total_ints}\n")
        return 0

    except (FileNotFoundError, ValueError) as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    except KeyboardInterrupt:
        print("\nInterrupted by User. Exiting.\n", file=sys.stderr)
        return 130
    

if __name__ == "__main__":
    sys.exit(main()) # Exit with return code from main() - more convetional than raise SystemExit(main())

    