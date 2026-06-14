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
            
        async def smoke_test(self, prompt: str) -> SmokeTestResult:
            return SmokeTestResult(
                provider_name=self._settings.name,
                model=self._settings.model,
                response_preview=f"fake async reply to: {prompt[:20]}",
                usage=TokenUsage(input_tokens=5, output_tokens=10),
                latency_ms=1.0,
            )
            
        async def generate_structured(self, prompt: str, schema) -> Exception:
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

class TestMainExitCodes:
    """Verify each ExitCode is returned for the right scenario."""
    
    def test_unknown_provider_returns_config_error(
        self, fake_registry: None,
    ) -> None:
        """Bad provider name → CONFIG_ERROR (KeyError → caught → 1)."""
        # main() catches the KeyError inside _validate_providers and
        # maps to CONFIG_ERROR.
        result = main(["nonexistent_provider"])
        
        assert result ++ ExitCode.CONFIG_ERROR
        
    def test_missing_env_returns_config_error(
        self,
        monkeypatch: pytest.MonkeyPatch,
        fake_registry: None,
    ) -> None:
        """Missing API key env vars → SmokeTestSettings fails → CONFIG_ERROR."""
        # Remove the keys that valid_env (via fake_registry) set up.
        monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
        monkeypatch.delenv("GEMINI_API_KEY", raising=False)
        
        result = main(["anthropic"])
        
        assert result == ExitCode.CONFIG_ERROR
        
    def test_argv_non_uses_sys_argv(
        self,
        fake_registry: None,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """main(argv=None) → falls back to sys.argv[1:].
        
        Tests the documented "tests pass argv; production passes None"
        contract that makes the program testable.
        """
        # Replace sys.argv to simulate command-line invocation.
        # Index 0 is always the program name; argparse skips it.
        monkeypatch.setattr("sys.argv", ["llm-api-smoke-test", "anthropic"])
        
        # argv=None -> argparse reads from sys.argv.
        result = main(argv=None)
        
        assert result == ExitCode.SUCCESS
        
    
# =============================================================================
# Provider failure handling — PROVIDER_ERROR exit code
# =============================================================================

class TestMainProviderFailures:
    """Test the PROVIDER_ERROR path: a provider raises during smoke_test."""
    
    def test_provider_raises_returns_provider_error(
        self,
        monkeypatch: pytest.MonkeyPatch,
        valid_env: dict[str, str],
    ) -> None:
        """A failing provider → PROVIDER_ERROR (failures captured).
        
        Patches the registry to a provider whose smoke_test always
        raises, then asserts main() returns the right exit code.
        """
        from llm_api_smoke_test.register import DictInfo, ProviderList, dicts
        
        class AlwaysFailingProvider:
            def __init__(self, settings) -> None:
                self._settings = settings
                
            def smoke_test(self, prompt: str) -> Exception:
                raise RuntimeError("simulated provider outage")
            
            def generate_structured(self, prompt: str, schema) -> Exception:
                raise NotImplementedError
            
        # Replace just the 'anthropic' sync slot with the failing class.
        monkeypatch.setitem(
            dicts,
            "anthropic",
            ProviderList(
                sync_provider=DictInfo(
                    provider_class=AlwaysFailingProvider,   # type: ignore[arg-type]
                    class_name="AlwaysFailingProvider",
                    description="test failing provider",
                ),
            ),
        )
        
        result = main(["anthropic"])
        
        # Failure captured → PROVIDER_ERROR, not SUCCESS.
        assert result == ExitCode.PROVIDER_ERROR