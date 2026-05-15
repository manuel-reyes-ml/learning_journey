from __future__ import annotations

import asyncio
import time

START = time.perf_counter()

def t() -> str:
    """Format elapsed time since program start, in ms."""
    return f"{(time.perf_counter() - START) * 1000:6.1f}ms"

async def fetch(name: str, duration: float) -> str:
    print(f"{t()}  {name}  ▶ body starts")
    print(f"{t()}  {name}  ⏸ about to await sleep({duration}s) — will yield")
    await asyncio.sleep(duration)
    print(f"{t()}  {name}  ▶ resumed after {duration}s I/O")
    return f"result-{name}"

async def main() -> None:
    print(f"{t()}  main: calling gather with three coroutines")
    results = await asyncio.gather(
        fetch("A", 0.3),
        fetch("B", 0.1),
        fetch("C", 0.2),
    )
    print(f"{t()} main: gather returned {results}")

asyncio.run(main())