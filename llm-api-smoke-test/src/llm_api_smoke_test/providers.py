"""Provider adapters for the API key smoke test.
 
Each provider is wrapped in an adapter that conforms to the ``LLMProvider``
Protocol. This is the same provider-agnostic abstraction pattern used in
DataVault and PolicyPulse — adding a third provider (e.g., OpenAI) later
requires only a new adapter, no changes to the runner.
 
Notes
-----
Adapters import their SDK lazily inside ``__init__`` rather than at module
scope. This keeps ``import llm_api_smoke_test.providers`` cheap during test
collection even when an SDK is not installed in the current environment.
"""

# =============================================================================
# IMPORTS
# =============================================================================

from __future__ import annotations
from typing_extensions import runtime

import httpx
import time

from dataclasses import dataclass
from pydantic import BaseModel
from typing import Protocol, runtime_checkable, TypeVar

from llm_api_smoke_test.config import ProviderSettings
from llm_api_smoke_test.register import register_class

# =============================================================================
# EXPORTS
# =============================================================================

__all__ = [
    "LLMProvider",
    "AnthropicProvider",
    "GeminiProvider",
    "OpenRouterProvider",
    "AsyncLLMProvider",
    "AsyncAnthropicProvider",
    "AsyncGeminiProvider",
    "AsyncOpenRouterProvider",
    "SmokeTestResult",
]


# =============================================================================
# MODULE CONFIGURATION
# =============================================================================
# =====================================================
# Constants
# =====================================================

# T is "any Pydantic model" — bound=BaseModel restricts T to BaseModel subclasses,
# which is what lets us call .model_json_schema() and .model_validate() on it.
T = TypeVar("T", bound=BaseModel)


# =============================================================================
# FROZEN DATACLASSES
# =============================================================================

@dataclass(frozen=True, slots=True)
class TokenUsage:
    """Token counts for a single LLM call — the basis of cost & rate-limit tracking."""
    
    input_tokens: int
    output_tokens: int
    
    @property  # call a class method like an attribute
    def total(self) -> int:
        """Convenience — most cost calcs need the sum."""
        return self.input_tokens + self.output_tokens
    

@dataclass(frozen=True, slots=True)
class SmokeTestResult:
    """Outcome of a single provider smoke test.
 
    Attributes
    ----------
    provider_name : str
        Display name of the provider that produced this result.
    model : str
        Model identifier used for the request.
    response_preview : str
        First N characters of the response, safe to log.
    """
    
    provider_name: str
    model: str
    response_preview: str
    request_id: str | None = None       # for log correlation / Anthropic support
    usage: TokenUsage | None = None     # input/output token counts
    latency_ms: float = 0.0             # wall-clock time of the call


# =============================================================================
# LLMProvider PROTOCOLS
# =============================================================================
# =====================================================
# SYNC LLMProvider
# =====================================================

@runtime_checkable  # Lets a Protocol class to be used in isinstance()
class LLMProvider(Protocol):
    """Provider Protocol — every adapter must implement ``smoke_test()``.
 
    The Protocol form (vs. an ABC) keeps this layer dependency-free; runners
    type-check against it without instantiating an inheritance chain.
    """
    
    def smoke_test(self, prompt: str) -> SmokeTestResult:
        """Send ``prompt`` to the provider and return a redacted result.
 
        Parameters
        ----------
        prompt : str
            The user message to send.
 
        Returns
        -------
        SmokeTestResult
            Provider name, model used, and a short response preview.
        """
        ...
    
    # The type[T] annotation (not T) is what lets you write
    # provider.generate_structured(prompt, SmokeTestReply) —
    # you're passing the class, not an instance, and the return
    # is typed as SmokeTestReply (instance).
    def generate_structured(self, prompt: str, schema: type[T]) -> T:
        """Generate output conforming to ``schema``, validated as that exact type.
        
        Parameters
        ----------
        prompt : str
            The user message.
        schema : type[T]
            A Pydantic ``BaseModel`` subclass. The returned object will be
            an instance of this class.
        
        Returns
        -------
        T
            A validated instance of ``schema``.
        
        Notes
        -----
        Design schemas with reasoning fields BEFORE answer fields — LLMs
        generate tokens left-to-right, so order in the schema shapes the
        model's thinking. See DataVault's QueryResponse for the pattern.
        """
        ...
        

# =====================================================
# ASYNC LLMProvider
# =====================================================

