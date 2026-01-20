from __future__ import annotations
from typing import Optional

from pathlib import Path
import argparse
import sys

SCRIPT_DIR = Path(__file__).parent
DEFAULT_DATA_DIR = SCRIPT_DIR / "data"

# Tries different Paths from default or user input
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
    

def append_extract_words(path: Path) -> list[str]:
    """
    Read a file and extract all words, returning them as a list.
    Words are converted to lowercase and stripped of whitespace.
    """
    with path.open("r", encoding="utf-8", errors="replace") as f:
        word_list = []
        for line in f:
            if line.strip() == "":
                continue
            words = line.split()
            word_list.extend([word.strip().lower() for word in words if word.strip().lower() not in word_list]) # Use list comprehension to build list of words
        
        if not word_list:
            raise ValueError(f"No words found in file: {path}")
        return word_list


def sort_list(word_list: list[str], descending: bool | None = False) -> list[str]:
    """
    Sort a list of words from a-z
    """
    return sorted(word_list, reverse=descending) # If .sort() is used, returns None not a list. 


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Compute unique word list from a plain text file.")
    parser.add_argument("--file", default="romeo.txt", help="Input filename or path")
    parser.add_argument("--data--dir", default=None, help="Optional data directory to search")
    parser.add_argument("--sort--order", type=bool, default=False, help="Ascending by default. Enter 'True' for Descending")
    args = parser.parse_args(argv)
    
    data_dir = Path(args.data__dir) if args.data__dir else None
    
    try:
        path = resolve_input_path(args.file, data_dir)
        word_list = append_extract_words(path)
    except (FileNotFoundError, ValueError) as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("\nInterrupted by User. Exiting.\n", file=sys.stderr)
        return 130
    
    sorted_word_list = sort_list(word_list, args.sort__order)
    
    print(f"File: {path}")
    print(f"\nSorted word list: {sorted_word_list}")
    return 1

if __name__ == "__main__":
    raise SystemExit(main())