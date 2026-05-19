"""
"""

# =============================================================================
# IMPORTS
# =============================================================================

from __future__ import annotations

import asyncio
import logging
import structlog

from aiolimiter import AsyncLimiter
from collections.abc import Iterator
from typing import Final

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
slogger = structlog.stdlib.get_logger(__name__)
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