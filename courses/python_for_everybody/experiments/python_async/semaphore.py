# Practice asyncio.Semaphore - counter Model

from __future__ import annotations

import asyncio
import time

from aiolimiter import AsyncLimiter

START = time.perf_counter()

def t() -> str:
    return f"{(time.perf_counter() - START) * 1000:6.1f}ms"

async def work(name: str, sem: asyncio.Semaphore, limiter: AsyncLimiter) -> str:
    print(f"{t()}  {name}  📩 arrived, attempting to acquire sem")
    # The 'async with sem' form is the recommended way — it guarantees release even
    # if do_work raises, just like a sync with block guarantees close() is called.
    #   - It does sem.acquire() and sem.release() automatically
    #
    async with limiter:
        # Without async with, a thrown exception would permanently consume one slot,
        # slowly starving the semaphore until everything deadlocks.
        # The context manager makes this impossible.
        async with sem:
            # Acquire — try to take one. If counter > 0: decrement and proceed.
            # If counter = 0: park the coroutine in a FIFO queue and wait.
            print(f"{t()}  {name}  ✅ acquired slot, starting work")
            await asyncio.sleep(0.2)  # simulate the LLM call
            print(f"{t()}  {name}  🏁 work done, releasing slot")
            return f"result-{name}"
            # Release — give one back. Increment the counter.
            # If anyone's waiting, wake the first in line.
        
async def main() -> None:
    # asyncio.Semaphore(n) is a counter starting at n, with two operations:
    #   - Acquire
    #   - Release
    sem = asyncio.Semaphore(2)  # cap at 2 concurrent (counter model)
    limiter = AsyncLimiter(50, 60)  # 50 calls per 60 seconds
    tasks = [work(name, sem, limiter) for name in "ABCDE"]
    
    results = await asyncio.gather(*tasks)
    print(f"{t()} done: {results}")
    
asyncio.run(main())

# Three phases visible:
# Phase 1: A & B grab slots immediately. C, D, E park in FIFO queue -> 0–200ms
# Phase 2: A & B finish at ~200ms. C & D wake (in arrival order) -> 200–400ms
# Phase 3: C & D finish at ~400ms. E wakes (last in queue) -> 400–600ms

# Total wall time: ~600ms = ceil(5 / 2) × 200ms. Compare to the no-semaphore
# version (~200ms — all 5 fire at once) and the sequential version (~1000ms).
# Semaphore gives you a tunable knob between those two extremes.