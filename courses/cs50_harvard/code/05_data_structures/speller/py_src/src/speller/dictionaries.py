"""Dictionary backends for the speller package.

Provides four concrete implementations of ``DictionaryProtocol``, all
built on the ``_BaseDictionary`` abstract base class:

- :class:`HashTableDictionary`  — ``set``-backed, O(1) average lookup.
- :class:`ListDictionary`       — unsorted ``list``-backed, O(n) lookup.
- :class:`SortedListDictionary` — sorted ``list`` + binary search, O(log n).
- :class:`DictDictionary`       — ``dict[str, None]``-backed, O(1) average lookup.

Each class is registered automatically at import time via the
``@register_class`` decorator.  ``__main__.py`` selects the active
backend by registry key (``"hash"``, ``"list"``, ``"sorted"``, ``"dict"``).

Template Method Pattern
-----------------------
``_BaseDictionary`` defines the algorithm skeleton in ``load()`` and
``check()``.  Subclasses supply only the two variable steps:

    _create_container() → returns the empty container (set, list, or dict)
    _add_word(word)     → inserts a word into that container

Everything else — file reading, case normalisation, guards, dunders,
logging — is inherited unchanged.

Generic[WordContainer]
----------------------
``_BaseDictionary`` is parameterised over ``WordContainer``, a
``TypeVar`` constrained to ``set[str]``, ``list[str]``, or
``dict[str, None]``.  Subclasses specialise it
(e.g. ``_BaseDictionary[set[str]]``) so pyright tracks the exact
container type through every method without an invariance violation.

C → Python Mapping (HashTableDictionary)
-----------------------------------------
This module replaces CS50's ``dictionary.c``::

    C (dictionary.c)                Python (HashTableDictionary)
    ─────────────────               ────────────────────────────
    node *table[N]                  self._words: set[str]
    malloc(sizeof(node))            self._words.add(word)
    strcasecmp(word, node->word)    word.lower() in self._words
    free(node) in unload()          Garbage collector (automatic)
    hash(word[0])-'A' (26 buckets)  Python uses ~2× set size buckets

Module Dependencies
-------------------
    config.py     → MAX_WORD_LENGTH (constant)
    register.py   → register_class() (decorator), dicts (registry)
"""

# =============================================================================
# IMPORTS
# =============================================================================

from __future__ import annotations

import bisect  # Binary Search
import logging
from abc import ABC, abstractmethod
from pathlib import Path
from typing import override

# PEP 484, using Generic and TypeVar for parameter
# from typing import Generic, TypeVar
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
    "DictDictionary",
    "HashTableDictionary",
    "ListDictionary",
    "SortedListDictionary",
]


# =============================================================================
# MODULE CONFIGURATION
# =============================================================================
# =====================================================
# Constants
# =====================================================

# PEP 484
# Constrained TypeVar: exactly set[str], list[str], or dict[str, None] — nothing else.
# Adding dict[str, None] enables DictDictionary: O(1) key lookup using None as a
# zero-cost sentinel value (None is a singleton — no new objects allocated per entry).
#   WordContainer = TypeVar("WordContainer", set[str], list[str], dict[str, None])

# A plain TypeVar says "any type at all." The bound= argument adds a constraint:
# "any type, as long as it's a subclass of this."
# T = TypeVar("T")              # accepts literally anything
# T = TypeVar("T", bound=int)   # accepts int, bool, or any subclass of int
# rejects str, list, dict, etc.

# PEP 695
# Bounded (single type): [T: Number]  -> T must be Number or a subclass
# Constrained (multiple types): [T: (set[str], list[str])]   -> T must be exactly one of these types


# =============================================================================
# ABSTRACT BASE CLASS — Shared Implementation
# =============================================================================

