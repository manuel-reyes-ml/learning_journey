"""Typed configuration via pydantic-settings — Correction 16's named standard.

Install:  uv add pydantic-settings
"""

from __future__ import annotations

from pathlib import Path

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

PROJECT_ROOT = Path(__file__).resolve().parents[4]  # /learning_journey


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


# import this everywhere; construct once
settings = Settings()  # type: ignore[call-arg]

if __name__ == "__main__":
    print(settings)

# Usage in a client module:
#   from learning_journey.claude.settings import settings
#   client = anthropic.Anthropic(api_key=settings.anthropic_api_key.get_secret_value())
# .get_secret_value() is the ONLY way to read it — leaks require intent.
