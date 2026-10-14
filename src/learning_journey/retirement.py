"""Retirement-plan calculation functions.

Week 1 logic, promoted from scripts into a reusable, testable module.
This triple-quoted string is a DOCSTRING — documentation that lives in the
code. Every module and function gets one. `help(retirement)` will print it.
"""

from __future__ import annotations

# --- Constants live at module level, named once ---

IRS_DEFERRAL_LIMIT = 23_500  # TODO: verify current-year limit
CATCH_UP_LIMIT = 7_500  # TODO: verify
CATCH_UP_AGE = 50


def annual_contribution(salary: float, deferral_rate: float, age: int) -> float:
    """Return the capped annual deferral for a participant.

    Anatomy of this line (new concepts):
      def              = define a function
      salary: float    = parameter with a TYPE HINT — documents what kind
                         of value belongs here. Python doesn't enforce hints,
                         but tools (mypy, Pylance) and humans rely on them.
                         Production habit: every signature is hinted. Always.
      -> float         = this function RETURNS a float.

    Args:
        salary: Annual gross salary in dollars. Must be positive.
        deferral_rate: Elected deferral as a decimal (0.06 = 6%).
        age: Participant age (drives catch-up eligibility).

    Raises:
        ValueError: If salary or rate is invalid. Bad input should fail
            LOUDLY at the boundary, not produce a quiet wrong number.
    """
    if salary <= 0:
        raise ValueError(f"Salary must be positive, got {salary}")
    if not 0 <= deferral_rate <= 1:
        raise ValueError(f"deferral_rate must be 0-1, got {deferral_rate}")

    limit = IRS_DEFERRAL_LIMIT
    if age >= CATCH_UP_AGE:
        limit += CATCH_UP_LIMIT  # += means limit = limit + CATCH_UP_LIMIT

    return min(salary * deferral_rate, limit)
    # `return` hands the result back to whoever called the function.
    # No print() in here! Functions COMPUTE; callers decide what to show.
    # (Roadmap trajectory note: the production standard's named answer to
    # "then how does a running system talk?" is STRUCTURED LOGGING via
    # structlog — Correction 16. You'll take a first taste of it in Week 4;
    # for now, the habit is simply: no print() inside functions.)


def vested_percent(years_of_service: int, schedule: str = "graded") -> float:
    """Return vested fraction (0.0-1.0) under a cliff or graded schedule.

    `schedule: str = "graded"` gives the parameter a DEFAULT — callers can
    omit it. Day 3's if/elif logic now lives here, reusable forever.
    """
    if schedule == "cliff":
        return 1.0 if years_of_service >= 3 else 0.0
        # ^ conditional expression: "A if condition else B" — one-line if/else

    if schedule == "graded":
        if years_of_service >= 6:
            return 1.0
        if years_of_service >= 2:
            return 0.20 * (years_of_service - 1)
        return 0.0

    raise ValueError(f"unknown schedule: {schedule!r}")


def project_balance(
    starting_balance: float,
    annual_contribution_amt: float,
    annual_return: float,
    years: int,
) -> list[float]:
    """Project year-end balances for `years` years.

    Returns a LIST — Python's ordered collection type: [year1, year2, ...].
    list[float] in the hint reads "a list of floats."
    Model (deliberately simple): contribute at year start, then grow.
    """
    balances: list[float] = []  # start empty
    balance = starting_balance

    for _ in range(1, years + 1):
        # range(1, years+1) counts 1,2,...,years — the end is EXCLUSIVE,
        # which surprises everyone once. Now it's surprised you; done.
        balance = (balance + annual_contribution_amt) * (1 + annual_return)
        balances.append(balance)  # .append() adds to the end of a list

    return balances


# --- The main guard: makes the file BOTH importable and runnable ---
if __name__ == "__main__":
    # This block runs ONLY when you execute the file directly
    # (uv run python src/learning_journey/retirement.py) — NOT when another
    # file imports it. Standard Python structure; you'll type it forever.
    print("Demo:")
    print(f"     $120K @ 25%, age 52 → ${annual_contribution(120_000, 0.25, 52):,.2f}")
    print(f"     4 yrs graded → {vested_percent(4):.0%} vested")

    projection = project_balance(50_000, 12_000, 0.07, 10)
    # enumerate() gives you position AND value while looping:
    for year_num, bal in enumerate(projection, start=1):
        print(f"  Year {year_num:>2}: ${bal:,.2f}")  # :>2 right-aligns
