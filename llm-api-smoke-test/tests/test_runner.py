"""
"""

# =============================================================================
# IMPORTS
# =============================================================================

from __future__ import annotations

import pytest

from llm_api_smoke_test.providers import SmokeTestResult
from llm_api_smoke_test.runner import DEFAULT_PROMPT, run_smoke_tests

# Note: FakeSyncProvider is in conftest.py — auto-discovered by pytest.
# We import it from conftest only for type hints.
from tests.conftest import FakeSyncProvider

# =============================================================================
# Happy path
# =============================================================================

class TestRunSmokeTestHappyPath:
    """Tests that exercise normal, successful flows."""
    
    def test_single_provider_returns_one_success(
        self, fake_sync_provider: FakeSyncProvider,
    ) -> None:
        """One provider, default prompt → one success, zero failures."""
        successes, failures = run_smoke_tests(
            providers=[fake_sync_provider],  # type: ignore[arg-type]
        )
        
        # The shape of the return value - single tuple, two lists.
        assert len(successes) == 1
        assert len(failures) == 0
        
        # The provider was called with the default prompt.
        assert fake_sync_provider.calls == [DEFAULT_PROMPT]
        
        # The success has the data the fake provider returned.
        result = successes[0]
        assert isinstance(result, SmokeTestResult)
        assert result.provider_name == "Anthropic"
        assert result.response_preview == "fake response"
        
    def test_explicit_prompt_passed_through(
        self, fake_sync_provider: FakeSyncProvider,
    ) -> None:
        """Custom prompt → provider receives it, not DEFAULT_PROMPT."""
        run_smoke_tests(
            providers=[fake_sync_provider],  # type: ignore[type-arg]
            prompt="custom test prompt",
        )
        
        # The fake recorded the actual prompt passed in.
        assert fake_sync_provider.calls == ["custom test prompt"]
        # NOT the default - explicit prompt wins. 
        assert DEFAULT_PROMPT not in fake_sync_provider.calls
        
    def test_multiple_providers_iterate_in_order(
        self, provider_settings,
    ) -> None:
        """Two providers → both called, both succeed, order preserved.
        
        Constructed manually because we want different instances with
        different responses to verify ordering.
        """
        first = FakeSyncProvider(provider_settings, response="first reply")
        second = FakeSyncProvider(provider_settings, response="second reply")
        
        # failures not used i this test
        successes, _ = run_smoke_tests(
            providers=[first, second],  # type: ignore[type-arg]
        )
        
        assert len(successes) == 2
        assert successes[0].response_preview == "first reply"
        assert successes[1].response_preview == "second reply"
        
    def test_accepts_any_iterable(
        self, fake_sync_provider: FakeSyncProvider,
    ) -> None:
        """Iterable[T] means tuple, list, set, generator all work.
        
        This is the contract test we discussed earlier — runner must
        NOT require an Iterator (one-shot cursor); it must accept any
        Iterable (re-iterable collection).
        """
        # Pass a tuple — not a list.  Should still work.
        successes_from_tuple, _ = run_smoke_tests(
            providers=(fake_sync_provider,),  # type: ignore[type-arg]
        )
        assert len(successes_from_tuple) == 1
        
        # Pass a generator.  Generators are iterators technically,
        # but the contract allows them.
        gen = (fake_sync_provider for _ in range(1))
        successes_from_gen, _ = run_smoke_tests(providers=gen)  # type: ignore[type-arg]
        assert len(successes_from_gen) == 1
        
    def test_empty_provider_list_returns_empty_results(self) -> None:
        """Edge case: zero providers → zero successes, zero failures.
        
        Important boundary case.  The runner must NOT crash on empty
        input; it must return clean empty lists.
        """
        successes, failures = run_smoke_tests(providers=[])
        
        assert successes == []
        assert failures == []
        

# =============================================================================
# Failure paths
# =============================================================================

