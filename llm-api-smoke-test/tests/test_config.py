"""Tests for llm_api_smoke_test.config.
 
Coverage targets
----------------
- :class:`ProviderSettings` — frozen, redacts secrets, rejects placeholders.
- :class:`SmokeTestSettings` — loads from env, validates, adapts to nested shape.
- :func:`load_config` — legacy env-loading function with explicit Mapping[K, V].
 
Why test config first?
----------------------
Config is the FIRST thing the program touches at startup.  If config
is broken, nothing else matters.  Testing it first builds confidence
in the foundation before any other test can pass.
"""

# =============================================================================
# IMPORTS
# =============================================================================

from __future__ import annotations

from _pytest import monkeypatch
import pytest
from pydantic import SecretStr, ValidationError

from llm_api_smoke_test.config import (
    ProviderSettings,
    SmokeTestConfig,
    SmokeTestSettings,
    load_config
)

# =============================================================================
# ProviderSettings — the small, well-tested unit
# =============================================================================

class TestProviderSettings:
    """Group related assertions in a class.
 
    Pytest classes have NO setUp/tearDown overhead — they're just
    namespacing.  The convention is: one class per unit-under-test,
    methods grouped by behaviour.
 
    Class-based grouping has two payoffs:
    1. Test reports read like a spec: TestProviderSettings::test_rejects_empty_key
    2. Shared fixtures via @pytest.fixture on class methods (rare; mostly
       just for the namespacing here).
    """
    
    def test_accepts_realistic_key(self) -> None:
        """Happy path — a normal-looking key constructs successfully."""
        # Arrange-Act-Assert pattern (AAA): explicit setup, single action,
        # assertion on the result.  This is the most readable shape.
        
        # Arrange
        valid_key = SecretStr("sk-ant-real-looking-key")
        
        # Act
        settings = ProviderSettings(
            name="Anthropic",
            api_key=valid_key,
            model="claude-sonnet-4-6",
        )
        
        # Assert
        assert settings.name == "Anthropic"
        assert settings.model == "claude-sonnet-4-6"
        # get_secret_value() is the canonical way to read a SecretStr.
        assert settings.api_key.get_secret_value() == "sk-ant-real-looking-key"
        
    def test_redacts_api_key_in_repr(self, provider_settings: ProviderSettings) -> None:
        """SecretStr must redact in repr — this is the contract that
        protects API keys from leaking into logs and tracebacks.
        """
        # repr() is what str.format / logging / IPython display call.
        rendered =repr(provider_settings)
        
        # The actual secret must not appear.
        assert "sk-ant-test-fake-key" not in rendered
        # Pydantic redacts SecretStr as **********.
        assert "**********" in rendered
        
    @pytest.mark.parametrize(
        "placeholder",
        [
            "",                  # empty string
            "your-key-here",     # common copy-paste leftover
            "sk-xxxxx",          # template placeholder
            "changeme",          # dev-default
            "YOUR-KEY-HERE",     # caseâ€"insensitive check 
        ],
    )
    def test_rejects_placeholder_keys(self, placeholder: str) -> None:
        """The _reject_placeholder validator must reject all known
        placeholder strings.
        
        Parametrize lets ONE test method cover N cases — pytest reports
        each parameter as a separate test, so you see precisely which
        placeholder slipped through if one fails.
        """
        # pytest.raises is the canonical way to assert on exceptions.
        # The 'match' arg checks the exception message via re.search.
        with pytest.raises(ValidationError, match="placeholder"):
            ProviderSettings(
                name="Anthropic",
                api_key=SecretStr(placeholder),
                model="claude-sonnet-4-6",
            )
            
    def test_is_frozen(self, provider_settings: ProviderSettings) -> None:
        """frozen=True must prevent attribute reassignment.
 
        This is the contract that prevents accidental key-swap inside
        long-running scripts.
        """
        # Pydantic raises ValidationError (with frozen_instance error)
        # when you try to mutate a frozen model.
        with pytest.raises(ValidationError):
            provider_settings.name = "Spoofed"  # type: ignore[misc]
            
    def test_forbids_extra_fields(self) -> None:
        """extra="forbid" rejects unknown fields at construction time.
 
        This catches typos like ``api_kye`` before they silently get
        dropped.
        """
        with pytest.raises(ValidationError, match="extra"):
            ProviderSettings(
                name="Anthropic",
                api_key=SecretStr("sk-ant-test"),
                model="claude-sonnet-4-6",
                bogus_field="should_fail",  # type: ignore[call-arg]
            )
            
            
# =============================================================================
# SmokeTestSettings — env-driven loading
# =============================================================================

