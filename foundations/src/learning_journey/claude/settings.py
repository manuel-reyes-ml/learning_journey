"""Typed configuration via pydantic-settings — Correction 16's named standard.

Install:  uv add pydantic-settings
"""

from __future__ import annotations

from functools import cache
from pathlib import Path
from typing import Final

from pydantic import SecretStr, ValidationError, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

__all__ = [
    "ConfigError",
    "Settings",
    "get_settings",
]

PROJECT_ROOT: Final[Path] = Path(__file__).resolve().parents[4]  # /learning_journey


class ConfigError(RuntimeError):
    """Raised when required configuration is missing or invalid."""


class Settings(BaseSettings):
    """Single config entrypoint. Reads environment variables by field name.

    Why this beats os.environ.get():
    1. FAIL FAST: no default on anthropic_api_key → missing key crashes at
       STARTUP with a clear error, not at 2am mid-pipeline (Correction 16's
       exact phrase).
    2. SecretStr: repr() and any debug print shows '**********', so the key
       cannot leak through a traceback, a log line, or a config dump.
    3. Typed: model gets a str, max_tokens gets an int — typos in .env
       become validation errors, not silent weirdness.
    """

    model_config = SettingsConfigDict(
        env_file=PROJECT_ROOT / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
        frozen=True,
    )

    anthropic_api_key: SecretStr  # <- no default = REQUIRED
    claude_model: str = "claude-haiku-4-5"
    default_max_tokens: int = 500
    system_prompt: str = (
        "You are chatting in a terminal. Reply conversationally in short plain-text "
        "paragraphs, like a text message. No headings, bullet lists, bold, or tables "
        "unless the user asks for them."
    )

    @field_validator("anthropic_api_key")
    @classmethod
    def not_blank(cls, v: SecretStr) -> SecretStr:
        if not v.get_secret_value().strip():
            raise ValueError("must not be empty")
        return v


# @cache = @lru_cache(maxsize=None)
# Both come from functools and do memoization: the first call with some arguments runs the
# function and stores the result, keyed by those arguments. Later calls with the same
# arguments return the stored result without running the function again.
#
# Prefer @cache on Python ≥ 3.9, and use lru_cache(maxsize=N) when arguments vary and
# memory must be bounded.
@cache
def get_settings() -> Settings:
    try:
        return Settings()  # type: ignore[call-arg]
    except ValidationError as e:
        fields = sorted({str(err["loc"][0]).upper() for err in e.errors()})
        # Pydantic errors can include the raw input value. With from None and only field
        # names in the message, a secret can never end up in your logs.
        raise ConfigError(
            f"Missing/invalid config: {', '.join(fields)}. "
            f"Set them in the environment or in {PROJECT_ROOT / '.env'}"
        ) from None


# Usage in a client module:
#   from learning_journey.claude.settings import Settings
#   settings = Settings()
#   client = anthropic.Anthropic(api_key=settings.anthropic_api_key.get_secret_value())
# .get_secret_value() is the ONLY way to read it — leaks require intent.
