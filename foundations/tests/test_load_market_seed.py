"""Test the market seed loader: exit codes, user messages and the log record.

Notes
-----
If the loader lives in ``foundations/scripts/``, which is not a package. One line in
``pyproject.toml`` makes it importable, with no ``sys.path`` hacks::

    [tool.pytest.ini_options]
    pythonpath = ["foundations/scripts"]
"""

import json
from pathlib import Path
from typing import Final

import duckdb
import pytest

import learning_journey.scripts.load_market_seed as loader
from learning_journey.errors import ExitCode
from learning_journey.logging_setup import REDACTED, redact_sensitive

BARS: Final[str] = (
    "ticker,session_date,open,high,low,close,volume\n"
    "ACME,2026-01-05,10.0,10.5,9.8,10.2,120000\n"
    "ACME,2026-01-06,10.2,10.9,10.1,10.8,98000\n"
)
EVENTS: Final[str] = (
    "event_id,ticker,txn_code,filing_date,accepted_at,boundary_case\n"
    "E1,ACME,P,2026-01-06,2026-01-06 16:05:00,after_close\n"
)


@pytest.fixture
def seed_dir(tmp_path: Path) -> Path:
    """Create a valid seed directory with both CSV files.

    Parameters
    ----------
    tmp_path : Path
        Per-test temporary directory provided by pytest.

    Returns
    -------
    Path
        The ``market`` directory holding ``bars_daily.csv`` and ``insider_events.csv``.
    """
    d = tmp_path / "market"
    d.mkdir()
    (d / "bars_daily.csv").write_text(BARS, encoding="utf-8")
    (d / "insider_events.csv").write_text(EVENTS, encoding="utf-8")

    return d


def run(seed_dir: Path, tmp_path: Path, *extra: str) -> int:
    """Run the loader's ``main`` against a temporary database.

    Parameters
    ----------
    seed_dir : Path
        Directory passed as ``--data-dir``.
    tmp_path : Path
        Directory that holds the ``m.duckdb`` database passed as ``--db``.
    *extra : str
        Additional command-line arguments, e.g. ``"--log-file", "x.jsonl"``.

    Returns
    -------
    int
        The exit code ``main`` returned.
    """
    return loader.main(["--data-dir", str(seed_dir), "--db", str(tmp_path / "m.duckdb"), *extra])


def read_jsonl(path: Path) -> list[dict[str, object]]:
    """Parse a JSON Lines log file.

    Parameters
    ----------
    path : Path
        The log file written with ``--log-file``.

    Returns
    -------
    list[dict[str, object]]
        One dict per log event, in file order.
    """
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]


