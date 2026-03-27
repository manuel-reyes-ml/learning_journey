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

from abc import ABC, abstractmethod
import bisect   # Binary Search
from pathlib import Path
import logging

from speller.config import MAX_WORD_LENGTH
from speller.register import register_class

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
    "HashTableDictionary", 
    "ListDictionary"
]


# =============================================================================
# ABSTRACT BASE CLASS — Shared Implementation
# =============================================================================

class _BaseDictionary(ABC):  # shared implementation 
    """Shared spell-check dictionary logic.

    Underscore prefix because this class is INTERNAL — external code
    uses HashTableDictionary or ListDictionary, never _BaseDictionary
    directly. It exists solely to eliminate code duplication.

    Subclasses MUST implement:
    - _create_container() → return the empty container (set or list)
    - _add_word(word)     → add a word to the container

    Everything else is inherited: load, check, size, dunders, unload.

    Why ABC and not just a regular parent class?
    ---------------------------------------------
    ABC with @abstractmethod prevents accidental instantiation:
        _BaseDictionary()  → TypeError (can't instantiate ABC)

    It also FORCES subclasses to implement the required methods:
        class BadDict(_BaseDictionary):
            pass
        BadDict()  → TypeError: Can't instantiate, missing _add_word

    Without ABC, you'd get a confusing AttributeError at RUNTIME
    when _add_word is called. With ABC, you get a clear TypeError
    at INSTANTIATION time — fail fast.

    Template Method Pattern
    -----------------------
    load() is the "template method" — it defines the algorithm:
        1. Check file exists
        2. Open file
        3. For each line: strip, validate, call _add_word()
        4. Set _loaded flag

    _add_word() is the "hook" — subclasses fill in the variable step.
    The algorithm stays the same; only the storage mechanism changes.

    Attributes
    ----------
    _words : set[str] or list[str]
        Created by subclass via _create_container().
    _loaded : bool
        Tracks whether load() has been called successfully.
    """
    
    def __init__(self) -> None:
        self._words = self._create_container()
        self._loaded: bool = False
        
        
    # =================================================================
    # ABSTRACT METHODS — Subclasses MUST implement these
    # =================================================================
    
    @abstractmethod
    def _create_container(self) -> set[str] | list[str]:
        """Create the empty word container.

        Returns
        -------
        set[str] or list[str]
            Empty container for storing dictionary words.
            HashTableDictionary returns set().
            ListDictionary returns [].
        """
        ...
        
        
    @abstractmethod
    def _add_word(self, word: str) -> None:
        """Add a word to the container.

        Parameters
        ----------
        word : str
            Lowercase word to store.
            HashTableDictionary calls self._words.add(word).
            ListDictionary calls self._words.append(word).
        """
        ...
        
        
    # =================================================================
    # CONCRETE METHODS — Shared by ALL subclasses (inherited as-is)
    # =================================================================
    
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
                    
                    self._add_word(word.lower())  # ← calls subclass method
        
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
    

# =============================================================================
# CONCRETE IMPLEMENTATIONS — Only the parts that differ
# =============================================================================

# Notice that dictionary.py imports DictionaryProtocol. It doesn't need to for
# the class builder. We use it here and on speller.py for type hints. 

@register_class(
    "hash",
    "Use Set as hash table - O(1) average lookup.",
)
class HashTableDictionary(_BaseDictionary):  # inherits from ABC
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
    
    def _create_container(self) -> set[str]:
        return set()
    
    
    def _add_word(self, word: str) -> None:
        return self._words.add(word)
    
    # satisfies Protocol via inherited methods
 

@register_class(
    "list",
    "Use a List - O(n) linear search lookup.",
)
class ListDictionary(_BaseDictionary):  # inherits from ABC
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
    
    def _create_container(self) -> list[str]:
        return []
    
    
    def _add_word(self, word: str) -> None:
        return self._words.append(word)

    # satisfies Protocol via inherited methods


# WHEN ADDING A Dictionary: Three lines for the container, and an override for check()
# — everything else is inherited. The @register_class decorator automatically adds it
# to the registry. The CLI immediately supports -o sorted without any changes to
# __main__.py, speller.py, or protocols.py.
#
# That's the power of Protocol + ABC + Registry working together.
@register_class(
    "sorted",
    "Use sorted list - O(log n) binary search lookup.",
)
class SortedListDictionary(_BaseDictionary):
    """
    """
    
    def _create_container(self) -> list[str]:
        return []
    
    
    def _add_word(self, word: str) -> None:
        bisect.insort(self._words, word)  # insert in sorted order
        
        
    def check(self, word: str) -> bool:
        """Override base check() to use binary search instead of 'in'."""
        if not self._loaded:
            raise RuntimeError(
                "Dictionary not loaded. Call load() before check()."
            ) 
        normalized = word.lower()
        
        # ── bisect_left: "Where would this value go?" ──
        # Returns the INDEX where the value would be inserted
        # to keep the list sorted. If the value exists, returns
        # the position BEFORE (left of) the existing entry.
        i = bisect.bisect_left(self._words, normalized)
        
        return i < len(self._words) and self._words[i] == normalized
        #      ↑                        ↑
        #      BOUNDS CHECK              VALUE CHECK
        #      "is i within the list?"   "is the word actually there?"

        # Without bounds check:
        # bisect_left(["ant", "bat"], "zebra") → returns 2
        # self._words[2] → IndexError! (list only has indices 0, 1)

        # Without value check:
        # bisect_left(["ant", "cat"], "bat") → returns 1
        # self._words[1] → "cat" (not "bat"!)
        # bisect tells you where "bat" WOULD go, not that it EXISTS



