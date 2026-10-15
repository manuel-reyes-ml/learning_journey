"""Day 15: parsing messy financial text with string methods.

Real systems export ugly text. Before regex (later), master the manual
tools: .split(), .strip(), .replace(), slicing. Feeling this pain is the
point — regex will then be a relief you understand, not an incantation.
"""

# Simulated export lines from a legacy system (note inconsistent spacing —
# that's realism, not sloppiness):
raw_lines = [
    "ACCT-10023 | GROSS: $12,450.00 | CODE: 7",
    "ACCT-10087 | GROSS: $3,200.50  | CODE: 1",
    "ACCT-10112 | GROSS: $45,000.00 | CODE: G",
    "ACCT-9 | GROSS: N/A | CODE:",
]

for line in raw_lines:
    # STEP 1 — split the line into parts on the delimiter:
    parts = line.split("|")  # → ["ACCT-10023 ", " GROSS: $12,450.00 ", " CODE: 7"]

    # STEP 2 — clean each part. Chaining methods reads left→right:
    account = parts[0].strip()  # kill stray spaces
    # [0] is INDEXING: Python counts from 0. parts[0] = first item.

    # STEP 3 — the amount needs surgery:
    gross_text = parts[1].strip()  # "GROSS: $12,450.00"
    gross_text = gross_text.removeprefix("GROSS:")  # " $12,450.00"
    gross_text = gross_text.strip().removeprefix("$")  # "12,450.00"
    gross_text = gross_text.replace(",", "")  # "12450.00" — commas break float()
    gross = float(gross_text)  # NOW it converts

    code = parts[2].split(":")[1].strip()  # split "CODE: 7" on ":", take part 1

    print(f"{account}: ${gross:>10,.2f}  code={code}")

# Exercise (do it now): add a malformed line like "ACCT-9 | GROSS: N/A | CODE:"
# and make the loop survive it with try/except, printing a clear warning.
# Data that can't be parsed must be REPORTED, never silently dropped —
# in a 1099 pipeline, a silently dropped row is a participant who doesn't
# get a form. Boundary rule, always.
