import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbose", action="store_true")
args = parser.parse_args()

print(f"verbose = {args.verbose}")
print(f"type = {type(args.verbose)}")

# =============================================================================
# ARGPARSE ACTION QUICK REFERENCE
# =============================================================================
#
# action controls WHAT HAPPENS when an argument is encountered.
#
# | action         | Meaning                        | Example        | Result        |
# |----------------|--------------------------------|----------------|---------------|
# | (none)         | Store the value (default)      | -v hello       | "hello"       |
# | "store_true"   | Store True if flag present     | -v             | True          |
# | "store_false"  | Store False if flag present    | --no-cache     | False         |
# | "count"        | Count occurrences              | -vvv           | 3             |
# | "append"       | Append to list                 | -f a -f b      | ["a", "b"]    |
# | "store_const"  | Store a constant value         | --debug        | "DEBUG_MODE"  |
#
# Usage Examples:
#     parser.add_argument("-v", "--verbose", action="store_true")
#     parser.add_argument("-q", "--quiet", action="store_false")
#     parser.add_argument("-v", "--verbose", action="count", default=0)  # -vvv = 3
#     parser.add_argument("--file", action="append")  # Multiple files
#
# =============================================================================