@runtime_checkable  # Lets a Protocol class to be used in isinstance()
class AsyncLLMProvider(Protocol):
    """Async variant of LLMProvider — for concurrent workloads.
    
    Methods have identical signatures to the sync versions but are coroutines.
    Used by DataVault's batch QueryEngine where many calls run concurrently
    via asyncio.gather().
    
    Notes
    -----
    The sync and async Protocols are deliberately separate. Mixing them on
    one Protocol breaks type checking because the return types differ
    (T vs. Awaitable[T]).
    """
    
    # `async def` here means the return type is implicitly Awaitable[SmokeTestResult] —
    # callers MUST await this. The Protocol checker verifies that implementations
    # use `async def` (not `def returning a coroutine manually`).
    async def smoke_test(self, prompt: str) -> SmokeTestResult:
        """Async variant of :meth:`LLMProvider.smoke_test`.

        Concrete implementations must use ``async def`` so the return
        type is implicitly ``Awaitable[SmokeTestResult]``.  Protocol
        body intentionally empty — the contract is the signature, not
        the body.
        """
        ...
        
    async def generate_structured(self, prompt: str, schema: type[T]) -> T:
        """Async variant of :meth:`LLMProvider.generate_structured`.

        Concrete implementations must use ``async def``.  Returns an
        instance of ``schema`` validated by Pydantic.
        """
        ...


# =============================================================================
# LLM PROVIDER IMPLEMENTATION
# =============================================================================

