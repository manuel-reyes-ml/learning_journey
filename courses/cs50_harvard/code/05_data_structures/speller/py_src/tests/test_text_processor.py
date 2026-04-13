# Test files must start with 'test_' so they are auto-discovery by pytest
"""
"""

from __future__ import annotations

from pathlib import Path
import pytest
from collections.abc import Callable, Iterator

from speller.text_processor import extract_words

## Simple Decision Rule
# "Is it a CONTAINER or CALLABLE type?"
#     YES → from collections.abc  (Generator, Iterator, Callable, Sequence, Mapping)

# "Is it a TYPE SYSTEM concept?"
#     YES → from typing  (Protocol, TypeVar, ParamSpec, Any, Final, TypedDict)


# =============================================================================
# HELPER — Create text file from string
# =============================================================================
# Only needed for integration-style tests
# This is a LOCAL fixture (not in conftest.py) because only this
# test file needs it. Fixtures used by one file stay in that file.

@pytest.fixture
def make_text_file(tmp_path: Path) -> Callable[[str, str], Path]:
    """Factory fixture — creates text files from content strings.

    A "factory fixture" returns a FUNCTION instead of a value.
    The test calls the function to create files with specific content.
    This avoids creating dozens of separate fixtures for each test case.

    Usage mirrors the production call pattern in speller.py::

        def test_something(make_text_file)
        path = make_text_file("Hello world")
        content = path.read_text(encoding="utf-8")
        words = list(extract_words(content, path.name))
 
    Returns
    -------
    Callable[[str, str], Path]
        Function that writes content to a tmp file and returns the Path.
    """
    def _create(content: str, filename: str = "test.txt") -> Path:
        file_path = tmp_path / filename
        file_path.write_text(content, encoding="utf-8")
        return file_path
    return _create


# =============================================================================
# BASIC EXTRACTION
# =============================================================================

# Test classes must start with capital T, colleted by class-name pattern
# Test functions/methods must start with 'test_', collected by function-name pattern

