"""Hash table dictionary implementation for spell checking.

Implements ``DictionaryProtocol`` using Python's built-in ``set`` as
the underlying hash table. Provides O(1) average-case lookup for
spell checking operations.

C → Python Mapping
-------------------
This module replaces CS50's ``dictionary.c`` where you would manually
build a hash table with linked-list buckets, malloc nodes, and free
memory. Python's ``set`` IS a hash table internally — it handles
hashing, collision resolution, and dynamic resizing automatically.

    C (dictionary.c)                 Python (dictionary.py)
    ──────────────────               ──────────────────────
    node *table[N]                   self._words: set[str]
    malloc(sizeof(node))             self._words.add(word)
    strcasecmp(word, node->word)     word.lower() in self._words
    free(node) in unload()           Garbage collector (automatic)
    hash(word[0]) - 'A' (26 buckets) Python uses ~2x set size buckets

Module Dependencies
-------------------
    config.py     → MAX_WORD_LENGTH (constant)
    protocols.py  → DictionaryProtocol (interface contract)
"""

# =============================================================================
# IMPORTS
# =============================================================================

from __future__ import annotations

from dataclasses import dataclass, KW_ONLY, field
from pathlib import Path
import logging
from typing import Callable

from speller.config import MAX_WORD_LENGTH
from speller.protocols import DictionaryProtocol
from speller.speller import SpellerResult

# No ImportError sys.exit() on regular module so the
# error propagates to the caller (__main__.py).


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

__all__ = [
    "DictInfo",
    "dicts",
    "HashTableDictionary", 
    "ListDictionary"
]


# =============================================================================
# MODULE CONFIGURATION
# =============================================================================

dicts: dict[str, DictInfo] = {}


# =====================================================
# Type Aliases
# =====================================================

type RegDecorator = Callable[[type[DictionaryProtocol]], type[DictionaryProtocol]]


# =====================================================
# Dict Metadata Configuration
# =====================================================

@dataclass
class DictInfo:
    """
    """
    
    # Required fields (no default) must come first
    # Optional fields with defaults afterwards
    _: KW_ONLY  # Everything after this is keyword-only
    dict_class: type[DictionaryProtocol]
    name: str
    description: str
    results: dict[str, SpellerResult] = field(default_factory=dict)


# =============================================================================
# DICTIONARY REGISTRY
# =============================================================================

# A decorator factory is just a function that takes custom parameters 
# and generates a decorator.
def register_class(name: str, description: str = "") -> RegDecorator:
    """
    """
    def decorator(dict_class: type[DictionaryProtocol]) -> type[DictionaryProtocol]:
        dicts[dict_class.__name__] = DictInfo(
            dict_class=dict_class,
            name=name,
            description=description or dict_class.__doc__ or "",
        )
        return dict_class  # Return unchanged class
        # class goes in, class comes out. The class' __name__, __doc__, __qualname__
        # are all intact because you never created a replacement. Nothing to fix,
        # so @wraps would do nothing useful.
    return decorator

# Instantiate by key - calling a class creates an instance
# dictionary = dicts["hash"]() -> HashTableDictionary()


# =============================================================================
# DICTIONARY CLASSES
# =============================================================================

# Notice that dictionary.py imports DictionaryProtocol. It doesn't need to for
# the class builder. We use it here and on speller.py for type hints. 

