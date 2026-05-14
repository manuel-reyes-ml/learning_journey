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

import httpx
import time

from dataclasses import dataclass
from pydantic import BaseModel
from typing import Protocol, TypeVar

from llm_api_smoke_test.config import ProviderSettings

# =============================================================================
# EXPORTS
# =============================================================================

__all__ = [
    "LLMProvider",
    "AnthropicProvider",
    "GeminiProvider",
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
# LLMProvider PROTOCOL
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
        

# =============================================================================
# LLM PROVIDER IMPLEMENTATION
# =============================================================================

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
    _SYSTEM_PROMPT = "You are terse assistant. Reply in one short sentence."
    
    def __init__(self, settings: ProviderSettings) -> None:
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
    
    _SYSTEM_PROMPT = "You are terse assistant. Reply in one short sentence."
    
    def __init__(self, settings: ProviderSettings) -> None:
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
            config=GenerateContentConfig(
                system_instruction=self._SYSTEM_PROMPT,
                # The two-line magic: tell Gemini to emit JSON, and give it the schema.
                # The SDK accepts a Pydantic class directly here — it calls
                # .model_json_schema() under the hood, same as we did manually
                # in the Anthropic version.
                response_mime_type="application/json",
                response_schema=schema,
            ),
        )
        
        # response.text contains JSON conforming to the schema.
        # model_validate_json parses + validates in one step.
        # (Gemini's SDK also exposes response.parsed, but going through
        # model_validate_json keeps both providers using identical Pydantic
        # validation paths — easier to reason about, easier to test.)
        return schema.model_validate_json(response.text or "{}")

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