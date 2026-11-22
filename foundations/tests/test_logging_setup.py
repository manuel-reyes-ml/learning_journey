"""Test `configure_logging` and JSON mode: handlers, LOG_FORMAT, quiet Rich, config errors."""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Final

import pytest
import structlog

import learning_journey.scripts.load_market_seed as loader
from learning_journey.errors import ConfigError, ExitCode
from learning_journey.logging_setup import LOG_FORMAT_ENV, configure_logging

BARS_HEADER: Final[str] = "ticker,session_date,open,high,low,close,volume"


def _write_seed(tmp_path: Path, *, bars_header: str = BARS_HEADER) -> Path:
    """Write a small valid seed directory, optionally with a drifted bars header.

    Parameters
    ----------
    tmp_path : Path
        Per-test temporary directory provided by pytest.
    bars_header : str, optional
        Header line for ``bars_daily.csv``. Default is the contract header.

    Returns
    -------
    Path
        The ``market`` directory holding both seed files.
    """
    seed = tmp_path / "market"
    seed.mkdir()
    (seed / "bars_daily.csv").write_text(
        f"{bars_header}\nACME,2026-01-05,1,1,1,1,1\n", encoding="utf-8"
    )
    (seed / "insider_events.csv").write_text(
        "event_id,ticker,txn_code,filing_date,accepted_at,boundary_case\n"
        "E1,ACME,P,2026-01-06,2026-01-06 16:05:00,x\n",
        encoding="utf-8",
    )
    return seed


def _run(seed: Path, tmp_path: Path) -> int:
    """Run the loader's ``main`` against a temporary database.

    Parameters
    ----------
    seed : Path
        Directory passed as ``--data-dir``.
    tmp_path : Path
        Directory that holds the ``m.duckdb`` database passed as ``--db``.

    Returns
    -------
    int
        The exit code ``main`` returned.
    """
    return loader.main(["--data-dir", str(seed), "--db", str(tmp_path / "m.duckdb")])


def _console_rendered_of_root() -> object:
    """Return the last processor of the root console handler's formatter.

    Returns
    -------
    object
        The final renderer: a ``ConsoleRenderer`` or a ``JSONRenderer``.
    """
    formatter = logging.getLogger().handlers[0].formatter
    assert isinstance(formatter, structlog.stdlib.ProcessorFormatter)
    return formatter.processors[-1]


def test_configure_logging_attaches_handlers(tmp_path: Path) -> None:
    """Check that the root logger gets its console and file handlers.

    Guards against silent ``dictConfig`` typos such as ``"handler"``.

    Parameters
    ----------
    tmp_path : Path
        Per-test temporary directory provided by pytest.
    """
    configure_logging(verbosity=1, log_file=tmp_path / "x.jsonl")
    assert len(logging.getLogger().handlers) == 2


