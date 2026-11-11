""" """

from __future__ import annotations

import argparse
import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Final

import duckdb
import structlog
from structlog.typing import FilteringBoundLogger

from learning_journey.paths import DATA_DIR, FOUNDATIONS_DIR

log: FilteringBoundLogger = structlog.get_logger("load_market_seed")

DEFAULT_SEED_DIR: Final[Path] = DATA_DIR / "market_seed"
DEFAULT_DB: Final[Path] = FOUNDATIONS_DIR / "db" / "market_rehearsal" / "market.duckdb"
# = profiles.yml path
RAW_SCHEMA: Final[str] = "raw_market"


@dataclass(frozen=True, slots=True)
class RawTable:
    """One CSV -> one raw table. The column dict is the contract (order matters)."""

    name: str
    file: str
    columns: dict[str, str]


TABLES: Final[tuple[RawTable, ...]] = (
    RawTable(
        name="bars_daily",
        file="bars_daily.csv",
        columns={
            "ticker": "VARCHAR",
            "session_date": "DATE",
            "open": "DOUBLE",
            "high": "DOUBLE",
            "low": "DOUBLE",
            "close": "DOUBLE",
            "volume": "BIGINT",
        },
    ),
    RawTable(
        name="insider_events",
        file="insider_events.csv",
        columns={
            "event_id": "VARCHAR",
            "ticker": "VARCHAR",
            "txn_code": "VARCHAR",
            "filing_date": "DATE",
            "accepted_at": "TIMESTAMP",  # naive America/New_York, by design
            "boundary_case": "VARCHAR",
        },
    ),
)


def check_header(path: Path, expected: list[str]) -> None:
    """Fail fast if the generator's header drifted from the contract.

    read_csv(columns=...) maps by POSITION, so a reordered or renamed column
    would load silently into the wrong field without this check.
    """
    with path.open(encoding="utf-8", newline="") as f:
        header = next(csv.reader(f), [])
    if header != expected:
        raise ValueError(f"{path.name}: header {header} != contract {expected}")


def load_all(seed_dir: Path, db_path: Path) -> dict[str, int]:
    """Load every table in ONE transaction: all three update, or none do."""
    for t in TABLES:  # validate everything before touching the database
        path = seed_dir / t.file
        if not path.is_file():
            raise FileNotFoundError(f"missing seed file: {path} (run the generator first)")
        check_header(path, list(t.columns))

    db_path.parent.mkdir(parents=True, exist_ok=True)
    counts: dict[str, int] = {}

    with duckdb.connect(str(db_path)) as con:
        con.begin()
        try:
            con.execute(f"create schema if not exists {RAW_SCHEMA}")
            for t in TABLES:
                path = seed_dir / t.file
                # Identifiers come from the TABLES constant (trusted); values are bound.
                con.execute(
                    f"""
                    create or replace table {RAW_SCHEMA}.{t.name} as
                    select *,
                           $file              as _source_file,
                           current_timestamp  as _loaded_at
                    from read_csv($path, header = true, columns = $cols)
                    """,
                    {"path": str(path), "cols": t.columns, "file": t.file},
                )
                row = con.execute(f"select count(*) from {RAW_SCHEMA}.{t.name}").fetchone()
                counts[t.name] = row[0] if row else 0
                if counts[t.name] == 0:
                    raise ValueError(f"{t.file} loaded 0 rows")
            con.commit()
        except Exception:
            con.rollback()
            raise

    return counts


def main(argv: list[str] | None = None) -> None:
    parse_description = __doc__.splitlines()[0] if __doc__ else ""
    parser = argparse.ArgumentParser(description=parse_description)

    parser.add_argument("--seed-dir", type=Path, default=DEFAULT_SEED_DIR)
    parser.add_argument("--db", type=Path, default=DEFAULT_DB)

    args = parser.parse_args(argv)

    counts = load_all(args.seed_dir.resolve(), args.db.resolve())
    for table, n in counts.items():
        log.info("loaded", schema=RAW_SCHEMA, table=table, rows=n)


if __name__ == "__main__":
    main()
