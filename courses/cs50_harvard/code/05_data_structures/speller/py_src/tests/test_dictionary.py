# Test files must start with 'test_' so they are auto-discovery by pytest
"""Tests for speller.dictionaries module.

Tests the HashTableDictionary class: loading, checking, size, dunders,
and error handling. Uses fixtures from conftest.py for file paths
and pre-loaded dictionary instances.

Pytest Patterns Introduced
--------------------------
- @pytest.mark.parametrize — run same test with multiple inputs
- Fixture chaining (loaded_dictionary depends on sample_dict_file)
- Testing Protocol satisfaction with isinstance()
- Negative testing (RuntimeError, missing files)
- Testing dunder methods (__len__, __contains__, __repr__)
"""

from __future__ import annotations

from pathlib import Path
import pytest

from speller.register import dicts  # triggers __ini__.py -> registration
from speller.protocols import DictionaryProtocol


# =============================================================================
# OVERRIDE confest.py fixtures (for this file only)
# =============================================================================

# When the thing that varies is the object under test (the dictionary backend), parametrize
# the fixture that produces it. Every test that uses that fixture automatically runs once
# per backend — zero changes to the test methods themselves.
@pytest.fixture(params=list(dicts.keys()))
def empty_dictionary(request: pytest.FixtureRequest) -> DictionaryProtocol:
        #                 ↑
        # pytest sees this parameter name "request" and injects
        # its own FixtureRequest object automatically — same way
        # it injects tmp_path or capsys by name
    """Unloaded instance of every registered backend.

    params=list(dicts.keys()) makes pytest run every test that uses
    this fixture once per registered backend key ("hash", "list",
    "sorted", "dict"). request.param holds the current key.

    This locally overrides the conftest.py fixture of the same name
    for this file only — conftest remains unchanged.
    """
    return dicts[request.param].dict_class()
    #                ↑
    # First run:  request.param == "hash"   → HashTableDictionary()
    # Second run: request.param == "list"   → ListDictionary()
    # Third run:  request.param == "sorted" → SortedListDictionary()
    # Fourth run: request.param == "dict"   → DictDictionary()

@pytest.fixture(params=list(dicts.keys()))
def loaded_dictionary(
    request: pytest.FixtureRequest,  # type annotation for the built-in request object that pytest injects
    sample_dict_file: Path,
) -> DictionaryProtocol:
    """Loaded instance of every registered backend."""
    d = dicts[request.param].dict_class()
    d.load(str(sample_dict_file))
    return d
    
    
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
        assert empty_dictionary.check("world")
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

class TestSizeAndDunders:
    """Test size(), __len__, __contains__, and __repr__."""
    
    def test_size_empty(
        self, empty_dictionary: DictionaryProtocol
    ) -> None:
        """size() returns 0 for unloaded dictionary."""
        assert empty_dictionary.size() == 0
        
    def test_size_after_load(
        self, loaded_dictionary: DictionaryProtocol
    ) -> None:
        """size() returns correct count after loading."""
        assert loaded_dictionary.size() > 0
        
    def test_len_matches_size(
        self, loaded_dictionary: DictionaryProtocol
    ) -> None:
        """len(dictionary) returns same value as dictionary.size().

        __len__ delegates to size() — DRY principle.
        """
        assert len(loaded_dictionary) == loaded_dictionary.size()
        
    def test_contains_existing_word(
        self, loaded_dictionary: DictionaryProtocol
    ) -> None:
        """'word in dictionary' returns True for existing words.

        Tests the Pythonic __contains__ syntax.
        """
        assert "cat" in loaded_dictionary
        
    def test_contains_missing_word(
        self, loaded_dictionary: DictionaryProtocol
    ) -> None:
        """'word in dictionary' returns False for missing words."""
        assert "xyz" not in loaded_dictionary
        
    def test_repr_format(
        self, loaded_dictionary: DictionaryProtocol
    ) -> None:
        """__repr__ includes class name, loaded status, and word count."""
        r = repr(loaded_dictionary)
        
        # type(class_instance).__name__ gets the class name "HashTableDictionary"
        assert type(loaded_dictionary).__name__ in r
        assert "loaded=True" in r
        
    def test_unload_clears_dictionary(
        self, loaded_dictionary: DictionaryProtocol
    ) -> None:
        """unload() resets the dictionary to empty state."""
        assert loaded_dictionary.size() > 0
        
        loaded_dictionary.unload()
        
        assert loaded_dictionary.size() == 0
        with pytest.raises(RuntimeError):
            loaded_dictionary.check("cat")
            
            
