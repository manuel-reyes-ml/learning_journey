"""Shared pytest fixtures for the llm_api_smoke_test test suite.
 
Why a top-level conftest.py?
----------------------------
Pytest auto-discovers ``conftest.py`` at every directory level on its
way down to a test file.  Fixtures defined here are visible to EVERY
test module in this folder without explicit imports — that's the
convention recruiters expect to see.
 
What goes here vs. in individual test modules?
----------------------------------------------
- Here: fixtures shared across ≥2 test files (env vars, fake providers,
  the validated settings object).
- In test modules: fixtures used by ONE test file (e.g., a registry
  snapshot used only by ``test_register.py``).
 
Roadmap relevance
-----------------
The fake-provider pattern below (a class that satisfies the Protocol
without making real API calls) carries forward to every Stage 2+
project that has external dependencies.  You'll reuse this exact
shape for DataVault's ``FakeLLMProvider``, PolicyPulse's
``FakeVectorStore``, and AFC's ``FakeSecAPI``.
"""

# =============================================================================
# IMPORTS
# =============================================================================

from __future__ import annotations

import pytest
from pydantic import SecretStr

from src.llm_api_smoke_test.config import ProviderSettings, SmokeTestSettings
from src.llm_api_smoke_test.providers import SmokeTestResult, TokenUsage

# =============================================================================
# ENVIRONMENT FIXTURES
# =============================================================================

@pytest.fixture
def valid_env(monkeypatch: pytest.MonkeyPatch) -> dict[str, str]:
    """Populate os.environ with VALID test credentials.
 
    Uses monkeypatch.setenv so the env is restored after the test —
    other tests aren't polluted with these fake keys.  This is the
    canonical pytest pattern for env-var manipulation: NEVER set
    os.environ directly in a test.
 
    Returns
    -------
    dict of {str : str}
        The same env vars as a dict for tests that want to inspect
        the values that were set.
    """
    # Fake-but-realistic-shaped keys.  The placeholder validator on
    # ProviderSettings.api_key rejects the literal strings "your-key-here",
    # "changeme", etc — anything else passes the validator.
    env = {
        "ANTHROPIC_API_KEY": "sk-ant-test-fake-key-not-real",
        "GEMINI_API_KEY": "AIza-test-fake-key-not-real",
        "ANTHROPIC_MODEL": "claude-sonnet-4-6",
        "GEMINI_MODEL": "gemini-2.5-flash",
    }
    
    # monkeypatch.setenv = "set this env var, restore after the test"
    # This is what makes the fixture safe to use in any test order.
    for key, value in env.items():
        monkeypatch.setenv(key, value)
        
    return env


@pytest.fixture
def settings(valid_env: dict[str, str]) -> SmokeTestSettings:
    """Validated SmokeTestSettings built from valid_env.
 
    Depends on valid_env so the env is populated BEFORE pydantic-settings
    reads from os.environ.  The dependency chain is automatic — pytest
    sees the parameter name and runs valid_env first.
 
    Returns
    -------
    SmokeTestSettings
        A validated, frozen settings instance.
    """
    # type: ignore[call-arg] is the documented Pydantic-Settings workaround —
    # pydantic populates fields from env, but mypy can't see that and thinks
    # the constructor is missing required args.
    return SmokeTestSettings()  # type: ignore[call-arg]


@pytest.fixture
def provider_settings() -> ProviderSettings:
    """A standalone ProviderSettings for unit tests.
 
    Returns
    -------
    ProviderSettings
        A frozen ProviderSettings with the "Anthropic" identity but a
        fake key — safe to use in any test that doesn't make real
        network calls.
    """
    # SecretStr wraps the key so it appears as ********** in repr —
    # the same redaction protection as in production.
    return ProviderSettings(
        name="Anthropic",
        api_key=SecretStr("sk-ant-test-fake-key"),
        model="claude-sonnet-4-6",
    )
    

# =============================================================================
# FAKE PROVIDER FIXTURES (no real API calls)
# =============================================================================
 
# Why classes, not fixtures, for the fakes?
# ----------------------------------------
# Fixtures are for INSTANCES — values that get constructed once per test.
# But a class is the right shape here because:
# 1. We want to instantiate it inside the test with different settings.
# 2. We want type checkers to recognise it as LLMProvider via Protocol.
# 3. We want to inspect it with isinstance() — works with a class, not a fn.
#
# So we define classes at module scope and pytest-style fixtures that
# return instances of them.

