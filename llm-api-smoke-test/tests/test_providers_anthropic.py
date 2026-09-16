""" """

# =============================================================================
# IMPORTS
# =============================================================================

from __future__ import annotations

import httpx

# =============================================================================
# MODULE CONFIGURATION
# =============================================================================
# =====================================================
# Constants
# =====================================================

# The SDK appends "/v1/messages" to its default base_url. Matching the
# absolute URL (rather than a respx base_url) keeps the assertion
# self-documenting: if this route fires, the client really did aim at
# Anthropic and not somewhere else.
_MESSAGES_URL: str = "https://api.anthropic.com/v1/messages"

# The SDK lifts `message._request_id` off this response header. It is NOT in
# the JSON body — a common source of "why is request_id None?".
_REQUEST_ID: str = "req_011CQtest"

# No fixture is defined here on purpose. conftest's `provider_settings` is
# already Anthropic-shaped (name="Anthropic", model="claude-sonnet-4-6"), so
# this module consumes it rather than duplicating it.


# =============================================================================
# TEST HELPERS
# =============================================================================


def _messages_payload(
    *,
    text: str | None = "hello world",
    message_id: str = "msg_01Atest",
    input_tokens: int = 7,
    output_tokens: int = 2,
    model: str = "claude-sonnet-4-6",
) -> dict[str, object]:
    """Build a minimal Anthropic ``message`` body the SDK will deserialise.

    Only the fields the SDK requires — plus the ones the adapter reads — are
    included.  Keyword flags let each test bend a single dimension without
    rebuilding the whole dict.

    Parameters
    ----------
    text : str or None, optional
        Text for the single ``TextBlock``.  Pass ``None`` to emit a
        ``tool_use`` block instead, exercising the path where the adapter's
        ``isinstance(block, TextBlock)`` loop finds nothing.  Default
        ``"hello world"``.
    message_id : str, optional
        Body-level ``id``.  The adapter does **not** read this — it uses the
        ``request-id`` header — but a realistic body keeps the fixture honest.
    input_tokens, output_tokens : int, optional
        Values the adapter copies into
        :class:`~llm_api_smoke_test.providers.TokenUsage`.
    model : str, optional
        Echoed model slug; not asserted on (the adapter reports
        ``self._settings.model``, not the body's), but kept realistic.

    Returns
    -------
    dict of {str : object}
        A JSON-serialisable payload for ``httpx.Response(200, json=...)``.
    """
    # `content` is a LIST of typed blocks — this is the main structural
    # difference from the OpenAI shape, where the text hangs off
    # choices[0].message.content as a plain string.
    content: list[dict[str, object]]
    if text is None:
        # A tool_use block is a valid, fully-typed block that is NOT a
        # TextBlock — the cleanest way to exercise the "no text found" branch.
        content = [{"type": "tool_use", "id": "toolu_01test", "name": "noop", "input": {}}]
        stop_reason = "tool_use"
    else:
        content = [{"type": "text", "text": text}]
        stop_reason = "end_turn"

    return {
        "id": message_id,
        "type": "message",
        "model": model,
        "content": content,
        "stop_reason": stop_reason,
        "stop_sequence": None,
        # Non-optional in the Messages API, unlike OpenRouter's `usage`.
        "usage": {"input_tokens": input_tokens, "output_tokens": output_tokens},
    }


def _ok(payload: dict[str, object]) -> httpx.Response:
    """Wrap a payload in a 200 response carrying the ``request-id`` header.

    Parameters
    ----------5
    payload : dict of {str : object}
        Body produced by :func:`_messages_payload`.

    Returns
    -------
    httpx.Response
        Canned response for ``route.mock(return_value=...)``.  Note this is
        ``httpx2.Response`` at runtime — ``tests/_alias_httpx.py`` aliases the
        name, so this module needs no edit to follow the SDK's transport.
    """
    return httpx.Response(200, json=payload, headers={"request-id": _REQUEST_ID})


# =============================================================================
# TRANSPORT GUARD
# =============================================================================


def test_httpx_is_aliased_to_httpx2() -> None:
    """The alias plugin ran, so respx and the SDK patch the same library.

    A canary, not a behaviour test.  If ``tests/_alias_httpx.py`` stops being
    loaded, every mocked test below would silently start hitting the network;
    this fails first and names the cause.
    """
    import httpx2

    # Same object, not merely a compatible one — proof the alias took effect.
    assert httpx.Client is httpx2.Client


# =============================================================================
# SYNC ADAPTER — AnthropicProvider
# =============================================================================
