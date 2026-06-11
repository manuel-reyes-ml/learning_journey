"""Tests for llm_api_smoke_test.runner.
 
Covers run_smoke_tests() — the synchronous driver.  Uses FakeSyncProvider
(defined in conftest.py) to avoid real API calls.
 
Why test runners?
-----------------
The runner is the only place "iterate providers, call smoke_test, capture
exceptions" lives.  A regression here silently breaks every CLI invocation.
The Iterable vs Iterator distinction we discussed earlier is also pinned
here as a contract test.
"""

# =============================================================================
# IMPORTS
# =============================================================================

from __future__ import annotations

from llm_api_smoke_test.config import ProviderSettings
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

class TestRunSmokeTestsFailures:
    """Exception handling — the key behavioral contract.
    
    The runner CATCHES exceptions and records them as failures rather
    than re-raising.  This lets one provider's outage not block other
    providers' tests.  Pin that behaviour.
    """
    
    def test_single_failure_recorded_not_raised(
        self, failing_sync_provider: FakeSyncProvider,
    ) -> None:
        """Provider raises → recorded in failures, no exception propagates."""
        # No try/except around the call — if the runner re-raised,
        # this test would fail with the exception, not the assertion.
        successess, failures = run_smoke_tests(
            providers=[failing_sync_provider],  # type: ignore[type-arg]
        )
        
        assert successess == []
        assert len(failures) == 1
        
        # The failure tuple shape: (class_name, exception).
        class_name, exc = failures[0]
        assert class_name == "FakeSyncProvider"
        assert isinstance(exc, RuntimeError)
        assert "simulated" in str(exc)
        
    def test_mixed_success_failure(
        self, provider_settings: ProviderSettings,
    ) -> None:
        """One success + one failure in the same call → both captured."""
        good = FakeSyncProvider(provider_settings, response="ok")
        bad = FakeSyncProvider(provider_settings, should_raise=ValueError("nope"))
        
        successes, failures = run_smoke_tests(providers=[good, bad])  # type: ignore[type-arg]
        
        # Each list has exactly one element.
        assert len(successes) == 1
        assert len(failures) == 1
        
        # Verify each is the right kind
        assert successes[0].response_preview == "ok"
        assert isinstance(failures[0][1], ValueError)
        
    def test_failure_doesnt_block_subsequent_providers(
        self, provider_settings: ProviderSettings,
    ) -> None:
        """A failure in position 0 must NOT prevent provider 1 from running.
        
        This is the core "fail individually, run independently" contract.
        """
        bad = FakeSyncProvider(provider_settings, should_raise=OSError("boom"))
        good = FakeSyncProvider(provider_settings, response="still ran")
        
        successes, failures = run_smoke_tests(providers=[bad, good])  # type: ignore[type-arg]
        
        # The good provider ran - its call is recorded
        assert good.calls == [DEFAULT_PROMPT]
        # And produced a success.
        assert len(successes) == 1
        assert successes[0].response_preview == "still ran"