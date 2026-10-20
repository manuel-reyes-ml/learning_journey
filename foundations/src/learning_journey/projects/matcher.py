"""Dict-based record matcher — the Python counterpart to the recon SQL.

Why build BOTH? (1) Each is the right tool in different situations —
SQL where data lives in a DB; Python where logic gets complex (fuzzy
matching, tolerances, multi-step rules). (2) Comparing their outputs
tests both: two independent implementations that agree are strong
evidence both are right. That's a verification technique you'll reuse
on real financial pipelines — and it becomes ADR 0001 on Friday.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class MatchResult:
    """A small typed container for the three outcome buckets.

    @dataclass auto-writes the boilerplate (__init__ etc.) for a class
    that just holds data. First touch of classes — gentle on purpose;
    OOP proper arrives with CS50P.
    """

    matched: list[dict] = field(default_factory=list)
    missing_in_b: list[dict] = field(default_factory=list)
    amount_mismatch: list[dict] = field(default_factory=list)


def match_records(
    participants: list[dict],
    distributions: list[dict],
    *,
    amount_tolerance: float,
) -> MatchResult:
    """Bucket every participant: matched / missing-in-B / amount-mismatch.

    `amount_tolerance` (default 1 cent) exists because floats and rounding
    make exact equality on money fragile — a tolerance is honest about
    that. In real reconciliation, tolerance thresholds are POLICY (a
    business decision, documented), not convenience. Note it as a
    consequence in Friday's ADR.
    """
    result = MatchResult()

    # Index B by participant_id — one pass, then instant lookups:
    dist_by_id: dict[str, dict] = {d["participant_id"]: d for d in distributions}

    for p in participants:
        pid = p["participant_id"]
        if pid not in dist_by_id:  # `in` on a dict checks KEYS, fast
            result.missing_in_b.append(p)
            continue

        dist = dist_by_id[pid]
        expected = round(float(p["salary"]) * float(p["deferral_pct"]), 2)
        actual = float(dist["gross"])

        if abs(actual - expected) <= amount_tolerance:
            # abs() = distance regardless of sign — the tolerance test.
            result.matched.append(p)
        else:
            result.amount_mismatch.append(
                {
                    "participant_id": pid,
                    "expected": expected,
                    "actual": actual,
                    "difference": round(actual - expected, 2),
                }
            )

    return result


if __name__ == "__main__":
    import csv
    from pathlib import Path

    DATA_DIR: Path = Path(__file__).resolve().parent / "data"
    participants: list[dict] = []
    distributions: list[dict] = []

    for table, path in {
        "participants": "system_a_participants.csv",
        "distributions": "system_b_distributions.csv",
    }.items():
        with (DATA_DIR / path).open(encoding="utf-8") as f:
            data = list(csv.DictReader(f))

        match table:
            case "participants":
                participants = data
            case "distributions":
                distributions = data

    result = match_records(participants, distributions, amount_tolerance=0.01)
    print(result)
