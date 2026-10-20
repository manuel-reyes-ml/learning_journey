"""recon-toy v0.1 — end-to-end pipeline: generate → load → reconcile → report.

One command, four stages — the shape of every data pipeline you will
ever build, including DataVault's real one:
    EXTRACT (make_data) → LOAD (load_db) → TRANSFORM/CHECK (recon) → REPORT
"""

from __future__ import annotations

import argparse
import sqlite3
from pathlib import Path

from learning_journey.projects import load_db, make_data, recon

OUTPUT_DIR: Path = Path(__file__).parent / "output"


def run_pipeline(n: int) -> Path:
    """Run all stages; write the exceptions report; return its path.

    Returning the path (instead of just printing) makes the pipeline
    TESTABLE — a test can open the file and check its contents.
    """
    print("[1/4] Generating synthetic data...")
    participants = make_data.make_partipants(n)
    distributions = make_data.make_distributions(participants)
    make_data.write_csv(make_data.OUT_DIR / "system_a_participants.csv", participants)
    make_data.write_csv(make_data.OUT_DIR / "system_b_distributions.csv", distributions)

    print("[2/4] Loading SQLite...")
    load_db.load()

    print("[3/4] Reconciling...")
    conn = sqlite3.connect(load_db.DB_PATH)
    missing = recon.missing_in_b(conn)
    totals = recon.totals_by_code(conn)
    conn.close()

    print("[4/4 Writing report...]")
    OUTPUT_DIR.mkdir(exist_ok=True)
    report_path = OUTPUT_DIR / "exceptions_report.txt"
    lines = [
        "RECONCILIATION EXCEPTIONS REPORT (synthetic data)",
        "=" * 50,
        f"Participants missing from System B: {len(missing)}",
        *(f"     {pid}  {name}" for pid, name in missing),
        # *( ... ) unpacks a generator into the list — a compact way to
        # splice many lines in. If it reads like magic today, write the
        # for-loop version instead; elegance is optional, clarity is not.
        "",
        "Total by Box-7 code:",
        *(f"     code {c}: {n:>3} rows  ${t:>12,.2f}" for c, n, t in totals),
    ]
    report_path.write_text("\n".join(lines))
    print(f"✅ Report → {report_path}")
    return report_path


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="recon-toy: generate, load, reconcile, and report."
    )
    parser.add_argument(
        "--participants",
        "-p",
        type=int,
        default=50,
        help="number of synthetic participants to generate (default: 50)",
    )
    parser.add_argument(
        "--tolerance",
        "-t",
        type=float,
        default=0.01,
        help="amount tolerance in dollars for matching (default: 0.01)",
    )
    args = parser.parse_args()

    run_pipeline(args.participants)
