"""
"""

# =============================================================================
# IMPORTS
# =============================================================================

from __future__ import annotations

from dataclasses import dataclass, KW_ONLY, field
import logging
from speller.protocols import DictionaryProtocol
from speller.speller import SpellerResult
from typing import Callable


# No ImportError sys.exit() on regular module so the
# error propagates to the caller (__main__.py).


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

__all__ = []


# =============================================================================
# MODULE CONFIGURATION
# =============================================================================
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
    _: KW_ONLY  # Everything after this is keyword-only
    dict_class: type[DictionaryProtocol]
    name: str
    description: str
    # Optional fields with defaults afterwards
    results: dict[str, SpellerResult] = field(default_factory=dict)

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

dicts: dict[str, DictInfo] = {}  # now DictInfo is defined above


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
        return dict_class  # Return unchanged class
        # class goes in, class comes out. The class' __name__, __doc__, __qualname__
        # are all intact because you never created a replacement. Nothing to fix,
        # so @wraps would do nothing useful.
    return decorator

# Instantiate by key - calling a class creates an instance
# dictionary = dicts["hash"].dict_class() -> HashTableDictionary()