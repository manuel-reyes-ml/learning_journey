"""
"""

# =============================================================================
# IMPORTS
# =============================================================================

from __future__ import annotations

import pytest
from pydantic import SecretStr, ValidationError

from src.llm_api_smoke_test.config import (
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
        assert settings.api_key.get_secret_value() == "sk_ant_real_looking-key"
        
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


    