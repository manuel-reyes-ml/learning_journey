"""
"""

# =============================================================================
# IMPORTS
# =============================================================================

from __future__ import annotations

import httpx
import pytest
import respx

from pydantic import SecretStr

from llm_api_smoke_test.config import ProviderSettings

# __all__ only governs `from ... import *`; an
# explicit import like this works regardless because the names exist at
# module scope.  (Adding them to __all__ is a one-line polish item.)
from llm_api_smoke_test.providers import (
    AsyncOpenRouterProvider,
    OpenRouterProvider,
    SmokeTestResult,
)

# =============================================================================
# MODULE CONFIGURATION
# =============================================================================
# =====================================================
# Constants
# =====================================================
 
# The OpenAI SDK appends "/chat/completions" to the client base_url.
# OpenRouterProvider sets base_url="https://openrouter.ai/api/v1", so the
# full URL respx must intercept is this.  Matching the absolute URL (rather
# than a respx base_url) keeps the assertion self-documenting.
_COMPLETION_URL: str = "https://openrouter.ai/api/v1/chat/completions"


# =============================================================================
# TEST HELPERS
# =============================================================================

def _chat_completion_payload(
    *,
    content: str | None = "hello world",
    include_usage: bool = True,
    response_id: str = "gen-abc123",
    model: str = "deepseek/deepseek-v4-flash",
) -> dict[str, object]:
    """Build a minimal OpenAI-/OpenRouter-shaped ``chat.completion`` body.
 
    Only the fields the SDK requires to deserialise — plus the ones our
    adapter reads — are included.  Keyword flags let each test bend a
    single dimension (null content, missing usage) without rebuilding the
    whole dict.
 
    Parameters
    ----------
    content : str or None, optional
        The assistant message text.  Pass ``None`` to simulate a body
        where ``message.content`` is null (exercises the ``or ""``
        coalesce).  Default ``"hello world"``.
    include_usage : bool, optional
        ``True`` embeds a ``usage`` block; ``False`` sets ``usage`` to
        ``null`` to exercise the ``if completion.usage is not None`` guard.
        Default ``True``.
    response_id : str, optional
        The body-level ``id`` our adapter maps to ``result.request_id``.
    model : str, optional
        Echoed model slug; not asserted on (the adapter reports
        ``self._settings.model``, not the body's), but kept realistic.
 
    Returns
    -------
    dict of {str : object}
        A JSON-serialisable payload for ``httpx.Response(200, json=...)``.
    """
    payload: dict[str, object] = {
        "id": response_id,
        "object": "chat.completion",
        "created": 1_700_000_000,
        "model": model,
        "choices": [
            {
                "index": 0,
                "finish_reason": "stop",
                # content may be a string OR null — the SDK types it as
                # Optional[str], so both deserialise cleanly.
                "message": {"role": "assistant", "content": content},
            }
        ],
    }

    if include_usage:
        payload["usage"] = {
            "prompt_tokens": 7,
            "completion_tokens": 2,
            "total_tokens": 9,
        }
    else:
        # Explicit null (not just omission) makes the intent obvious:
        # "the API returned usage: null" — some OpenRouter-routed models do.
        payload["usage"] = None

    return payload


# =============================================================================
# FIXTURES
# =============================================================================