@register_class(
    "anthropic",
    "sync",
    "Anthropic's sync LLM provider class",
)
class AnthropicProvider:
    """Adapter for the Anthropic Claude SDK (``anthropic`` package).
 
    Parameters
    ----------
    settings : ProviderSettings
        Validated configuration including the API key and model name.
 
    Notes
    -----
    This adapter uses the synchronous ``Anthropic`` client because the
    smoke test runs sequentially. For production code (DataVault, AFC),
    swap to ``AsyncAnthropic`` to enable concurrent calls.
    """
    
    # Class-level constant — same pattern across all calls from this adapter.
    # In DataVault you'd inject this via ProviderSettings instead of hardcoding.
    _SYSTEM_PROMPT = "You are a terse assistant. Reply in one short sentence."
    
    def __init__(self, settings: ProviderSettings) -> None:
        """Construct the adapter and its synchronous Anthropic client.

        Parameters
        ----------
        settings : ProviderSettings
            Validated config — API key (unwrapped here via
            ``get_secret_value()``) and model identifier.

        Notes
        -----
        The ``anthropic`` SDK is imported lazily inside this method,
        not at module scope, so ``import providers`` stays cheap during
        test collection even when the SDK isn't installed.
        """
        from anthropic import Anthropic  # lazy import - keeps module import cheap
        
        self._settings = settings
        self._client = Anthropic(
            api_key=settings.api_key.get_secret_value(),
            max_retries=3,  # default is 2 - bump for flakier CI environments
            timeout=httpx.Timeout(60.0, read=30.0, write=10.0, connect=5.0),
        )
    
    # Instance method (the default) - gets 'self'  
    # Needs instance first -> a = AntropicProvider("") -> a.smoke_test()    
    def smoke_test(self, prompt: str) -> SmokeTestResult:
        """Send a single short prompt to Claude and return a preview.
 
        Parameters
        ----------
        prompt : str
            The user message.
 
        Returns
        -------
        SmokeTestResult
            Result containing a 60-character preview of the reply text.
 
        Raises
        ------
        anthropic.AnthropicError
            For any API-level failure (auth, rate-limit, billing).
        """
        from anthropic.types import TextBlock
        
        # perf_counter is the right clock for measuring elapsed time —
        # monotonic, high-resolution, immune to system clock changes.
        start = time.perf_counter()
        
        message = self._client.messages.create(
            model=self._settings.model,
            max_tokens=64,
            system=self._SYSTEM_PROMPT,
            messages=[{"role": "user", "content": prompt}],
        )
        
        latency_ms = (time.perf_counter() - start) * 1000.0
        
        # ``content`` is a union of many block types (TextBlock, ToolUseBlock,
        # CodeExecutionToolResultBlock, ...). For a plain prompt with no tools,
        # we expect TextBlock — narrow explicitly so pyright is happy and the
        # behavior is correct if the SDK ever returns a non-text block first.
        text = ""
        for block in message.content:
            if isinstance(block, TextBlock):
                text = block.text
                break
            
        return SmokeTestResult(
            provider_name=self._settings.name,
            model=self._settings.model,
            response_preview=text[:60],
            # Production observability - capture these on every call:
            # _request_id looks private but is documented as public. Use it to
            # correlate logs with Anthropic-side traces if you ever need support.
            request_id=message._request_id,
            usage=TokenUsage(
                input_tokens=message.usage.input_tokens,
                output_tokens=message.usage.output_tokens,
            ),
            latency_ms=latency_ms,
        )
        # Log them via your structlog set up
        
    def generate_structured(self, prompt: str, schema: type[T]) -> T:
        """Generate a response conforming to ``schema`` using the tool-use pattern."""
        from anthropic.types import MessageParam, ToolParam, ToolUseBlock
        from anthropic.types.message_create_params import ToolChoiceToolChoiceTool
        
        # Pydantic generates the JSON Schema for us — no double-maintenance of
        # schema definitions. This is the same schema Pydantic uses internally
        # for validation, so client and server see identical contracts.
        tool_name = "report"
        
        # Annotate request-param variables with the SDK's exported TypedDict
        # before passing them into the call.
        
        # Annotating the variable as list[ToolParam] makes pyright validate
        # the dict literal AS the TypedDict (checks keys, types of values)
        # instead of inferring a loose dict[str, Unknown].
        tools: list[ToolParam] = [{
            "name": tool_name,
            "description": f"Report the result as a structured {schema.__name__}.",
            "input_schema": schema.model_json_schema(),
        }]
        
        # Forced-tool choice — its own TypedDict
        tool_choice: ToolChoiceToolChoiceTool = {"type": "tool", "name": tool_name}
        
        # Messages — Iterable[MessageParam]
        messages: list[MessageParam] = [{"role": "user", "content": prompt}]
        
        message = self._client.messages.create(
            model=self._settings.model,
            max_tokens=1024,
            system=self._SYSTEM_PROMPT,
            tools=tools,
            # Force the model to call our tool — without this, it might respond
            # in free text. `tool_choice` with a specific name = "you MUST call this".
            tool_choice=tool_choice,
            messages=messages,
        )
        
        # Narrow the union to find the ToolUseBlock — same pattern as Block 4
        # but looking for a different block type.
        for block in message.content:
            if isinstance(block, ToolUseBlock):
                # block.input is a dict matching the schema. model_validate
                # is the canonical Pydantic V2 method for validating dicts;
                # it raises ValidationError on mismatch — defense in depth
                # in case the SDK's tool enforcement ever lets something slip.
                return schema.model_validate(block.input)
            
        # If we get here, the model returned text instead of calling the tool —
        # shouldn't happen with tool_choice forced, but explicit is better.
        raise RuntimeError(
            f"Anthropic did not call the {tool_name!r} tool - got blocks: "
            f"{[type(b).__name__ for b in message.content]}"
        )
        