# PEP 484
# Generic[WordContainer] means: "_BaseDictionary is parameterised over WordContainer.
# Each sublcass declares what WordContainer resolves to. Pyright tracks WordContainer
# through the entire class - no invariance violation"
#
# PEP 695
# Stop using Generic[] and TypeVar. The Type parameter WordContainer is now scoped to
# the class itself — declared in the brackets after the class name.
#
# class _BaseDictionary[WordContainer: set[str] | list[str] | dict[str, None]](ABC):
# The wrong version above looks similar but means something different — it would mean
# WordContainer must be a subtype of the union, which type-checkers handle differently
# than constraints. Constraints force the type to be exactly one of the listed options;
# bounds allow subclasses.
class _BaseDictionary[WordContainer: (set[str], list[str], dict[str, None])](ABC):  # shared implementation
    """Shared spell-check dictionary logic.

    Underscore prefix because this class is INTERNAL — external code
    uses HashTableDictionary or ListDictionary, never _BaseDictionary
    directly. It exists solely to eliminate code duplication.

    Subclasses MUST implement:
    - _create_container() → return the empty container (set, list, or dict)
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
    _words : WordContainer
        Typed as the constrained ``TypeVar`` ``WordContainer``
        (``set[str]``, ``list[str]``, or ``dict[str, None]``).
        The concrete type is determined by the subclass at
        specialisation time (e.g. ``_BaseDictionary[set[str]]``
        → ``_words`` is ``set[str]``).  Created by
        :meth:`_create_container`.
    _loaded : bool
        Set to ``True`` after :meth:`load` completes successfully.
        Guards :meth:`check` and :meth:`size` against use before
        the dictionary has been populated.

    Type Parameters
    ---------------
    WordContainer : TypeVar
        Constrained to ``set[str]``, ``list[str]``, or
        ``dict[str, None]``.  Resolved once per subclass — pyright
        propagates the concrete type through every inherited method.
    """

    def __init__(self) -> None:
        """Initialise the word container and loaded flag.

        Called automatically by Python when a subclass is instantiated.
        Delegates container creation to the abstract
        :meth:`_create_container` so each subclass controls its own
        storage type while sharing this initialisation logic.

        Notes
        -----
        ``_words`` is typed as ``WordContainer`` — the constrained
        ``TypeVar`` is resolved by the subclass declaration
        (``_BaseDictionary[set[str]]`` or ``_BaseDictionary[list[str]]``),
        giving pyright full visibility of the concrete container type
        without an invariance violation.
        """
        self._words: WordContainer = self._create_container()
        self._loaded: bool = False

    def _ensure_loaded(self) -> None:
        """Raise ``RuntimeError`` if the dictionary has not been loaded.

        Centralises the guard logic so every method that requires a
        populated dictionary calls one line instead of duplicating the
        ``if not self._loaded`` check.  Fail-fast principle: an
        informative error at the call site beats a silent wrong answer.

        Raises
        ------
        RuntimeError
            If :meth:`load` has not been called, or if it returned
            ``False`` (load failed).

        Examples
        --------
        Called at the top of :meth:`check` and
        :meth:`SortedListDictionary.check`::

            def check(self, word: str) -> bool:
                self._ensure_loaded()   # raises here if not ready
                return word.lower() in self._words
        """
        if not self._loaded:
            raise RuntimeError("Dictionary not loaded. Call load() before check().")

    # =================================================================
    # ABSTRACT METHODS — Subclasses MUST implement these
    # =================================================================

    # The key insight: WordContainer is resolved once per instance, not once per
    # method call. Every method on that instance sees the same WordContainer.

    @abstractmethod
    def _create_container(self) -> WordContainer:
        """Create the empty word container.

        Returns
        -------
        set[str] or list[str] or dict[str, None]
            Empty container for storing dictionary words.
            HashTableDictionary  returns ``set()``.
            ListDictionary       returns ``[]``.
            SortedListDictionary returns ``[]``.
            DictDictionary       returns ``{}``.
        """
        ...

    @abstractmethod
    def _add_word(self, word: str) -> None:
        """Add a word to the container.

        Parameters
        ----------
        word : str
            Lowercase word to store.
            HashTableDictionary  calls ``self._words.add(word)``.
            ListDictionary       calls ``self._words.append(word)``.
            SortedListDictionary calls ``bisect.insort(self._words, word)``.
            DictDictionary       calls ``self._words[word] = None``.
        """
        ...

    # =================================================================
    # CONCRETE METHODS — Shared by ALL subclasses (inherited as-is)
    # =================================================================

    def load(self, filepath: str) -> bool:
        """Load a dictionary file into the word container.

        Reads the file line by line, strips whitespace, skips empty
        lines and words longer than ``MAX_WORD_LENGTH``, converts each
        valid word to lowercase, then delegates insertion to the
        abstract :meth:`_add_word`.  Uses a ``with`` block to guarantee
        the file handle is closed even if an error occurs.

        Parameters
        ----------
        filepath : str
            Path to the dictionary file.  One word per line.
            CS50\'s default is ``dictionaries/large`` (143,091 words).

        Returns
        -------
        bool
            ``True`` if the dictionary loaded successfully,
            ``False`` if the file was not found or could not be read.

        Notes
        -----
        Why lowercase on load?
            Storing words in lowercase means :meth:`check` only needs
            to normalise the incoming word once — ``word.lower() in
            self._words`` — regardless of the mixed-case text input.

        Why ``Path(filepath)`` wrapping?
            :class:`pathlib.Path` provides ``.exists()``,
            ``.name``, and consistent cross-platform path handling.
            The ``filepath: str`` signature matches
            ``DictionaryProtocol`` for compatibility; conversion to
            ``Path`` is an internal detail.

        Why catch ``OSError`` rather than ``FileNotFoundError``?
            ``OSError`` is the parent of ``FileNotFoundError``,
            ``PermissionError``, ``IsADirectoryError``, and others.
            A single ``except OSError`` handles every file-system
            failure mode — disk full, bad permissions, wrong type —
            which matters in Stage 2 production pipelines.

        Why skip words longer than ``MAX_WORD_LENGTH``?
            Matches CS50\'s ``#define LENGTH 45``.  The text processor
            also enforces this limit so long tokens are never passed to
            :meth:`check`.
        """

        path = Path(filepath)

        if not path.exists():
            logger.error("Dictionary file not found: %s", path)
            return False

        try:
            # Context manager guarantees file.close() even if exception occurs.
            # encoding="utf-8" is explicit - never rely on platform default.
            with open(path, encoding="utf-8") as dict_file:
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
            "Loaded %s words from '%s'",
            format(
                len(self._words), ","
            ),  # format number to use ',' separator and return str
            path.name,
        )
        return True

    def check(self, word: str) -> bool:
        """Check if a word exists in the loaded dictionary.

        Case-insensitive: ``"Hello"``, ``"HELLO"``, and ``"hello"``
        all match a dictionary entry of ``"hello"`` because the lookup
        normalises the incoming word with ``.lower()``.

        Parameters
        ----------
        word : str
            The word to look up.  Case does not matter.

        Returns
        -------
        bool
            ``True`` if the normalised word is in the dictionary,
            ``False`` otherwise.

        Raises
        ------
        RuntimeError
            If called before :meth:`load` has been called successfully.
            Delegated to :meth:`_ensure_loaded` — fail fast rather
            than silently reporting every word as misspelled.

        Notes
        -----
        The lookup expression ``word.lower() in self._words`` resolves
        differently depending on the concrete ``WordContainer``:

        - ``set[str]``        → calls ``set.__contains__()``  → O(1) average
          (Python hashes the normalised word and checks the bucket).
        - ``list[str]``       → calls ``list.__contains__()`` → O(n) linear
          scan (used only by :class:`ListDictionary` as a benchmark).
        - ``dict[str, None]`` → calls ``dict.__contains__()`` → O(1) average
          (checks keys only — the ``None`` values are never read).

        :class:`SortedListDictionary` overrides this method to use
        :func:`bisect.bisect_left` for O(log n) lookup instead of the
        linear ``in`` operator.

        Why raise instead of returning ``False`` when not loaded?
            Returning ``False`` silently would flag every word as
            misspelled.  A ``RuntimeError`` surfaces the bug immediately
            at the call site — the "fail fast" principle.
        """
        # Without this guard, an unloaded dictionary silently returns False
        # for every word — the entire text appears "misspelled."
        self._ensure_loaded()

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

        Delegates to :meth:`size` so the logic lives in one place (DRY).
        Defined in ``_BaseDictionary`` and inherited by all four
        concrete classes.

        Making ``__len__`` delegate to ``size()`` — rather than the
        reverse — preserves ``DictionaryProtocol`` compatibility:
        ``size()`` is the named Protocol method; ``__len__`` is the
        Pythonic sugar that wraps it.

        Returns
        -------
        int
            Number of words currently loaded in the dictionary.

        Notes
        -----
        Satisfies ``collections.abc.Sized`` — any object with
        ``__len__`` works with Python\'s built-in ``len()``.

        Roadmap relevance:
            - DataVault: ``len(results)`` on query-result objects.
            - PolicyPulse: ``len(chunks)`` on retrieval batches.
            - Stage 2 ETL: ``len(batch)`` on pipeline windows.
        """
        return self.size()

    def __contains__(self, word: str) -> bool:
        """Support ``word in dictionary`` — Pythonic interface.

        Delegates to :meth:`check` so the logic lives in one place (DRY).
        Defined in ``_BaseDictionary`` and inherited by all four
        concrete classes.  Enables the natural Python idiom::

            if word in dictionary:   # __contains__ → check()
                ...

        rather than the more verbose explicit call::

            if dictionary.check(word):
                ...

        Parameters
        ----------
        word : str
            Word to look up (case-insensitive, normalised in
            :meth:`check`).

        Returns
        -------
        bool
            ``True`` if the word is in the dictionary.

        Notes
        -----
        Satisfies ``collections.abc.Container``.  Combined with
        ``__len__``, the class also satisfies ``collections.abc.Sized``
        — together these are the two requirements for
        ``collections.abc.Collection``.
        """
        return self.check(word)

    # type(self).__name__ instead of hardcoding "HashTableDictionary" means
    # if someone subclasses your class, __repr__ automatically uses the subclass
    # name. The :, format specifier adds thousand separators (143,091 instead of 143091).
    def __repr__(self) -> str:
        """Developer-facing string representation.

        Uses ``type(self).__name__`` rather than a hard-coded class name
        so any future subclass automatically gets the correct label in
        logs and reprs.  The ``:,`` format specifier adds thousand
        separators for readability (``143,091`` instead of ``143091``).

        Returns
        -------
        str
            ``"ClassName(loaded=True, words=143,091)"``

        Notes
        -----
        Convention: ``__repr__`` targets developers (debugging, logging,
        interactive shell); ``__str__`` targets end users (print,
        display).  Only ``__repr__`` is defined here because the
        developer view is sufficient — Python falls back to ``__repr__``
        when ``__str__`` is absent.
        """
        return (
            f"{type(self).__name__}(loaded={self._loaded}, words={len(self._words):,})"
        )

    def unload(self) -> bool:
        """Clear the dictionary from memory and reset the loaded flag.

        Returns
        -------
        bool
            Always ``True`` — provided for API symmetry with
            :meth:`load`.

        Notes
        -----
        Python's garbage collector reclaims the memory automatically
        once ``self._words`` is cleared, so explicit unloading is not
        required for correctness.  This method exists to match CS50\'s
        ``unload()`` function signature and to give callers a clear
        way to signal intent when reloading with a different dictionary
        file in the same process.
        """
        self._words.clear()
        self._loaded = False
        return True


# =============================================================================
# CONCRETE IMPLEMENTATIONS — Only the parts that differ
# =============================================================================

# Notice that dictionary.py imports DictionaryProtocol. It doesn't need to for
# the class builder. We use it here and on speller.py for type hints.


# The moment you write `_BaseDictionary[set[str]]`, the type checker substitutes
# `set[str]` everywhere `WordContainer` appears in `_BaseDictionary`:
@register_class(
    "hash",
    "Use Set as hash table - O(1) average lookup.",
)
class HashTableDictionary(_BaseDictionary[set[str]]):  # inherits from ABC
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
        """Return an empty ``set`` — O(1) average lookup container."""
        return set()

    def _add_word(self, word: str) -> None:
        """Add ``word`` to the set via ``set.add()``."""
        self._words.add(word)

    # satisfies Protocol via inherited methods


@register_class(
    "list",
    "Use a List - O(n) linear search lookup.",
)
class ListDictionary(_BaseDictionary[list[str]]):  # inherits from ABC
    """Spell-check dictionary backed by an unsorted Python ``list``.

    Satisfies ``DictionaryProtocol`` through structural typing — no
    inheritance required.  Stores words in insertion order and uses
    Python\'s linear ``in`` operator for lookup.

    This implementation exists as a **performance baseline** to
    demonstrate the O(n) lookup cost relative to
    :class:`HashTableDictionary` (O(1)) and
    :class:`SortedListDictionary` (O(log n)).

    Attributes
    ----------
    _words : list[str]
        Unsorted word store.  Order follows the dictionary file —
        typically alphabetical for CS50\'s word lists, but not
        guaranteed.
    _loaded : bool
        Set to ``True`` after :meth:`load` completes successfully.

    Examples
    --------
    >>> dictionary = ListDictionary()
    >>> dictionary.load("dictionaries/small")
    True
    >>> dictionary.check("cat")
    True
    >>> dictionary.check("xyz")
    False

    Notes
    -----
    Performance (143,091 words, 376,904 checks against ``aca.txt``):

    .. code-block:: text

        Backend               check() cost   Total checks (376 K)
        ────────────────────  ─────────────  ─────────────────────
        HashTableDictionary   O(1)           ~376 K comparisons
        SortedListDictionary  O(log n)       ~6.4 M comparisons
        ListDictionary        O(n)           ~53 B comparisons  ← this class

    Use ``ListDictionary`` only to observe and measure linear-search
    cost — never in production.
    """

    def _create_container(self) -> list[str]:
        """Return an empty ``list`` — O(n) linear-search container."""
        return []

    def _add_word(self, word: str) -> None:
        """Append ``word`` to the list in insertion order."""
        self._words.append(word)

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
class SortedListDictionary(_BaseDictionary[list[str]]):
    """Spell-check dictionary backed by a sorted ``list`` with binary search.

    Stores words in ascending alphabetical order using
    :func:`bisect.insort` during :meth:`load`, then uses
    :func:`bisect.bisect_left` for O(log n) lookup in an overridden
    :meth:`check`.

    Satisfies ``DictionaryProtocol`` through structural typing.

    Attributes
    ----------
    _words : list[str]
        Sorted word store.  :func:`bisect.insort` maintains ascending
        order on every insertion during :meth:`load`.
    _loaded : bool
        Set to ``True`` after :meth:`load` completes successfully.

    Examples
    --------
    >>> dictionary = SortedListDictionary()
    >>> dictionary.load("dictionaries/large")
    True
    >>> dictionary.check("hello")
    True
    >>> dictionary.check("xyz")
    False

    Notes
    -----
    Trade-off vs :class:`HashTableDictionary`:

    - **Load** — O(n log n): ``bisect.insort`` pays a logarithmic cost
      per insertion to maintain sorted order.  ``set.add()`` is O(1).
    - **Check** — O(log n): ~17 comparisons for 143 K words vs O(1)
      for the hash table, but orders of magnitude faster than
      :class:`ListDictionary`\'s O(n) linear scan.
    - **Memory** — ``list`` is slightly more compact than ``set``
      (no hash-table overhead), but the difference is negligible here.

    Prefer this backend when ordered iteration over the word list is
    required, or as a teaching example for binary search mechanics.
    """

    def _create_container(self) -> list[str]:
        """Return an empty ``list`` — maintained in sorted order by ``_add_word``."""
        return []

    def _add_word(self, word: str) -> None:
        """Insert ``word`` in alphabetical order via :func:`bisect.insort`."""
        bisect.insort(self._words, word)  # insert in sorted order

    # Override the parent's check method
    # Apply override decorator to a subclass method that overrides a base class method.
    # Static type checkers will warn if the base class is modified such that the overridden method
    # no longer exists — avoiding accidentally turning a method override into dead code.
    @override
    def check(self, word: str) -> bool:
        """Check if a word exists using binary search — O(log n).

        Overrides :meth:`_BaseDictionary.check` to replace the linear
        ``in`` operator with :func:`bisect.bisect_left` on the sorted
        word list.

        Parameters
        ----------
        word : str
            The word to look up.  Case-insensitive: normalised to
            lowercase before the search.

        Returns
        -------
        bool
            ``True`` if the normalised word is found, ``False``
            otherwise.

        Raises
        ------
        RuntimeError
            If called before :meth:`load` has been called successfully.
            Delegated to :meth:`_ensure_loaded`.

        Notes
        -----
        Two conditions are required for a successful lookup:

        1. **Bounds check** — ``bisect_left`` returns
           ``len(self._words)`` when the target exceeds every element.
           Without ``i < len(self._words)``, the next line would raise
           :class:`IndexError`.

        2. **Value check** — ``bisect_left`` returns the *insertion
           position*, not a confirmation of presence.
           ``self._words[i] == normalized`` verifies the word actually
           exists at that position::

               sorted_list = ["ant", "cat", "dog"]
               bisect_left(sorted_list, "bat")   # → 1 (insert here)
               sorted_list[1]                    # → "cat"  (not "bat"!)
        """
        # Without this guard, an unloaded dictionary silently returns False
        # for every word — the entire text appears "misspelled."
        self._ensure_loaded()

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


@register_class(
    "dict",
    "Use Dictionary as hash table - O(1) average lookup.",
)
class DictDictionary(_BaseDictionary[dict[str, None]]):  # inherits from ABC
    """Spell-check dictionary backed by a Python ``dict[str, None]``.

    Satisfies ``DictionaryProtocol`` through structural typing — no
    inheritance required.  Stores words as **keys** with ``None`` as
    the value, exploiting the fact that ``word in my_dict`` checks
    keys only.  Lookup is O(1) average — identical algorithmic
    complexity to :class:`HashTableDictionary`.

    Why ``dict[str, None]`` and not ``set[str]``?
    ----------------------------------------------
    This backend demonstrates an important Python memory concept:
    using a dict as a set-like structure with an explicit sentinel
    value.  ``None`` is a **singleton** — Python creates it once at
    interpreter start and reuses the same object everywhere.  Every
    value slot in the dict holds a pointer to that single ``None``
    rather than allocating a new object per entry.

    Memory comparison for 143,091 words:

    .. code-block:: text

        Container          Approx memory    Per-entry overhead
        ─────────────────  ─────────────    ──────────────────
        set[str]           ~8–12 MB         key + hash only
        dict[str, None]    ~16–20 MB        key + hash + pointer to None (singleton)
        dict[str, str]     ~20–25 MB        key + hash + new str object per entry

    The ``set[str]``-backed :class:`HashTableDictionary` is more
    memory-efficient for pure membership testing.  Use
    ``DictDictionary`` when you want to understand the dict-vs-set
    trade-off, or as a foundation for backends that store
    **meaningful** values (e.g. part-of-speech tags, confidence
    scores, or frequency counts) without restructuring the hierarchy.

    Attributes
    ----------
    _words : dict[str, None]
        Word store keyed by lowercase word.  All values are ``None``
        — the dict is used purely for O(1) key-membership testing.
        Private (underscore prefix) because external code should call
        :meth:`check`, not access ``_words`` directly.
    _loaded : bool
        Set to ``True`` after :meth:`load` completes successfully.

    Examples
    --------
    >>> dictionary = DictDictionary()
    >>> dictionary.load("dictionaries/large")
    True
    >>> dictionary.size()
    143091
    >>> dictionary.check("hello")
    True
    >>> dictionary.check("xyz")
    False
    >>> "hello" in dictionary          # __contains__ → check()
    True

    Notes
    -----
    **Algorithmic equivalence to** :class:`HashTableDictionary`:

    Both ``set.__contains__()`` and ``dict.__contains__()`` compute a
    hash of the key and probe the internal hash table — O(1) average.
    In practice :class:`HashTableDictionary` is faster and uses half
    the memory because a ``set`` has no value slots.

    **When dict values become meaningful (Stage 3+ pattern)**::

        # Stage 3 — ML-powered spell correction with confidence scores
        class MLDictionary(_BaseDictionary[dict[str, float]]):
            def _add_word(self, word: str) -> None:
                self._words[word] = model.confidence(word)

            def check(self, word: str) -> bool:
                self._ensure_loaded()
                score = self._words.get(word.lower(), 0.0)
                return score >= CONFIDENCE_THRESHOLD

    That evolution requires only a new subclass — ``_BaseDictionary``,
    ``speller.py``, and ``protocols.py`` are unchanged.
    """

    def _create_container(self) -> dict[str, None]:
        """Return an empty ``dict[str, None]`` — O(1) key-lookup container."""
        return {}

    def _add_word(self, word: str) -> None:
        """Store ``word`` as a key with ``None`` sentinel value."""
        self._words[word] = None

    # satisfies Protocol via inherited methods


# A singleton is an object that exists exactly once in memory. No matter how many
# times you reference it, you always get the same object--Python never creates
# a second copy.

# Python creates None once when the interpreter starts, stores it at a fixed memory
# address, and reuses that address everywhere. When you write None anywhere in your code,
# Python doesn't allocate anything — it just hands back the pointer it already has.

# When you build a 143,091-word dictionary:
# dict[str, str] with ""
#   words = {"cat": "", "dog": "", "bird": ""}
# Python allocates: 3 string keys + 3 string values ("" objects)
# Even though "" looks empty, it's still a str object in memory

# dict[str, None]
#   words = {"cat": None, "dog": None, "bird": None}
# Python allocates: 3 string keys + 0 new objects
# All three values point to the ONE None that already exists
# With 143,091 entries, dict[str, None] avoids creating 143,091 empty string objects.
# Each value slot holds a pointer to the same None that was already there.


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
# ┌─────────────────────────────────────────────────────────────────┐
# │              LINEAR SEARCH vs BINARY SEARCH                      │
# │─────────────────────────────────────────────────────────────────│
# │                                                                  │
# │  Sorted list: [apple, banana, cherry, dog, elephant, fish, grape]│
# │  Looking for: "dog"                                              │
# │                                                                  │
# │  LINEAR SEARCH (word in my_list):                                │
# │    Check "apple"    → no                                         │
# │    Check "banana"   → no                                         │
# │    Check "cherry"   → no                                         │
# │    Check "dog"      → YES! (4 comparisons)                       │
# │    Worst case: check ALL 143,091 words → O(n)                    │
# │                                                                  │
# │  BINARY SEARCH (bisect):                                         │
# │    Middle = "dog"   → FOUND! (1 comparison)                      │
# │    But usually:                                                   │
# │    Middle = "cherry" → "dog" > "cherry" → search RIGHT half      │
# │    Middle = "fish"   → "dog" < "fish"   → search LEFT half       │
# │    Middle = "dog"    → FOUND! (3 comparisons)                    │
# │    Worst case: log₂(143,091) = ~17 comparisons → O(log n)       │
# │                                                                  │
# │  143,091 comparisons vs 17 comparisons.                          │
# └─────────────────────────────────────────────────────────────────┘

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
# │ DictDictionary       │ O(1)          │ 376,904 operations     │
# │ (dict[str, None])    │ ~1 comparison │ Fast (2× memory of set)│
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

# =====================================================
# Built-in Singletons
# =====================================================
# None   # the absence of a value
# True   # boolean true
# False  # boolean false

# All three: always use `is` to check, never `==`
# if x is None: ...    # correct
# if x == None: ...    # works but wrong style — mypy will warn you
