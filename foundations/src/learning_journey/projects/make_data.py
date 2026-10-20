"""Generate synthetic data simulating TWO systems that should agree — but don't.

This mirrors the real DataVault S1 problem (Matrix vs Relius): two systems
about the same participants, with discrepancies hiding between them.
Public-repo governance: 100% synthetic, invented names, fake IDs. Always.
"""

from __future__ import annotations

import csv
import random
from pathlib import Path

# --- SEEDING: the reproducibility habit ---
# random normally differs every run. seed(42) makes the "random" sequence
# IDENTICAL every run → teammates (and tests!) see exactly your data.
# Reproducibility is a pillar of production data work; it starts here.
random.seed(42)

OUT_DIR: Path = Path(__file__).resolve().parent / "data"

FIRST: list[str] = ["Ana", "Luis", "Mia", "Omar", "Sara", "Ken", "Rita", "Jon", "Eva", "Max"]
LAST: list[str] = ["Torres", "Vega", "Chen", "Ali", "Kim", "Ruiz", "Cole", "Diaz", "Wu", "Ford"]
BOX7_CODES: list[str] = ["1", "2", "4", "7", "G"]


def make_participants(n: int) -> list[dict]:
    """System A: the recordkeeper's participant file."""
    rows = []
    for i in range(n):
        rows.append(
            {
                "participant_id": f"P{1000 + i}",
                "name": f"{random.choice(FIRST)} {random.choice(LAST)}",
                "salary": round(random.uniform(40_000, 180_000), 2),
                "deferral_pct": round(random.uniform(0.03, 0.05), 3),
            }
        )
    return rows


def make_distributions(participants: list[dict]) -> list[dict]:
    """System B: the payer's distribution file — WITH planted defects.

    We inject known discrepancies ON PURPOSE, so we can verify our recon
    logic finds exactly them. This is the golden-dataset idea: you can't
    trust a checker you haven't checked. (Your future eval gates — RAGAS
    thresholds on PolicyPulse — are this same principle aimed at LLMs.)
    """
    rows = []
    for p in participants:
        if random.random() < 0.15:
            continue  # DEFECT 1: ~15% missing from System B

        gross = round(random.uniform(1_000, 50_000), 2)
        if random.random() < 0.10:
            gross = round(gross + 0.10, 2)  # DEFECT 2: ~10% off-by-10-cents

        rows.append(
            {
                "participant_id": p["participant_id"],
                "gross": gross,
                "box7_code": random.choice(BOX7_CODES),
                "dist_date": f"2026-{random.randint(1, 6):02d}-{random.randint(1, 28):02d}",
                # :02d pads to 2 digits → "2026-03-07" not "2026-3-7".
                # Consistent date formats: tiny habit, prevents entire bug species.
            }
        )
    return rows


def write_csv(path: Path, rows: list[dict]) -> None:
    """-> None: this function performs an ACTION, returns nothing."""
    path.parent.mkdir(parents=True, exist_ok=True)  # ensure folder exists
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    participants = make_participants(50)
    distributions = make_distributions(participants)

    write_csv(OUT_DIR / "system_a_participants.csv", participants)
    write_csv(OUT_DIR / "system_b_distributions.csv", distributions)

    print(f"System A: {len(participants)} participants")
    print(f"System B: {len(distributions)} distributions")
    print(f"Planted gap: {len(participants) - len(distributions)} missing rows to find")
