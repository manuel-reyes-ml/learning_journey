"""
1) Read through the file: mbox-short.txt
2) Extract lines starting with ´X-DSPAM-Confidence
3) From those lines, extract the floating point values on each of the lines and compute the average of those values
4) Print out the average as a floating point number
"""

from __future__ import annotations # For future compatibility with type hinting of return types

from pathlib import Path
from typing import Iterator, Optional
import argparse
import sys

SCRIPT_DIR = Path(__file__).parent
DEFAULT_DATA_DIR = SCRIPT_DIR / "data"

PREFIX = "X-DSPAM-Confidence:"

def extract_confidences(path: Path) -> Iterator[float]:
    """
    Yield spam-confidence floats from lines starting with PREFIX.
    Uses fast parsing via partition, not regex.
    """
    with path.open("r", encoding ="utf-8", errors="replace") as f:
        for line in f:
            if not line.startswith(PREFIX):
                continue
            _, _, tail = line.partition(":")
            tail = tail.strip()
            if not tail:
                continue
            
            try:
                yield float(tail)
            except ValueError:
                # Skip lines where conversion to float fails
                continue

def compute_mean_and_count(path: Path) -> tuple[float, int]:
    total = 0.0
    count = 0
    for x in extract_confidences(path):
        total += x
        count += 1
    if count == 0:
        raise ValueError(f"No '{PREFIX}' values found in file: {path}")
    return (total / count), count

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

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Compute mean X-DSPAM-Confidence from an mbox file.")
    parser.add_argument("--file", default="mbox-short.txt", help="Input filename or path")
    parser.add_argument("--data--dir", default=None, help="Optional data directory to search")
    parser.add_argument("--round", type=int, default=2, dest="round_digits", help="Digits to round output")
    args = parser.parse_args(argv)
    
    data_dir = Path(args.data__dir) if args.data__dir else None
    
    try:
        path = resolve_input_path(args.file, data_dir)
        avg, count = compute_mean_and_count(path)
    except (FileNotFoundError, ValueError) as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("\nInterrupted by User. Exiting.\n", file=sys.stderr)
        return 130
    
    print(f"File: {path}")
    print(f"Count: {count}")
    print(f"Average: {avg} (rounded: {round(avg, args.round_digits)})")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())