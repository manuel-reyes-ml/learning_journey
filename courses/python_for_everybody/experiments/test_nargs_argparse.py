import argparse

parser = argparse.ArgumentParser()
parser.add_argument("height", nargs="?") # Accept Zero or one value (optional)
parser.add_argument("--files", nargs="*")
args = parser.parse_args()

print(f"height = {args.height}")
print(f"type = {type(args.height)}")
print(f"files = {args.files}")

# =============================================================================
# ARGPARSE NARGS QUICK REFERENCE
# =============================================================================
#
# nargs controls HOW MANY values an argument accepts.
#
# | nargs   | Meaning              | Example Input  | Result                    |
# |---------|----------------------|----------------|---------------------------|
# | (none)  | Exactly 1 (required) | 5              | "5"                       |
# | "?"     | Zero or one          | (empty) or 5   | None or "5"               |
# | "*"     | Zero or more         | 5 10 15        | ["5", "10", "15"]         |
# | "+"     | One or more          | 5 10 15        | ["5", "10", "15"]         |
# | 2       | Exactly N            | 5 10           | ["5", "10"]               |
#
# Usage Example:
#     parser.add_argument("height", nargs="?")  # Optional positional arg
#     parser.add_argument("files", nargs="*")   # Zero or more files
#     parser.add_argument("coords", nargs=2)    # Exactly 2 values (x, y)
#
# =============================================================================