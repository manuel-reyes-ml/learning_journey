"""Mini-project #1: contribution & vesting report from a participant CSV.

Pipeline shape (the same shape DataVault will have, in miniature):
    read file → validate each row → compute → report
Pure stdlib `csv` on purpose — feel the manual work now; pandas (later)
will then be a convenience you understand, not magic you depend on.
"""

from __future__ import annotations

import csv
from pathlib import Path
# pathlib.Path = the modern way to handle file paths (portable, readable).

from learning_journey.retirement import annual_contribution, vested_percent

DATA_FILE: Path = Path(__file__).resolve().parent / "participants.csv"
# __file__ = this script's own location; .parent = its folder; / joins paths.
# Why not just "participants.csv"? Because that breaks when the program is
# run from a different folder. Path-relative-to-file always works.


def load_participants(path: Path) -> list[dict[str, str]]:
    """Read the CSV into a list of dicts (one dict per row).

    DictReader maps each row to {"name": "Ana Torres", "age": "34", ...}.
    NOTE: every value arrives as a STRING — files don't carry types.
    Converting str→int/float at the boundary is OUR job (Day 4's lesson,
    now at file scale).
    """
    with path.open(encoding="utf-8") as f:
        # `with` = context manager: guarantees the file closes, even on error.
        return list(csv.DictReader(f))


def build_report(participants: list[dict[str, str]]) -> list[str]:
    """Compute one report line per participant. Returns lines, prints nothing.

    (Separating computation from printing = testable computation.)
    """
    lines = []
    for p in participants:
        contribution = annual_contribution(
            salary=float(p["salary"]),
            deferral_rate=float(p["deferral_pct"]),
            age=int(p["age"]),
        )
        vested = vested_percent(int(p["years_service"]))
        lines.append(
            f"{p['name']:<12} contributes ${contribution:>9,.2f} | {vested:>4.0%} vested"
        )  # :<12 pads name to 12 chars → columns align like a real report
    return lines


if __name__ == "__main__":
    participants = load_participants(DATA_FILE)
    print(f"CONTRIBUTION REPORT - {len(participants)} participants")
    print("-" * 55)
    for line in build_report(participants):
        print(line)
