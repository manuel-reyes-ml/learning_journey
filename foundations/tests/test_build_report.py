from __future__ import annotations

import csv

import pytest

from learning_journey.projects.contribution_report import (
    DATA_FILE,
    ReportRow,
    build_report,
    compute_rows,
    format_row,
    load_participants,
)


def participant(**overrides: str) -> dict[str, str]:
    """A valid CSV row as DictReader returns it (all strings); override one field per test."""
    row = {
        "name": "Ana Torres",
        "age": "34",
        "salary": "62000",
        "deferral_pct": "0.06",
        "years_service": "3",
    }
    return row | overrides


def _read() -> list[dict[str, str]]:
    with DATA_FILE.open(encoding="utf-8") as f:
        return list(csv.DictReader(f))


def test_csv_loads_correctly() -> None:
    "load_participants() returns complete file."
    assert _read() == load_participants(DATA_FILE)


def test_row_count_matches_input() -> None:
    "Python build_report() lines must match CSV file rows."
    lines = build_report(_read())
    assert len(lines) == len(_read())


# --- 1. The computation: assert on numbers, never on text -----------------


# --- HOW @pytest.mark.parametrize WORKS ---
#
# Instead of writing 5 separate test functions that do the same
# thing with different inputs, parametrize runs the SAME test
# function once per case. Each case is reported as its own test.
#
# Format:
#   @pytest.mark.parametrize(
#       ("name_1", "name_2"),       # argnames: a tuple of strings
#       [case_1, case_2, ...],      # argvalues: one entry per case
#   )
#   def test_something(name_1, name_2):     # (inside a class: self first)
#
# - argnames can also be one comma-separated string: "name_1, name_2".
#   Both work; the tuple is explicit, and ruff's PT006 rule expects it.
# - Every name in argnames must match a parameter of the test function.
# - Each case's values are unpacked IN ORDER into those names:
#   the 1st value goes to name_1, the 2nd to name_2, and so on.
# - A case can be a plain tuple (1, 2) or a pytest.param(1, 2, ...).
#   The two styles can be mixed in the same list.
#
# The text inside [brackets] is the test ID. Without an id, pytest
# builds one from the values:           test_eval[3+5-8]
# Show every ID:      uv run pytest --collect-only -q
# Run cases by ID:    uv run pytest -k "catch-up or capped"
#
# --- HOW pytest.param() WORKS ---
#
# pytest.param() wraps ONE case together with its name and marks
# (part of pytest since version 3.1):
#
#   pytest.param(*values, id="readable-name", marks=...)
#
# It returns a small container (a ParameterSet) with three fields:
#   pytest.param({}, 3720.0, 0.40, id="under-limit")
#   -> ParameterSet(values=({}, 3720.0, 0.4), marks=(), id='under-limit')
#
# - values: the case's arguments, in argnames order (same as a tuple)
# - id:     the name shown in [brackets]  -> test_compute_rows[under-limit]
# - marks:  a mark for THIS case only, e.g. a known bug:
#     pytest.param("6*9", 42, id="known-wrong",
#                  marks=pytest.mark.xfail(reason="bug #12", strict=True))
#   strict=True makes the run FAIL if that case unexpectedly passes,
#   so a fixed bug can't hide behind the mark.
#
# --- WHY pytest.param(id=...) INSTEAD OF A SEPARATE ids=[...] LIST ---
#
# A separate ids list matches names to cases by POSITION. Insert a case
# in the middle, add its id at the end, and every name after it shifts
# by one, so a failure report names the WRONG case. pytest catches a
# length mismatch ("3 parameter sets ... different number of ids: 2"),
# but not a shifted order. With pytest.param the name sits on the same
# line as its data, so it can't drift. If a case gets both, the
# pytest.param id wins.
@pytest.mark.parametrize(
    ("overrides", "expected_contribution", "expected_vested"),
    [
        pytest.param({}, 3_720.0, 0.40, id="under-limit-graded-yr3"),
        pytest.param(
            {"salary": "500000", "deferral_pct": "0.20", "age": "40"},
            23_500.0,
            0.40,
            id="capped-at-base-limit",
        ),
        pytest.param(
            {"salary": "500000", "deferral_pct": "0.20", "age": "50"},
            31_000.0,
            0.40,
            id="catch-up-starts-at-50",
        ),
        pytest.param({"years_service": "1"}, 3_720.0, 0.0, id="graded-yr1-zero"),
        pytest.param({"years_service": "6"}, 3_720.0, 1.0, id="graded-yr6-full"),
    ],
)
def test_compute_rows(
    overrides: dict,
    expected_contribution: float,
    expected_vested: float,
) -> None:
    [row] = compute_rows([participant(**overrides)])
    assert row.contribution == pytest.approx(expected_contribution)
    assert row.vested == pytest.approx(expected_vested)


def test_one_row_per_participant_in_input_order() -> None:
    rows = compute_rows([participant(name="A"), participant(name="B"), participant(name="C")])
    assert [r.name for r in rows] == ["A", "B", "C"]


def test_empty_input_gives_empty_report() -> None:
    assert build_report([]) == []


@pytest.mark.parametrize(
    ("overrides", "error"),
    [
        pytest.param({"salary": "abc"}, ValueError, id="non-numeri-salary"),
        pytest.param({"salary": "-5"}, ValueError, id="negative-salary"),
        pytest.param({"age": "34.5"}, ValueError, id="age-not-an-integer"),
    ],
)
def test_bad_input_fails_loudly(overrides, error) -> None:
    with pytest.raises(error):
        compute_rows([participant(**overrides)])


def test_missing_column_fails_loudly() -> None:
    row = participant()
    del row["salary"]
    with pytest.raises(KeyError, match="salary"):
        compute_rows([row])


# --- 2. The layout: a few exact strings are the contract ------------------


def test_format_row_exact_layout() -> None:
    assert format_row(ReportRow("Ana Torres", 3_720.0, 0.40)) == (
        "Ana Torres   contributes $3,720.00  |  40% vested"
    )


def test_format_row_columns_align() -> None:
    a = format_row(ReportRow("Ana Torres", 3_720.0, 0.40))
    b = format_row(ReportRow("Luis Vega", 23_500.0, 1.0))
    assert a.index("$") == b.index("$")
    assert a.index("|") == b.index("|")


# --- 3. End to end: compute + format together, on a known input -----------


def test_build_report_end_to_end() -> None:
    participants = [
        participant(),
        participant(
            name="Luis Vega", age="51", salary="98000", deferral_pct="0.15", years_service="7"
        ),
    ]
    assert build_report(participants) == [
        "Ana Torres   contributes $3,720.00  |  40% vested",
        "Luis Vega    contributes $14,700.00 | 100% vested",
    ]