@register_class(
    "gemini",
    "sync",
    "Gemini's sync LLM provider class",
)
class GeminiProvider:
    """Adapter for the Google Gen AI SDK (``google-genai`` package).
 
    Parameters
    ----------
    settings : ProviderSettings
        Validated configuration including the API key and model name.
 
    Notes
    -----
    Uses the new unified ``google-genai`` SDK (``from google import genai``),
    NOT the legacy ``google-generativeai`` package. The legacy package is
    deprecated as of Gemini 2.0 per Google's migration guide.
    """
    
    _SYSTEM_PROMPT = "You are a terse assistant. Reply in one short sentence."
    
    def __init__(self, settings: ProviderSettings) -> None:
        """Construct the adapter and its synchronous Gemini client.

        Parameters
        ----------
        settings : ProviderSettings
            Validated config — API key and model identifier.

        Notes
        -----
        Uses the unified ``google-genai`` SDK, imported lazily.  Note
        the timeout is in milliseconds (``30_000``), unlike Anthropic's
        seconds-based ``httpx.Timeout``.
        """
        from google import genai  # lazy import
        from google.genai.types import HttpOptions
        
        # Instance-level attributes
        self._settings = settings
        self._client = genai.Client(
            api_key=settings.api_key.get_secret_value(),
            # Gemini's SDK takes HTTP-level options through HttpOptions.
            # timeout is in MILLISECONDS here (different from Anthropic's seconds).
            # The SDK has its own retry handling — less configurable than
            # Anthropic's max_retries, but adequate for the same error classes.
            http_options=HttpOptions(timeout=30_000),
        )
    
    # Instance method (the default) - gets 'self'    
    def smoke_test(self, prompt: str) -> SmokeTestResult:
        """Send a single short prompt to Gemini and return a preview.
 
        Parameters
        ----------
        prompt : str
            The user message.
 
        Returns
        -------
        SmokeTestResult
            Result containing a 60-character preview of the reply text.
 
        Raises
        ------
        google.genai.errors.APIError
            For any API-level failure.
        """
        from google.genai.types import GenerateContentConfig
        
        start = time.perf_counter()
        
        response = self._client.models.generate_content(
            model=self._settings.model,
            contents=prompt,
            config=GenerateContentConfig(
                system_instruction=self._SYSTEM_PROMPT,  # parallel to Anthropic's system=
                max_output_tokens=64,  # parallel to Anthropic's max_tokens
            ),
        )
        
        latency_ms = (time.perf_counter() - start) * 1000.0
        
        text = response.text or ""
        
        # Gemini exposes usage on usage_metadata. Field names differ from
        # Anthropic — `prompt_token_count` vs `input_tokens`. The TokenUsage
        # dataclass normalizes them so downstream code is provider-agnostic.
        usage = None
        if response.usage_metadata is not None:
            usage = TokenUsage(
                input_tokens=response.usage_metadata.prompt_token_count or 0,
                output_tokens=response.usage_metadata.candidates_token_count or 0,
            )
            
        return SmokeTestResult(
            provider_name=self._settings.name,
            model=self._settings.model,
            response_preview=text[:60],
            request_id=None,            # Gemini doesn't expose this the same way — honest None.
            usage=usage,
            latency_ms=latency_ms,
        )
    
    def generate_structured(self, prompt: str, schema: type[T]) -> T:
        """Generate a response conforming to ``schema`` via Gemini's native JSON mode."""
        from google.genai.types import GenerateContentConfig
        
        response = self._client.models.generate_content(
            model=self._settings.model,
            contents=prompt,
            # No TypedDict-style annotation needed — GenerateContentConfig is a
            # Pydantic model, so pyright validates every kwarg at the constructor.
            # Mistyped field names or wrong value types fail at edit time.
            config=GenerateContentConfig(
                system_instruction=self._SYSTEM_PROMPT,
                # The two-line magic: tell Gemini to emit JSON, and give it the schema.
                # The SDK accepts a Pydantic class directly here — it calls
                # .model_json_schema() under the hood, same as we did manually
                # in the Anthropic version.
                response_mime_type="application/json",
                response_schema=schema,  # SDK calls model_json_schema() internally
            ),
        )
        
        # response.text contains JSON conforming to the schema.
        # model_validate_json parses + validates in one step.
        # (Gemini's SDK also exposes response.parsed, but going through
        # model_validate_json keeps both providers using identical Pydantic
        # validation paths — easier to reason about, easier to test.)
        return schema.model_validate_json(response.text or "{}")


