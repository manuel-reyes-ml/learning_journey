from __future__ import annotations

import csv
import sqlite3

from learning_journey.projects.load_db import DB_PATH, load
from learning_journey.projects.make_data import OUT_DIR
from learning_journey.projects.matcher import match_records
from learning_journey.projects.recon import missing_in_b


def _read(name) -> list[dict]:
    with (OUT_DIR / name).open(encoding="utf-8") as f:
        return list(csv.DictReader(f))


def test_python_and_sql_agree_on_missing():
    """Two independent implementations, one answer — or a bug exists."""
    load()
    result = match_records(_read("system_a_participants.csv"), _read("system_b_distributions.csv"))
    conn = sqlite3.connect(DB_PATH)
    assert len(result.missing_in_b) == len(missing_in_b(conn))
    conn.close()
