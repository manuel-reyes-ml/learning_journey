"""Shared pytest fixtures for the speller test suite.

HOW THIS FILE WORKS
====================

conftest.py is a SPECIAL filename in pytest:

1. AUTO-DISCOVERED — pytest finds it automatically by name.
   You never import conftest.py in your test files. pytest
   reads it before running any tests and registers all fixtures.

2. SHARED FIXTURES — any fixture defined here is available to
   ALL test files in this directory (and subdirectories).
   Test files just use the fixture NAME as a parameter:

       # test_dictionary.py (no import needed!)
       def test_check(loaded_dictionary):
           assert loaded_dictionary.check("cat")

3. SCOPE — this conftest.py covers all files in tests/:
       tests/
       ├── conftest.py          ← YOU ARE HERE
       ├── test_config.py       ← can use any fixture below
       ├── test_benchmarks.py   ← can use any fixture below
       ├── test_dictionary.py   ← can use any fixture below
       └── ...

4. MULTIPLE conftest.py — you can have conftest.py at different
   directory levels. Deeper ones override/extend higher ones.
   For now, one file is plenty.

WHAT GOES IN conftest.py vs IN A TEST FILE?
=============================================

Put a fixture HERE if:
  - 2+ test files need it (shared across files)
  - It's a mock class used by multiple tests
  - It's a path/directory fixture used everywhere

Put a fixture IN THE TEST FILE if:
  - Only that one file uses it
  - It's highly specific to one test class

FIXTURE EXECUTION ORDER
========================

When pytest sees: def test_check(loaded_dictionary)

It resolves the dependency chain BOTTOM-UP:
  1. loaded_dictionary needs → sample_dict_file
  2. sample_dict_file needs → tmp_path (built-in)
  3. tmp_path needs         → nothing (it's the root)

Then executes TOP-DOWN:
  1. Create tmp_path         → /tmp/pytest-abc/test_check0/
  2. Create sample_dict_file → write dict.txt in tmp dir
  3. Create loaded_dictionary → load dict.txt into HashTableDictionary
  4. Pass to test_check      → your test runs
  5. Cleanup (after test)    → tmp dir deleted

Your v8.1 Roadmap Usage
------------------------
Every project gets its own conftest.py:
- DataVault:    MockLLMProvider, mock API responses
- PolicyPulse:  MockVectorStore, sample embeddings
- FormSense:    Sample form images, mock Gemini responses
- AFC:          Synthetic market data, mock SEC responses
"""

from __future__ import annotations

from pathlib import Path

import pytest

from speller.dictionaries import HashTableDictionary


# =============================================================================
# PATH FIXTURES — Resolve test file locations
# =============================================================================
# These fixtures provide Path objects to your project directories.
# They depend on each other in a chain:
#
#   project_root → dict_dir → large_dict_path
#                → texts_dir
#                → keys_dir


@pytest.fixture
def project_root() -> Path:
    """Resolve the speller project root directory.

    HOW IT WORKS:
      __file__                → /path/to/speller/tests/conftest.py
      Path(__file__).resolve() → absolute path (resolves symlinks)
      .parent                 → /path/to/speller/tests/
      .parent                 → /path/to/speller/  ← project root!

    WHY resolve()?
      Without resolve(), relative paths and symlinks could cause
      tests to find wrong directories. resolve() guarantees an
      absolute, canonical path.

    Returns
    -------
    Path
        Absolute path to the speller project root.
    """
    # tests/conftest.py → parent is tests/ → parent is speller/
    return Path(__file__).resolve().parent.parent


@pytest.fixture
def dict_dir(project_root: Path) -> Path:
    """Path to the dictionaries/ directory.

    FIXTURE CHAINING IN ACTION:
      This fixture has a parameter named 'project_root'.
      pytest sees this, finds the project_root fixture above,
      calls it, and passes the result to this function.

      You never write: dict_dir(project_root())
      pytest does: dict_dir(result_of_project_root_fixture)

    Parameters
    ----------
    project_root : Path
        Injected by pytest from the project_root fixture.

    Returns
    -------
    Path
        Path to dictionaries/ directory.
    """
    return project_root / "dictionaries"


