"""Load the seeded market CSVs into DuckDB as typed raw tables.

Python ingests, dbt decides: this script only lands the files as they are, with
explicit types and load metadata. Every business rule lives in dbt.

Same pipeline everywhere: your laptop, the extension and CI all run identical steps.

See Also
--------
learning_journey.cli.run : The error boundary that maps failures to exit codes.
learning_journey.logging_setup.configure_logging : Where the log events go.

Notes
-----
Exit codes: 0 success, 2 bad flags, 65 bad data, 66 missing input, 75 database
locked by another process, 130 Ctrl-C, 1 unexpected error.

Examples
--------
Run from the repo root::

    uv run python foundations/scripts/load_market_seed.py
    uv run python foundations/scripts/load_market_seed.py -v --log-file logs/load_market_seed.jsonl
"""

from __future__ import annotations

import sys

try:
    import argparse
    import csv
    import functools
    import time
    from dataclasses import dataclass
    from pathlib import Path
    from typing import Final

    import duckdb
    from rich.table import Table

    from learning_journey import cli
    from learning_journey.errors import DataContractError, InputNotFoundError, ResourceBusyError
    from learning_journey.logging_setup import configure_logging, get_logger
    from learning_journey.paths import DATA_MARKET_DIR, MARKET_DB
except ImportError as e:
    sys.exit(f"ERROR: missing module. Details: {e}")

COMMAND: Final[str] = "load_market_seed"

# A namespaced name (not __name__, which is "__main__" for a script) puts this
# logger under learning_journey.*, so the console filter and the JSON file
# treat it as part of the app.
log = get_logger(f"learning_journey.scripts.{COMMAND}")

# The oldest DuckDB that must open market.duckdb is the driver bundled in
# dbt 2.0.11 (reads storage 64-68 = DuckDB ≤ 1.5.x). Remove when dbt ships a 2.0 driver.
DUCKDB_STORAGE_VERSION: Final[str] = "v1.5.0"

# = profiles.yml path
RAW_SCHEMA: Final[str] = "raw_market"

# Shown in hints. Point this at your real generator command.
GENERATE_SEED_HINT: Final[str] = "Runt he market seed generator first, then rerun this loader."


# `numpydoc ignore=PR02` on the dataclasses below: numpydoc's linter reads source code
# without running it, so it cannot see the __init__ that @dataclass generates.
# The runtime validator (used by Sphinx) sees it and accepts these docstrings.
@dataclass(frozen=True, slots=True)
class RawTable:  # numpydoc ignore=PR02
    """Map one CSV file to one raw table.

    Parameters
    ----------
    name : str
        Table name inside `RAW_SCHEMA`.
    file : str
        CSV file name inside the seed directory.
    columns : dict[str, str]
        Column name to DuckDB type. This dict is the contract, and its order
        matters: ``read_csv(columns=...)`` maps columns by position.
    """

    name: str
    file: str
    columns: dict[str, str]


# Explicit column types are a data contract at the point where data enters the warehouse.
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


@dataclass(frozen=True, slots=True)
class TableLoad:  # numpydoc ignore=PR02
    """Record what one table load produced.

    A typed result instead of a list of mixed types.

    Parameters
    ----------
    table : str
        Table name inside `RAW_SCHEMA`.
    rows : int
        Number of rows loaded.
    """

    table: str
    rows: int


@dataclass(frozen=True, slots=True, kw_only=True)
class LoadReport:  # numpydoc ignore=PR02
    """Record what the whole run produced.

    Parameters
    ----------
    db_path : Path
        The DuckDB file that was written.
    storage_version : str or None
        The file's storage format as DuckDB reports it, e.g. ``"v1.5.0+"``.
    tables : tuple[TableLoad, ...]
        One entry per loaded table, in load order.
    duration_s : float
        Wall-clock time of the load, in seconds.
    """

    db_path: Path
    storage_version: str | None
    tables: tuple[TableLoad, ...]
    duration_s: float


# Also we can use KW_ONLY from dataclasses to select if only some attributes
# are keyword only while others are not '_: KW_ONLY'
@dataclass(frozen=True, slots=True, kw_only=True)
class LoaderArgs:  # numpydoc ignore=PR02
    """Hold the parsed CLI arguments with real types.

    Converts ``argparse.Namespace``, whose attributes are typed as ``Any``, into a
    fully typed, immutable dataclass, so Pyright checks every ``args.*`` access.

    Parameters
    ----------
    data_dir : Path
        Directory containing the seed CSV files.
    db : Path
        DuckDB database file to create or update.
    verbose : int
        Number of ``-v`` flags (0, 1 or 2+).
    log_file : Path or None
        JSON log file path, or None to keep no log file.
    traceback : bool
        Print a full traceback on an unexpected error.
    """

    data_dir: Path
    db: Path
    verbose: int
    log_file: Path | None
    traceback: bool


