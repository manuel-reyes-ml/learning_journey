# Test files must start with 'test_' so they are auto-discovery by pytest

"""
"""

from __future__ import annotations

from pathlib import Path

from speller.register import dicts  # triggers __ini__.py -> registration
from speller.protocols import DictionaryProtocol


# =============================================================================
# PROTOCOL SATISFACTION
# =============================================================================

# Test classes must start with capital T, colleted by class-name pattern
# Test functions/methods must start with 'test_', collected by function-name pattern

class TestProtocolSatisfaction:
    """Every registered backend satisfies DictionaryProtocol.
    This is the structural typing test — no inheritance needed.
    isinstance() works because DictionaryProtocol is @runtime_checkable.
    """
    
    def test_satisfies_protocol(self) -> None:
        """HashTableDictionary passes isinstance check for Protocol."""
        for _, dict_info in dicts.items():
            dictionary = dict_info.dict_class()
            assert isinstance(dictionary, DictionaryProtocol)
   
        
# =============================================================================
# LOADING
# =============================================================================    