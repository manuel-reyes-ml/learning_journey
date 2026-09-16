""" """

# =============================================================================
# IMPORTS
# =============================================================================

from __future__ import annotations

import httpx
import respx

from llm_api_smoke_test.config import ProviderSettings
from llm_api_smoke_test.providers import AnthropicProvider, SmokeTestResult

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


class TestAnthropicProviderSmokeTest:
    """Sync adapter parsing, with the transport faked by respx.

    ``@respx.mock`` (the bare decorator, global router) asserts that no
    unmocked request escapes to the network — but it does **not** assert that
    registered routes were called.  ``assert_all_called`` is disabled on the
    global router; it only defaults on for routers built by calling
    ``respx.mock(**kwargs)``.  Hence the explicit ``assert route.called`` in
    every test below: it is the only thing enforcing that the HTTP call
    actually happened.
    """

    @respx.mock  # swap the transport for the duration of this function
    def test_happy_path_parses_response(
        self,
        provider_settings: ProviderSettings,
    ) -> None:
        """A well-formed body → a fully-populated SmokeTestResult."""
        # Register the rule. Nothing has happened yet — this only records
        # "if a POST to this URL shows up, answer with that".
        route = respx.post(_MESSAGES_URL).mock(return_value=_ok(_messages_payload()))

        # Constructing the client touches no network (the SDK's `Anthropic`
        # import is lazy, inside __init__); the call below is what fires.
        provider = AnthropicProvider(provider_settings)  # type: ignore[arg-call]
        result = provider.smoke_test("say hello")

        # Route firing proves the client aimed at api.anthropic.com AND that
        # respx patched the transport the SDK actually reached for.
        assert route.called
        assert isinstance(result, SmokeTestResult)

        # Identity fields come from OUR settings, never from the body — the
        # adapter reports what it was configured with.
        assert result.provider_name == "Anthropic"
        assert result.model == "claude-sonnet-4-6"

        # Payload fields come from the deserialised SDK object.
        assert result.response_preview == "hello world"

        # From the HEADER, not the body. This assertion is what catches a
        # mock that forgot `headers={"request-id": ...}`.
        assert result.request_id == _REQUEST_ID

        assert result.usage is not None
        assert result.usage.input_tokens == 7
        assert result.usage.output_tokens == 2

        # perf_counter is monotonic, so elapsed time can never be negative.
        # A loose bound on purpose — asserting a tight range would make this
        # test flaky on a loaded CI runner.
        assert result.latency_ms >= 0.0

    @respx.mock
    def test_long_text_is_truncated_to_sixty_chars(
        self,
        provider_settings: ProviderSettings,
    ) -> None:
        """``text[:60]`` caps the preview — a preview is not the full reply.

        Pins the slice in the adapter.  Without it a multi-kilobyte reply
        would be copied wholesale into logs and result objects.
        """
        long_text = "x" * 100
        route = respx.post(_MESSAGES_URL).mock(return_value=_ok(_messages_payload(text=long_text)))

        provider = AnthropicProvider(provider_settings)  # type: ignore[arg-call]
        result = provider.smoke_test("say hello")

        assert route.called
        assert isinstance(result, SmokeTestResult)
        # Both halves matter: the right LENGTH and the right CONTENT. Checking
        # only the length would pass for any 60 characters.
        assert len(result.response_preview) == 60
        assert result.response_preview == long_text[:60]

    @respx.mock
    def test_non_text_block_yields_empty_preview(
        self,
        provider_settings: ProviderSettings,
    ) -> None:
        """No ``TextBlock`` in ``content`` → the preview stays ``""``.

        The adapter loops over ``message.content`` and breaks on the first
        ``TextBlock``.  If a reply contains only tool-use blocks the loop
        finds nothing, and ``text`` must remain the empty-string default
        rather than raising or leaking ``None``.
        """
        route = respx.post(_MESSAGES_URL).mock(return_value=_ok(_messages_payload(text=None)))

        provider = AnthropicProvider(provider_settings)  # type: ignore[arg-call]
        result = provider.smoke_test("say hello")

        assert route.called
        assert isinstance(result, SmokeTestResult)

        assert result.response_preview == ""
        # The rest of the result is still well-formed — only the text is absent.
        assert result.usage is not None
        assert result.usage.input_tokens == 7


# =============================================================================
# ASYNC ADAPTER — AsyncAnthropicProvider
# =============================================================================