def test_json_format_writes_our_events_to_stderr_as_json_lines(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """Check ``LOG_FORMAT=json``: stdout is silent and every stderr line is JSON.

    The Rich summary table must not be printed, and our own INFO events
    (including ``load_committed``, which replaces the table) must be present
    even without ``-v``.

    Parameters
    ----------
    tmp_path : Path
        Per-test temporary directory provided by pytest.
    monkeypatch : pytest.MonkeyPatch
        Built-in pytest fixture, used to set ``LOG_FORMAT``.
    capsys : pytest.CaptureFixture[str]
        Built-in pytest fixture that captures stdout and stderr.
    """
    monkeypatch.setenv(LOG_FORMAT_ENV, "json")

    code = _run(_write_seed(tmp_path), tmp_path)

    captured = capsys.readouterr()
    assert code == ExitCode.SUCCESS
    assert captured.out == ""  # Rich summary table silenced
    events = [json.loads(line) for line in captured.err.splitlines()]  # every line parses
    names = {e["event"] for e in events}
    assert {"table_loaded", "load_committed", "command_succeeded"} <= names  # no -v needed
    assert all(e["level"] != "debug" for e in events)  # starts at INFO, not DEBUG


def test_json_mode_failure_keeps_stderr_pure_json(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """Check that Rich's ``error:`` / ``hint:`` lines are silenced in JSON mode.

    The JSON ``command_failed`` event must carry the error code and the hint
    instead, so nothing is lost for the log collector.

    Parameters
    ----------
    tmp_path : Path
        Per-test temporary directory provided by pytest.
    monkeypatch : pytest.MonkeyPatch
        Built-in pytest fixture, used to set ``LOG_FORMAT``.
    capsys : pytest.CaptureFixture[str]
        Built-in pytest fixture that captures stdout and stderr.
    """
    monkeypatch.setenv(LOG_FORMAT_ENV, "json")
    seed = _write_seed(tmp_path, bars_header=BARS_HEADER.replace("session_date", "date"))

    code = _run(seed, tmp_path)

    captured = capsys.readouterr()
    assert code == ExitCode.DATA_ERROR
    events = [json.loads(line) for line in captured.err.splitlines()]  # no plain-text lines
    failed = [e for e in events if e["event"] == "command_failed"]
    assert failed[0]["error_code"] == "data-contract-violation"
    assert failed[0]["hint"]


def test_console_run_after_json_run_prints_summary(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """Check that JSON mode's silenced stdout does not leak into the next run.

    Parameters
    ----------
    tmp_path : Path
        Per-test temporary directory provided by pytest.
    monkeypatch : pytest.MonkeyPatch
        Built-in pytest fixture, used to set and remove ``LOG_FORMAT``.
    capsys : pytest.CaptureFixture[str]
        Built-in pytest fixture that captures stdout and stderr.
    """
    seed = _write_seed(tmp_path)
    monkeypatch.setenv(LOG_FORMAT_ENV, "json")
    _run(seed, tmp_path)
    assert capsys.readouterr().out == ""  # silenced in JSON mode

    monkeypatch.delenv(LOG_FORMAT_ENV)
    _run(seed, tmp_path)

    assert "bars_daily" in capsys.readouterr().out  # summary from Rich is back to stdout


def test_console_run_after_json_run_is_not_silenced(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """Check that JSON mode's silenced stderr does not leak into the next run.

    Parameters
    ----------
    tmp_path : Path
        Per-test temporary directory provided by pytest.
    monkeypatch : pytest.MonkeyPatch
        Built-in pytest fixture, used to set and remove ``LOG_FORMAT``.
    capsys : pytest.CaptureFixture[str]
        Built-in pytest fixture that captures stdout and stderr.
    """
    seed = _write_seed(tmp_path, bars_header=BARS_HEADER.replace("session_date", "date"))
    monkeypatch.setenv(LOG_FORMAT_ENV, "json")
    _run(seed, tmp_path)
    capsys.readouterr()  # discard the JSON run's output

    monkeypatch.delenv(LOG_FORMAT_ENV)
    _run(seed, tmp_path)

    assert "error[data-contract-violation]" in capsys.readouterr().err


def test_explicit_log_format_overrides_environment(monkeypatch: pytest.MonkeyPatch) -> None:
    """Check that the ``log_format`` argument wins over ``LOG_FORMAT``.

    Parameters
    ----------
    monkeypatch : pytest.MonkeyPatch
        Built-in pytest fixture, used to set ``LOG_FORMAT``.
    """
    monkeypatch.setenv(LOG_FORMAT_ENV, " json ")
    configure_logging(log_format="console")
    assert isinstance(_console_rendered_of_root(), structlog.dev.ConsoleRenderer)


@pytest.mark.parametrize(
    "value",
    [
        pytest.param("JSON", id="JSON-all-caps"),
        pytest.param("json", id="json-lower-case"),
    ],
)
def test_log_format_ignores_case_and_spaces(monkeypatch: pytest.MonkeyPatch, value: str) -> None:
    """Check that ``LOG_FORMAT`` values are normalized before validation.

    Parameters
    ----------
    monkeypatch : pytest.MonkeyPatch
        Built-in pytest fixture, used to set ``LOG_FORMAT``.
    value : str
        A spelling of ``json`` with different case or spacing.
    """
    monkeypatch.setenv(LOG_FORMAT_ENV, value)
    assert configure_logging() == "json"
    assert isinstance(_console_rendered_of_root(), structlog.processors.JSONRenderer)


def test_unknown_log_format_raises_config_error(monkeypatch: pytest.MonkeyPatch) -> None:
    """Check that a typo in ``LOG_FORMAT`` raises `ConfigError` with a hint.

    Parameters
    ----------
    monkeypatch : pytest.MonkeyPatch
        Built-in pytest fixture, used to set ``LOG_FORMAT``.
    """
    monkeypatch.setenv(LOG_FORMAT_ENV, "jsn")
    with pytest.raises(ConfigError) as caught:
        configure_logging()
    assert caught.value.exit_code == ExitCode.CONFIG
    assert caught.value.hint


def test_unkwnown_log_format_is_shown_by_rich_and_exits_78(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """Check the CLI path: a bad ``LOG_FORMAT`` prints ``error:`` + ``hint:``, no traceback.

    Parameters
    ----------
    tmp_path : Path
        Per-test temporary directory provided by pytest.
    monkeypatch : pytest.MonkeyPatch
        Built-in pytest fixture, used to set ``LOG_FORMAT``.
    capsys : pytest.CaptureFixture[str]
        Built-in pytest fixture that captures stdout and stderr.
    """
    monkeypatch.setenv(LOG_FORMAT_ENV, "jsn")

    code = _run(_write_seed(tmp_path), tmp_path)

    captured = capsys.readouterr()
    assert code == ExitCode.CONFIG
    assert captured.out == ""  # nothing ran, and nothing was logged to stdout
    assert "error[invalid-config]" in captured.err
    assert "hint:" in captured.err
    assert "Traceback" not in captured.err
