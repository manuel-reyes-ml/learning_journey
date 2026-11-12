"""Seeded synthetic market data for practice — invented tickers, invented prices.

Nothing here is vendor data, so a public repo raises no licence question.
Run:  uv run python scripts/gen_market_seed.py --out data/market_seed
"""

from __future__ import annotations

import argparse
import csv
import random
from dataclasses import dataclass
from datetime import date, datetime, time, timedelta
from pathlib import Path
from typing import Final, Literal

from learning_journey.paths import DATA_MARKET_DIR, MARKET_SEEDS_DIR

SEED: Final[int] = 41  # same seed -> same files, every run
TICKERS: Final[list[str]] = ["ALFA", "BRVO", "CHRL", "DLTA", "ECHO"]
N_SESSIONS: Final[int] = 120
FIRST_DAY: Final[date] = date(2026, 1, 5)  # a monday


@dataclass(frozen=True, slots=True, kw_only=True)
class GenArgs:
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

    data_dir: Path
    seeds_dir: Path


def trading_days(first: date, n: int) -> list[date]:
    """Weekdays only. Holidays are ignored: a documented simplification."""
    days, d = [], first
    while len(days) < n:
        if d.weekday() < 5:  # 0=Mon ... 4=Fri
            days.append(d)
        d += timedelta(days=1)
    return days


def make_bars(rng: random.Random, days: list[date]) -> list[dict]:
    rows = []
    for ticker in TICKERS:
        close = rng.uniform(8, 60)
        for i, d in enumerate(days):
            open_ = round(close * (1 + rng.gauss(0, 0.01)), 2)  # overnight gap
            close = round(open_ * (1 + rng.gauss(0, 0.02)), 2)
            high = round(max(open_, close) * (1 + abs(rng.gauss(0, 0.01))), 2)
            low = round(min(open_, close) * (1 - abs(rng.gauss(0, 0.01))), 2)
            volume = int(rng.lognormvariate(13, 0.04))
            if ticker == "DLTA" and 60 <= i < 65:  # PLANTED: a 5-session volume dry-up
                volume = int(volume * 0.3)
            rows.append(
                {
                    "ticker": ticker,
                    "session_date": d.isoformat(),
                    "open": open_,
                    "high": high,
                    "low": low,
                    "close": close,
                    "volume": volume,
                }
            )
    return rows


def make_events(rng: random.Random, days: list[date]) -> tuple[list[dict], dict]:
    """Form 4 purchases (code P). Two clocks per filing: filing_date and accepted_at."""
    events: list[dict] = []

    def add(
        event_id: str,
        ticker: str,
        txn_code: Literal["P"],
        d: date,
        t: time,
        boundary_case: str = "",
    ) -> None:
        # Forms 3/4/5 accepted up to 10 p.m. ET keep that day's filing date;
        # most other EDGAR forms accepted after 5:30 p.m. get the NEXT business day.
        events.append(
            {
                "event_id": event_id,
                "ticker": ticker,
                "txn_code": txn_code,
                "filing_date": d.isoformat(),
                "accepted_at": datetime.combine(d, t),
                "boundary_case": boundary_case,
            }
        )

    for n in range(30):  # random time from 6 a.m. to 9:59 p.m.
        d = rng.choice(days[20:-3])
        t = time(rng.randint(6, 21), rng.randint(0, 59), rng.randint(0, 59))
        add(f"EVT-{n:03d}", rng.choice(TICKERS), "P", d, t)

    # PLANTED boundary cases: each must trade on the NEXT session, never the same day
    add("EVT-B1", "ALFA", "P", days[40], time(18, 0, 0), "after_close_1800")
    add("EVT-B2", "CHRL", "P", days[50], time(9, 30, 0), "at_open_0930")
    # PLANTED: accepted after the LAST session's open -> no later session exists
    add("EVT-U1", "BRVO", "P", days[-1], time(16, 30, 0))
    add("EVT-U2", "ECHO", "P", days[-1], time(19, 5, 0))

    manifest = {"seed": SEED, "n_events": len(events), "expected_unmatched": 2}

    return events, manifest


def write_csv(path: Path, rows: list[dict]) -> Path:
    path.resolve().parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

    return path


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--data-dir",
        type=Path,
        default=DATA_MARKET_DIR,
        help=f"Directory to save market data CSV files. Default: {DATA_MARKET_DIR}",
    )
    parser.add_argument(
        "--seeds-dir",
        type=Path,
        default=MARKET_SEEDS_DIR,
        help=f"Directory to save seed data CSV files. Default: {MARKET_SEEDS_DIR}",
    )

    raw_args = parser.parse_args(argv)
    args = GenArgs(data_dir=raw_args.data_dir, seeds_dir=raw_args.seeds_dir)

    rng = random.Random(SEED)  # never the global random: reproducibility
    days = trading_days(FIRST_DAY, N_SESSIONS)

    f_path = write_csv(args.data_dir / "bars_daily.csv", make_bars(rng, days))
    print(f"bars_daily.csv created succesfully. Find it in: {f_path}")

    # events, [manifest] -> On the left side of =, square brackets don't build a list. They're
    # unpacking syntax, and Python reads them as “take the second returned value, iterate it,
    # and expect exactly one item inside. On the right they mean “build a list.”
    # Iterating a dict gives you its keys. If your manifest has more than one key, you get:
    #   In this case -> ValueError: too many values to unpack (expected 1, got 3)
    events, manifest = make_events(rng, days)

    f_path = write_csv(args.data_dir / "insider_events.csv", events)
    print(f"insider_events.csv created succesfully. Find it in: {f_path}")

    f_path = write_csv(args.seeds_dir / "gen_manifest.csv", [manifest])
    print(f"gen_manifest.csv created succesfully. Find it in: {f_path}")


if __name__ == "__main__":
    main()
