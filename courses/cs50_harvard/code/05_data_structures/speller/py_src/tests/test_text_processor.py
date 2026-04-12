# Test files must start with 'test_' so they are auto-discovery by pytest
"""
"""

from __future__ import annotations

from pathlib import Path
import pytest
from collections.abc import Callable

from speller.text_processor import extract_words

## Simple Decision Rule
# "Is it a CONTAINER or CALLABLE type?"
#     YES → from collections.abc  (Generator, Iterator, Callable, Sequence, Mapping)

# "Is it a TYPE SYSTEM concept?"
#     YES → from typing  (Protocol, TypeVar, ParamSpec, Any, Final, TypedDict)


# =============================================================================
# HELPER — Create text file from string
# =============================================================================
# This is a LOCAL fixture (not in conftest.py) because only this
# test file needs it. Fixtures used by one file stay in that file.

@pytest.fixture
def make_text_file(tmp_path: Path) -> Callable[[str, str], Path]:
    """Factory fixture — creates text files from content strings.

    A "factory fixture" returns a FUNCTION instead of a value.
    The test calls the function to create files with specific content.
    This avoids creating dozens of separate fixtures for each test case.

    Usage in tests::

        def test_something(make_text_file):
            path = make_text_file("Hello world")
            words = list(extract_words(path))
            assert words == ["Hello", "world"]
    """
    def _create(content: str, filename: str = "test.txt") -> Path:
        file_path = tmp_path / filename
        file_path.write_text(content, encoding="utf-8")
        return file_path
    return _create