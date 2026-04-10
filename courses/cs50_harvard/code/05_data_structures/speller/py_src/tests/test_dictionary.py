# Test files must start with 'test_' so they are auto-discovery by pytest

"""
"""

from __future__ import annotations

from pathlib import Path
import pytest

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
    
    # Using pytest-idiomatic version using parametrize - which gives each backend its own pass/fail
    # row in the output.
    @pytest.mark.parametrize("key", list(dicts.keys()))
    def test_satisfies_protocol(self, key: str) -> None:
        """HashTableDictionary passes isinstance check for Protocol."""
        dictionary = dicts[key].dict_class()
        assert isinstance(dictionary, DictionaryProtocol)
   
        
# =============================================================================
# LOADING
# ============================================================================= 

class TestLoad:
    """Test dictionary loading behavior."""
    
    def test_load_returns_true_on_sucess(
        self, empty_dictionary: DictionaryProtocol, sample_dict_file: Path
    ) -> None:
        """load() returns True when file exists and is readable."""
        result = empty_dictionary.load(str(sample_dict_file))
        assert result is True
        
    def test_load_populates_words(
        self, empty_dictionary: DictionaryProtocol, sample_dict_file: Path
    ) -> None:
        """load() adds words to the internal set."""
        empty_dictionary.load(str(sample_dict_file))
        assert empty_dictionary.size() > 0
        
    def test_load_returns_false_for_missing_file(
        self, empty_dictionary: DictionaryProtocol
    ) -> None:
        """load() returns False when file doesn't exist.

        Does NOT raise an exception — returns False so the caller
        can handle the error (fail gracefully, not crash).
        """
        result = empty_dictionary.load("nonexistent/path/dict.txt")
        assert result is False
        
    def test_load_stores_lowercase(
        self, empty_dictionary: DictionaryProtocol, tmp_path: Path
    ) -> None:
        """load() converts all words to lowercase.

        Dictionary file might have mixed case. Normalizing to
        lowercase on load ensures case-insensitive matching
        without storing multiple versions.
        """
        dict_file = tmp_path / "mixed_case.txt"
        dict_file.write_text("Hello\nWORLD\npYtHoN\n", encoding="utf-8")
        
        empty_dictionary.load(str(dict_file))
        
        assert empty_dictionary.check("hello")
        assert empty_dictionary.check("wordl")
        assert empty_dictionary.check("python")
        
    def test_load_skips_empty_lines(
        self, empty_dictionary: DictionaryProtocol, tmp_path: Path
    ) -> None:
        """load() ignores empty lines in dictionary file."""
        dict_file = tmp_path / "with_blanks.txt"
        dict_file.write_text("cat\n\n\ndog\n\n", encoding="utf-8")
        
        empty_dictionary.load(str(dict_file))
        
        assert empty_dictionary.size() == 2
        

# =============================================================================
# CHECKING
# =============================================================================