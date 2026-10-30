"""Reconciliation queries, callable (and therefore testable) from Python."""

from __future__ import annotations

import sqlite3
from pathlib import Path

from learning_journey.paths import DATA_DIR

DB_PATH: Path = DATA_DIR / "recon.db"


def missing_in_b(conn: sqlite3.Connection) -> list[tuple[str, str]]:
    """Participants with no distribution row. Returns (id, name) tuples.

    A TUPLE is like a list but immutable (can't be changed after creation) —
    the natural shape for a fixed-size record like a query row.
    """
    query = """
        SELECT p.participant_id, p.name
            FROM participants       AS p                -- AS p = table alias (shorthand)
            LEFT JOIN distributions AS d
                ON p.participant_id = d.participant_id  -- ON = the matching rule
            WHERE d.participant_id IS NULL;             -- NULL needs IS, not =
    """
    return conn.execute(query).fetchall()


def totals_by_code(conn: sqlite3.Connection) -> list[tuple[str, int, float]]:
    """(box7_code, count, total_gross) per code, largest total first."""
    query = """
        SELECT box7_code,
               COUNT(*)             AS n_distributions,
               ROUND(SUM(gross), 2) AS total_gross
            FROM distributions
            GROUP BY box7_code
            ORDER BY total_gross DESC;
    """
    return conn.execute(query).fetchall()


if __name__ == "__main__":
    conn = sqlite3.connect(DB_PATH)
    missing = missing_in_b(conn)
    print(f"⚠️   {len(missing)} participants missing from System B:")
    for pid, name in missing:  # tuple UNPACKING: two names, one tuple
        print(f"     {pid}  {name}")

    print("\nTotal by Box-7 code:")
    for code, n, total in totals_by_code(conn):
        print(f"     code {code}: {n:>3} rows   ${total:>12,.2f}")
    conn.close()
