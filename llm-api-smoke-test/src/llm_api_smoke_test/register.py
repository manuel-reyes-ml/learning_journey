"""
"""

# =============================================================================
# IMPORTS
# =============================================================================

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field, KW_ONLY

from speller.register import DictInfo

from llm_api_smoke_test.providers import (
    AsyncLLMProvider,
    LLMProvider,
    SmokeTestResult,
)

# No ImportError sys.exit() on regular module so the
# error propagates to the caller (__main__.py).

# =============================================================================
# EXPORTS
# =============================================================================

__all__ = []


# =============================================================================
# MODULE CONFIGURATION
# =============================================================================
# =====================================================
# Type Aliases
# =====================================================

type RegDecorator = Callable[
    [type[LLMProvider | AsyncLLMProvider]],
    type[LLMProvider | AsyncLLMProvider],
]


# =====================================================
# Dict Metadata Configuration
# =====================================================

@dataclass(frozen=True)
class DicInfo:
    """
    """
    
    # Required fields (no default) must come first
    _:  KW_ONLY  # Everything after this is keyword-only
    provider_class: type[LLMProvider | AsyncLLMProvider]
    class_name: str
    
    # Optional fields with defaults afterwards
    results: dict[str, SmokeTestResult] = field(default_factory=dict)
    
# Tells pyright this is an INSTANCE
#   dict_class: DictionaryProtocol          # an object with .load(), .check()

# Tells pyright this is a CLASS
#   dict_class: type[DictionaryProtocol]    # a class you can call with ()

# type[X] means "the class itself, not an instance of it." Pyright knows
# dict_class() is valid because you're calling a class constructor, which
# returns an instance of DictionaryProtocol.


# =====================================================
# Constants
# =====================================================

dicts: dict[str, DictInfo] = {}


# =============================================================================
# DICTIONARY REGISTRY
# =============================================================================

