"""First pytest suite.

Why tests, and why NOW:
1. Proof — not "it seems to work" but "these cases verifiably pass."
2. A safety net — refactor freely; tests catch what breaks.
3. The habit that becomes your eval-gate discipline: PolicyPulse's RAGAS
   gates are this exact idea aimed at LLM outputs. Same muscle, Week 2.

How pytest works: it finds files named test_*.py, runs functions named
test_*, and `assert <claim>` passes silently or fails loudly.
"""

from __future__ import annotations

import pytest

from learning_journey.retirement import annual_contribution, vested_percent

# ^ imports work because of the src/ layout + pyproject.toml. This line IS
# the payoff of Day-0 structure: your code is a real, importable package.


def test_basic_contribution() -> None:
    # 60k at 10% = 6k — under every limit, simple math must hold.
    assert annual_contribution(60_000, 0.10, age=35) == 6_000.0


def test_limit_caps_high_earner() -> None:
    # 500k at 20% requests 100k → must cap at the base IRS limit (age < 50).
    assert annual_contribution(500_000, 0.20, age=40) == 23_500.0


def test_catch_up_raises_limit() -> None:
    # Same request at age 55 → base + catch-up.
    assert annual_contribution(500_000, 0.20, age=55) == 31_000.0


def test_graded_vesting_year_four() -> None:
    # Domain truth: 6-yr graded, year 4 → 60%.
    # pytest.approx handles float rounding fuzz — exact == on floats bites.
    import pytest

    assert vested_percent(4, "graded") == pytest.approx(0.60)


def test_negative_salary_rejected() -> None:
    # Testing that bad input FAILS CORRECTLY is as important as testing
    # that good input succeeds. pytest.raises asserts "this MUST raise".
    with pytest.raises(ValueError):
        annual_contribution(-50_000, 0.10, age=40)


def test_rate_above_one_rejected() -> None:
    with pytest.raises(ValueError):
        annual_contribution(60_000, 1.5, age=40)  # 150% deferral = nonsense


def test_unknown_schedule_rejected() -> None:
    with pytest.raises(ValueError):
        vested_percent(4, "immediate-maybe")
