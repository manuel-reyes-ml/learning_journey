"""
"""

# =============================================================================
# IMPORTS
# =============================================================================

from __future__ import annotations

import logging
import structlog

from collections.abc import Iterable
from typing import Final

from llm_api_smoke_test.providers import (
    LLMProvider,
    SmokeTestResult,
)

# =============================================================================
# EXPORTS
# =============================================================================

__all__ = []


# =============================================================================
# LOGGER SETUP
# =============================================================================

# Use structlog on Python's stdlib since some external packages
# use stdlib still.
slogger = structlog.stdlib.get_logger(__name__)
logger = logging.getLogger(__name__)


# =============================================================================
# MODULE CONFIGURATION
# =============================================================================
# =====================================================
# Constants
# =====================================================

# A minimal prompt — small enough to round-trip cheaply, complete enough to
# distinguish "API works" from "API returns garbage".
DEFAULT_PROMPT: Final[str] = "Reply with exactly the words: hello word"


# =============================================================================
# CORE FUNCTION
# =============================================================================

