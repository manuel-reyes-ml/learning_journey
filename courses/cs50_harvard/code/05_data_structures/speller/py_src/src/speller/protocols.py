"""Protocol definitions for spell-checker components.

Protocols define structural interfaces (contracts) — any class that
implements the required methods satisfies the protocol automatically.
No inheritance needed. This is Python's version of Go's interfaces
or TypeScript's structural typing.

This module sits at the BOTTOM of the dependency chain alongside
config.py — it has zero internal imports.

How Protocol works
------------------
1. Define a Protocol class with method signatures (this file)
2. Implement a concrete class with matching methods (dictionary.py)
3. Type-hint function parameters with the Protocol (speller.py)
4. mypy verifies at compile time that the concrete class satisfies it
5. @runtime_checkable adds isinstance() support for runtime checks

Why Protocol over ABC for my projects
----------------------------------------
- You can't make third-party classes inherit from YOUR base class
- ChromaDB, LangChain, OpenAI SDK all have their own class hierarchies
- Protocol says "I don't care what you ARE, I care what you CAN DO"
- This enables swappable backends without modifying existing code

My v8.1 projects that reuse this pattern
--------------------------------------------
- DataVault:    LLMProvider protocol (swap Gemini/OpenAI/Claude/Ollama)
- PolicyPulse:  VectorStore protocol (swap ChromaDB → Pinecone)
                EmbeddingProvider protocol (swap embedding models)
- FormSense:    ExtractionBackend protocol (swap Gemini Vision → custom)
- StreamSmart:  ContentAPI protocol (swap Watchmode → TMDB)
- AFC:          DataSource protocol (swap SEC/Wikipedia/news providers)

References
----------
.. [1] PEP 544 — Protocols: Structural subtyping (static duck typing)
   https://peps.python.org/pep-0544/
.. [2] Python Docs — typing.Protocol
   https://docs.python.org/3/library/typing.html#typing.Protocol
.. [3] mypy — Protocols and structural subtyping
   https://mypy.readthedocs.io/en/stable/protocols.html
"""

# =============================================================================
# IMPORTS
# =============================================================================

from __future__ import annotations

from typing import Protocol, runtime_checkable

# =============================================================================
# EXPORTS
# =============================================================================

__all__ = ["DictionaryProtocol"]


# =============================================================================
# DICTIONARY PROTOCOL — Core interface for spell-checking backends
# =============================================================================

# Protocols define structural interfaces (contracts) — any class that
# implements the required methods satisfies the protocol automatically.
# No inheritance needed. This is Python's version of Go's interfaces
# or TypeScript's structural typing.


@runtime_checkable
class DictionaryProtocol(Protocol):
    """Interface any dictionary backend must satisfy.

    Any class that implements load(), check(), and size() with matching
    signatures automatically satisfies this protocol — no inheritance needed.

    How this enables swappable backends
    ------------------------------------
    speller.py accepts DictionaryProtocol, not a concrete class.
    This means you can swap implementations without changing speller.py:

        # Today (Speller Stage 1): hash table backed by a set
        dictionary = HashTableDictionary()

        # Future (Stage 2): PostgreSQL-backed dictionary
        dictionary = DatabaseDictionary(connection_string)

        # Future (Stage 3): ML-powered spell correction
        dictionary = MLDictionary(model_path)

        # All three work with: run_speller(dictionary)
        # Because all three satisfy DictionaryProtocol

    Why @runtime_checkable?
    -----------------------
    Adds isinstance() support for runtime validation:

        if not isinstance(dictionary, DictionaryProtocol):
            raise TypeError("Expected a DictionaryProtocol implementation")

    Without @runtime_checkable, Protocol only works at mypy compile time.
    With it, you get BOTH compile-time AND runtime checks.

    Note: @runtime_checkable only checks method EXISTENCE, not signatures.
    Full signature checking happens at mypy compile time.
    """

    # The Rule: Protocol Contains What the CONSUMER Uses

    def load(self, filepath: str) -> bool:
        """Load dictionary from a source into memory.

        Parameters
        ----------
        filepath : str
            Path to the dictionary source (file, database URL, etc.).

        Returns
        -------
        bool
            True if dictionary was loaded successfully, False otherwise.
        """
        ...

    def check(self, word: str) -> bool:
        """Check if a word exists in the loaded dictionary.

        The check must be case-insensitive: "Hello", "HELLO", and "hello"
        should all match a dictionary entry of "hello".

        Parameters
        ----------
        word : str
            The word to look up.

        Returns
        -------
        bool
            True if the word is in the dictionary, False otherwise.
        """
        ...

    def size(self) -> int:
        """Return the number of words in the loaded dictionary.

        Returns
        -------
        int
            Word count if dictionary is loaded, 0 if not yet loaded.
        """
        ...

    def __len__(self) -> int:
        """Declare that implementations must support ``len(dictionary)``.

        Including ``__len__`` in the Protocol means pyright will flag
        any implementation that forgets to provide it, and any code
        that calls ``len(dictionary)`` on a ``DictionaryProtocol``
        variable gets a known return type instead of ``Any``.

        Returns
        -------
        int
            Number of words currently loaded.
        """
        ...

    def __contains__(self, word: str) -> bool:
        """Declare that implementations must support ``word in dictionary``.

        Including ``__contains__`` in the Protocol means pyright will
        flag any implementation that forgets to provide it, and the
        ``word in dictionary`` expression in ``run_speller()`` is
        fully type-safe against any ``DictionaryProtocol`` variable.

        Parameters
        ----------
        word : str
            The word to look up.

        Returns
        -------
        bool
            ``True`` if the word is present
        """
        ...

    def unload(self) -> bool:
        """Clear all words from memory and reset the loaded state.

        Releases the internal word container and resets any loaded
        flag so the instance can be reloaded with a different
        dictionary file in the same process.

        Returns
        -------
        bool
            ``True`` if the dictionary was cleared successfully.
            Implementations should always return ``True`` — provided
            for API symmetry with :meth:`load`.

        Notes
        -----
        Python's garbage collector reclaims memory automatically once
        the word container is cleared, so explicit unloading is not
        required for correctness.  This method exists to signal intent
        clearly when reloading a backend within the same process, and
        to satisfy type checkers that verify full Protocol compliance.

        Any call to :meth:`check` after ``unload()`` must raise
        :exc:`RuntimeError` — the same guard as before :meth:`load`
        is first called.
        """
        ...


# How Protocol works
# ------------------
# 1. Define a Protocol class with method signatures (this file)
# 2. Implement a concrete class with matching methods (dictionary.py)
# 3. Type-hint function parameters with the Protocol (speller.py)
# 4. mypy verifies at compile time that the concrete class satisfies it
# 5. @runtime_checkable adds isinstance() support for runtime checks