@pytest.fixture
def texts_dir(project_root: Path) -> Path:
    """Path to the texts/ directory.

    Parameters
    ----------
    project_root : Path
        Injected by pytest from the project_root fixture.

    Returns
    -------
    Path
        Path to texts/ directory.
    """
    return project_root / "texts"


@pytest.fixture
def keys_dir(project_root: Path) -> Path:
    """Path to the keys/ directory (CS50 answer keys).

    Parameters
    ----------
    project_root : Path
        Injected by pytest from the project_root fixture.

    Returns
    -------
    Path
        Path to keys/ directory.
    """
    return project_root / "keys"


@pytest.fixture
def large_dict_path(dict_dir: Path) -> Path:
    """Path to the large dictionary (143,091 words).

    DEEPER CHAINING:
      This fixture needs dict_dir, which needs project_root.
      pytest resolves the full chain automatically:
        project_root() → dict_dir(project_root) → large_dict_path(dict_dir)

    Parameters
    ----------
    dict_dir : Path
        Injected by pytest from the dict_dir fixture.

    Returns
    -------
    Path
        Path to dictionaries/large.
    """
    return dict_dir / "large"


@pytest.fixture
def small_dict_path(dict_dir: Path) -> Path:
    """Path to the small dictionary (2 words: cat, caterpillar).

    Parameters
    ----------
    dict_dir : Path
        Injected by pytest from the dict_dir fixture.

    Returns
    -------
    Path
        Path to dictionaries/small.
    """
    return dict_dir / "small"


# =============================================================================
# TEMPORARY FILE FIXTURES — Create test files that auto-cleanup
# =============================================================================
# These fixtures use tmp_path, a BUILT-IN pytest fixture that:
#   - Creates a unique temporary directory for each test
#   - Automatically deletes it after the test session
#   - You never need to manually create or clean up temp files
#
# tmp_path is available without defining it — pytest provides it.
# Just use "tmp_path" as a parameter name and pytest injects it.


@pytest.fixture
def sample_text_file(tmp_path: Path) -> Path:
    """Create a simple text file for basic testing.

    WHY USE tmp_path INSTEAD OF REAL FILES?
      - Isolation: each test gets its own directory
      - No cleanup: pytest deletes tmp dirs automatically
      - Deterministic: we control the exact content
      - Fast: no disk seek for real files
      - Safe: tests can't corrupt real project files

    Parameters
    ----------
    tmp_path : Path
        Built-in pytest fixture. Provides a unique temporary
        directory for this specific test invocation.
        Example: /tmp/pytest-of-manuel/pytest-42/test_check0/

    Returns
    -------
    Path
        Path to the created text file containing "The cat sat on the mat".
    """
    text_file = tmp_path / "sample.txt"
    text_file.write_text("The cat sat on the mat\n", encoding="utf-8")
    return text_file


@pytest.fixture
def mixed_text_file(tmp_path: Path) -> Path:
    """Create a text file with digits, apostrophes, and edge cases.

    This fixture tests the TRICKY parts of text_processor.py:
    - "abc123def" → digit mid-word → skip entire token
    - "cat's" → apostrophe mid-word → include
    - "'apostrophe" → apostrophe at start → not part of word
    - Multiple spaces → treated as delimiters

    Parameters
    ----------
    tmp_path : Path
        Built-in pytest fixture.

    Returns
    -------
    Path
        Path to the created text file with edge case content.
    """
    content = (
        "Hello world\n"
        "cat's hat\n"
        "abc123def next\n"            # digit mid-word: skip "abc123def"
        "test   multiple   spaces\n"  # multiple spaces between words
        "'apostrophe start\n"         # apostrophe at start: not part of word
        "word123 another\n"           # digit mid-word: skip "word123"
        "superlongword end\n"         # normal words (under 45 chars)
    )
    text_file = tmp_path / "mixed.txt"
    text_file.write_text(content, encoding="utf-8")
    return text_file