@register_class(
    "hash",
    "Use Set as hash table data structure "
    "for dictionary container.",
)
class HashTableDictionary:
    """Spell-check dictionary backed by a Python ``set`` (hash table).

    Satisfies ``DictionaryProtocol`` through structural typing — no
    inheritance needed. This class has ``load()``, ``check()``, and
    ``size()`` with matching signatures, so mypy and ``isinstance()``
    recognize it as a valid ``DictionaryProtocol`` implementation.

    Why NOT inherit from DictionaryProtocol?
    -----------------------------------------
    Protocol uses structural typing (duck typing with type safety).
    Inheriting from a Protocol makes YOUR class also a Protocol,
    which is almost never what you want. Just implement the methods.

    Attributes
    ----------
    _words : set[str]
        Internal hash table storing lowercase dictionary words.
        Private (underscore prefix) because external code should use
        check(), not access the set directly.
    _loaded : bool
        Tracks whether load() has been called successfully.
        Prevents check() from silently returning False on an
        unloaded dictionary (which would flag every word as misspelled).

    Examples
    --------
    >>> dictionary = HashTableDictionary()
    >>> dictionary.load("dictionaries/large")
    True
    >>> dictionary.size()
    143091
    >>> dictionary.check("hello")
    True
    >>> dictionary.check("xyz")
    False
    """
    
    def __init__(self) -> None:
        self._words: set[str] = set()
        self._loaded: bool = False
        
        
    def load(self, filepath: str) -> bool:
        """Load dictionary file into the hash table (set).

        Reads the file line by line, strips whitespace, converts to
        lowercase, and adds each word to the internal set. Uses a
        context manager (``with``) to guarantee the file handle is
        closed even if an error occurs.

        Parameters
        ----------
        filepath : str
            Path to dictionary file. One lowercase word per line.
            Default in CS50 is ``dictionaries/large`` (143,091 words).

        Returns
        -------
        bool
            True if dictionary loaded successfully, False otherwise.

        Notes
        -----
        Why ``set.add()`` and not ``list.append()``?
            - ``set`` uses a hash table internally → O(1) average lookup
            - ``list`` would require O(n) linear search for every check()
            - With 143,091 words and thousands of checks per text file,
              O(1) vs O(n) is the difference between instant and slow

        Why lowercase on load AND on check?
            - Dictionary file contains lowercase words ("hello")
            - Text files contain mixed case ("Hello", "HELLO", "hello")
            - Normalizing both sides to lowercase ensures case-insensitive
              matching without storing multiple versions of each word

        Why ``Path(filepath)`` wrapping?
            - The Protocol defines filepath as ``str`` for flexibility
              (callers might pass a string or a Path)
            - We convert to Path internally for robust path operations
            - ``path.exists()`` is cleaner than ``os.path.exists(str)``
        """
        
        path = Path(filepath)
        
        if not path.exists():
            logger.error("Dictionary file not found: %s", path)
            return False
        
        try:
            # Context manager guarantees file.close() even if exception occurs.
            # encoding="utf-8" is explicit - never rely on platform default.
            with open(path, "r", encoding="utf-8") as dict_file:
                for line in dict_file:
                    word = line.strip()
                    
                    # Skip empty lines (defensive - large dict shouldn't have them)
                    if not word:
                        continue
                    
                    # Skip words exceeding CS50's LENGTH constant. 
                    # The C version uses #define LENGTH 45.
                    if len(word) > MAX_WORD_LENGTH:
                        continue
                    
                    self._words.add(word.lower())
        
        # OSError is the parent of FileNotFoundError, PermissionError, IsADirectoryError,
        # and other file-related errors. Catching OSError handles all of them in one block.
        # In production (Stage 2 pipelines, Stage 4 LLM apps), files can fail for many reasons
        # beyond "not found" — permissions, disk full, encoding problems. OSError covers them all.
        except OSError as e:
            logger.error("Failed to read dictionary '%s': %s", path, e)
            return False
        
        self._loaded = True
        logger.info(
            "Loaded %d words from '%s'",
            len(self._words),
            path.name,
        )
        return True
    
    
    def check(self, word: str) -> bool:
        """Check if a word exists in the loaded dictionary.

        Case-insensitive: "Hello", "HELLO", and "hello" all match
        a dictionary entry of "hello" because we normalize with
        ``.lower()`` before lookup.

        Parameters
        ----------
        word : str
            The word to look up. Case does not matter.

        Returns
        -------
        bool
            True if the word is in the dictionary, False otherwise.

        Raises
        ------
        RuntimeError
            If called before ``load()`` has been called successfully.
            This prevents silent bugs where an unloaded dictionary
            reports every word as misspelled.

        Notes
        -----
        Why raise instead of returning False?
            - Returning False silently would mean every word is "misspelled"
            - The caller might not realize the dictionary isn't loaded
            - A RuntimeError makes the bug immediately visible
            - This is the "fail fast" principle — catch bugs early

        What ``word.lower() in self._words`` does under the hood:
            1. ``word.lower()`` creates a normalized copy → "HELLO" → "hello"
            2. ``in self._words`` calls ``set.__contains__()``
            3. Python hashes "hello" → gets bucket index
            4. Checks bucket for matching entry → O(1) average
            This is the SAME operation as the C hash table lookup,
            but Python handles the hashing and collision resolution.
        """
        # Without this guard, an unloaded dictionary silently returns False
        # for every word — the entire text appears "misspelled."
        if not self._loaded:
            raise RuntimeError(
                "Dictionary not loaded. Call load() before check()."
            )
        
        return word.lower() in self._words
    
    
    def size(self) -> int:
        """Return the number of words in the loaded dictionary.

        Returns
        -------
        int
            Word count if dictionary is loaded, 0 if not yet loaded.

        Notes
        -----
        In C (``dictionary.c``), you would maintain a counter variable
        that increments during ``load()``, then ``size()`` returns it.
        Python's ``set`` already tracks its own length internally via
        ``len()``, so no manual counter is needed.
        """
        return len(self._words)
    
    
    def __len__(self) -> int:
        """Support ``len(dictionary)`` — Pythonic interface.

        This dunder method makes HashTableDictionary satisfy the
        ``collections.abc.Sized`` protocol. Any object with ``__len__``
        can be used with Python's built-in ``len()`` function.

        Why BOTH size() and __len__()?
            - ``size()`` satisfies DictionaryProtocol (explicit method name)
            - ``__len__()`` satisfies Python's Sized protocol (Pythonic)
            - ``__len__`` delegates to ``size()`` — single source of truth
            - DRY principle: the logic lives in one place (size())

        Where you'll reuse this pattern:
            - DataVault: len(results) on query result objects
            - PolicyPulse: len(chunks) on retrieval results
            - Stage 2: len(batch) on ETL pipeline batches
        """
        return self.size()
    
    
    def __contains__(self, word: str) -> bool:
        """Support ``"hello" in dictionary`` — Pythonic interface.

        This dunder method makes HashTableDictionary satisfy the
        ``collections.abc.Container`` protocol. It enables the
        natural Python syntax ``word in dictionary`` instead of
        ``dictionary.check(word)``.

        Why BOTH check() and __contains__()?
            - ``check()`` satisfies DictionaryProtocol (explicit interface)
            - ``__contains__()`` satisfies Python's Container protocol
            - Enables idiomatic Python: ``if word in dictionary:``
            - ``__contains__`` delegates to ``check()`` — DRY principle
        """
        return self.check(word)
    
    
    # type(self).__name__ instead of hardcoding "HashTableDictionary" means
    # if someone subclasses your class, __repr__ automatically uses the subclass
    # name. The :, format specifier adds thousand separators (143,091 instead of 143091).
    def __repr__(self) -> str:
        """Developer-facing string representation.

        ``__repr__`` is for DEVELOPERS (debugging, logging).
        ``__str__`` is for USERS (display, print).

        Convention: __repr__ should look like a valid constructor call
        when possible, or at minimum identify the object uniquely.
        """
        return (
            f"{type(self).__name__}("
            f"loaded={self._loaded}, "
            f"words={len(self._words):,})"
        )
        
        
    def unload(self) -> bool:
        """Clear dictionary from memory. Python's GC handles this
        automatically, but explicit unload provides API symmetry
        with load().
        """
        self._words.clear()
        self._loaded = False
        return True


