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

# Phase 1: gather schedules all three coroutines as Tasks on the event loop.
# The loop picks the first one (A), runs it. A runs synchronously until it hits
# await asyncio.sleep(0.3). At that moment A parks itself — registers a 300ms
# timer with the event loop, then yields control. The loop picks B, same dance.
# Then C. By 0.5ms, all three coroutines are parked, each registered for a different timer.

# Phase 2: the wait. The event loop has nothing ready to run. It calls into the OS
# (epoll on Linux, kqueue on Mac) and effectively says "wake me when any of these
# three timers fires." The OS handles the actual waiting at the kernel level.
# Your Python process is using ~0% CPU.

# Phase 3:  the resumes, in completion order. B's timer fires first because it had
# the shortest sleep. The loop wakes, sees B is ready, resumes B from exactly where
# it parked — the line after await. B runs to completion. Same for C at 200ms,
# then A at 300ms.

# Phase 4: gather collects results. Once all three Tasks finish, gather returns.
# Crucially, in input order, not completion order.

# Three coroutines wait in parallel, on one thread. The total wall time is ~300ms
# (the longest single wait) instead of 100+200+300 = 600ms sequential.

# What await actually does — the one-sentence rule
#
# await X says: "if X isn't ready, park this coroutine and tell the event loop to run
# something else; resume me here when X is done."
#
# That's the entire model. The "where does it stop, process, resume" answer is:
#   Stops: at every await line, only if the awaited operation isn't immediately ready.
#   Processes (other coroutines): while parked, the event loop runs any other coroutine that's ready.
#   Resumes: when the OS notifies the loop that the awaited I/O is complete.
#
# Between two awaits, code runs straight through with no interruption — there's no preemption.
# This is why async is called cooperative concurrency: each coroutine voluntarily marks
# its yield points.

# If you call requests.get inside an async function, the event loop has no chance to run anything
# else for the duration of that call. The whole point of async is lost. This is why every LLM SDK
# ships an explicit async client (AsyncAnthropic, client.aio.models) — the sync versions would
# silently destroy concurrency if you used them inside async def.