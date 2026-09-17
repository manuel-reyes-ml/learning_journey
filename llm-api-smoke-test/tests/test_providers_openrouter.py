"""Contract tests for the OpenRouter adapters, with the HTTP boundary faked.

Covers :class:`~llm_api_smoke_test.providers.OpenRouterProvider` (sync) and
:class:`~llm_api_smoke_test.providers.AsyncOpenRouterProvider` (async).  Both
speak to OpenRouter through the OpenAI SDK, so these tests pin the
*translation layer* — how an OpenAI-shaped ``chat.completion`` body becomes a
:class:`~llm_api_smoke_test.providers.SmokeTestResult` — without ever leaving
the process.

Every test asserts ``route.called``.  Under the bare ``@respx.mock`` decorator
a registered-but-never-called route is **not** an error, so without that line
a test where the HTTP call never happened would still pass green.  Route
firing also proves the client aimed at ``openrouter.ai`` rather than
``api.openai.com`` — the one thing an OpenAI-SDK-based adapter can get wrong
in a way no parsing assertion would catch.

Notes
-----
The OpenAI SDK appends ``/chat/completions`` to the client ``base_url``, so
:data:`_COMPLETIONS_URL` is the absolute URL respx must intercept.  Matching
the full URL rather than configuring a respx ``base_url`` keeps the assertion
self-documenting.

See Also
--------
tests.test_providers_anthropic : the same contract for the Anthropic path.
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
    AsyncLLMProvider,
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
_COMPLETIONS_URL: str = "https://openrouter.ai/api/v1/chat/completions"


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


@pytest.fixture
def openrouter_settings() -> ProviderSettings:
    """Frozen OpenRouter ProviderSettings with a fake (non-placeholder) key.

    Kept local to this module because it carries the "OpenRouter" identity
    and a provider/model slug — distinct from conftest's Anthropic-shaped
    ``provider_settings``.  Promote it to conftest only if a second module
    needs it.

    Returns
    -------
    ProviderSettings
        Validated settings; the key is fake but passes the placeholder
        validator, and no network call is made at construction time.
    """
    return ProviderSettings(
        name="OpenRouter",
        api_key=SecretStr("sk-or-test-fake-key-not-real"),
        model="deepseek/deepseek-v4-flash",
    )


# =============================================================================
# SYNC ADAPTER — OpenRouterProvider
# =============================================================================


class TestOpenRouterProviderSmokeTest:
    """Sync adapter parsing, with the httpx boundary faked by respx.

    ``@respx.mock`` (the bare decorator, global router) asserts that no
    unmocked request escapes to the network — but it does **not** assert that
    registered routes were called.  ``assert_all_called`` is disabled on the
    global router; it only defaults on for routers built by calling
    ``respx.mock(**kwargs)``.  Hence the explicit ``assert route.called`` in
    every test below: it is the only thing enforcing that the HTTP call
    actually happened.
    """

    # 1. The fake transport is now in place. Nothing can reach the internet
    # for the rest of this function.
    # 2. You register one rule. respx.post(url) creates the rule; .mock(return_value=...)
    # says what it answers with. Nothing has happened yet — you've only written it down.
    # 3. Building the provider doesn't touch the network, so nothing fires.
    # 4. This is the moment. The SDK builds a POST to
    # https://openrouter.ai/api/v1/chat/completions, hands it to the transport —
    # which is respx's fake — and respx checks its rules. The URL matches, so it hands
    # back your fake httpx.Response(200, ...) instead of making a connection.
    # Total elapsed: microseconds. No API key used, no money spent.
    #
    # The SDK then parses that fake response exactly as it would a real one.
    # Your adapter reads .content, .id, .usage off it and builds a SmokeTestResult.
    # Every line of your own code ran for real.
    #
    # 5. route.called is True because the rule got used.
    # Without that line, a test where the HTTP call never happened at all
    # would still go green.

    @respx.mock  # 1. swap the transport
    def test_happy_path_parses_response(
        self,
        openrouter_settings: ProviderSettings,
    ) -> None:
        """A well-formed body → a fully-populated SmokeTestResult."""
        # Register the fake endpoint; the SDK's POST will match it.
        route = respx.post(_COMPLETIONS_URL).mock(  # 2. write the sticky note
            return_value=httpx.Response(200, json=_chat_completion_payload())
        )

        # Constructing the client touches no network; the call below does
        # (and respx intercepts it).
        # 3. no network yet
        provider = OpenRouterProvider(openrouter_settings)  # type: ignore[arg-call]
        # 4. the call happens
        result = provider.smoke_test("say hello")

        # Route firing proves base_url → OpenRouter, not api.openai.com.
        assert route.called  # 5. check the sticky note
        assert isinstance(result, SmokeTestResult)

        # Field-by-field: the adapter reports its OWN settings for name/model
        # and pulls preview/id/usage off the deserialised SDK object.
        assert result.provider_name == "OpenRouter"
        assert result.model == "deepseek/deepseek-v4-flash"
        assert result.response_preview == "hello world"
        assert result.request_id == "gen-abc123"

        # Usage guard took the happy branch → a real TokenUsage.
        assert result.usage is not None
        assert result.usage.input_tokens == 7
        assert result.usage.output_tokens == 2

    @respx.mock
    def test_none_content_coalesces_to_empty_string(
        self,
        openrouter_settings: ProviderSettings,
    ) -> None:
        """``message.content`` is null → ``content or ""`` yields ``""``.

        Without the coalesce, ``None[:60]`` would raise ``TypeError`` —
        this pins the guard that prevents it.
        """
        route = respx.post(_COMPLETIONS_URL).mock(
            return_value=httpx.Response(200, json=_chat_completion_payload(content=None))
        )

        provider = OpenRouterProvider(openrouter_settings)  # type: ignore[arg-call]
        result = provider.smoke_test("say hello")

        assert route.called
        assert isinstance(result, SmokeTestResult)

        # The line under test: None becomes "", never reaches the slice as None.
        assert result.response_preview == ""

    @respx.mock
    def test_missing_usage_yields_none(
        self,
        openrouter_settings: ProviderSettings,
    ) -> None:
        """``usage`` is null → the ``is not None`` guard leaves usage as None.

        The distinction matters: a missing usage block must surface as
        ``None`` (unknown), NOT a zero-filled TokenUsage (which would lie
        about a genuine "0 tokens" call).
        """
        route = respx.post(_COMPLETIONS_URL).mock(
            return_value=httpx.Response(200, json=_chat_completion_payload(include_usage=False))
        )

        provider = OpenRouterProvider(openrouter_settings)  # type: ignore[arg-call]
        result = provider.smoke_test("say hello")

        assert route.called
        assert isinstance(result, SmokeTestResult)

        assert result.usage is None
        # The rest of the result is still well-formed — only usage is absent.
        assert result.response_preview == "hello world"


# =============================================================================
# ASYNC ADAPTER — AsyncOpenRouterProvider
# =============================================================================


class TestAsyncOpenRouterProviderSmokeTest:
    """Async adapter — identical parsing contract, awaited HTTP call.

    Relies on ``asyncio_mode = "auto"`` so each ``async def test_*`` runs
    in an event loop without a marker.  Deliberately NO module-level
    ``pytestmark = pytest.mark.asyncio`` — that would wrongly tag the sync
    tests above as asyncio.  respx intercepts the SDK's ``httpx.AsyncClient``
    exactly as it does the sync client.
    """

    @respx.mock
    async def test_happy_patch_parses_response(
        self,
        openrouter_settings: ProviderSettings,
    ) -> None:
        """Async happy path — same parsing as the sync adapter, awaited."""
        route = respx.post(_COMPLETIONS_URL).mock(
            return_value=httpx.Response(200, json=_chat_completion_payload())
        )

        provider = AsyncOpenRouterProvider(openrouter_settings)  # type: ignore[arg-call]

        # runtime_checkable must be implement in AsyncLLMProvider
        # so it can be used in isinstance().
        assert isinstance(provider, AsyncLLMProvider)
        result = await provider.smoke_test("say hello")

        assert route.called
        assert result.provider_name == "OpenRouter"
        assert result.response_preview == "hello world"
        assert result.request_id == "gen-abc123"
        assert result.usage is not None
        assert result.usage.input_tokens == 7
        assert result.usage.output_tokens == 2

    @respx.mock
    async def test_none_content_coalesces_to_empty_string(
        self,
        openrouter_settings: ProviderSettings,
    ) -> None:
        """Async — null content coalesces to ``""`` (same guard, async path)."""
        route = respx.post(_COMPLETIONS_URL).mock(
            return_value=httpx.Response(200, json=_chat_completion_payload(content=None))
        )

        provider = AsyncOpenRouterProvider(openrouter_settings)  # type: ignore[arg-call]

        assert isinstance(provider, AsyncLLMProvider)
        result = await provider.smoke_test("say hello")

        assert route.called
        assert isinstance(result, SmokeTestResult)

        # The line under test: None becomes "", never reaches the slice as None.
        assert result.response_preview == ""