@pytest.fixture
def empty_text_file(tmp_path: Path) -> Path:
    """Create an empty text file.

    Tests the edge case: what happens when there are zero words?
    extract_words() should yield nothing (empty generator).

    Parameters
    ----------
    tmp_path : Path
        Built-in pytest fixture.

    Returns
    -------
    Path
        Path to an empty file.
    """
    text_file = tmp_path / "empty.txt"
    text_file.write_text("", encoding="utf-8")
    return text_file


@pytest.fixture
def sample_dict_file(tmp_path: Path) -> Path:
    """Create a small dictionary file for controlled testing.

    WHY NOT USE THE REAL dictionaries/large FILE?
      - Speed: loading 143K words takes time
      - Control: we know EXACTLY which words are in the dictionary
      - Predictability: we can calculate expected misspellings
      - Isolation: tests don't depend on external file state

    Contains known words so we can predict exactly which words
    from sample_text_file ("The cat sat on the mat") will be found.

    Parameters
    ----------
    tmp_path : Path
        Built-in pytest fixture.

    Returns
    -------
    Path
        Path to the created dictionary file with 10 words.
    """
    # These words match what sample_text_file contains
    # so we can predict: 0 misspelled from "The cat sat on the mat"
    words = "the\ncat\nsat\non\nmat\nhello\nworld\nnext\ntest\nend\n"
    dict_file = tmp_path / "test_dict.txt"
    dict_file.write_text(words, encoding="utf-8")
    return dict_file


# =============================================================================
# DICTIONARY FIXTURES — Pre-loaded dictionary instances
# =============================================================================
# These provide HashTableDictionary objects ready to use in tests.
# They demonstrate fixture CHAINING — each fixture depends on
# fixtures defined above.


@pytest.fixture
def empty_dictionary() -> HashTableDictionary:
    """Create an unloaded HashTableDictionary.

    WHY TEST THE UNLOADED STATE?
      - check() should raise RuntimeError before load()
      - size() should return 0
      - This catches the "forgot to call load()" bug

    Returns
    -------
    HashTableDictionary
        Fresh instance with no words loaded.
    """
    return HashTableDictionary()


@pytest.fixture
def loaded_dictionary(sample_dict_file: Path) -> HashTableDictionary:
    """Create a HashTableDictionary loaded with test words.

    FULL FIXTURE CHAIN (pytest resolves automatically):
      1. pytest creates tmp_path (built-in)
      2. sample_dict_file creates dict.txt inside tmp_path
      3. THIS fixture loads that file into a HashTableDictionary

    The test just asks for 'loaded_dictionary' and gets a fully
    prepared dictionary object. No setup code in the test itself.

    Parameters
    ----------
    sample_dict_file : Path
        Injected by pytest from the sample_dict_file fixture above.

    Returns
    -------
    HashTableDictionary
        Dictionary loaded with: the, cat, sat, on, mat, hello,
        world, next, test, end.
    """
    dictionary = HashTableDictionary()
    dictionary.load(str(sample_dict_file))
    return dictionary


# =============================================================================
# MOCK CLASSES — Test doubles for dependency injection
# =============================================================================
#
# WHY MOCKS?
# ==========
# run_speller() accepts DictionaryProtocol — it doesn't know or care
# what concrete class it receives. In production, it gets HashTableDictionary.
# In tests, we give it these mocks instead.
#
# Benefits:
#   - No file I/O (fast)
#   - Deterministic (always same words)
#   - Isolated (no dependency on real dictionary files)
#   - Controllable (can simulate failures)
#
# NOTICE: These classes DO NOT inherit from DictionaryProtocol.
# They satisfy it through STRUCTURAL TYPING — they have matching
# method signatures, and that's enough. This is the Protocol pattern
# in action.
#
# This is the SAME pattern you'll use in every future project:
#   DataVault:   MockLLMProvider (avoids API costs during testing)
#   PolicyPulse: MockVectorStore (no ChromaDB server needed)
#   FormSense:   MockExtractor (no Gemini Vision API calls)
#   AFC:         MockDataSource (no SEC API rate limiting)


