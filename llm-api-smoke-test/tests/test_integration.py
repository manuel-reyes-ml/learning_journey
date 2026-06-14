"""
"""

# =============================================================================
# IMPORTS
# =============================================================================

from __future__ import annotations

import pytest

from llm_api_smoke_test.__main__ import ExitCode, main

# =============================================================================
# Helper — swap real providers for fakes in the live registry
# =============================================================================

@pytest.fixture
def fake_registry(
    monkeypatch: pytest.MonkeyPatch,
    valid_env: dict[str, str],
) -> None:
    """Replace the LIVE provider classes with fakes for the duration.
    
    main() instantiates providers by reading ``dicts[name].sync_provider``
    or ``.async_provider`` and calling the .provider_class.  If we
    swap those entries with ProviderList wrappers around our fakes,
    main() runs end-to-end without any HTTP.
    
    monkeypatch.setitem reverts the change after the test — fixture
    is safe to combine with any other test.
    """
    from llm_api_smoke_test.config import ProviderSettings
    from llm_api_smoke_test.providers import SmokeTestResult, TokenUsage
    from llm_api_smoke_test.register import DictInfo, ProviderList, dicts
    
    # Define fakes inline — they're integration-test specific.
    class FakeSync:
        def __init__(self, settings: ProviderSettings) -> None:
            self._settings = settings
            
        def smoke_test(self, prompt: str) -> SmokeTestResult:
            return SmokeTestResult(
                provider_name=self._settings.name,
                model=self._settings.model,
                response_preview=f"fake reply to: {prompt[:20]}",
                usage=TokenUsage(input_tokens=5, output_tokens=10),
                latency_ms=1.0,
            )
            
        def generate_structured(self, prompt: str, schema) -> Exception:
            raise NotImplementedError
        
    class FakeAsync:
        def __init__(self, settings: ProviderSettings) -> None:
            self._settings = settings
            
        def smoke_test(self, prompt: str) -> SmokeTestResult:
            return SmokeTestResult(
                provider_name=self._settings.name,
                model=self._settings.model,
                response_preview=f"fake async reply to: {prompt[:20]}",
                usage=TokenUsage(input_tokens=5, output_tokens=10),
                latency_ms=1.0,
            )
            
        def generate_structured(self, prompt: str, schema) -> Exception:
            raise NotImplementedError
        
    # For each registered provider name, swap both slots.
    for name in list(dicts.keys()):
        bundle = ProviderList(
            sync_provider=DictInfo(
                provider_class=FakeSync,    # type: ignore[arg-type]
                class_name="FakeSync",
                description="integration fake sync",
            ),
            async_provider=DictInfo(
                provider_class=FakeAsync,   # type: ignore[arg-type]
                class_name="FakeAsync",
                description="integration fake async",
            ),
        )
        monkeypatch.setitem(dicts, name, bundle)
        
        
# =============================================================================
# Happy-path integration
# =============================================================================

class TestMainHappyPath:
    """Successful end-to-end invocations."""
    
    def test_sync_path_returns_success(self, fake_registry: None) -> None:
        """Default sync invocation → ExitCode.SUCCESS."""
        result = main(["anthropic"])
        
        assert result == ExitCode.SUCCESS
        
    def test_async_path_returns_success(self, fake_registry: None) -> None:
        """--async invocation → ExitCode.SUCCESS, exercises asyncio.run."""
        result = main(["anthropic", "--async"])
        
        assert result == ExitCode.SUCCESS
        
    def test_multiple_providers_sync(self, fake_registry: None) -> None:
        """Two providers, sync path → SUCCESS."""
        result = main(["anthropic", "gemini"])
        
        assert result == ExitCode.SUCCESS
        
    def test_multiple_prompts_sync(self, fake_registry: None) -> None:
        """Multiple prompts via --prompts → all run, SUCCESS."""
        result = main([
            "anthropic",
            "--prompts", "first prompt", "second prompt",
        ])
        
        assert result == ExitCode.SUCCESS
        
    def test_verbose_flag_doesnt_break(self, fake_registry: None) -> None:
        """--verbose → logging configured for DEBUG, still returns SUCCESS."""
        result = main(["anthropic", "-v"])
        
        assert result == ExitCode.SUCCESS
        
    def test_no_log_file_flag(self, fake_registry: None) -> None:
        """--no-log-file → console only, still returns SUCCESS."""
        result = main(["anthropic", "--no-log-file"])
        
        assert result == ExitCode.SUCCESS
        
        
# s=============================================================================
# Failure-path integration
# =============================================================================

