"""
"""

# =============================================================================
# IMPORTS
# =============================================================================

from __future__ import annotations

import asyncio
import pytest

from llm_api_smoke_test.batch_runner import batch_smoke_test

# Note: FakeAsyncProvider is in conftest.py
from tests.conftest import FakeAsyncProvider


# pytestmark applies @pytest.mark.asyncio to EVERY test in this file —
# the per-test decorator boilerplate disappears.
pytestmark = pytest.mark.asyncio

# =============================================================================
# Happy path
# =============================================================================

class TestBatchSmokeTestHappyPath:
    """Async batch runner — successful flows."""
    
    async def test_single_provider_single_prompt(
        self, fake_async_provider: FakeAsyncProvider,
    ) -> None:
        """One provider × one prompt → one success."""
        successes, failures = await batch_smoke_test(
            providers=[fake_async_provider],  # type: ignore[type-arg]
            prompts=["hello"],
        )
        
        assert len(successes) == 1
        assert len(failures) == 0
        assert fake_async_provider.calls == ["hello"]
        
    async def test_multiple_prompts_iterate_via_gather(
        self, fake_async_provider: FakeAsyncProvider,
    ) -> None:
        """Multiple prompts → all sent to the provider, all captured.
        
        Each prompt becomes one _bounded_call coroutine, gathered
        concurrently inside the rate limiter.
        """
        prompts = ["one", "two", "three"]
        
        successes, failures = await batch_smoke_test(
            providers=[fake_async_provider],  # type: ignore[type-arg]
            prompts=prompts,
        )
        
        # One success per prompt.  Order may differ inside successes
        # because tasks run concurrently — don't pin order.
        assert len(successes) == 3
        # But the provider DID receive all three prompts (order may
        # vary due to gather + semaphore scheduling).
        assert sorted(fake_async_provider.calls) == sorted(prompts)
        
    async def test_iterable_contracts_lists_accepted(
        self, fake_async_provider: FakeAsyncProvider,
    ) -> None:
        """Iterable[T] means a plain list is enough — no iter() needed.
        
        Contract test for the Iterable vs Iterator distinction.  A
        prior version of this code required iter(providers) — that's
        a foot-gun this test guards against re-introducing.
        """
        # Pass a list directly - no iter().
        result = await batch_smoke_test(
            providers=[fake_async_provider],  # type: ignore[type-ignore]
            prompts=["x"],
        )
        
        # Just needs to not crash.
        assert isinstance(result, tuple)
        
        
# =============================================================================
# Failure paths
# =============================================================================