@register_class(
    "anthropic",
    "async",
    "Anthropic's async LLM provider class",
)
class AsyncAnthropicProvider:
    """Asynchronous Anthropic (Claude) adapter — the ``AsyncLLMProvider`` variant.

    Awaitable twin of :class:`AnthropicProvider`.  Wraps
    ``anthropic.AsyncAnthropic`` so calls can be scheduled concurrently
    by :func:`~llm_api_smoke_test.batch_runner.batch_smoke_test` behind
    a semaphore + rate limiter.

    Parameters
    ----------
    settings : ProviderSettings
        Validated configuration including the API key and model name.

    Notes
    -----
    Same request and response shape as the sync adapter — the only
    behavioural difference is that ``smoke_test`` and
    ``generate_structured`` are coroutines that ``await`` the HTTP call,
    yielding control to the event loop while waiting on bytes.
    """
    
    _SYSTEM_PROMPT = "You are a terse assistant. Reply in one short sentence."
    
    def __init__(self, settings: ProviderSettings) -> None:
        """Construct the adapter and its asynchronous Anthropic client.

        Parameters
        ----------
        settings : ProviderSettings
            Validated config — API key and model identifier.

        Notes
        -----
        ``AsyncAnthropic`` is a distinct class from ``Anthropic`` —
        same constructor kwargs, but every method is a coroutine, and
        it uses ``httpx.AsyncClient`` internally.
        """
        # AsyncAnthropic is a separate class — same kwargs as Anthropic,
        # but every method on it is a coroutine. Internally it uses
        # httpx.AsyncClient instead of httpx.Client.
        from anthropic import AsyncAnthropic
        
        self._settings = settings
        self._client = AsyncAnthropic(
            api_key=settings.api_key.get_secret_value(),
            max_retries=3,
            timeout=httpx.Timeout(60.0, read=30.0, write=10.0, connect=5.0)
        )
        
    async def smoke_test(self, prompt: str) -> SmokeTestResult:
        """Async smoke test — same return shape as the sync version."""
        from anthropic.types import TextBlock
        
        start = time.perf_counter()
        
        # The ONLY behavioral change vs the sync version: `await`.
        # The HTTP request still happens — but Python yields control to
        # the event loop while waiting for bytes, letting other coroutines
        # run on the same thread.
        message = await self._client.messages.create(
            model=self._settings.model,
            max_tokens=64,
            system=self._SYSTEM_PROMPT,
            messages=[{"role": "user", "content": prompt}]
        )

        latency_ms = (time.perf_counter() - start) * 1000.0
        
        text = ""
        for block in message.content:
            if isinstance(block, TextBlock):
                text = block.text
                break
        
        return SmokeTestResult(
            provider_name=self._settings.name,
            model=self._settings.model,
            response_preview=text[:60],
            request_id=message._request_id,
            usage=TokenUsage(
                input_tokens=message.usage.input_tokens,
                output_tokens=message.usage.output_tokens,
            ),
            latency_ms=latency_ms,
        )

    async def generate_structured(self, prompt: str, schema: type[T]) -> T:
        """Async generate structured — same return shape as the sync version."""
        from anthropic.types import MessageParam, ToolParam, ToolUseBlock
        from anthropic.types.message_create_params import ToolChoiceToolChoiceTool
        
        tool_name = "report"
        tools: list[ToolParam] = [{
            "name": tool_name,
            "description": f"Report the result as a structured {schema.__name__}.",
            "input_schema": schema.model_json_schema(),
        }]
        tool_choice: ToolChoiceToolChoiceTool = {"type": "tool", "name": tool_name}
        messages: list[MessageParam] = [{"role": "user", "content": prompt}]
        
        message = await self._client.messages.create(
            model=self._settings.model,
            max_tokens=1024,
            system=self._SYSTEM_PROMPT,
            tools=tools,
            tool_choice=tool_choice,
            messages=messages,
        )
        
        for block in message.content:
            if isinstance(block, ToolUseBlock):
                return schema.model_validate(block.input)
            
        raise RuntimeError(
            f"Anthropic did not call the {tool_name!r} tool - got blcks: "
            f"{[type(b).__name__ for b in message.content]}"
        )
    