@register_class(
    "list",
    "Use a List data structure as dictionary container.",
)
class ListDictionary:
    """Spell-check dictionary backed by a Python ``set`` (hash table).

    Satisfies ``DictionaryProtocol`` through structural typing — no
    inheritance needed. This class has ``load()``, ``check()``, and
    ``size()`` with matching signatures, so mypy and ``isinstance()``
    recognize it as a valid ``DictionaryProtocol`` implementation.

    Why NOT inherit from DictionaryProtocol?
    -----------------------------------------
    Protocol uses structural typing (duck typing with type safety).
    Inheriting from a Protocol makes YOUR class also a Protocol,
    which is almost never what you want. Just implement the methods.

    Attributes
    ----------
    _words : set[str]
        Internal hash table storing lowercase dictionary words.
        Private (underscore prefix) because external code should use
        check(), not access the set directly.
    _loaded : bool
        Tracks whether load() has been called successfully.
        Prevents check() from silently returning False on an
        unloaded dictionary (which would flag every word as misspelled).

    Examples
    --------
    >>> dictionary = HashTableDictionary()
    >>> dictionary.load("dictionaries/large")
    True
    >>> dictionary.size()
    143091
    >>> dictionary.check("hello")
    True
    >>> dictionary.check("xyz")
    False
    """
    
    def __init__(self) -> None:
        self._words: list[str] = []
        self._loaded: bool = False
        
        
    def load(self, filepath: str) -> bool:
        """Load dictionary file into the hash table (set).

        Reads the file line by line, strips whitespace, converts to
        lowercase, and adds each word to the internal set. Uses a
        context manager (``with``) to guarantee the file handle is
        closed even if an error occurs.

        Parameters
        ----------
        filepath : str
            Path to dictionary file. One lowercase word per line.
            Default in CS50 is ``dictionaries/large`` (143,091 words).

        Returns
        -------
        bool
            True if dictionary loaded successfully, False otherwise.

        Notes
        -----
        Why ``set.add()`` and not ``list.append()``?
            - ``set`` uses a hash table internally → O(1) average lookup
            - ``list`` would require O(n) linear search for every check()
            - With 143,091 words and thousands of checks per text file,
              O(1) vs O(n) is the difference between instant and slow

        Why lowercase on load AND on check?
            - Dictionary file contains lowercase words ("hello")
            - Text files contain mixed case ("Hello", "HELLO", "hello")
            - Normalizing both sides to lowercase ensures case-insensitive
              matching without storing multiple versions of each word

        Why ``Path(filepath)`` wrapping?
            - The Protocol defines filepath as ``str`` for flexibility
              (callers might pass a string or a Path)
            - We convert to Path internally for robust path operations
            - ``path.exists()`` is cleaner than ``os.path.exists(str)``
        """
        
        path = Path(filepath)
        
        if not path.exists():
            logger.error("Dictionary file not found: %s", path)
            return False
        
        try:
            # Context manager guarantees file.close() even if exception occurs.
            # encoding="utf-8" is explicit - never rely on platform default.
            with open(path, "r", encoding="utf-8") as dict_file:
                for line in dict_file:
                    word = line.strip()
                    
                    # Skip empty lines (defensive - large dict shouldn't have them)
                    if not word:
                        continue
                    
                    # Skip words exceeding CS50's LENGTH constant. 
                    # The C version uses #define LENGTH 45.
                    if len(word) > MAX_WORD_LENGTH:
                        continue
                    
                    self._words.append(word.lower())
                      
        # OSError is the parent of FileNotFoundError, PermissionError, IsADirectoryError,
        # and other file-related errors. Catching OSError handles all of them in one block.
        # In production (Stage 2 pipelines, Stage 4 LLM apps), files can fail for many reasons
        # beyond "not found" — permissions, disk full, encoding problems. OSError covers them all.
        except OSError as e:
            logger.error("Failed to read dictionary '%s': %s", path, e)
            return False
        
        self._loaded = True
        logger.info(
            "Loaded %d words from '%s'",
            len(self._words),
            path.name,
        )
        return True
    
    
    def check(self, word: str) -> bool:
        """Check if a word exists in the loaded dictionary.

        Case-insensitive: "Hello", "HELLO", and "hello" all match
        a dictionary entry of "hello" because we normalize with
        ``.lower()`` before lookup.

        Parameters
        ----------
        word : str
            The word to look up. Case does not matter.

        Returns
        -------
        bool
            True if the word is in the dictionary, False otherwise.

        Raises
        ------
        RuntimeError
            If called before ``load()`` has been called successfully.
            This prevents silent bugs where an unloaded dictionary
            reports every word as misspelled.

        Notes
        -----
        Why raise instead of returning False?
            - Returning False silently would mean every word is "misspelled"
            - The caller might not realize the dictionary isn't loaded
            - A RuntimeError makes the bug immediately visible
            - This is the "fail fast" principle — catch bugs early

        What ``word.lower() in self._words`` does under the hood:
            1. ``word.lower()`` creates a normalized copy → "HELLO" → "hello"
            2. ``in self._words`` calls ``set.__contains__()``
            3. Python hashes "hello" → gets bucket index
            4. Checks bucket for matching entry → O(1) average
            This is the SAME operation as the C hash table lookup,
            but Python handles the hashing and collision resolution.
        """
        # Without this guard, an unloaded dictionary silently returns False
        # for every word — the entire text appears "misspelled."
        if not self._loaded:
            raise RuntimeError(
                "Dictionary not loaded. Call load() before check()."
            )
        
        return word.lower() in self._words
    
    
    def size(self) -> int:
        """Return the number of words in the loaded dictionary.

        Returns
        -------
        int
            Word count if dictionary is loaded, 0 if not yet loaded.

        Notes
        -----
        In C (``dictionary.c``), you would maintain a counter variable
        that increments during ``load()``, then ``size()`` returns it.
        Python's ``set`` already tracks its own length internally via
        ``len()``, so no manual counter is needed.
        """
        return len(self._words)
    
    
    def __len__(self) -> int:
        """Support ``len(dictionary)`` — Pythonic interface.

        This dunder method makes HashTableDictionary satisfy the
        ``collections.abc.Sized`` protocol. Any object with ``__len__``
        can be used with Python's built-in ``len()`` function.

        Why BOTH size() and __len__()?
            - ``size()`` satisfies DictionaryProtocol (explicit method name)
            - ``__len__()`` satisfies Python's Sized protocol (Pythonic)
            - ``__len__`` delegates to ``size()`` — single source of truth
            - DRY principle: the logic lives in one place (size())

        Where you'll reuse this pattern:
            - DataVault: len(results) on query result objects
            - PolicyPulse: len(chunks) on retrieval results
            - Stage 2: len(batch) on ETL pipeline batches
        """
        return self.size()
    
    
    def __contains__(self, word: str) -> bool:
        """Support ``"hello" in dictionary`` — Pythonic interface.

        This dunder method makes HashTableDictionary satisfy the
        ``collections.abc.Container`` protocol. It enables the
        natural Python syntax ``word in dictionary`` instead of
        ``dictionary.check(word)``.

        Why BOTH check() and __contains__()?
            - ``check()`` satisfies DictionaryProtocol (explicit interface)
            - ``__contains__()`` satisfies Python's Container protocol
            - Enables idiomatic Python: ``if word in dictionary:``
            - ``__contains__`` delegates to ``check()`` — DRY principle
        """
        return self.check(word)
    
    
    # type(self).__name__ instead of hardcoding "HashTableDictionary" means
    # if someone subclasses your class, __repr__ automatically uses the subclass
    # name. The :, format specifier adds thousand separators (143,091 instead of 143091).
    def __repr__(self) -> str:
        """Developer-facing string representation.

        ``__repr__`` is for DEVELOPERS (debugging, logging).
        ``__str__`` is for USERS (display, print).

        Convention: __repr__ should look like a valid constructor call
        when possible, or at minimum identify the object uniquely.
        """
        return (
            f"{type(self).__name__}("
            f"loaded={self._loaded}, "
            f"words={len(self._words):,})"
        )
        
        
    def unload(self) -> bool:
        """Clear dictionary from memory. Python's GC handles this
        automatically, but explicit unload provides API symmetry
        with load().
        """
        self._words.clear()
        self._loaded = False
        return True
    
    
# Without dunder methods — works but verbose:
#   dictionary.check("hello")     # explicit method call
#   dictionary.size()              # explicit method call

# With dunder methods — idiomatic Python:
#   "hello" in dictionary          # __contains__ → calls check()
#   len(dictionary)                # __len__ → calls size()

# Both __len__ and __contains__ delegate to the Protocol methods (size()
# and check()). The logic lives in one place (DRY), but users get two interfaces
# — the explicit Protocol methods and the Pythonic dunder syntax.

# This is how Python's built-in types work: "hello" in my_set calls set.__contains__(),
# len(my_list) calls list.__len__(). Your class follows the same pattern.