# =============================================================================
# REFERENCE GUIDES
# =============================================================================

# The relationship:
#   Protocol:  speller.py says "I need load/check/size"
#   ABC:       dictionaries.py says "here's shared code for my classes"
#   Both:      HashTableDictionary satisfies Protocol AND inherits from ABC
#
#   Protocol is HORIZONTAL (any class, anywhere, can satisfy it)
#   ABC is VERTICAL (only YOUR subclasses inherit from it)

# =====================================================
# What stays the SAME (goes in ABC):
# =====================================================
# - File reading (open, strip, skip empty, skip long)
# - _loaded guard in check()
# - word.lower() normalization
# - __len__, __contains__, __repr__, unload
# - Error handling (OSError)
# - Logging

# =====================================================
# What DIFFERS (abstract methods for subclasses):
# =====================================================
# - Container type:  set() vs []
# - Add a word:      .add() vs .append()
# - That's it. Two lines of difference in 300+ lines.


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

# =====================================================
# What BISECT does:
# =====================================================
# bisect finds where a value belongs in a sorted list using binary search — O(log n) instead of O(n).
#┌─────────────────────────────────────────────────────────────────┐
#│              LINEAR SEARCH vs BINARY SEARCH                      │
#│─────────────────────────────────────────────────────────────────│
#│                                                                  │
#│  Sorted list: [apple, banana, cherry, dog, elephant, fish, grape]│
#│  Looking for: "dog"                                              │
#│                                                                  │
#│  LINEAR SEARCH (word in my_list):                                │
#│    Check "apple"    → no                                         │
#│    Check "banana"   → no                                         │
#│    Check "cherry"   → no                                         │
#│    Check "dog"      → YES! (4 comparisons)                       │
#│    Worst case: check ALL 143,091 words → O(n)                    │
#│                                                                  │
#│  BINARY SEARCH (bisect):                                         │
#│    Middle = "dog"   → FOUND! (1 comparison)                      │
#│    But usually:                                                   │
#│    Middle = "cherry" → "dog" > "cherry" → search RIGHT half      │
#│    Middle = "fish"   → "dog" < "fish"   → search LEFT half       │
#│    Middle = "dog"    → FOUND! (3 comparisons)                    │
#│    Worst case: log₂(143,091) = ~17 comparisons → O(log n)       │
#│                                                                  │
#│  143,091 comparisons vs 17 comparisons.                          │
#└─────────────────────────────────────────────────────────────────┘

# sorted_list = [10, 20, 30, 40, 50]

# ── bisect_left: "Where would this value go?" ──
# Returns the INDEX where the value would be inserted
# to keep the list sorted. If the value exists, returns
# the position BEFORE (left of) the existing entry.

# bisect.bisect_left(sorted_list, 30)    # → 2 (30 is at index 2)
# bisect.bisect_left(sorted_list, 25)    # → 2 (25 would go before 30)
# bisect.bisect_left(sorted_list, 5)     # → 0 (5 would go at the start)
# bisect.bisect_left(sorted_list, 99)    # → 5 (99 would go at the end)

# ── bisect_right: same but position AFTER existing entry ──
# bisect.bisect_right(sorted_list, 30)   # → 3 (after the existing 30)

# ── insort: INSERT and keep sorted ──
# Equivalent to: find position + list.insert()
# but done in one step
# bisect.insort(sorted_list, 25)
# sorted_list is now [10, 20, 25, 30, 40, 50]

# How SortedListDictionary._add_word uses insort:

# self._words = []

# bisect.insort(self._words, "dog")     # [dog]
# bisect.insort(self._words, "ant")     # [ant, dog]
# bisect.insort(self._words, "cat")     # [ant, cat, dog]
# bisect.insort(self._words, "bat")     # [ant, bat, cat, dog]

# insort = bisect_left + list.insert in one call
# The list stays sorted after every insertion
# No need to sort() at the end


## Performance Comparison for Your Speller

# Dictionary: 143,091 words
# Text: aca.txt (376,904 word checks)

# ┌──────────────────────┬───────────────┬────────────────────────┐
# │ Backend              │ check() cost  │ Total checks (376K)    │
# │──────────────────────┼───────────────┼────────────────────────│
# │ HashTableDictionary  │ O(1)          │ 376,904 operations     │
# │ (set — hash table)   │ ~1 comparison │ Fast                   │
# │──────────────────────┼───────────────┼────────────────────────│
# │ SortedListDictionary │ O(log n)      │ 376,904 × 17 steps    │
# │ (sorted list)        │ ~17 compares  │ = ~6.4M comparisons    │
# │──────────────────────┼───────────────┼────────────────────────│
# │ ListDictionary       │ O(n)          │ 376,904 × 143,091     │
# │ (unsorted list)      │ ~143K compares│ = ~53 BILLION compares │
# └──────────────────────┴───────────────┴────────────────────────┘

# hash:   seconds
# sorted: noticeably slower
# list:   minutes to hours (O(n) × O(n) = O(n²))