@register_class(
    "gemini",
    "async",
    "Gemini's async LLM provider class",
)
class AsyncGeminiProvider:
    """Asynchronous Google Gemini adapter — the ``AsyncLLMProvider`` variant.

    Awaitable twin of :class:`GeminiProvider`.  Reuses the same
    ``genai.Client`` class and reaches the async operations through its
    ``.aio`` accessor, so calls can be scheduled concurrently by
    :func:`~llm_api_smoke_test.batch_runner.batch_smoke_test`.

    Parameters
    ----------
    settings : ProviderSettings
        Validated configuration including the API key and model name.

    Notes
    -----
    Unlike Anthropic, Gemini has no separate async client class — the
    same ``genai.Client`` exposes sync methods on ``.models`` and async
    methods on ``.aio.models``.  ``request_id`` on the result is always
    ``None`` because the Gemini SDK does not surface a per-call ID.
    """
    
    _SYSTEM_PROMPT = "You are a terse assistant. Reply in one short sentence."
    
    def __init__(self, settings: ProviderSettings) -> None:
        """Construct the adapter and its Gemini client (async via ``.aio``).

        Parameters
        ----------
        settings : ProviderSettings
            Validated config — API key and model identifier.

        Notes
        -----
        Gemini uses the *same* ``genai.Client`` class for sync and
        async — the async methods live on the ``.aio`` accessor, so
        there is no separate ``AsyncClient`` to construct here.
        """
        from google import genai
        from google.genai.types import HttpOptions
        
        self._settings = settings
        # Same Client class as the sync version — no AsyncClient.
        # The async methods live on the .aio accessor.
        self._client = genai.Client(
            api_key=settings.api_key.get_secret_value(),
            http_options=HttpOptions(timeout=30_000),
        )
    
    async def smoke_test(self, prompt: str) -> SmokeTestResult:
        """Send a single short prompt to Gemini asynchronously.

        Awaits ``client.aio.models.generate_content`` — same kwargs and
        return shape as :meth:`GeminiProvider.smoke_test`, just
        non-blocking.

        Parameters
        ----------
        prompt : str
            The user message.

        Returns
        -------
        SmokeTestResult
            Preview, token usage, and latency.  ``request_id`` is
            ``None`` — the Gemini SDK exposes no per-call request ID.

        Raises
        ------
        google.genai.errors.APIError
            For any API-level failure.
        """
        from google.genai.types import GenerateContentConfig
        
        start = time.perf_counter()
        
        # The .aio namespace exposes async versions of every operation.
        # Same kwargs, same return shape — just awaitable.
        response = await self._client.aio.models.generate_content(
            model=self._settings.model,
            contents=prompt,
            config=GenerateContentConfig(
                system_instruction=self._SYSTEM_PROMPT,
                max_output_tokens=64,
            ),
        )
        
        latency_ms = (time.perf_counter() - start) * 1000.0
        text = response.text or ""
        
        usage = None
        if response.usage_metadata is not None:
            usage = TokenUsage(
                input_tokens=response.usage_metadata.prompt_token_count or 0,
                output_tokens=response.usage_metadata.candidates_token_count or 0,
            )
            
        return SmokeTestResult(
            provider_name=self._settings.name,
            model=self._settings.model,
            response_preview=text[:60],
            request_id=None,
            usage=usage,
            latency_ms=latency_ms,
        )
        
    async def generate_structured(self, prompt: str, schema: type[T]) -> T:
        """Asynchronously generate a response conforming to ``schema``.

        Uses Gemini's native JSON-output mode
        (``response_mime_type="application/json"`` +
        ``response_schema=schema``) and validates the returned JSON
        through Pydantic, so both providers share an identical
        validation path.

        Parameters
        ----------
        prompt : str
            The user message.
        schema : type[T]
            A Pydantic ``BaseModel`` subclass.  The returned object is
            an instance of this class.

        Returns
        -------
        T
            A validated instance of ``schema``.
        """
        from google.genai.types import GenerateContentConfig
        
        # Each call to generate_structured() will stop here and await until reponse 
        # from Anthropic is received, and give control to event loop (asyncio.gather()).
        response = await self._client.aio.models.generate_content(
            model=self._settings.model,
            contents=prompt,
            config=GenerateContentConfig(
                system_instruction=self._SYSTEM_PROMPT,
                response_mime_type="application/json",
                response_schema=schema,
            ),
        )
    
        return schema.model_validate_json(response.text or "{}")


