"""Load the seeded market CSVs into DuckDB as typed raw tables.

Python ingests, dbt decides: this script only lands the files as they are, with
explicit types and load metadata. Every business rule lives in dbt.

Run:  uv run python scripts/load_market_seed.py
"""

from __future__ import annotations

import sys

try:
    import argparse
    import csv
    from dataclasses import dataclass
    from enum import IntEnum, unique
    from pathlib import Path
    from typing import Final

    import duckdb
    import structlog
    from structlog.typing import FilteringBoundLogger

    from learning_journey.paths import DATA_DIR, FOUNDATIONS_DIR
except ImportError as e:
    sys.exit(f"ERROR: missing module. Details: {e}")


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


# Also we can use KW_ONLY from dataclasses to select if only some attributes
# are keyword only while others are not '_: KW_ONLY'


@unique
class ExitCode(IntEnum):
    """POSIX-aligned process exit codes for the Loader CLI.

    ``IntEnum`` values are passed directly to ``sys.exit()``.
    ``@unique`` prevents accidental duplicate values at definition time.
    """

    SUCCESS = 0
    BAD_FILE = 1
    FILE_NOT_FOUND = 2
    OTHER_EXCEPTION = 3


@dataclass(frozen=True, slots=True, kw_only=True)
class LoaderArgs:
    """Typed container for parsed CLI arguments.

    Converts ``argparse.Namespace`` — whose attributes are typed as
    ``Any`` — into a fully typed, immutable dataclass.  Pyright then
    has complete static coverage for every ``args.*`` access in
    ``main()`` and helper functions, catching typos and type
    mismatches at analysis time rather than at runtime.

    ``frozen=True`` prevents accidental mutation after construction.
    Constructed once in ``main()`` immediately after ``parse_args()``;
    passed by value to helper functions.
    """

    seed_dir: Path
    db: Path


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
        except Exception as exc:
            con.rollback()
            raise exc

    return counts


def main(argv: list[str] | None = None) -> ExitCode:
    parse_description = __doc__.splitlines()[0] if __doc__ else ""
    parser = argparse.ArgumentParser(description=parse_description)

    parser.add_argument(
        "--seed-dir",
        type=Path,
        default=DEFAULT_SEED_DIR,
        help=f"Directory where CSV files are. Default: {DEFAULT_SEED_DIR}",
    )
    parser.add_argument(
        "--db",
        type=Path,
        default=DEFAULT_DB,
        help=f"Directory where DuckDB database should be created at. Default: {DEFAULT_DB}",
    )

    raw_args = parser.parse_args(argv)
    args = LoaderArgs(seed_dir=raw_args.seed_dir, db=raw_args.db)

    try:
        counts = load_all(args.seed_dir.resolve(), args.db.resolve())
        for table, n in counts.items():
            log.info("loaded", schema=RAW_SCHEMA, table=table, rows=n)
    except ValueError as e:
        log.error("value_error", message=e)
        return ExitCode.BAD_FILE
    except FileNotFoundError as e:
        log.error("file_not_found_error", message=e)
        return ExitCode.FILE_NOT_FOUND
    except Exception as e:
        log.error("other_error", message=e)
        return ExitCode.OTHER_EXCEPTION

    return ExitCode.SUCCESS


if __name__ == "__main__":
    sys.exit(main())
