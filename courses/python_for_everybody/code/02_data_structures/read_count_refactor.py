"""
1) Read through the file: mbox-short.txt
2) Extract lines starting with ´X-DSPAM-Confidence
3) From those lines, extract the floating point values on each of the lines and compute the average of those values
4) Print out the average as a floating point number
"""

from __future__ import annotations # Allows to use Types Hinting features (like using | for Union) in older versions of Python

from pathlib import Path # Modern standard library for handling file system paths. Treats paths as objects instead of strings. Script is portable across OSes.
from typing import Iterator, Optional # These are used for type hinting to specify expected types of variables and function return values(act as documentation)
                                      #     - Iterator: describes an object that can be iterated over (like a generator or a list)
                                      #     - Optional: indicates that a variable can be of a specified type or None

import argparse # Used to build a command-line interface(CLI) for the script. Handles logical parsing of command-line arguments.
import sys # Provides tools and functions to interact with the Python runtime environment, including access to command-line arguments and error output.


# ALL_CAPS indicates a constant value that should not change during execution.
SCRIPT_DIR = Path(__file__).parent # __file__ is a special variable that holds the path of the current script. .parent gets the directory containing the script.
DEFAULT_DATA_DIR = SCRIPT_DIR / "data" # ´/´ operator is overloaded in Path objects to join paths in a platform-independent way.

PREFIX = "X-DSPAM-Confidence:" # The prefix string to look for in the file lines. If changes in the file format, only this constant needs to be updated.

def extract_confidences(path: Path) -> Iterator[float]:
    """
    Yield spam-confidence floats from lines starting with PREFIX.
    Uses fast parsing via partition, not regex.
    """
    with path.open("r", encoding ="utf-8", errors="replace") as f: # with statement ensures the file is properly closed after its block is executed.
        for line in f: # Instead of reading the entire file into memory, we iterate line by line.
            if not line.startswith(PREFIX):
                continue # Skip lines that do not start with the desired prefix and move to the next iteration of the loop (next line in the file).
            _, _, tail = line.partition(":") # partition splits the string into three parts: before the separator, the separator itself ´:´, and after the separator.
                                             # Using ´_´as a variable name is a convention in Python to indicate that we don´t plan to use that value.
            tail = tail.strip() # Remove any leading or trailing whitespace from the extracted value (including newline characters '\n').             
            if not tail:
                continue
            
            try:
                yield float(tail) # Turns function into a generator that yields one value at a time, allowing for memory-efficient processing of large files.
                                  # Yield pauses the function, returning the value to the caller, and retains the function's state for the next call.
            except ValueError:
                # Skip lines where conversion to float fails
                continue

def compute_mean_and_count(path: Path) -> tuple[float, int]:
    """
    Compute the mean of spam-confidence values from the given file path.
    Returns a tuple of (mean, count).
    Raises ValueError if no valid values are found.
    """
    total = 0.0
    count = 0
    for x in extract_confidences(path): # Reaches into the generator function to get each confidence value one by one. Memory usage stays flat for 10 lines or 10 million lines.
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
    p = Path(fname) # Convert the input filename string into a Path object for easier manipulation( use Path methods: is_file(), open(), exists(), etc.)
    if p.is_file(): # Check if the provided path exists as a file.
        return p
    
    if data_dir is None:
        data_dir = DEFAULT_DATA_DIR
        
    candidate = data_dir / fname
    if candidate.is_file():
        return candidate
    
    raise FileNotFoundError(f"File not found: {fname} (also tried: {candidate})")

def main(argv: list[str] | None = None) -> int: # Use a main function as the entry point for the script. Makes it testable and reusable.
    parser = argparse.ArgumentParser(description="Compute mean X-DSPAM-Confidence from an mbox file.") # argparse.ArgumentParser creates a new argument parser object. 
                                                                                                       #   is like a receptionist that understands how to interpret command-line arguments.
    parser.add_argument("--file", default="mbox-short.txt", help="Input filename or path") # .add_argument, this tells the receptionist what arguments to expect, here: --file
    parser.add_argument("--data--dir", default=None, help="Optional data directory to search")
    parser.add_argument("--round", type=int, default=2, dest="round_digits", help="Digits to round output")
    args = parser.parse_args(argv) # .parse_args processes the command-line arguments provided when the script is run. It returns an object (args) with attributes corresponding to the defined arguments.
    
    data_dir = Path(args.data__dir) if args.data__dir else None
    
    try:
        path = resolve_input_path(args.file, data_dir)
        avg, count = compute_mean_and_count(path)
    except (FileNotFoundError, ValueError) as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1 # Return a non-zero exit code to indicate an error occurred.
    except KeyboardInterrupt:
        print("\nInterrupted by User. Exiting.\n", file=sys.stderr)
        return 130 # 130 is the standard exit code for script termination due to Ctrl+C (KeyboardInterrupt)
    
    print(f"File: {path}")
    print(f"Count: {count}")
    print(f"Average: {avg} (rounded: {round(avg, args.round_digits)})")
    return 0 # Return 0 to indicate successful completion of the script.

if __name__ == "__main__": # This condition checks if the script is being run directly (not imported as a module).
    raise SystemExit(main()) # SystemExit is raised to exit the program cleanly, passing the return value of main() as the exit code.
                             #    if main() returns 0, the program exits successfully; any non-zero value indicates an error.


"""
Why argparse is better than input()
You might be used to using input("Enter filename: "). In data science, argparse is superior because it allows for Automation. 
You can write a "Bash Script" (a simple text file) that runs your Python code 100 times with 100 different files overnight, 
without a human needing to sit there and type into a prompt.
"""