class TestSmokeTestSettings:
    """Tests for the env-loading pydantic-settings class."""
    
    def test_loads_from_env(self, valid_env: dict[str, str]) -> None:
        """Settings populates from env vars automatically.
 
        valid_env fixture set the env BEFORE this test runs — pytest
        resolves the dependency for us.
        """
        # The construct-from-env call.  type: ignore matches what your
        # __main__.py does — pydantic-settings reads env, mypy can't see it.
        settings = SmokeTestSettings()  # type: ignore[call-arg]
        
        # Verify each field was populated from its env counterpart.
        assert settings.anthropic_api_key.get_secret_value() == valid_env["ANTHROPIC_API_KEY"]
        assert settings.anthropic_model == valid_env["ANTHROPIC_MODEL"]
        assert settings.gemini_api_key.get_secret_value() == valid_env["GEMINI_API_KEY"]
        assert settings.gemini_model == valid_env["GEMINI_MODEL"]
        
    def test_uses_defaults_when_models_omitted(
        self,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """Optional model env vars fall back to declared defaults.
 
        Only the *_API_KEY vars are required; *_MODEL has a class default.
        """
        # Set only what's required.  delenv with raising=False is the
        # "remove if present, silent if absent" pattern.  
        monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-ant-fake")
        monkeypatch.setenv("GEMINI_API_KEY", "AIza-fake")
        monkeypatch.delenv("ANTHROPIC_MODEL", raising=False)
        monkeypatch.delenv("GEMINI_MODEL", raising=False)
        
        settings = SmokeTestSettings()  # type: ignore[call-arg]
        
        # The defaults declared on the class fields.
        assert settings.anthropic_model == "claude-sonnet-4-6"
        assert settings.gemini_model == "gemini-2.5-flash"
        
    def test_missing_required_key_raises(
        self,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """Missing API key → ValidationError from pydantic-settings."""
        # Remove BOTH keys so we know which error trips.  Otherwise the
        # first missing field would mask the second.
        monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
        monkeypatch.delenv("GEMINI_API_KEY", raising=False)
        
        with pytest.raises(ValidationError):
            SmokeTestSettings()  # type: ignore[call-arg]
            
    def test_to_smoke_test_config_adapter(
        self,
        settings: SmokeTestSettings,  # from 'settings' pytest.fixture
    ) -> None:
        """The adapter method should produce a valid SmokeTestConfig.
 
        Tests the bridge between the flat env-var shape and the nested
        SmokeTestConfig shape that other code may consume.
        """
        config = settings.to_smoke_test_config()
        
        # Verify isinstance — the adapter must return the right type.
        assert isinstance(config, SmokeTestConfig)
        assert isinstance(config.anthropic, ProviderSettings)
        assert isinstance(config.gemini, ProviderSettings)
        
        # Verify the data flows through correctly.
        assert config.anthropic.name == "Anthropic"
        assert config.gemini.name == "Gemini"
        

class TestOpenRouterConfig:
    """OpenRouter is OPTIONAL: None when unset, a real ProviderSettings when set."""

    def test_absent_is_none(
        self, valid_env: dict[str, str], monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """No OPENROUTER_API_KEY → openrouter collapses to None, doesn't crash."""
        # Defensive: a stray key in your shell OR a local .env would make
        # "absent" non-absent. delenv clears the process env...
        monkeypatch.delenv("OPENROUTER_API_KEY", raising=False)
        # ...and _env_file=None disables .env reading for THIS instance — the
        # documented pydantic-settings escape hatch for hermetic tests.
        #
        # That _env_file=None  it's the canonical way to make pydantic-settings
        # tests independent of whatever .env happens to sit in the working directory.
        settings = SmokeTestSettings(_env_file=None)    # type: ignore[call-arg]

        assert settings.openrouter_api_key is None
        assert settings.to_smoke_test_config().openrouter is None

    def test_default_model_slug(self, settings: SmokeTestSettings) -> None:
        """The default slug is a cheap model — never a flagship for a 200-OK check."""
        assert settings.openrouter_model == "deepseek/deepseek-v4-flash"

    def test_present_build_provider(
        self, settings_with_openrouter: SmokeTestSettings,
    ) -> None:
        """Key present → to_smoke_test_config() yields a named OpenRouter provider."""
        cfg = settings_with_openrouter.to_smoke_test_config()
        assert cfg.openrouter is not None
        assert cfg.openrouter.name == "OpenRouter"
        assert cfg.openrouter.model == "deepseek/deepseek-v4-flash"
        assert cfg.openrouter.api_key.get_secret_value() == "sk-or-test-fake-key-not-real"   


# =============================================================================
# load_config — legacy explicit-Mapping function
# =============================================================================

class TestLoadConfig:
    """Tests for the explicit-mapping load_config() function.
    
    Note: This function is superseded by SmokeTestSettings, but it's still
    exported.  Worth keeping these tests until you decide to remove it.
    """
    
    def test_loads_from_explicit_mapping(self) -> None:
        """Pass a dict — get a SmokeTestConfig back.
        
        This is the dependency-injection pattern: the function accepts
        a Mapping rather than reading os.environ directly, so tests
        can pass any dict-like object.
        """
        env = {
            "ANTHROPIC_API_KEY": "sk-ant-explicit",
            "GEMINI_API_KEY": "AIza-explicit",
        }
        
        config = load_config(env)
        
        assert config.anthropic.api_key.get_secret_value() == "sk-ant-explicit"
        assert config.gemini.api_key.get_secret_value() == "AIza-explicit"
        
    def test_missing_key_raises_keyerror(self) -> None:
        """Missing env var → KeyError with a helpful message."""
        # Pass ONLY one of the two required keys.
        env = {"ANTHROPIC_API_KEY": "sk-ant"}
        
        # KeyError, not ValidationError — load_config raises before
        # construction.  Worth pinning the distinction in a test.
        with pytest.raises(KeyError, match="GEMINI_API_KEY"):
            load_config(env)
            
    def test_uses_default_model_when_omitted(self) -> None:
        """ANTHROPIC_MODEL omitted → falls back to load_config's default."""
        env = {
            "ANTHROPIC_API_KEY": "sk-ant",
            "GEMINI_API_KEY": "AIza",
        }
        config = load_config(env)
        
        # Note: This default lives in load_config() and is DIFFERENT
        # from SmokeTestSettings' default.  If you delete load_config,
        # this test goes away with it.
        # ⚠️ Bug flagged in review: load_config default is stale 
        # ("claude-opus-4-6") — fix it to match SmokeTestSettings.
        assert config.anthropic.model == "claude-sonnet-4-6"