class FakeSyncProvider:
    """A test double that satisfies LLMProvider without network calls.
 
    Records every prompt it receives and returns a configurable result.
    This is the textbook fake-object pattern from "xUnit Test Patterns"
    by Meszaros — it stands in for the real provider in tests without
    requiring an API key or producing flaky network behaviour.
 
    Parameters
    ----------
    settings : ProviderSettings
        Matches the real provider's constructor signature so the
        Protocol is satisfied.
    response : str, optional
        What to return as the preview text.  Default: "fake response".
    should_raise : Exception or None, optional
        If non-None, ``smoke_test`` raises this exception instead of
        returning.  Used to test failure paths.
 
    Examples
    --------
    >>> provider = FakeSyncProvider(settings)
    >>> result = provider.smoke_test("hello")
    >>> provider.calls
    ['hello']
    """
    
    def __init__(
        self,
        settings: ProviderSettings,
        response: str = "fake response",
        should_raise: Exception | None = None,
    ) -> None:
        self._settings = settings
        self._response = response
        self._should_raise = should_raise
        # Public so tests can assert on call history.
        self.calls: list[str] = []
        
    def smoke_test(self, prompt: str) -> SmokeTestResult:
        """Record the prompt; return a SmokeTestResult or raise."""
        self.calls.append(prompt)
        
        # Failure path — test how runners handle exceptions.
        if self._should_raise is not None:
            raise self._should_raise
        
        # Success path — return a result with all fields populated, so
        # downstream tests can assert on token counts, latency, etc.
        return SmokeTestResult(
            provider_name=self._settings.name,
            model=self._settings.model,
            response_preview=self._response,
            request_id="fake-req-id",
            usage=TokenUsage(input_tokens=10, output_tokens=5),
            latency_ms=12.3,
        )
        
    def generate_structured(self, prompt: str, schema) -> Exception:
        """Stub — not used by smoke_test runners."""
        raise NotImplementedError(
            "FakeSyncProvider doesn't implement structured output"
        )
    

class FakeAsyncProvider:
    """Async twin of FakeSyncProvider.
    
    Same attributes, same constructor — only smoke_test is async.
    Used to test batch_runner.py without real network I/O.
    """
    
    def __init__(
        self,
        settings: ProviderSettings,
        response: str = "fake response",
        should_raise: Exception | None = None,
    ) -> None:
        self._settings = settings
        self._response = response
        self._should_raise = should_raise
        self.calls: list[str] = []
        
    async def smoke_test(self, prompt: str) -> SmokeTestResult:
        """Async — same shape as FakeSyncProvider.smoke_test."""
        self.calls.append(prompt)
        
        if self._should_raise is not None:
            raise self._should_raise
        
        return SmokeTestResult(
            provider_name=self._settings.name,
            model=self._settings.model,
            response_preview=self._response,
            request_id="fake-async-req-id",
            usage=TokenUsage(input_tokens=10, output_tokens=5),
            latency_ms=8.1,
        )
        
    async def generate_structured(self, prompt: str, schema) -> Exception:
        """Stub — not used by smoke_test runners."""
        raise NotImplementedError(
            "FakeAsyncProvider doesn't implement structured output"
        )
        

@pytest.fixture
def fake_sync_provider(provider_settings: ProviderSettings) -> FakeSyncProvider:
    """Construct a fresh FakeSyncProvider with the provider_settings fixture."""
    return FakeSyncProvider(provider_settings)


@pytest.fixture
def fake_async_provider(provider_settings: ProviderSettings) -> FakeAsyncProvider:
    """Construct a fresh FakeAsyncProvider with the provider_settings fixture."""
    return FakeAsyncProvider(provider_settings)


@pytest.fixture
def failing_sync_provider(provider_settings: ProviderSettings) -> FakeSyncProvider:
    """A FakeSyncProvider that always raises RuntimeError."""
    return FakeSyncProvider(
        provider_settings,
        should_raise=RuntimeError("simulated API outage"),
    )
    
    
@pytest.fixture
def failing_async_provider(provider_settings: ProviderSettings) -> FakeAsyncProvider:
    """A FakeAsyncProvider that always raises RuntimeError."""
    return FakeAsyncProvider(
        provider_settings,
        should_raise=RuntimeError("simulated async API outage"),
    )