class MockDictionary:
    """Test double that satisfies DictionaryProtocol.

    Provides deterministic, predictable behavior for testing
    run_speller() without real file I/O. The words set is
    configurable so each test can control what's "in the dictionary."

    NO INHERITANCE from DictionaryProtocol needed:
      - Has load() → bool           ✓ matches Protocol
      - Has check() → bool          ✓ matches Protocol
      - Has size() → int            ✓ matches Protocol
      - Has __len__() → int         ✓ matches Protocol
      - Has __contains__() → bool   ✓ matches Protocol
      = Structural typing satisfied  ✓

    Parameters
    ----------
    words : set of str, optional
        Words to include in the mock dictionary.
        Defaults to {"the", "cat", "sat", "on", "mat"}.
    """

    def __init__(self, words: set[str] | None = None) -> None:
        # If no words provided, use a default set that matches
        # sample_text_file content ("The cat sat on the mat")
        self._words = words or {"the", "cat", "sat", "on", "mat"}
        self._loaded = False

    def load(self, filepath: str) -> bool:
        """Pretend to load — always succeeds, ignores the filepath.

        In real code, this reads a file. In the mock, we skip file I/O
        entirely. The words were set in __init__.
        """
        self._loaded = True
        return True

    def check(self, word: str) -> bool:
        """Check if word is in the mock word set (case-insensitive)."""
        return word.lower() in self._words

    def size(self) -> int:
        """Return the number of words in the mock dictionary."""
        return len(self._words)

    def __len__(self) -> int:
        """Support len(dictionary) — delegates to size()."""
        return self.size()

    def __contains__(self, word: str) -> bool:
        """Support 'word in dictionary' — delegates to check()."""
        return self.check(word)


class FailingDictionary:
    """Mock dictionary that ALWAYS fails to load.

    Used to test error handling paths — what happens when
    run_speller() can't load the dictionary? It should raise
    SystemExit, and main() should catch it and return LOAD_FAILED.

    This is NEGATIVE TESTING — verifying that error paths work
    correctly is just as important as testing happy paths.
    """

    def load(self, filepath: str) -> bool:
        """Always returns False — simulates a load failure."""
        return False

    def check(self, word: str) -> bool:
        """Always returns False (dictionary has no words)."""
        return False

    def size(self) -> int:
        """Always returns 0 (empty dictionary)."""
        return 0

    def __len__(self) -> int:
        """Always returns 0."""
        return 0

    def __contains__(self, word: str) -> bool:
        """Always returns False (nothing is 'in' a failed dictionary)."""
        return False


# =============================================================================
# MOCK FIXTURES — Provide mock instances to test functions
# =============================================================================
# These fixtures wrap the mock classes above so test functions
# can request them by parameter name.
#
# WHY WRAP CLASSES IN FIXTURES?
#   Without a fixture, tests would need to create the mock themselves:
#       def test_speller():
#           mock = MockDictionary()          ← setup in every test
#           result = run_speller(dictionary=mock, ...)
#
#   With a fixture, the setup happens automatically:
#       def test_speller(mock_dictionary):   ← pytest creates it for you
#           result = run_speller(dictionary=mock_dictionary, ...)


@pytest.fixture
def mock_dictionary() -> MockDictionary:
    """Provide a MockDictionary instance with default words.

    Usage in tests (no import needed — conftest fixtures are auto-discovered):

        def test_speller(mock_dictionary):
            result = run_speller(dictionary=mock_dictionary, ...)

    Returns
    -------
    MockDictionary
        Pre-configured with default words:
        {"the", "cat", "sat", "on", "mat"}.
    """
    return MockDictionary()


@pytest.fixture
def failing_dictionary() -> FailingDictionary:
    """Provide a FailingDictionary for error path testing.

    Usage in tests:

        def test_load_failure(failing_dictionary):
            with pytest.raises(SystemExit):
                run_speller(dictionary=failing_dictionary, ...)

    Returns
    -------
    FailingDictionary
        Dictionary whose load() always returns False.
    """
    return FailingDictionary()