@register_class(
    "openrouter",
    "sync",
    "OpenRouter (OpenAI-compatible) sync LLM provider class",
)
class OpenRouterProvider:
    """Synchronous OpenRouter adapter — the ``LLMProvider`` variant.

    OpenRouter exposes an OpenAI-compatible endpoint, so this adapter
    uses the ``openai`` SDK pointed at OpenRouter's base URL.  A single
    OpenRouter key reaches hundreds of models, selected via the
    ``provider/model-name`` slug in ``settings.model``.

    Parameters
    ----------
    settings : ProviderSettings
        Validated configuration — API key and model slug
        (e.g. ``"anthropic/claude-sonnet-4.5"``).

    Notes
    -----
    The ``base_url`` override is the only thing that distinguishes this
    from a plain OpenAI client.  Everything else — retries, typed
    responses, error classes — comes from the OpenAI SDK unchanged.
    """

    _SYSTEM_PROMPT: str = "You are a terse assistant. Reply in one short sentence."

    # OpenRouter's API base. The OpenAI SDK appends /chat/completions etc.
    _BASE_URL: str = "https://openrouter.ai/api/v1"

    def __init__(self, settings: ProviderSettings) -> None:
        """Construct the adapter and its OpenAI client pointed at OpenRouter.

        Parameters
        ----------
        settings : ProviderSettings
            Validated config — API key and model slug.

        Notes
        -----
        The ``openai`` SDK is imported lazily, keeping module import
        cheap during test collection.  ``base_url`` is the single line
        that turns an OpenAI client into an OpenRouter client.
        """
        from openai import OpenAI   # lazy import — keeps module import cheap

        self._settings = settings
        self._client = OpenAI(
            api_key=settings.api_key.get_secret_value(),
            base_url=self._BASE_URL,    # ← the OpenRouter redirect
            max_retries=3,              # same as our Anthropic adapter
            timeout=httpx.Timeout(60.0, read=30.0, write=10.0, connect=5.0),
        )

    def smoke_test(self, prompt: str) -> SmokeTestResult:
        """Send a single short prompt through OpenRouter and return a preview.

        Parameters
        ----------
        prompt : str
            The user message.

        Returns
        -------
        SmokeTestResult
            Preview, token usage, latency, and the OpenRouter request ID.

        Raises
        ------
        openai.OpenAIError
            For any API-level failure (auth, rate-limit, billing).
        """
        start = time.perf_counter()

        # OpenAI-compatible chat.completions call. The `model` is the
        # OpenRouter slug — "anthropic/claude-...", "openai/gpt-...", etc.
        completion = self._client.chat.completions.create(
            model=self._settings.model,
            max_tokens=64,
            messages=[
                {"role": "system", "content": self._SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
            # OpenRouter-specific optional headers for leaderboard analytics.
            # Harmless to include; remove if you don't want to appear there.
            extra_headers={
                "HTTP-Referer": "https://github.com/manuel-reyes-ml/learning_journey",
                "X-Title": "llm-api-smoke-test",
            },
        )

        latency_ms = (time.perf_counter() - start) * 1000.0

        # OpenRouter normalizes to the OpenAI schema: choices is ALWAYS
        # an array, even for a single completion. message.content may be
        # None for some finish reasons, so coalesce to "".
        text = completion.choices[0].message.content or ""

        # usage may be None on some providers; guard before reading.
        usage = None
        if completion.usage is not None:
            usage = TokenUsage(
                input_tokens=completion.usage.prompt_tokens,
                output_tokens=completion.usage.completion_tokens,
            )

        return SmokeTestResult(
            provider_name=self._settings.name,
            model=self._settings.model,
            response_preview=text[:60],
            request_id=completion.id,   # OpenRouter returns an id per call
            usage=usage,
            latency_ms=latency_ms,
        )

    def generate_structured(self, prompt: str, schema: type[T]) -> T:
        """Generate a response conforming to ``schema`` via JSON mode.

        Parameters
        ----------
        prompt : str
            The user message.
        schema : type[T]
            A Pydantic ``BaseModel`` subclass.

        Returns
        -------
        T
            A validated instance of ``schema``.

        Notes
        -----
        Uses OpenRouter's ``response_format`` with a JSON schema.  Not
        every underlying model supports structured output — check the
        model's capabilities on openrouter.ai/models before relying on
        this in production.
        """
        completion = self._client.chat.completions.create(
            model=self._settings.model,
            max_tokens=1024,
            messages=[
                {"role": "system", "content": self._SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
            response_format={
                "type": "json_schema",
                "json_schema": {
                    "name": schema.__name__,
                    "schema": schema.model_json_schema(),
                },
            },
        )

        text = completion.choices[0].message.content or "{}"
        return schema.model_validate_json(text)


@register_class(
    "openrouter",
    "async",
    "OpenRouter (OpenAI-compatible) async LLM provider class",
)
class AsyncOpenRouterProvider:
    """Asynchronous OpenRouter adapter — the ``AsyncLLMProvider`` variant.

    Awaitable twin of :class:`OpenRouterProvider`, built on
    ``openai.AsyncOpenAI`` pointed at OpenRouter's base URL so calls can
    be scheduled concurrently by
    :func:`~llm_api_smoke_test.batch_runner.batch_smoke_test`.

    Parameters
    ----------
    settings : ProviderSettings
        Validated configuration including the API key and model slug.

    Notes
    -----
    Same request and response shape as the sync adapter — the only
    behavioural difference is that the methods ``await`` the HTTP call.
    """

    _SYSTEM_PROMPT = "You are a terse assistant. Reply in one short sentence."
    _BASE_URL = "https://openrouter.ai/api/v1"

    def __init__(self, settings: ProviderSettings) -> None:
        """Construct the adapter and its async OpenAI client (→ OpenRouter)."""
        from openai import AsyncOpenAI

        self._settings = settings
        self._client = AsyncOpenAI(
            api_key=settings.api_key.get_secret_value(),
            base_url=self._BASE_URL,
            max_retries=3,
            timeout=httpx.Timeout(60.0, read=30.0, write=10.0, connect=5.0),
        )

    async def smoke_test(self, prompt: str) -> SmokeTestResult:
        """Async — same return shape as the sync version."""
        start = time.perf_counter()

        completion = await self._client.chat.completions.create(
            model=self._settings.model,
            max_tokens=64,
            messages=[
                {"role": "system", "content": self._SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
        )

        latency_ms = (time.perf_counter() - start) * 1000.0
        text = completion.choices[0].message.content or ""

        usage = None
        if completion.usage is not None:
            usage = TokenUsage(
                input_tokens=completion.usage.prompt_tokens,
                output_tokens=completion.usage.completion_tokens,
            )

        return SmokeTestResult(
            provider_name=self._settings.name,
            model=self._settings.model,
            response_preview=text[:60],
            request_id=completion.id,
            usage=usage,
            latency_ms=latency_ms,
        )

    async def generate_structured(self, prompt: str, schema: type[T]) -> T:
        """Async — same return shape as the sync version."""
        completion = await self._client.chat.completions.create(
            model=self._settings.model,
            max_tokens=1024,
            messages=[
                {"role": "system", "content": self._SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
            response_format={
                "type": "json_schema",
                "json_schema": {
                    "name": schema.__name__,
                    "schema": schema.model_json_schema(),
                },
            },
        )
        text = completion.choices[0].message.content or "{}"
        return schema.model_validate_json(text)


# class Provider:
#     default_model = "claude-opus-4-7"      # class-level attribute (shared by all instances)
    
#     def __init__(self, api_key):
#         self.api_key = api_key              # instance-level attribute
    
    # 1. Instance method (the default) — gets `self`
#     def show_key(self):
#         return f"Key: {self.api_key}"
    
    # 2. Class method — gets `cls`
#     @classmethod
#     def show_default_model(cls):
#         return f"Default model: {cls.default_model}"
    
    # 3. Static method — gets neither
#     @staticmethod
#     def is_valid_key_format(key):
#         return key.startswith("sk-")

# The bigger principle for your toolkit
# This is worth internalizing because the same divide shows up in every SDK ecosystem:
# TypedDict-based request params:
#   Anthropic, OpenAI, AWS Bedrock -- Annotate the variable: tools: list[ToolParam] = [{...}]
# Pydantic-based request params: 
#   Google google-genai, LangChain, Pydantic AI -- Just call the constructor — validation is automatic

# When DataVault eventually calls:
# pythonresults = await asyncio.gather(*[
#     provider.generate_structured(q, QueryResponse) for q in questions
# ])
# …here's what actually happens, in your code:
# 1. List comprehension builds 50 coroutine objects. Nothing runs yet.
# 2. gather schedules all 50 as Tasks. The event loop picks them up one by one.
# 3. Each Task runs from the top of generate_structured — builds the tools list,
# builds messages, hits await self._client.messages.create(...). Parks.
# 4. By the time the 50th Task has parked, all 50 HTTP requests are in flight to Anthropic.
# Your CPU usage: ~0%.
# 5. Responses come back from Anthropic's servers in some order — likely close to their issue
# order, with some jitter.
# 6. As each response arrives, the OS notifies the event loop, which resumes that specific Task.
# The Task runs the for block in message.content loop, returns the validated model.
# 7. When all 50 are done, gather returns the list of QueryResponse instances in input order.

# Wall time: ~the slowest single Anthropic response (~2s). Sequential time would've been ~100s.
# That's the 50× speedup async gives you for free on this workload.
#
# Summary
# Where does code stop?
#   At every await whose operation isn't ready yet.
# What happens during the pause?
#   The event loop runs other ready coroutines. If none, it waits on OS-level I/O readiness.
# Where does code resume?
#   The exact line after await, with local variables and call stack restored.
# What controls the switching?
#   Cooperative — only await yields. No preemption.
# How many threads?
#   One. Concurrency, not parallelism.
# What's the speedup mechanism?
#   Overlapping wait time, not overlapping computation.
# gather result order?
#   Input order, regardless of completion order.