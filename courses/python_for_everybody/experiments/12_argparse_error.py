import argparse

def validate_name(value):
    """Custom validator for name argument."""
    if len(value) < 2:
        raise argparse.ArgumentTypeError("Name must be at least 2 characters")
    if not value.isalpha():
        raise argparse.ArgumentTypeError("Name must contain only letters")
    return value.title()  # Transform: "john" -> "John"

parser = argparse.ArgumentParser(description="Test program")
parser.add_argument("name", type=validate_name, help="Your name")

args = parser.parse_args()

print(f"Hello, {args.name}")

# =============================================================================
# ARGPARSE CUSTOM VALIDATION QUICK REFERENCE
# =============================================================================
#
# Use `type=` with a custom function to validate AND transform input.
#
# Pattern:
#     def validate_something(value):
#         if invalid_condition:
#             raise argparse.ArgumentTypeError("Your custom message")
#         return transformed_value  # Optional transformation
#
#     parser.add_argument("arg", type=validate_something)
#
# Key Points:
#     - Raise `argparse.ArgumentTypeError` (not `ValueError`)
#     - Function receives the raw string from CLI
#     - Return value becomes `args.your_arg`
#     - Validation happens BEFORE your try/except in main()
#
# =============================================================================