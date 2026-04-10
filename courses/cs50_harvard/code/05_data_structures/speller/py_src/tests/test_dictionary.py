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

class TestCheck:
    """Test word checking behavior."""
    
    def test_check_finds_existing_word(
        self, loaded_dictionary: DictionaryProtocol
    ) -> None:
        """check() returns True for a word in the dictionary."""
        assert loaded_dictionary.check("cat") is True
        
    def test_check_is_case_insensitive(
        self, loaded_dictionary: DictionaryProtocol
    ) -> None:
        """check() matches regardless of case.

        "Cat", "CAT", and "cat" should all match a dictionary
        entry of "cat".
        """
        assert loaded_dictionary.check("cat") is True
        assert loaded_dictionary.check("Cat") is True
        assert loaded_dictionary.check("CAT") is True
        
    def test_check_rejects_missing_word(
        self, loaded_dictionary: DictionaryProtocol
    ) -> None:
        """check() returns False for a word NOT in the dictionary."""
        assert loaded_dictionary.check("xyz") is False
        
    def test_check_raises_if_not_loaded(
        self, empty_dictionary: DictionaryProtocol
    ) -> None:
        """check() raises RuntimeError if dictionary not loaded.

        This is the "fail fast" guard — prevents silent bugs where
        an unloaded dictionary reports every word as misspelled.

        pytest.raises() with match= verifies both the exception
        TYPE and the error MESSAGE.
        """
        # match= checks that the exception's error message contains a specific
        # pattern, not just that the right exception type was raised.
        #
        # This only passes if a RunTime is raised and its message
        # contains "not loaded".If the wrong RunTime fires, the test fails.
        with pytest.raises(RuntimeError, match="not loaded"):
            empty_dictionary.check("hello")
            
    @pytest.mark.parametrize(
        "word, expected",
        [
            ("the", True),      # common word
            ("cat", True),      # in test dictionary
            ("xyz", False),     # not in dictionary
            ("THE", True),      # uppercase version
            ("", False),        # empty string
        ],
        # --- HOW @pytest.mark.parametrize WORKS ---
        #
        # Instead of writing 5 separate test functions that do the
        # same thing with different inputs, parametrize runs the SAME
        # test function multiple times with different arguments.
        #
        # pytest output shows each case separately:
        #   test_check_parametrized[the-True]     PASSED
        #   test_check_parametrized[cat-True]      PASSED
        #   test_check_parametrized[xyz-False]     PASSED
        #   test_check_parametrized[THE-True]      PASSED
        #   test_check_parametrized[-False]        PASSED
        #
        # The string after [brackets] is auto-generated from the args.
        #
        # Format:
        #   @pytest.mark.parametrize("param_names", [list_of_tuples])
        #   def test_something(self, param_names, ...):
        #
        # Each tuple in the list becomes one test invocation.
        # The tuple values are unpacked into the parameter names.
    )
    def test_check_parametrized(
        self,
        loaded_dictionary: DictionaryProtocol,
        word: str,
        expected: bool,
    ) -> None:
        """check() returns correct result for various inputs.

        Uses @pytest.mark.parametrize to test multiple word/expected
        pairs with a single test function. DRY — one assertion logic,
        many data points.
        """
        assert loaded_dictionary.check(word) is expected
        

# =============================================================================
# SIZE AND DUNDERS
# =============================================================================