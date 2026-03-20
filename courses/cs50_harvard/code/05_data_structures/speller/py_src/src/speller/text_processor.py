"""
"""

# =============================================================================
# IMPORTS
# =============================================================================

from __future__ import annotations

# Runtime collection types → collections.abc
from collections.abc import Iterator
from pathlib import Path
import logging

from speller.config import MAX_WORD_LENGTH

# No ImportError sys.exit() on regular module so the
# error propagates to the caller (__main__.py).

## Simple Decision Rule
# "Is it a CONTAINER or CALLABLE type?"
#     YES → from collections.abc  (Generator, Iterator, Callable, Sequence, Mapping)

# "Is it a TYPE SYSTEM concept?"
#     YES → from typing  (Protocol, TypeVar, ParamSpec, Any, Final, TypedDict)


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
# INTERNAL HELPER FUNCTIONS
# =============================================================================

def _consume_alpha(content: str, pos: int, length: int) -> int:
    """
    """
    while pos < length and content[pos].isalpha():
        pos += 1
        
    # Skip the terminating non-alpha character (matches C's fread
    # consumption: the inner loop reads the terminator, then the
    # outer loop's fread reads the NEXT char, so the terminator 
    # is effectively consumed/lost).
    if pos < length:
        pos += 1
    
    return pos


def _consume_alnum(content: str, pos: int, length: int) -> int:
    """
    """
    while pos < length and content[pos].isalnum():
        pos += 1
    
    if pos < length:
        pos += 1
        
    return pos


# =============================================================================
# CORE FUNCTIONS
# =============================================================================