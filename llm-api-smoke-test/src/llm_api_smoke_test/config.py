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
from pydantic_settings import BaseSettings, SettingsConfigDict

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
    #
    # Class method - gets 'cls' -> works WITHOUT an instance (ProviderSettings._reject_placeholder())
    # cls is the class object itself, not an instance of it. Inside a classmethod, cls and
    # ProviderSettings refer to the same thing.
    #
    # When field_validator runs, the model instance doesn't exist yet.
    # Pydantic validates each field during construction, before __init__ finishes. So at that moment,
    # there's no self to give the validator. What Pydantic has on hand is the class itself —
    # so it passes cls.
    #
    # That's why @classmethod is required. It tells Python: "this method takes the class as its first
    # argument, not an instance" — which matches exactly how Pydantic calls it.
    @field_validator("api_key")  # <- which field - outer decorator (applied last)
    @classmethod  # <- MUST be classmethod - inner decorator (applied first)
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
    

# Base class for settings, allowing values to be overridden by environment variables.
# This is useful in production for secrets you do not wish to save in code, it plays
# nicely with docker(-compose), Heroku and any 12 factor app design.
class SmokeTestSettings(BaseSettings):
    """Loads from env automatically. Drop-in replacement for load_config()."""
    
    # Two more flags worth knowing:
    # - env_prefix="MYAPP_": When you want MYAPP_ANTHROPIC_API_KEY in env to map to
    # anthropic_api_key field. Useful when several apps share the same host machine or .env file.
    # - env_nested_delimiter="__": When you have nested config: LLM__PROVIDER=gemini →
    # settings.llm.provider. Lets you keep your nested ProviderSettings shape from the original
    # config.py but load it from flat env vars.
    model_config = SettingsConfigDict(
        # Also looks at the .env file in the working directory. Real env vars win if both exists.
        env_file=".env",
        # Specifies the text encoding when reading .env. Without it, Python falls back to the OS default
        # Explicit "utf-8" makes the behavior identical everywhere. 
        env_file_encoding="utf-8",
        # Decides how to handle env vars (or .env entries) that don't correspond to a field on your model.
        # 'forbid' (default in pydantic-settings): Raise ValidationError if any extra appears
        # 'ignore': Silently drop unknown variables
        # 'allow': Accept and store them as model attributes
        extra="ignore",
        # Same flag as on ConfigDict — locks the instance against mutation after it's built.
        frozen=True
    )
    # Each field auto-binds to the matching env var (case-insensitive)
    anthropic_api_key: SecretStr
    anthropic_model: str = "claude-opus-4-7"
    gemini_api_key: SecretStr
    gemini_model: str = "gemini-2.5-flash"
    
    def to_smoke_test_config(self) -> SmokeTestConfig:
        """Adapter back to your existing nested shape if other code depends on it."""
        return SmokeTestConfig(
            anthropic=ProviderSettings(
                name="Anthropic",
                api_key=self.anthropic_api_key,
                model=self.anthropic_model,
            ),
            gemini=ProviderSettings(
                name="Gemini",
                api_key=self.gemini_api_key,
                model=self.gemini_model,
            ),
        )
    
    
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
    

# from pydantic import BaseModel, SecretStr, field_validator

# class Provider(BaseModel):
#     api_key: SecretStr
    
#     @field_validator("api_key")
#     @classmethod
#     def _check(cls, value: SecretStr) -> SecretStr:
#         print(f"Inside validator — cls is: {cls.__name__}")
#         print(f"  Does the instance exist yet? No — we're building it.")
#         if value.get_secret_value() == "":
#             raise ValueError("empty")
#         return value

# p = Provider(api_key=SecretStr("sk-xxx"))

# OUTPUT:
# → Inside validator — cls is: Provider
# →   Does the instance exist yet? No — we're building it.

# Construction order:
# 1. You call Provider(api_key="sk-xxx")
# 2. Pydantic intercepts each field — runs validators
# 3. _check(cls=Provider, value=SecretStr("sk-xxx"))   ← classmethod call
# 4. If all validators pass, Pydantic assigns fields onto a new instance
# 5. Now the instance exists, and `p` points to it

# What you can do inside a classmethod-validator
# Because you have cls available, you can access:
#
# Class-level attributes (e.g., constants defined on the class)
# Other class methods
# The class itself for type checks

# class Provider(BaseModel):
#     PLACEHOLDERS = {"", "your-key-here", "sk-xxxxx", "changeme"}   # class constant
    
#     api_key: SecretStr
    
#     @field_validator("api_key")
#     @classmethod
#     def _check(cls, value: SecretStr) -> SecretStr:
#         raw = value.get_secret_value().strip()
#         if raw in cls.PLACEHOLDERS:                # ← use cls to reach class constant
#             raise ValueError(f"API key for {cls.__name__} is a placeholder")
#         return value
#
# What you cannot do is access self.other_field — the instance isn't built yet. For
# cross-field validation, you use @model_validator(mode="after"), which runs after the
# instance exists, so it gets self:
#
# from pydantic import model_validator

# class Provider(BaseModel):
#     provider: str
#     model: str
    
#     @model_validator(mode="after")
#     def _check_provider_model_match(self) -> "Provider":
          # Now self EXISTS — model is fully built
#         if self.provider == "anthropic" and not self.model.startswith("claude"):
#             raise ValueError(f"Anthropic model must start with 'claude', got {self.model}")
#         return self
#
# That contrast — cls for per-field (pre-construction), self for cross-field (post-construction) —
# is the cleanest way to remember the two validator types.