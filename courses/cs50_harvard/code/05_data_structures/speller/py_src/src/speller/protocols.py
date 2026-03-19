"""
"""

# =============================================================================
# IMPORTS
# =============================================================================

from __future__ import annotations

from typing import Protocol, runtime_checkable


# =============================================================================
# DICTIONARY PROTOCOL — Core interface for spell-checking backends
# =============================================================================

@runtime_checkable
class DictionaryProtocol(Protocol):
    """
    """
    def load(self, filepath: str) -> bool:
        """
        """
        ...
        
    def check(self, word: str) -> bool:
        """
        """
        ...
    
    def size(self) -> int:
        """
        """
        ...
        

# Protocols define structural interfaces (contracts) — any class that
# implements the required methods satisfies the protocol automatically.
# No inheritance needed. This is Python's version of Go's interfaces
# or TypeScript's structural typing.

# How Protocol works
# ------------------
# 1. Define a Protocol class with method signatures (this file)
# 2. Implement a concrete class with matching methods (dictionary.py)
# 3. Type-hint function parameters with the Protocol (speller.py)
# 4. mypy verifies at compile time that the concrete class satisfies it
# 5. @runtime_checkable adds isinstance() support for runtime checks

# Why @runtime_checkable?
# -----------------------
# Adds isinstance() support for runtime validation:

#   if not isinstance(dictionary, DictionaryProtocol):
#       raise TypeError("Expected a DictionaryProtocol implementation")

# Without @runtime_checkable, Protocol only works at mypy compile time.
# With it, you get BOTH compile-time AND runtime checks.

# Note: @runtime_checkable only checks method EXISTENCE, not signatures.
# Full signature checking happens at mypy compile time.