#!/bin/bash
# Auto-format Python files after every agent edit.
# Prevents the agent from generating code that fails `make lint`.
# Your diff is always pre-formatted when you review it.

FILE="$1"

# Only format Python files
if [[ "$FILE" == *.py ]]; then
    black "$FILE" 2>/dev/null
    ruff check --fix "$FILE" 2>/dev/null
fi
