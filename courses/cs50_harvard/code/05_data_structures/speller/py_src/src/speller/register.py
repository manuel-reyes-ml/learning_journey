"""
"""

# =============================================================================
# IMPORTS
# =============================================================================

from __future__ import annotations

from dataclasses import dataclass, KW_ONLY, field
import logging
from typing import Callable

from speller.protocols import DictionaryProtocol
from speller.speller import SpellerResult


# =============================================================================
# LOGGER SETUP
# =============================================================================

# __name__ resolves to 'speller.dictionary' - follows the package hierarchy.
# This logger is a CHILD of the 'speller' logger configured in logger.py.
# Log messages flow upward: speller.dictionary -> speller -> handlers.
# You never configure handlers here - that's logger.py / __main__.py's job.
logger = logging.getLogger(__name__)


# =============================================================================
# EXPORTS
# =============================================================================

__all__ = [
    "DictInfo",
    "dicts",
    "register_class",
]


# =============================================================================
# MODULE CONFIGURATION
# =============================================================================
# =====================================================
# Constants
# =====================================================

dicts: dict[str, DictInfo] = {}


# =====================================================
# Type Aliases
# =====================================================

type RegDecorator = Callable[[type[DictionaryProtocol]], type[DictionaryProtocol]]


# =====================================================
# Dict Metadata Configuration
# =====================================================

@dataclass
class DictInfo:
    """
    """
    # Required fields (no default) must come first
    # Optional fields with defaults afterwards
    _: KW_ONLY  # Everything after this is keyword-only
    dict_class: type[DictionaryProtocol]
    name: str
    description: str
    
    results: dict[str, SpellerResult] = field(default_factory=dict)


# =============================================================================
# DICTIONARY REGISTRY
# =============================================================================

# A decorator factory is just a function that takes custom parameters 
# and generates a decorator.
def register_class(name: str, description: str = "") -> RegDecorator:
    """
    """
    def decorator(dict_class: type[DictionaryProtocol]) -> type[DictionaryProtocol]:
        dicts[name] = DictInfo(
            dict_class=dict_class,
            name=dict_class.__name__,
            description=description or dict_class.__doc__ or "",
        )
        return dict_class # Return unchanged class
        # class goes in, class comes out. The class' __name__, __doc__, __qualname__
        # are all intact because you never created a replacement. Nothing to fix,
        # so @wraps would do nothing useful.
    return decorator

# Instantiate by key - calling a class creates an instance
# dictionary = dicts["hash"]() -> HashTableDictionary()