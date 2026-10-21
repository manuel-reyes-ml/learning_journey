"""recon-toy v0.1 — end-to-end pipeline: generate → load → reconcile → report.

One command, four stages — the shape of every data pipeline you will
ever build, including DataVault's real one:
    EXTRACT (make_data) → LOAD (load_db) → TRANSFORM/CHECK (recon) → REPORT
"""

from __future__ import annotations

import argparse
import sqlite3
from contextlib import closing
from pathlib import Path

import structlog

from learning_journey.projects import load_db, make_data, matcher, recon

log = structlog.get_logger()
# get_logger() gives you a logger. With structlog, you log EVENTS with
# KEY-VALUE data, not sentences with numbers baked in.

ROOT_DIR: Path = Path(__file__).resolve().parents[4]
OUTPUT_DIR: Path = Path(__file__).parent / "output"


def render_report(result: matcher.MatchResult, totals: list[tuple[str, int, float]]) -> str:
    """Build the exceptions-report text from a MatchResult.

    PURE function: data in, string out — no files, no DB, no prints.
    That is what lets a test check the report without running the pipeline.
    """
    checked = len(result.matched) + len(result.missing_in_b) + len(result.amount_mismatch)

    lines: list[str] = [
        "RECONCILIATION EXCEPTIONS REPORT (synthetic data)",
        "=" * 50,
        f"Participants checked  : {checked:>5}",
        f"   Matched            : {len(result.matched):>5}",
        f"   Missing in System B: {len(result.missing_in_b):>5}",
        f"   Amount mismatch    : {len(result.amount_mismatch):>5}",
        "",
        "MISSING IN SYSTEM B",
    ]
    if result.missing_in_b:
        for p in result.missing_in_b:
            lines.append(f"  {p['participant_id']}  {p['name']}")
    else:
        lines.append("  none")

    lines += ["", "AMOUNT MISMATCHES"]
    if result.amount_mismatch:
        lines.append(f"  {'participant':<12}{'expected':>14}{'actual':>14}{'difference':>14}")
        for m in result.amount_mismatch:
            lines.append(
                f"   {m['participant_id']:<12}"
                f"{m['expected']:>14,.2f}"
                f"{m['actual']:>14,.2f}"
                f"{m['difference']:>+14,.2f}"  # + shows direction: over vs under
            )
    else:
        lines.append("  none")

    lines += ["", "TOTALS BY BOX-7 CODE (System B)"]
    for code, n, total in totals:
        lines.append(f"  code {code}: {n:>3} rows   ${total:>12,.2f}")

    log.info(
        "report_rendered",
        missing_b=len(result.missing_in_b),
        mismatch=len(result.amount_mismatch),
        matched=len(result.matched),
    )

    return "\n".join(lines) + "\n"  # files end with a newline


def run_pipeline(n: int, tol: float) -> Path:
    """Run all stages; write the exceptions report; return its path.

    Returning the path (instead of just printing) makes the pipeline
    TESTABLE — a test can open the file and check its contents.
    """
    participants = make_data.make_participants(n)
    distributions = make_data.make_distributions(participants)
    make_data.write_csv(make_data.OUT_DIR / "system_a_participants.csv", participants)
    make_data.write_csv(make_data.OUT_DIR / "system_b_distributions.csv", distributions)
    log.info(
        "[1/5]_synthetic_data_generated",
        participants=len(participants),
        distributions=len(distributions),
    )

    load_db.load()
    log.info("[2/4]_sqlite_loaded", db_path=load_db.DB_PATH)

    # Python matcher is the report's source of truth. Default tolerance for
    # now; --tolerance gets wired in a later step.
    result = matcher.match_records(participants, distributions, amount_tolerance=tol)
    log.info("[3/5]_recon_data_generated", data_container=str(type(result)))

    # The current conn.close() would also be skipped if a query raised an error.
    # 'closing' covers that case.
    with closing(sqlite3.connect(load_db.DB_PATH)) as conn:
        totals = recon.totals_by_code(conn)
        sql_missing = {pid for pid, _name in recon.missing_in_b(conn)}

    # (R2) Parity gate: two independent implementations must agree.
    py_missing = {p["participant_id"] for p in result.missing_in_b}
    if py_missing != sql_missing:
        raise RuntimeError(
            "SQL/Python disagree on missing-in-B: "
            f"only SQL={sorted(sql_missing - py_missing)}, "
            f"only Python={sorted(py_missing - sql_missing)}"
        )
    log.info("[4/5]_sql_python_reconciled", status=py_missing == sql_missing)

    OUTPUT_DIR.mkdir(exist_ok=True)
    report_path = OUTPUT_DIR / "exceptions_report.txt"
    report_path.write_text(render_report(result, totals), encoding="utf-8")
    log.info("[5/5]_txt_file_written", file_path=report_path)

    print(f"✅ Report → {report_path.relative_to(ROOT_DIR)}")

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

    run_pipeline(args.participants, args.tolerance)
