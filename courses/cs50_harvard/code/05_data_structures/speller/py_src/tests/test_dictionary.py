"""
"""

from __future__ import annotations

from pathlib import Path

from speller.dictionaries import HashTableDictionary
from speller.protocols import DictionaryProtocol


# =============================================================================
# PROTOCOL SATISFACTION
# =============================================================================

class TestProtocolSatisfaction:
    """Verify HashTableDictionary satisfies DictionaryProtocol.

    This is the structural typing test — no inheritance needed.
    isinstance() works because DictionaryProtocol is @runtime_checkable.
    """
    
    def test_satisfies_protocol(self) -> None:
        """HashTableDictionary passes isinstance check for Protocol."""
        dictionary = HashTableDictionary()
        assert isinstance(dictionary, DictionaryProtocol)
   
        
# =============================================================================
# LOADING
# =============================================================================    