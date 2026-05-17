from __future__ import annotations

import asyncio
import time

START = time.perf_counter()

def t() -> str:
    return f"{(time.perf_counter() - START) * 1000:6.1f}ms"

async def work(name: str, sem: asyncio.Semaphore) -> str:
    print(f"{t()}  {name}  📩 arrived, attempting to acquire sem")
    # Acquire — try to take one. If counter > 0: decrement and proceed.
    # If counter = 0: park the coroutine in a FIFO queue and wait.
    async with sem:
        print(f"{t()}  {name}  ✅ acquired slot, starting work")
        await asyncio.sleep(0.2)  # simulate the LLM call
        print(f"{t()}  {name}  🏁 work done, releasing slot")
        return f"result-{name}"
    
async def main() -> None:
    # asyncio.Semaphore(n) is a counter starting at n, with two operations:
    #   - Acquire
    #   - Release
    sem = asyncio.Semaphore(2)  # cap at 2 concurrent (counter model)
    tasks = [work(name, sem) for name in "ABCDE"]
    results = await asyncio.gather(*tasks)
    print(f"{t()} done: {results}")
    
asyncio.run(main())   