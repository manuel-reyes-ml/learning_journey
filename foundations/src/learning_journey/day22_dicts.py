"""Day 22: dictionaries — THE data structure of data work.

A dict maps keys → values with instant lookup. Your mental model from
work: a dict is an indexed filing cabinet. participant_id → their record,
in one step, no searching. DataVault's canonical model will be exactly
'dicts with discipline.'
"""

from __future__ import annotations

import csv
from pathlib import Path

DATA: Path = Path(__file__).resolve().parent / "projects" / "data"

with (DATA / "system_b_distributions.csv").open(encoding="utf-8") as f:
    distributions = list(csv.DictReader(f))

# --- Pattern 1: COUNT per key (top-3 most useful loop in data work) ---
count_by_code: dict[str, int] = {}
for row in distributions:
    code = row["box7_code"]
    # .get(key, default) reads a key OR returns the default if absent —
    # this line means "current count, or 0 if first sighting, plus one":
    count_by_code[code] = count_by_code.get(code, 0) + 1
print("Distributions per code:", count_by_code)

# --- Pattern 2: SUM per key (same shape, different aggregate) ---
total_by_participant: dict[str, float] = {}
for row in distributions:
    pid = row["participant_id"]
    total_by_participant[pid] = total_by_participant.get(pid, 0.0) + float(row["gross"])

# --- Pattern 3: INDEX for instant lookup (the join, in Python form) ---
with (DATA / "system_a_participants.csv").open(encoding="utf-8") as f:
    participants = list(csv.DictReader(f))
by_id = {p["participant_id"]: p for p in participants}
# ^ a DICT COMPREHENSION: builds {id: row} in one line.
# Looking up by_id["P1007"] is instant — no scanning. This index IS what
# a SQL JOIN does under the hood. Yesterday SQL; today you see the gears.

sample_id = distributions[0]["participant_id"]
print(
    f"{sample_id} belongs to {by_id[sample_id]['name']}, "
    f"total distributed ${total_by_participant[sample_id]:,.2f}"
)
