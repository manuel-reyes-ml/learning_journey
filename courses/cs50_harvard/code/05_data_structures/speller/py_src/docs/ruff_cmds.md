# Speller Ruff Lint commands — `ruff` Cookbook

```bash
# Counts violations per rule
ruff check src/ --statistics

# Group specific codes (E501) per file
ruff check src/ --select <CODE> --output-format=concise | \
  awk -F: '{print $1}' | sort | uniq -c | sort -rn

# Get a file with actual error lines, sorted by source code file
ruff check src/ --select <CODE> --output-format=concise > <code>_report.txt

# Show each violation with surrounding context per code (E501)
ruff check src/ --select <CODE> --output-format=full

# Preview safe fixes
# Read what will change before it changes
ruff check src/ --diff

# Apply safe fixes
ruff check src/ --fix

# Unsafe fixes. Decide rule-by-rule, commit-by-commit
ruff check src/ --select <CODE> --diff --unsafe-fixes

# Preview format fixes
ruff format src/ --diff

# Is faster and safer for whitespace rules, than ruff check src/ --fix
ruff format src/
```

If you need green CI today because pre-commit + Actions is the next milestone and you can't ship
it red, Ruff has an explicit migration escape hatch: ruff check /path/to/file.py --add-noqa
automatically adds noqa directives to all lines containing violations, with the appropriate rule
codes — explicitly designed for migrating a codebase to Ruff.

Combined with RUF100 (which Ruff calls "unused-noqa"), this becomes a ratchet: every existing
violation is suppressed with an explicit # noqa: RULE comment, new code must be clean, and you
remove noqa comments as you fix them. RUF100 itself flags any noqa that no longer suppresses
anything, so you can't forget about them.

