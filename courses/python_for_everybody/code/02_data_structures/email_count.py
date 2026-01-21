"""
1) Read through the file: mbox-short.txt
2) Extract lines starting with 'PREFIX' (constant variable)
3) Extract the email from each qualified line, print it out and compute the total counter of qualified lines extracted.
4) Print out the total counter.
"""

from __future__ import annotations

from pathlib import Path
from typing import Iterator, Optional

import argparse
import sys

SCRIPT_DIR = Path(__file__).parent
DEFAULT_DATA_DIR = SCRIPT_DIR / "data"
PREFIX = "From " # Update here if search patter changes in the future

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


def _extract_and_generate_emails(path: Path) -> Iterator[str]:
    """
    - Extract lines from txt file that start with 'From '.
    - Review such lines have at least two words.
    - Extract and print out email only.
    - Count number of emails printed out.
    """
    empty = True # Boolean to determine if after 'for loop' finishes no qualified line was found in file
    with path.open() as f:
        for line in f:
            words = line.strip().split() if (line.startswith(PREFIX) and len(line.strip().split()) >= 2) else None
            if not words:
                continue
            empty = False
            email = words[1]
            yield email
    if empty:        
        raise ValueError(f"No lines starting with '{PREFIX}' found in file: {path}")

            
def printout_and_count(path: Path) -> int:
    """
    Utilizer generator function _extract_and_generate_emails to print
    each email and totalized a counter that will be returned from this function.
    """
    counter = 0
    
    print(f"\nList of emails in lines starting with '{PREFIX}' is below:\n")
    for email in _extract_and_generate_emails(path):
        print(email)
        counter += 1
    return counter
        
        
def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=f"Extract lines starting with '{PREFIX}', list emails and count total emails extracted.")
    parser.add_argument("--file", default="mbox-short.txt", help="Input filename or path")
    parser.add_argument("--data--dir", default=None, help="Optional data directory to search")
    args = parser.parse_args(argv)
    
    data_dir = Path(args.data__dir) if args.data__dir else None
    
    
    try:
        path = resolve_input_path(args.file, data_dir)
        counter = printout_and_count(path)
    except (FileNotFoundError, ValueError) as e:
        print(f"Error: {e}", sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("\nInterrupted by User. Exiting.\n", file=sys.stderr)
        return 130
    
    print(f"\nThere were {counter} lines in the file with '{PREFIX}' as the first word.\n")
    return 0



if __name__ == "__main__":
    raise SystemExit(main())
    