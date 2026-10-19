"""Mini-project #1: contribution & vesting report from a participant CSV.

Pipeline shape (the same shape DataVault will have, in miniature):
    read file → validate each row → compute → report
Pure stdlib `csv` on purpose — feel the manual work now; pandas (later)
will then be a convenience you understand, not magic you depend on.
"""

from __future__ import annotations

import csv
from dataclasses import dataclass

# pathlib.Path = the modern way to handle file paths (portable, readable).
from pathlib import Path

from learning_journey.retirement import annual_contribution, vested_percent

DATA_FILE: Path = Path(__file__).resolve().parent / "participants.csv"
# __file__ = this script's own location; .parent = its folder; / joins paths.
# Why not just "participants.csv"? Because that breaks when the program is
# run from a different folder. Path-relative-to-file always works.


@dataclass(frozen=True, slots=True)
class ReportRow:
    """One participant's computed numbers - data, not text."""

    name: str
    contribution: float
    vested: float


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


def compute_rows(participants: list[dict[str, str]]) -> list[ReportRow]:
    """Convert at the boundary, then compute. No formatting here."""
    return [
        ReportRow(
            name=p["name"],
            contribution=annual_contribution(
                salary=float(p["salary"]),
                deferral_rate=float(p["deferral_pct"]),
                age=int(p["age"]),
            ),
            vested=vested_percent(int(p["years_service"])),
        )
        for p in participants
    ]


def format_row(row: ReportRow) -> str:
    """The report's layout contract, in one place."""
    return f"{row.name:<12} contributes ${row.contribution:<9,.2f} | {row.vested:>4.0%} vested"


def build_report(participants: list[dict[str, str]]) -> list[str]:
    """Compute, then format. Two small pure functions, composed."""
    return [format_row(row) for row in compute_rows(participants)]


if __name__ == "__main__":
    participants = load_participants(DATA_FILE)
    print(f"CONTRIBUTION REPORT - {len(participants)} participants")
    print("-" * 55)
    for line in build_report(participants):
        print(line)
