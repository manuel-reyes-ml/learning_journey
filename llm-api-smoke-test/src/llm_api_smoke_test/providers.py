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