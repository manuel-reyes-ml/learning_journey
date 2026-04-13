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

class TestBasicExtraction:
    """Test fundamental word extraction behavior.
 
    All tests pass content strings directly — no file I/O needed.
    path_name is a logging label; "test.txt" is used as a placeholder.
    """
    
    def test_simple_sentence(self) -> None:
        """Extract words from a simple sentence."""
        words = list(extract_words("The cat sat on the mat", "test.txt"))
        assert words == ["The", "cat", "sat", "on", "the", "mat"]
        
    def test_preserves_original_case(self) -> None:
        """Words are yielded in original case (not lowered).

        Case normalization is dictionary.check()'s job, not
        text_processor's. Preserving case ensures misspelled
        words are printed as they appear in the original text.
        """
        words = list(extract_words("Hello WORLD Python", "test.txt"))
        assert words == ["Hello", "WORLD", "Python"]
        
    def test_empty_content(self) -> None:
        """Empty content string yields no words."""
        words = list(extract_words("", "empty.txt"))
        assert words == []
        
    def test_single_word(self) -> None:
        """Single word with no surrounding whitespace."""
        words = list(extract_words("hello", "single.txt"))
        assert words == ["hello"]
        
    def test_multiple_spaces(self) -> None:
        """Multiple spaces between words are treated as delimiters."""
        words = list(extract_words("hello   world", "spaces.txt"))
        assert words == ["hello", "world"]
        
    def test_newlines_as_delimiters(self) -> None:
        """Newlines act as word delimiters."""
        words = list(extract_words("hello\nworld\npython\n", "newlines.txt"))
        assert words == ["hello", "world", "python"]
        
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