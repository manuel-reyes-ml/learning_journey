"""Load the synthetic CSVs into SQLite.

SQLite = a full SQL database in a single file, built into Python (import
sqlite3 — nothing to install). Perfect for learning; also genuinely used
in production for embedded cases. Your Mode tutorial SQL now runs against
data YOU made.
"""

from __future__ import annotations

import csv
import sqlite3
from pathlib import Path

DATA_DIR: Path = Path(__file__).resolve().parent / "data"
DB_PATH: Path = DATA_DIR / "recon.db"


def load() -> None:
    conn = sqlite3.connect(DB_PATH)  # opens (or creates) the DB file

    # Schema = the table blueprint: column names + types.
    # SQL types here: TEXT (string), REAL (float).
    # PRIMARY KEY = unique identifier; the DB REFUSES duplicate ids.
    # The database enforcing rules itself (not trusting the app to behave)
    # is a core data-engineering idea — your first data contract.
    conn.execute("DROP TABLE IF EXISTS participants")  # clean slate on rerun
    conn.execute("DROP TABLE IF EXISTS distributions")
    conn.execute("""
        CREATE TABLE participants (
            participant_id TEXT PRIMARY KEY,
            name           TEXT NOT NULL,
            salary         REAL NOT NULL,
            deferral_pct   REAL NOT NULL
        )
    """)
    conn.execute("""
        CREATE TABLE distributions (
            participant_id TEXT NOT NULL,
            gross          REAL NOT NULL,
            box7_code      TEXT NOT NULL,
            dist_date      TEXT NOT NULL
        )
    """)

    for table, filename in [
        ("participants", "system_a_participants.csv"),
        ("distributions", "system_b_distributions.csv"),
    ]:
        with (DATA_DIR / filename).open(encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
        cols = list(rows[0].keys())
        placeholders = ", ".join("?" for _ in cols)  # "?, ?, ?, ?"
        # The ?s are PARAMETERIZED values — sqlite fills them safely.
        # NEVER build SQL by pasting values into the string (f-strings here
        # = SQL injection, the classic security hole). ?s, always.
        conn.executemany(
            f"INSERT INTO {table} ({', '.join(cols)}) VALUES ({placeholders})",
            [tuple(r.values()) for r in rows],
        )

    conn.commit()  # commit = actually save the changes
    n_p = conn.execute("SELECT COUNT(*) FROM participants").fetchone()[0]
    n_d = conn.execute("SELECT COUNT(*) FROM distributions").fetchone()[0]
    print(f"Loaded {n_p} participants, {n_d} distributions -> {DB_PATH.name}")
    conn.close()


if __name__ == "__main__":
    load()
