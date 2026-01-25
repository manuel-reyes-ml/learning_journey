
from __future__ import annotations
from typing import Optional, Iterator

from pathlib import Path

import re
import argparse
import sys

SCRIPT_DIR: Path = Path(__file__).parent
DEFAULT_DATA_DIR: Path = SCRIPT_DIR / 'data'
SEARCH_PREFIX: str = '[0-9]+'
FILE_DEFAULT: str = 'regex_sum_42.txt'


def resolve_input_path(fname: str, data_dir: Optional[Path]) -> Path:
    """
     Resolve a file path:
    - If fname is absolute or exists as given, use it.
    - Else, if data_dir provided, look under data_dir/fname.
    - Else, look under ./data/fname relative to current working directory.
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


def _extract_and_generate_numbers(path: Path) -> Iterator[Optional[list[str]]]:
    """
    - Extract string from txt file that match regex pattern 'PREFIX'.
    - Return list of strings(digits) if match found, None otherwise.
    """
    with path.open() as f:
        for line in f:
            yield re.findall(SEARCH_PREFIX, line.strip())
    

def _convert_and_generate_ints(path: Path) -> Iterator[int]:
    """
    - Convert string to int and yield it.
    """
    for slist in _extract_and_generate_numbers(path):
        if slist is None:
            continue
        for digit in slist:
            yield int(digit)


def add_ints(path: Path) -> int:
    """
    - Add all integers extracted from file.
    - Return sum.
    """
    total_ints = None
    for i in _convert_and_generate_ints(path):
        total_ints = i if total_ints is None else total_ints + i
    
    if total_ints:
        return total_ints
    
    raise ValueError(f"No integers found in file: {path}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=f"Extract numbers from file and add them to get a total.")
    parser.add_argument("--file", default=FILE_DEFAULT, help="Input filename or path")
    parser.add_argument("--data--dir", default=None, help="Optional data directory to search")
    args = parser.parse_args(argv)

    data_dir = Path(args.data__dir) if args.data__dir else None

    try:
        path = resolve_input_path(args.file, data_dir)
        total_ints = add_ints(path)
        print(f"\nTotal of integers in file: {total_ints}\n")
    except (FileNotFoundError, ValueError) as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("\nInterrupted by User. Exiting.\n", file=sys.stderr)
        return 130
    
    return 0

if __name__ == "__main__":
    raise SystemExit(main())

    