def _check_header(path: Path, expected: list[str]) -> None:
    """Fail fast if the generator's header drifted from the contract.

    Parameters
    ----------
    path : Path
        The CSV file to check.
    expected : list[str]
        Column names in contract order.

    Raises
    ------
    DataContractError
        If the header differs from `expected` in names, order or count,
        including an empty file.

    Notes
    -----
    ``read_csv(columns=...)`` maps by *position*, so without this check a
    reordered or renamed column would load silently into the wrong field.
    """
    with path.open(encoding="utf-8", newline="") as f:
        header = next(csv.reader(f), [])
    if header != expected:
        raise DataContractError(
            f"{path.name} does not match its column contract",
            hint="Regenerate the seed files, or update TABLES if the contract changed on purpose.",
            details={"expected": ", ".join(expected), "found": ", ".join(header) or "(empty file)"},
        )
    log.debug("heder_checked", file=path.name, columns=len(header))


def _validate_inputs(seed_dir: Path) -> None:
    """Check every seed file before touching the database.

    Parameters
    ----------
    seed_dir : Path
        Directory expected to contain every file listed in `TABLES`.

    Raises
    ------
    InputNotFoundError
        If `seed_dir` or any seed file is missing.
    DataContractError
        If any file's header breaks its contract (see `check_header`).
    """
    if not seed_dir.is_dir():
        raise InputNotFoundError(
            "Seed data directory does not exist",
            hint=GENERATE_SEED_HINT,
            details={"data_dir": str(seed_dir)},
        )
    for t in TABLES:
        path = seed_dir / t.file
        if not path.is_file():
            raise InputNotFoundError(
                f"Seed file not found: {t.file}",
                hint=GENERATE_SEED_HINT,
                details={"path": str(path)},
            )
        _check_header(path, list(t.columns))


def _connect(db_path: Path) -> duckdb.DuckDBPyConnection:
    """Open the DuckDB file in the storage format dbt's driver can read.

    Parameters
    ----------
    db_path : Path
        The database file; created if it does not exist.

    Returns
    -------
    duckdb.DuckDBPyConnection
        An open connection. Use it as a context manager so it gets closed.

    Raises
    ------
    ResourceBusyError
        If another process holds a lock on the file.
    duckdb.IOException
        For any other I/O failure, re-raised unchanged so the error boundary
        reports it as unexpected.

    Notes
    -----
    Python keeps DuckDB 2.0 and simply creates the file in the older format
    (`DUCKDB_STORAGE_VERSION`), so dbt's DuckDB 1.5 can read it.
    """
    try:
        return duckdb.connect(
            str(db_path), config={"storage_compatibility_version": DUCKDB_STORAGE_VERSION}
        )
    except duckdb.IOException as exc:
        if "lock" not in str(exc).lower():
            raise
        raise ResourceBusyError(
            f"{db_path.name} is locked by another process",
            hint="Close whatever holds it open (dbt extension, DuckDB UI, a notebook), then rerun.",
            details={"db": str(db_path)},
        ) from exc


def _load_table(con: duckdb.DuckDBPyConnection, t: RawTable, path: Path) -> TableLoad:
    """Create or replace one raw table from its CSV.

    Parameters
    ----------
    con : duckdb.DuckDBPyConnection
        Connection with an open transaction.
    t : RawTable
        The table and its column contract.
    path : Path
        The CSV file to load.

    Returns
    -------
    TableLoad
        The table name and the number of rows loaded.

    Raises
    ------
    DataContractError
        If a value does not fit its declared type, or the file has no data rows.

    Notes
    -----
    * Identifiers come from the `TABLES` constant (trusted); values are bound
      as parameters, never formatted into the SQL.
    * ``create or replace`` makes reruns idempotent: same result every time.
    * ``_source_file`` and ``_loaded_at`` record lineage and enable dbt source
      freshness checks later.
    * ``raise ... from exc`` keeps DuckDB's original error in the traceback chain.
    """
    try:
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
    except (duckdb.ConversionException, duckdb.InvalidInputException) as exc:
        raise DataContractError(
            f"{t.file} has a value that does not fit its declared column type",
            hint="Fix the value in the file, or the type in TABLE if the contract "
            "changed on purpose.",
            details={"table": t.name, "duckdb_error": str(exc).splitlines()[0]},
        ) from exc

    row = con.execute(f"select count(*) from {RAW_SCHEMA}.{t.name}").fetchone()
    rows = row[0] if row else 0
    if rows == 0:
        raise DataContractError(
            f"{t.file} has a header but no data rows",
            hint=GENERATE_SEED_HINT,
            details={"table": t.name},
        )
    log.info("table_loaded", schema=RAW_SCHEMA, table=t.name, row=rows)

    return TableLoad(table=t.name, rows=rows)