class TestBasicExtraction:
    """Test fundamental word extraction behavior.
 
    All tests pass content strings directly — no file I/O needed.
    path_name is a logging label; "test.txt" is used as a placeholder.
    """
    
    @pytest.mark.parametrize(
        "content, path_name, expected",
        [
            ("The cat sat on the mat", "test.txt", ["The", "cat", "sat", "on", "the", "mat"]),  # simple sentence
            ("Hello WORLD Python", "test.txt", ["Hello", "WORLD", "Python"]),  # preserves original case 
            ("", "empty.txt", []),                                      # empty content
            ("hello", "single.txt", ["hello"]),                         # single word no space
            ("hello     world", "spaces.txt", ["hello", "world"]),      # words with multiple spaces
            ("hello\nworld\npython\n", "newlines.txt", ["hello", "world", "python"]),  # words with delimiters
        ],
        # --- HOW @pytest.mark.parametrize WORKS ---
        #
        # Instead of writing 6 separate test functions that do the
        # same thing with different inputs, parametrize runs the SAME
        # test function multiple times with different arguments.
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
    def test_content_extraction(self, content: str, path_name: str, expected: list[str]) -> None:
        """Extract words from a simple sentence."""
        words = list(extract_words(content, path_name))
        assert words == expected
        
    def test_returns_iterator(self) -> None:
        """extract_words returns an iterator (generator), not a list.

        This verifies the streaming pattern — words are yielded
        lazily one at a time, never accumulated into a list.
        The same streaming pattern appears in LangChain (LLM tokens),
        PolicyPulse (RAG chunks), and PySpark (partition streaming).
        """
        result: Iterator[str] = extract_words("hello world", "iter.txt")
        assert hasattr(result, "__next__")
        assert hasattr(result, "__iter__")
        
    def test_path_name_is_label_only(self) -> None:
        """path_name is a logging label — does not affect extraction.

        The same content produces identical words regardless of
        what path_name string is provided. path_name only appears
        in DEBUG log messages — it is never used for file access.
        """
        content = "cat dog"
        words_a = list(extract_words(content, "label_a.txt"))
        words_b = list(extract_words(content, "label_b.txy"))
        assert words_a == words_b == ["cat", "dog"]
        
        
# =============================================================================
# APOSTROPHE HANDLING
# =============================================================================

class TestApostrophes:
    """Test apostrophe handling — matches speller.c rules exactly.

    Rules from speller.c:
    - Apostrophe MID-WORD (index > 0): included in word → "it's"
    - Apostrophe at START (index == 0): treated as delimiter → "hello"
    """
    
    @pytest.mark.parametrize(
        "content, path_name, expected",
        [
            ("it's don't can't", "apos.txt", ["it's", "don't", "can't"]),  # apostrophe inside a word is included
            ("'hello world", "start_apos.txt", ["hello", "world"]),  # apostrohpe at start of word is NOT included
            ("cat's dog's", "possessive.txt", ["cat's", "dog's"]),   # possesive forms are trated as single words
        ],
    )
    def test_apostrophe_in_content(self, content: str, path_name: str, expected: list[str]) -> None:
        """
        """
        words = list(extract_words(content, path_name))
        assert words == expected
        
        
# =============================================================================
# DIGIT HANDLING — THE TRICKY PART
# =============================================================================

class TestDigitHandling:
    """Test digit behavior — must match speller.c exactly.

    Critical rules:
    - Digit OUTSIDE a word: consume remaining alnum, skip entire token
    - Digit MID-WORD: discard word being built AND consume remaining alnum
    - The consumption affects the position of the NEXT word
    """
    
    @pytest.mark.parametrize(
        "content, path_name, expected",
        [
            ("123 hello 456 world", "digits.txt", ["hello", "world"]),     # pure digit sequences
            ("abc123def next", "mid_digit.txt", ["next"]),  # digit mid-word
            ("123abc_next", "start_digit.txt", ["next"]),   # digit at word start
            ("hello word123 world", "word_digit.txt", ["hello", "world"]), # valid word before and after
            ("Section 401k plan", "section.txt", ["Section", "plan"]),     # section numbers mixed with text
        ],
    )
    def test_digits_in_content(self, content: str, path_name: str, expected: list[str]) -> None:
        """
        """
        words = list(extract_words(content, path_name))
        assert words == expected
        
        
# =============================================================================
# WORD LENGTH — MAX_WORD_LENGTH (45)
# =============================================================================

class TestWordLength:
    """Test word length handling — MAX_WORD_LENGTH = 45.

    CS50's #define LENGTH 45 was chosen specifically to accommodate
    the longest word in the English language.
    """
    
    def test_word_at_max_length(self) -> None:
        """Word at exactly 45 characters is accepted."""
        word_45 = "a" * 45
        words = list(extract_words(f"{word_45} next", "max.txt"))
        assert word_45 in words
        
    def test_word_over_max_length(self) -> None:
        """Word over 45 characters is discarded.

        The state machine consumes the remaining alpha characters
        and continues from the next delimiter — "next" is not lost.
        """
        word_46 = "a" * 46
        words = list(extract_words(f"{word_46} next", "over_max.txt"))
        assert word_46 not in words
        assert "next" in words
        
    def test_pneumonoultramicroscopicsilicovolcanoconiosis(self) -> None:
        """The famous 45-character word is accepted.

        CS50's LENGTH constant (45) was specifically chosen to
        accommodate this word — a useful boundary-condition test.
        """
        long_word = "pneumonoultramicroscopicsilicovolcanoconiosis"
        assert len(long_word) == 45
        words = list(extract_words(f"{long_word} end", "long_word.txt"))
        assert long_word in words
        
        
# =============================================================================
# PUNCTUATION HANDLING
# =============================================================================

class TestPunctuation:
    """Test punctuation characters as word delimiters."""
    
    @pytest.mark.parametrize(
        "content, expected",
        [
            ("hello, world", ["hello", "world"]),
            ("hello. world", ["hello", "world"]),
            ("hello! world", ["hello", "world"]),
            ("hello? world", ["hello", "world"]),
            ("hello; world", ["hello", "world"]),
            ("hello: world", ["hello", "world"]),
            ("(hello) world", ["hello", "world"]),
            ('"hello" world', ["hello", "world"]),
            ("hello-world", ["hello", "world"]),
        ],
        # IDs make test output more readable:
        #   test_punctuation_as_delimiter[comma]       PASSED
        #   test_punctuation_as_delimiter[period]      PASSED
        ids=[
            "comma", "period", "exclamation", "question",
            "semicolon", "colon", "parens", "quotes", "hyphen",
        ],
    )
    def test_punctuation_as_delimiter(
        self, content: str, expected: list[str]
    ) -> None:
        """All punctuation characters act as word delimiters."""
        words = list(extract_words(content, "punctuation.txt"))
        assert words == expected
        
        
# =============================================================================
# INTERFACE CONTRACT
# =============================================================================

class TestInterface:
    """Verify the extract_words(content, path_name) calling contract.

    extract_words() does NO file I/O. It receives pre-decoded content
    as a str. path_name is a label for DEBUG logging only.

    The production calling pattern (from speller.py):
        content = path.read_text(encoding="utf-8")
        words = extract_words(content, path.name)

    These tests confirm that contract and replace the old TestPathHandling
    class which assumed extract_words() accepted file paths directly.
    """
    
    def test_accepts_plain_string(self) -> None:
        """extract_words works with any decoded string content."""
        words = list(extract_words("hello world", "label.txt"))
        assert words == ["hello", "world"]
        
    def test_accepts_multiline_string(self) -> None:
        """extract_words works with multiline content strings."""
        content = "line one\nline two\nline three"
        words = list(extract_words(content, "multi.txt"))
        assert words == ["line", "one", "line", "two", "line", "three"]
        
    def test_path_name_any_string_accepted(self) -> None:
        """path_name can be any string — it is a logging label only.

        Callers typically pass path.name for readable log output,
        but any string is valid. extract_words() never opens a file.
        """
        words_a = list(extract_words("cat", "real_file.txt"))
        words_b = list(extract_words("cat", "any_string_at_all"))
        assert words_a == words_b == ["cat"]
        
    def test_production_call_pattern(self, make_text_file) -> None:
        """Mirrors the exact call pattern used in speller.py.

        run_speller() does:
            content = path.read_text(encoding="utf-8")
            words = extract_words(content, path.name)

        This test verifies that reading a file and passing its decoded
        content produces the same result as passing the string directly.
        """
        raw = "The cat sat on the mat"
        path: Path = make_text_file(raw)
        
        # Production pattern - read file, then call extract_words
        content = path.read_text(encoding="utf-8")
        words_from_file = list(extract_words(content, path.name))
        
        # Direct string - must product identical results
        words_from_string = list(extract_words(raw, path.name))
        
        assert words_from_file == words_from_string == [
            "The", "cat", "sat", "on", "the", "mat"
        ]
        
        
# =============================================================================
# INTEGRATION — REAL CS50 TEXT FILES
# =============================================================================

