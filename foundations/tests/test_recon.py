"""Prove the recon finds EXACTLY the planted defects — the golden-dataset test."""

from __future__ import annotations

import sqlite3

from learning_journey.projects.load_db import DB_PATH, load
from learning_journey.projects.recon import missing_in_b, totals_by_code


def test_missing_count_matches_planted_gap() -> None:
    load()  # rebuild DB fresh → deterministic (seed 42)
    conn = sqlite3.connect(DB_PATH)
    n_participants = conn.execute("SELECT COUNT(*) FROM participants").fetchone()[0]
    n_distributions = conn.execute("SELECT COUNT(*) from distributions").fetchone()[0]
    planted_gap = n_participants - n_distributions
    assert len(missing_in_b(conn)) == planted_gap
    conn.close()


def test_every_code_total_positive() -> None:
    conn = sqlite3.connect(DB_PATH)
    for _code, n, total in totals_by_code(conn):
        # _code: leading underscore = "unpacked but deliberately unused"
        assert n > 0 and total > 0
    conn.close()
