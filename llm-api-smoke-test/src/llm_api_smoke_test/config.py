"""
"""

# =============================================================================
# IMPORTS
# =============================================================================

from __future__ import annotations

import os
from collections.abc import Mapping

from pydantic import BaseModel, ConfigDict, SecretStr, field_validator

# =============================================================================
# CONSTANTS CONFIGURATION
# =============================================================================
# =====================================================
# Pydantic Class Configuration
# =====================================================

class ProviderSettings(BaseModel):
    """Validated settings for a single LLM provider.
 
    Parameters
    ----------
    name : str
        Display name for log messages (e.g., ``"Anthropic"``).
    api_key : SecretStr
        The provider API key, redacted in any string representation.
    model : str
        Default model identifier for the smoke test request.
 
    Notes
    -----
    ``model_config`` freezes instances so settings cannot be mutated after
    construction. This protects against accidental key swaps inside long-
    running scripts.
    """
    
    model_config = ConfigDict(frozen=True, extra="forbid")
    
    name: str
    api_key: SecretStr
    model: str
    
    @field_validator("api_key")
    @classmethod
    def _reject_placeholder(cls, value: SecretStr) -> SecretStr:
        """Reject obvious placeholder values that indicate misconfiguration.
 
        Parameters
        ----------
        value : SecretStr
            The candidate API key.
 
        Returns
        -------
        SecretStr
            The unchanged value if it passes the placeholder check.
 
        Raises
        ------
        ValueError
            If the unwrapped key is empty or matches a known placeholder
            string (e.g., the literal text ``"your-key-here"``).
        """
        raw = value.get_secret_value().strip()
        placeholders = {"", "your-key-here", "sk-xxxxx", "changeme"}
        if raw in placeholders or raw.lower() in placeholders:
            raise ValueError("API key is empty or a placeholder value.")
        return value
    
    
class SmokeTestConfig(BaseModel):
    """Top-level config aggregating both providers under test.
 
    Parameters
    ----------
    anthropic : ProviderSettings
        Configured Anthropic Claude provider.
    gemini : ProviderSettings
        Configured Google Gemini provider.
    """
    
    model_config = ConfigDict(frozen=True, extra="forbid")
    
    anthropic: ProviderSettings
    gemini: ProviderSettings
    
    
def load_config(env: Mapping[str, str] | None = None) -> SmokeTestConfig:
    """Build a ``SmokeTestConfig`` from a mapping of environment variables.
 
    Parameters
    ----------
    env : Mapping[str, str] or None, optional
        Environment-style mapping. If ``None``, reads from ``os.environ``.
        Accepting an injected mapping makes the function trivially testable
        without monkey-patching globals.
 
    Returns
    -------
    SmokeTestConfig
        Validated configuration ready for use by the smoke test runner.
 
    Raises
    ------
    KeyError
        If any required environment variable is absent.
    ValueError
        If any required key fails the placeholder check.
 
    Examples
    --------
    >>> cfg = load_config({
    ...     "ANTHROPIC_API_KEY": "sk-ant-real-key",
    ...     "GEMINI_API_KEY": "AIza-real-key",
    ... })
    >>> cfg.anthropic.name
    'Anthropic'
    """
    source = env if env is not None else os.environ
    
    required = ("ANTHROPIC_API_KEY", "GEMINI_API_KEY")
    missing = [k for k in required if k not in source]
    if missing:
        raise KeyError(f"Missing required environment variables: {missing}")
    
    return SmokeTestConfig(
        anthropic=ProviderSettings(
            name="Anthropic",
            api_key=SecretStr(source["ANTHROPIC_API_KEY"]),
            model=source.get("ANTHROPIC_MODEL", "claude-opus-4-6"),
        ),
        gemini=ProviderSettings(
            name="Gemini",
            api_key=SecretStr(source["GEMINI_API_KEY"]),
            model=source.get("GEMINI_MODEL", "gemini-2.5-flash"),
        ),
    )