# =============================================================================
# INTEGRATION WITH REAL DICTIONARY
# =============================================================================

class TestWithLargeDictionary:
    """Integration tests using the real CS50 large dictionary.

    These tests are slower (loading 143K words) so they're marked
    with @pytest.mark.integration. Run them explicitly:
        pytest -m integration

    Or exclude them for fast feedback:
        pytest -m "not integration"

    The markers are registered in pyproject.toml [tool.pytest.ini_options].
    """
    
    # pytest.mark.integration -> It's a custom marker that lets us filter tests at the
    # CLI level without changing any code.
    @pytest.mark.integration
    def test_large_dict_word_count(
        self, 
        empty_dictionary: DictionaryProtocol,
        large_dict_path: Path,
    ) -> None:
        """Large dictionary contains exactly 143,091 words."""
        empty_dictionary.load(str(large_dict_path))
        assert empty_dictionary.size() == 143_091
        
    @pytest.mark.integration
    @pytest.mark.parametrize(
        "word, expected",
        [
            ("hello", True),
            ("python", True),
            ("Bingley", False),     # proper noun - not in dictionary
            ("xyz", False),
            ("pneumonoultramicroscopicsilicovolcanoconiosis", True),    # longest word
        ],
    )
    def test_large_dict_check(
        self,
        empty_dictionary: DictionaryProtocol,
        large_dict_path: Path,
        word: str,
        expected: bool,
    ) -> None:
        """Spot-check words against the real dictionary."""
        empty_dictionary.load(str(large_dict_path))
        assert empty_dictionary.check(word) is expected



# =============================================================================
# REFERENCE GUIDES
# =============================================================================
# =====================================================
# Pytest 'request' Object
# ===================================================== 

# pytest.FixtureRequest is the type annotation for the built-in request object that pytest
# automatically injects into any fixture. It gives the fixture metadata about its own
# execution context.

# What request provides
#   pythonrequest.param        # the current parameter value when fixture uses params=
#   request.fixturename        # the name of the fixture being executed
#   request.node               # the test item currently being collected
#   request.scope              # "function", "class", "module", or "session" 

# request is just a built-in fixture
# It works exactly like tmp_path or capsys — pytest recognizes the parameter name request and
# injects the object automatically. The pytest.FixtureRequest type annotation is only there to
# make pyright aware of what .param and .node are. Without it, pyright would type request as
# Any and lose all static coverage.

# You only need request when using params=
# A fixture without params= never needs request:
#   No params= → no request needed
#   @pytest.fixture
#   def empty_dictionary() -> HashTableDictionary:
#       return HashTableDictionary()

#   params= → request.param holds the current value
#   @pytest.fixture(params=list(dicts.keys()))
#   def empty_dictionary(request: pytest.FixtureRequest):
#       return dicts[request.param].dict_class()


# =============================================================================
# HOW pytest.mark.integration WORKS END TO END
# =============================================================================

# ── Step 1: Register the marker in pyproject.toml ────────────────────────────
#
# [tool.pytest.ini_options]
# markers = [
#     "integration: marks integration tests (require real files)",
# ]
#
# Registration is required because addopts includes --strict-markers.
# Without it, pytest raises an error on any unknown marker name.

# ── Step 2: Tag the test ─────────────────────────────────────────────────────
#
# @pytest.mark.integration
# def test_large_dict_word_count(self, large_dict_path: Path) -> None:
#     ...

# ── Step 3: Filter at the CLI ────────────────────────────────────────────────
#
# pytest -m integration            → run ONLY integration tests
# pytest -m "not integration"      → run everything EXCEPT integration (fast)
# pytest tests/test_dictionary.py -m "not integration"  → file + filter
# pytest                           → run all tests (no filter)

# ── Why this matters in your workflow ────────────────────────────────────────
#
# Your test suite has two speeds:
#
#   Fast tests (mocks, tmp files)  → milliseconds → run on every save
#   Integration tests (143K dict)  → seconds      → run before commit
#
# During active development: pytest -m "not integration"  (instant feedback)
# Before pushing to GitHub:  pytest                       (full suite)
#
# This is the same pattern production CI pipelines use:
#   - Fast unit stage   → runs on every pull request
#   - Integration stage → runs on merge to main