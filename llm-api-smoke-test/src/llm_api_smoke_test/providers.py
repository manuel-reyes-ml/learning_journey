"""
"""

# =============================================================================
# IMPORTS
# =============================================================================

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from llm_api_smoke_test.config import ProviderSettings

# =============================================================================
# EXPORTS
# =============================================================================

__all__ = []


# =============================================================================
# LLMProvider PROTOCOL
# =============================================================================

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
    
    def __init__(self, settings: ProviderSettings) -> None:
        from anthropic import Anthropic  # lazy import - see module docstring
        
        self._settings = settings
        self._client = Anthropic(api_key=settings.api_key.get_secret_value())
        
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
        
        message = self._client.messages.create(
            model=self._settings.model,
            max_tokens=64,
            messages=[{"role": "user", "content": prompt}],
        )
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
    
    def __init__(self, settings: ProviderSettings) -> None:
        from google import genai  # lazy import
        
        self._settings = settings
        self._client = genai.Client(api_key=settings.api_key.get_secret_value())
        
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
        response = self._client.models.generate_content(
            model=self._settings.model,
            contents=prompt,
        )
        text = response.text or ""
        return SmokeTestResult(
            provider_name=self._settings.name,
            model=self._settings.model,
            response_preview=text[:60],
        )