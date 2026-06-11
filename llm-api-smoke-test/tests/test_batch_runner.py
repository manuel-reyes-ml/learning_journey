"""Tests for llm_api_smoke_test.batch_runner.
 
Covers batch_smoke_test() — the async driver with semaphore + rate limiter.
 
Why pytest-asyncio?
-------------------
Async tests need an event loop.  Manual ``asyncio.run()`` in every test
is repetitive and error-prone.  The ``pytest-asyncio`` plugin gives us
``@pytest.mark.asyncio`` which provides an event loop automatically.
 
Install with:
    pip install pytest-asyncio
 
Then in pyproject.toml:
    [tool.pytest.ini_options]
    asyncio_mode = "auto"   # any async def test_* runs in an event loop
 
With auto mode, you don't even need @pytest.mark.asyncio on each test —
just write ``async def test_x()`` and it works.
"""

# =============================================================================
# IMPORTS
# =============================================================================

from __future__ import annotations

import asyncio
import pytest

from llm_api_smoke_test.config import ProviderSettings
from llm_api_smoke_test.batch_runner import batch_smoke_test
from llm_api_smoke_test.providers import SmokeTestResult

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

class TestBatchSmokeTestFailures:
    "Async exception handling — same contract as the sync runner."""
    
    async def test_failure_captured_not_raised(
        self, failing_async_provider: FakeAsyncProvider,
    ) -> None:
        """Async provider raises → recorded in failures, not propagated."""
        # No try/except — the runner must catch internally.
        successes, failures = await batch_smoke_test(
            providers=[failing_async_provider],  # type: ignore[type-arg]
            prompts=["test"],
        )
        
        assert successes == []
        assert len(failures) == 1
        
        class_name, exc = failures[0]
        assert class_name == "FakeAsyncProvider"
        assert isinstance(exc, RuntimeError)
        

# =============================================================================
# Concurrency contract
# =============================================================================

class TestConcurrencyLimits:
    """The semaphore + rate-limiter ARE the production patterns
    that make batch_runner.py worth reviewing.  Pin their behaviour.
    """
    
    async def test_respects_max_concurrency_cap(
        self, provider_settings: ProviderSettings,
    ) -> None:
        """At any moment, no more than max_concurrent coroutines hold the
        semaphore slot inside the provider call.
 
        The technique: instrument the fake to track ENTRY and EXIT, then
        verify the running count never exceeded the cap.
        """
        # Track concurrent calls.  We need to mutate from inside the
        # async method, so use lists/atomics.
        current = [0]  # current in_flight calls
        peak = [0]     # max ever seen
        
        class InstrumentedAsyncProvider:
            def __init__(self, settings: ProviderSettings) -> None:
                self._settings = settings
                self.calls: list[str] = []
                
            async def smoke_test(self, prompt: str) -> SmokeTestResult:
                # Entry: increment, update peak.
                current[0] += 1
                peak[0] = max(peak[0], current[0])
                
                # Hold the slot for a moment so concurrency can be
                # observed.  Tiny sleep = real async yield.
                await asyncio.sleep(0.01)
                self.calls.append(prompt)
                
                # Exit: decrement.
                current[0] -= 1
                
                return SmokeTestResult(
                    provider_name="fake",
                    model="fake",
                    response_preview="ok",
                )
                
            async def generate_structured(self, prompt: str, schema) -> Exception:
                raise NotImplementedError
            
        provider = InstrumentedAsyncProvider(provider_settings)                
        max_cap = 3
        
        # Launch 10 prompts against a single provider with cap=3.
        await batch_smoke_test(
            providers=[provider],   # type: ignore[type-arg]
            prompts=[f"p{i}" for i in range(10)],
            max_concurrent=max_cap,
        )
        
        # Peak concurrency never exceeded the cap.
        assert peak[0] <= max_cap, (
            f"Peak concurrency {peak[0]} exceeded cap {max_cap} - "
            "semaphore is not actually constraining concurrency."
        )
        # But did approach it — otherwise the test is trivially true.
        # With 10 tasks + cap=3 + 10ms hold, we expect to hit at least 2.
        assert peak[0] >= 2, (
            "Peak concurrency too low ' tasks are running serially, "
            "which suggests gather() isn't being awaited."
        )
        
    async def test_all_prompts_processed_even_with_low_concurrency(
        self, fake_async_provider: FakeAsyncProvider,
    ) -> None:
        """max_concurrent=1 → all prompts still run, just serially."""
        # Cap of 1 means strictly serial execution.
        await batch_smoke_test(
            providers=[fake_async_provider],  # type: ignore[type-arg]
            prompts=["a", "b", "c"],
            max_concurrent=1,
        )
        
        # ALL three prompts arrived.
        assert sorted(fake_async_provider.calls) == ["a", "b", "c"]