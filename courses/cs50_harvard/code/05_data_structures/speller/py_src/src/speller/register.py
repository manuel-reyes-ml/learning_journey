"""
"""

# =============================================================================
# IMPORTS
# =============================================================================

from __future__ import annotations

from dataclasses import dataclass, KW_ONLY
import logging

from speller.protocols import DictionaryProtocol


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


@dataclass
class DictInfo:
    """
    """
    # Required fields (no default) must come first
    # Optional fields with defaults afterwards
    _: KW_ONLY  # Everything after this is keyword-only
    dict_class: DictionaryProtocol
    name: str
    description: str


# =============================================================================
# DICTIONARY REGISTRY
# =============================================================================

 