"""
This program counts the number of messages sent in each hour in the file.
It returns the hour with the most messages and count.
"""
from __future__ import annotations
from typing import Optional, Iterator

from collections import defaultdict, Counter
from pathlib import Path

import argparse
import sys

SCRIPT_DIR: Path = Path(__file__).parent
DATA_DIR: Path = SCRIPT_DIR / "data"
PREFIX: str = "From "
DEFAULT_FILE: str = "mbox-short.txt"


def resolve_input_path(fname: str, data_dir: Optional[Path] = None) -> Path:
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
        data_dir = DATA_DIR
    candidate = data_dir / fname

    if candidate.is_file():
        return candidate
    
    raise FileNotFoundError(f"File not found: {fname} (also tried: {candidate}")


def _extract_lines( path: Path) -> Iterator[str]:
    """
    - Extract lines from txt file that start with 'From '.
    - Review such lines have at least two words.
    - Extract and yield email only.
    """

    empty = True # Boolean to determine if after 'for loop' finishes no qualified line was found in file
    with open(path) as f:
        for line in f:
            words = line.strip().split() if (line.startswith(PREFIX) and len(line.strip().split()) >= 2) else None
            if not words:
                continue
            empty = False
            hour, _, _ = words[5].partition(":")
            yield hour # yield -> generator function (returns one value at a time)
    
    if empty:
        raise ValueError(f"No lines starting with '{PREFIX}' found in file: {path}")


def count_messages_by_hour(path: Path) -> Counter[(str, int)]:
    """
    Count the number of messages sent in each hour in the file.
    Return a list of tuples (hour, count) sorted by count in descending order.
    """
    hour_count = defaultdict(int) # Initialize a dictionary(default value 0 when key is not found) to store the count of each sender
    for hour in _extract_lines(path):
        hour_count[hour] += 1
    
    return Counter(hour_count).most_common() # returns a list of tuples (hour, count) sorted by count in descending order



def main(args: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=f"Count the number of times each sender appears in the file from lines startin with '{PREFIX}.")
    parser.add_argument("--file", default=DEFAULT_FILE, help="Input filename or path")
    parser.add_argument("--data--dir", default=None, help="Optional data directory to search")
    args = parser.parse_args(args)

    data_dir = Path(args.data__dir) if args.data__dir else None

    try:
        path = resolve_input_path(args.file, data_dir)
        hour_count_list = list(count_messages_by_hour(path))
        print("\nList of hour and count of messages sent by:")
        for hour, count in hour_count_list:
            print(f"{hour}: {count}")

    except (FileNotFoundError, ValueError) as e:
        print(f"Error: {e}", sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("\nInterrupted by User. Exiting.\n", file=sys.stderr)
        return 130
    
    return 0    


if __name__ == "__main__":
    raise SystemExit(main())





    