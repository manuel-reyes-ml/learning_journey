"""Synchronous smoke-test driver.

Calls :meth:`~llm_api_smoke_test.providers.LLMProvider.smoke_test` once
per provider with a shared default prompt and returns a
``(successes, failures)`` tuple.  Failures are captured rather than
raised so one provider's outage does not block the second.

This is the simplest possible shape for the smoke-test:

- No concurrency — sequential round-trips, easiest to trace in logs.
- No rate-limit logic — one call per provider stays well under every
  free-tier ceiling.
- No retry — a failed smoke test should surface immediately; the user
  needs to know the key is bad, not wait for backoff to give up.

For higher-throughput workloads use
:func:`~llm_api_smoke_test.batch_runner.batch_smoke_test`, which adds
:class:`asyncio.Semaphore` + :class:`aiolimiter.AsyncLimiter` protection.

Roadmap relevance
-----------------
The "iterate providers under a Protocol contract, capture failures"
pattern reappears in DataVault's provider-comparison harness and
AFC's data-source fan-out — both will reuse this exact return shape.
"""

# =============================================================================
# IMPORTS
# =============================================================================

from __future__ import annotations

import logging

from collections.abc import Iterable
from typing import Final

from llm_api_smoke_test.logger import get_structured_logger
from llm_api_smoke_test.providers import (
    LLMProvider,
    SmokeTestResult,
)

# =============================================================================
# EXPORTS
# =============================================================================

__all__ = [
    "run_smoke_tests",
    "CallFailure",
    "BatchResult",
]


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

# A minimal prompt — small enough to round-trip cheaply, complete enough to
# distinguish "API works" from "API returns garbage".
DEFAULT_PROMPT: Final[str] = "Reply with exactly the words: hello word"

type CallFailure = tuple[str, Exception]
type BatchResult = tuple[list[SmokeTestResult], list[CallFailure]]


# =============================================================================
# CORE FUNCTION
# =============================================================================

def run_smoke_tests(
    *,
    providers: Iterable[LLMProvider],
    prompt: str = DEFAULT_PROMPT,
) -> BatchResult:
    """Run the smoke test against every provided adapter.
 
    Parameters
    ----------
    providers : Iterable[LLMProvider]
        Configured adapters. Each adapter is exercised exactly once.
    prompt : str, optional
        Prompt sent to each provider. Defaults to ``DEFAULT_PROMPT``.
 
    Returns
    -------
    tuple[list[SmokeTestResult], list[tuple[str, Exception]]]
        A pair ``(successes, failures)``. ``failures`` is a list of
        ``(provider_class_name, exception)`` tuples — failures are
        captured rather than raised so one provider's outage does not
        block the second test.
 
    Notes
    -----
    Logger calls use ``%s``-style lazy formatting so the format string is
    only interpolated when the level is enabled. This is the runtime-
    efficient pattern enforced across the portfolio.
    """
    successes: list[SmokeTestResult] = []
    failures: list[CallFailure] = []
    
    for provider in providers:
        provider_class = type(provider).__name__
        logger.debug("Running smoke test with %s", provider_class)
        
        try:
            result = provider.smoke_test(prompt)
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
            
    return successes, failures