class TestHappyPath:
    """ """

    def test_happy_path_loads_tables_and_prints_summary_on_stdout(
        self, seed_dir: Path, tmp_path: Path, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """Check a clean run: exit 0, summary on stdout, silent stderr, rows in DuckDB.

        Parameters
        ----------
        seed_dir : Path
            Fixture with valid seed files.
        tmp_path : Path
            Per-test temporary directory provided by pytest.
        capsys : pytest.CaptureFixture[str]
            Built-in pytest fixture that captures stdout and stderr.
        """
        assert run(seed_dir, tmp_path) == ExitCode.SUCCESS

        captured = capsys.readouterr()
        assert "bars_daily" in captured.out
        assert captured.err == ""  # nothing to report, so stderr stays silent

        with duckdb.connect(str(tmp_path / "m.duckdb"), read_only=True) as con:
            row = con.execute("select count(*)  from raw_market.bars_daily").fetchone()
        assert row == (2,)


class TestNoInput:
    """ """

    def test_missing_file_exits_no_input_with_hint_on_stderr(
        self, seed_dir: Path, tmp_path: Path, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """Check a missing seed file: exit 66, error and hint on stderr, no traceback.

        Parameters
        ----------
        seed_dir : Path
            Fixture with valid seed files; one is deleted by the test.
        tmp_path : Path
            Per-test temporary directory provided by pytest.
        capsys : pytest.CaptureFixture[str]
            Built-in pytest fixture that captures stdout and stderr.
        """
        (seed_dir / "insider_events.csv").unlink()  # TODO: removes it from local disk?

        assert run(seed_dir, tmp_path) == ExitCode.NO_INPUT

        captured = capsys.readouterr()
        assert captured.out == ""  # errors never pollute stdout
        assert "error[input-not-found]" in captured.err
        assert "hint:" in captured.err
        assert "Traceback" not in captured.err  # expected errors get no traceback


class TestDataError:
    """ """

    def test_header_drift_is_logged_as_structured_fields(
        self, seed_dir: Path, tmp_path: Path, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """Check header drift: exit 65 and one structured ``command_failed`` log event.

        The event must carry the error code, the expected and found headers, and the
        same ``run_id`` the user sees on stderr, and no traceback.

        Parameters
        ----------
        seed_dir : Path
            Fixture with valid seed files; one header is changed by the test.
        tmp_path : Path
            Per-test temporary directory provided by pytest.
        capsys : pytest.CaptureFixture[str]
            Built-in pytest fixture that captures stdout and stderr.
        """
        (seed_dir / "bars_daily.csv").write_text(
            BARS.replace("session_date", "date"), encoding="utf-8"
        )
        log_file = tmp_path / "logs" / "load.jsonl"  # TODO what is jsonl format?

        assert run(seed_dir, tmp_path, "--log-file", str(log_file)) == ExitCode.DATA_ERROR

        failed = [e for e in read_jsonl(log_file) if e["event"] == "command_failed"]
        assert len(failed) == 1

        event = failed[0]
        assert event["error_code"] == "data-contract-violation"
        assert event["exit_code"] == ExitCode.DATA_ERROR
        assert "date" in str(event["found"])
        assert str(event["run_id"]) in capsys.readouterr().err  # terminal <-> log file correlation
        assert "exception" not in event  # expected error: fields, not a traceback

    def test_bad_value_maps_duckdb_error_to_data_error(
        self, seed_dir: Path, tmp_path: Path
    ) -> None:
        """Check that a value DuckDB cannot convert exits with 65, not as a crash.

        Parameters
        ----------
        seed_dir : Path
            Fixture with valid seed files; one value is corrupted by the test.
        tmp_path : Path
            Per-test temporary directory provided by pytest.
        """
        (seed_dir / "bars_daily.csv").write_text(BARS.replace("120000", "lots"), encoding="utf-8")

        assert run(seed_dir, tmp_path) == ExitCode.DATA_ERROR


class TestTracebackNoLocals:
    """ """

    def test_unexpected_error_logs_traceback_without_locals(
        self, seed_dir: Path, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Check a crash: exit 1, structured traceback in the log, no local values.

        Parameters
        ----------
        seed_dir : Path
            Fixture with valid seed files.
        tmp_path : Path
            Per-test temporary directory provided by pytest.
        monkeypatch : pytest.MonkeyPatch
            Built-in pytest fixture, used to replace ``load_all`` with a function that fails.
        """

        def boom(_seed_dir: Path, _db_path: Path) -> None:
            """Fail like a bug would, holding a sensitive local variable.

            Parameters
            ----------
            _seed_dir : Path
                Unused.
            _db_path : Path
                Unused.

            Raises
            ------
            RuntimeError
                Always.
            """
            participant_ssn = "123-45-6789"  # a local that must never reach the log

            raise RuntimeError(f"bug near {len(participant_ssn)} chars")

        monkeypatch.setattr(loader, "load_all", boom)
        log_file = tmp_path / "load.jsonl"

        assert run(seed_dir, tmp_path, "--log-file", str(log_file)) == ExitCode.FAILURE

        text = log_file.read_text(encoding="utf-8")
        crashed = [e for e in read_jsonl(log_file) if e["event"] == "command_crashed"]
        assert crashed
        assert crashed[0]["exception"]  # full structured traceback recorded
        assert "123-45-6789" not in text  # show_locals=False held

    def test_redaction_masks_sensitive_keys_case_insensitive(self) -> None:
        """Check that the redaction processor masks ``SSN`` and leaves other keys alone."""
        event = redact_sensitive(None, "info", {"event": "x", "SSN": "123-45-6789", "rows": 3})
        assert event == {"event": "x", "SSN": REDACTED, "rows": 3}
