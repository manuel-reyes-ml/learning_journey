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