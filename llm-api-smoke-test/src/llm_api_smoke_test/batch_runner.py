"""Async batch driver for the smoke-test runner.

Schedules many concurrent provider calls behind two protective layers:

- :class:`asyncio.Semaphore` — caps the number of *in-flight* requests.
- :class:`aiolimiter.AsyncLimiter` — caps the number of requests *per
  time window* (leaky-bucket rate limiter).

Both context managers compose cleanly: every call acquires the limiter
first (rate-limit) and the semaphore second (concurrency-cap), so a
burst is throttled to the provider's free-tier ceiling while a slow
provider still progresses without piling up backlog.

This is the same shape used by DataVault's batch query engine and AFC's
multi-symbol backtest fan-out.  Reusing it here in miniature gives the
smoke-test runner a structure that scales without rewrite.

References
----------
.. [1] aiolimiter — Leaky-bucket asyncio rate limiter
   https://aiolimiter.readthedocs.io/
.. [2] asyncio — Synchronization Primitives (Semaphore)
   https://docs.python.org/3/library/asyncio-sync.html
"""

# =============================================================================
# IMPORTS
# =============================================================================

from __future__ import annotations

import asyncio
import logging

from aiolimiter import AsyncLimiter
from collections.abc import Iterator
from typing import Final, TYPE_CHECKING

from llm_api_smoke_test.logger import get_structured_logger

if TYPE_CHECKING:
    from llm_api_smoke_test.providers import (
        AsyncLLMProvider,
        SmokeTestResult,
    )

# =============================================================================
# EXPORTS
# =============================================================================

__all__ = ["batch_smoke_test"]


# =============================================================================
# LOGGER SETUP
# =============================================================================

# Use structlog on Python's stdlib since some external packages
# use stdlib still.
slogger = get_structured_logger(__name__)
logger = logging.getLogger(__name__)


# =============================================================================
# MODULE CONFIGURATION
# =============================================================================
# =====================================================
# Constants
# =====================================================

# Cannot re assign global variable due to Final
MAX_CONCURRENT: Final[int] = 5

type CallFailure = tuple[str, Exception]
type BatchResult = tuple[list[SmokeTestResult], list[CallFailure]]


# =============================================================================
# CORE FUNCTION
# =============================================================================

async def batch_smoke_test(
    *,  # after this all parameters are keyword only
    providers: Iterator[AsyncLLMProvider],
    prompts: list[str],
    max_concurrent: int = MAX_CONCURRENT,
) -> BatchResult:
    """Run many smoke-test calls against one provider, capped at max_concurrent.
    
    This is the DataVault batch pattern in miniature:
      - `gather` schedules all N requests
      - The semaphore caps how many fly at once (rate-limit safety)
      - Results return in INPUT order (gather's guarantee)
    
    Parameters
    ----------
    provider : AsyncLLMProvider
        Any async provider — AsyncAnthropicProvider, AsyncGeminiProvider, etc.
        The Protocol contract means the runner doesn't care which.
    prompts : list[str]
        Prompts to send. Each one becomes one LLM call.
    max_concurrent : int
        Cap on in-flight calls. Below the provider's rate limit but high
        enough to overlap I/O. 5–10 is a sensible starting point for
        Anthropic/Gemini free tiers; bump for paid tiers.
    
    Returns
    -------
    list[SmokeTestResult]
        Results in input order — `results[i]` corresponds to `prompts[i]`.
    """
    successes: list[SmokeTestResult] = []
    failures: list[CallFailure] = []
    
    # Create the semaphore INSIDE the async function (or anywhere after the
    # event loop is running). Creating it at module scope used to attach it
    # to the wrong loop in older Python versions — still safest to do it here.
    sem = asyncio.Semaphore(max_concurrent)
    limiter = AsyncLimiter(50, 60)  # 50 calls per 60 seconds
    
    async def _bounded_call(prompt: str) -> None:
        """Run one prompt across every provider under the shared limits.

        Acquires the leaky-bucket limiter (rate cap) and the semaphore
        (concurrency cap) before iterating the providers.  Successes go
        into the outer ``successes`` list; exceptions are caught,
        logged structurally, and recorded in ``failures`` — one
        provider's outage does not abort the batch.

        Parameters
        ----------
        prompt : str
            Single prompt to send to every provider.

        Notes
        -----
        The function returns ``None`` — results are accumulated into the
        closures' ``successes`` and ``failures`` lists.  This keeps the
        ``asyncio.gather(...)`` call site simple at the cost of relying
        on shared mutable state (acceptable because all writes happen
        sequentially within a single coroutine).
        """
        async with limiter:   # composes cleanly with Semaphore
            # The semaphore protocol in 3 lines:
            # - `async with sem:` acquires a slot (parks if 0 free)
            # - The body runs only when this coroutine holds a slot
            # - Exit releases the slot, wakes the next waiter
            async with sem:
                for provider in providers:
                    provider_class = type(provider).__name__
                    logger.debug("Running smoke test with %s", provider_class)
                    
                    try:
                        result = await provider.smoke_test(prompt)
                        slogger.info(
                            "call_successful", 
                            provider_name=result.provider_name,
                            model=result.model,
                            response=result.response_preview,
                        )
                        successes.append(result)
                    except Exception as exc:
                        slogger.error(
                            "call_failed",
                            provider_class=provider_class,
                            type_exception=type(exc).__name__,
                            exception=exc,
                        )
                        failures.append((provider_class, exc))
        
    # Schedule all N tasks. `gather` returns them in input order even though
    # they complete in some other order, which is what we want for matching
    # results back to prompts.
    await asyncio.gather(*[_bounded_call(p) for p in prompts])
    
    return successes, failures