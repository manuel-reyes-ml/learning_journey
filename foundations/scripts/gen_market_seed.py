"""Seeded synthetic market data for practice — invented tickers, invented prices.

Nothing here is vendor data, so a public repo raises no licence question.
Run:  uv run python scripts/gen_market_seed.py --out data/market_seed
"""

from __future__ import annotations

import argparse
import csv
import random
from datetime import date, timedelta
from pathlib import Path
from typing import Final

SEED: Final[int] = 41  # same seed -> same files, every run
TICKERS: Final[list[str]] = ["ALFA", "BRVO", "CHRL", "DLTA", "ECHO"]
N_SESSIONS: Final[int] = 120
FIRST_DAY: Final[date] = date(2026, 1, 5)  # a monday
PROJECT_ROOT: Final[Path] = Path(__file__).resolve().parents[1]  # foundations/


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


def write_csv(path: Path, rows: list[dict]) -> Path:
    path.resolve().parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

    return path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, default=(PROJECT_ROOT / "data" / "market_seed"))
    args = parser.parse_args()

    rng = random.Random(SEED)  # never the global random: reproducibility
    days = trading_days(FIRST_DAY, N_SESSIONS)
    file_path = write_csv(args.out / "bars_daily.csv", make_bars(rng, days))

    print(f"File created succesfully. Find it in: {file_path}")


if __name__ == "__main__":
    main()
