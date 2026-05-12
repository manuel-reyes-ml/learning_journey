"""Configuration module for API key smoke test.
 
Loads provider credentials and model identifiers from environment variables
into Pydantic-validated settings. Reading from process environment lets the
script run cleanly inside Docker containers, GitHub Actions, or local shells
without importing dotenv at module scope.
 
Notes
-----
This module never logs or prints API keys. The ``SecretStr`` type from
Pydantic redacts the value in repr/str output, which is the recommended
production-grade pattern for credential handling.
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

# It turns type hints into runtime checks. A plain class trusts whatever
# you pass it; a BaseModel rejects bad input at construction.
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
    
    # ConfigDict is a TypedDict you assign to model_config to configure the
    # entire model (not individual fields).
    #   - Models can be configured to be immutable via model_config['frozen'] = True.
    #     When this is set, attempting to change the values of instance attributes will
    #     raise errors. Also auto-generates __hash__() so instances become hashable. Same
    #     intent as frozen=True on dataclasses.
    #   - If extra was set to 'forbid', Pydantic Rejects unknown fields instead of silently
    #     dropping them. 'api_kye' would not be permitted in construction.
    #
    # Other production flags worth knowing for later: strict=True (no type coercion — int won't accept "5")
    # and validate_assignment=True (re-validates on attribute set, only meaningful if not frozen).
    model_config = ConfigDict(frozen=True, extra="forbid")
    
    # SecretStr wraps a string so it appears as ********** in repr,
    # str, print, JSON dump, and tracebacks. Only .get_secret_value()
    # returns the real value.
    name: str
    api_key: SecretStr
    model: str
    
    # Decorate a classmethod that runs after Pydantic's type check.
    # Raise ValueError to reject; return the value to accept.
    # Instead of a 401 Unauthorized from Anthropic 30 seconds into your script,
    # you get a clear ValidationError pointing at the exact field on the line
    # load_config() runs. Fail fast, fail at the boundary.
    @field_validator("api_key")  # <- which field
    @classmethod  # <- MUST be classmethod
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
            # MUST raise ValueError (not custom exception)
            raise ValueError("API key is empty or a placeholder value.")
        # Return the value on good input. Don't mutate self.
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
    

# Mapping[K, V] - the read-only dict contract
# Mapping describes a dict-like object (with "getitem") that we won't mutate, and MutableMapping one
# (with "setitem") that we might. By annotating env: Mapping[str, str] | None instead of
# env: dict[str, str] | None, you're making two statements:
#   1. To the caller: "Pass me anything dict-like — os.environ, a real dict, a ChainMap,
#   a custom config object."
#   2. To future-you: "I promise not to mutate this." The type checker will flag any
#   attempt to do source["X"] = ... inside load_config.
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
    # os.environ is a dict-like object (actually os._Environ, which implements MutableMapping)
    # representing the current process's environment variables. 
    # When you run ANTHROPIC_API_KEY=sk-... python script.py, that key shows up in
    # os.environ["ANTHROPIC_API_KEY"] for the lifetime of that Python process.
    #
    # 1. It's per-process, not global. A subprocess inherits a copy; changes don't propagate back.
    # Changes you make in Python (os.environ["X"] = "y") only affect the current process and
    # its future children.
    # 2. Values are always strings. No types, no validation — which is exactly why your load_config()
    # exists: to translate the untyped string world into the typed SmokeTestConfig world.
    # 3. Reading it directly couples your code to the OS. Your decision to accept
    # env: Mapping[str, str] | None = None and default to os.environ is the right one —
    # it's the dependency-injection pattern applied to the environment. Tests pass a dict;
    # production uses the real os.environ. Zero monkey-patching needed.
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