def load_all(seed_dir: Path, db_path: Path) -> LoadReport:
    """Load every table in one transaction: all tables update, or none do.

    Parameters
    ----------
    seed_dir : Path
        Directory containing the seed CSV files.
    db_path : Path
        DuckDB database file to create or update; parent folders are created.

    Returns
    -------
    LoadReport
        What was loaded, the file's storage version and how long it took.

    Raises
    ------
    InputNotFoundError
        If the seed directory or a seed file is missing.
    DataContractError
        If a file breaks its header, type or row-count contract.
    ResourceBusyError
        If another process holds a lock on `db_path`.

    Notes
    -----
    Every input is validated before the database is opened. On any failure,
    Ctrl-C included (hence ``except BaseException``), the transaction is rolled
    back and the error is re-raised with a bare ``raise``, which keeps its
    original traceback.
    """
    started = time.perf_counter()

    _validate_inputs(seed_dir)
    db_path.parent.mkdir(parents=True, exist_ok=True)

    with _connect(db_path) as con:
        con.begin()  # TODO what is begin()
        try:
            con.execute(f"create schema if not exists {RAW_SCHEMA}")
            loads = [_load_table(con, t, seed_dir / t.file) for t in TABLES]
            storage = con.execute(
                "select tags['storage_version'] from duckdb_databases() "
                "where database_name = current_database()"
            ).fetchone()
            con.commit()
        except BaseException:
            con.rollback()
            raise

    report = LoadReport(
        db_path=db_path,
        storage_version=str(storage[0]) if storage else None,
        tables=tuple(loads),
        duration_s=time.perf_counter() - started,
    )
    log.info(
        "load_committed",
        db=str(db_path),  # log primitives: str, int, float, bool
        tables=len(report.tables),
        rows=sum(t.rows for t in report.tables),
        storage_version=report.storage_version,
        duration_ms=round(report.duration_s * 1000),
    )

    return report


def render_report(report: LoadReport) -> None:
    """Print the user-facing summary table to stdout.

    Parameters
    ----------
    report : LoadReport
        The result of `load_all`.
    """
    table = Table()
    table.add_column(f"{RAW_SCHEMA} table")
    table.add_column("rows", justify="right")
    for t in report.tables:
        table.add_row(t.table, f"{t.rows:,}")
    cli.out.print(table)
    cli.out.print(
        f"[green]✓ Loaded {len(report.tables)} tables into {report.db_path.name}[/] "
        f"[green]in {report.duration_s:.2f}s (storage {report.storage_version})[/]"
    )


def _load_and_report(args: LoaderArgs) -> None:
    """Load the seed files and print the summary; the command `cli.run` executes.

    Parameters
    ----------
    args : LoaderArgs
        The parsed CLI arguments.
    """
    render_report(load_all(args.data_dir.resolve(), args.db.resolve()))


def build_parser() -> argparse.ArgumentParser:
    """Build the command-line parser.

    Returns
    -------
    argparse.ArgumentParser
        The parser with ``--data-dir``, ``--db`` and the shared ``-v``,
        ``--log-file`` and ``--traceback`` flags.
    """
    parser = argparse.ArgumentParser(
        prog=COMMAND, description=__doc__.splitlines()[0] if __doc__ else None
    )

    parser.add_argument(
        "--data-dir",
        type=Path,
        default=DATA_MARKET_DIR,
        help="Directory with the seed CSV files. Default: %(default)s",
    )
    parser.add_argument(
        "--db",
        type=Path,
        default=MARKET_DB,
        help="DuckDB database file to create or update. Default: %(default)s",
    )
    cli.add_observability_args(parser)

    return parser


def main(argv: list[str] | None = None) -> int:
    """Run the loader as a command-line program.

    Parameters
    ----------
    argv : list[str] or None, optional
        Arguments without the program name. Default is None, which reads
        ``sys.argv[1:]``; tests pass a list instead.

    Returns
    -------
    int
        The process exit code (an `learning_journey.errors.ExitCode` value).

    Notes
    -----
    Order matters: parse arguments first (bad flags exit with 2 before anything
    runs), then configure logging, then run the command inside the error
    boundary.
    """
    ns = build_parser().parse_args(argv)
    args = LoaderArgs(
        data_dir=ns.data_dir,
        db=ns.db,
        verbose=ns.verbose,
        log_file=ns.log_file,
        traceback=ns.traceback,
    )

    configure_logging(verbosity=args.verbose, log_file=args.log_file)

    return cli.run(
        functools.partial(_load_and_report, args),
        name=COMMAND,
        log_file=args.log_file,
        show_traceback=args.traceback,
    )


if __name__ == "__main__":
    sys.exit(main())
