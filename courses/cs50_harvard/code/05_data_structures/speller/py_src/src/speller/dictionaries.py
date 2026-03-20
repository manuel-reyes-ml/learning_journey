"""
"""

# =============================================================================
# IMPORTS
# =============================================================================

from __future__ import annotations

from pathlib import Path
import logging

from speller.config import MAX_WORD_LENGTH

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

__all__ = ["HashTableDictionary"]


# Notice that dictionary.py never imports DictionaryProtocol. It doesn't need to.
# The module that uses the protocol (speller.py) imports it for type hints. 

class HashTableDictionary:
    """
    """
    def __init__(self) -> None:
        self._words: set[str] = set()
        self._loaded: bool = False
        
        
    def load(self, filepath: str) -> bool:
        """
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
        """
        """
        # Without this guard, an unloaded dictionary silently returns False
        # for every word — the entire text appears "misspelled."
        if not self._loaded:
            raise RuntimeError(
                "Dictionary not loaded. Call load() before check()."
            )
        
        return word.lower() in self._words
    
    
    def size(self) -> int:
        """
        """
        return len(self._words)
    
    
    def __len__(self) -> int:
        """
        """
        return self.size()
    
    
    def __contains__(self, word: str) -> bool:
        """
        """
        return self.check(word)
    
    # type(self).__name__ instead of hardcoding "HashTableDictionary" means
    # if someone subclasses your class, __repr__ automatically uses the subclass
    # name. The :, format specifier adds thousand separators (143,091 instead of 143091).
    def __repr__(self) -> str:
        """
        """
        return (
            f"{type(self).__name__}("
            f"loaded={self._loaded}, "
            f"words={len(self._words):,}"
        )
        
        
    def unload(self) -> bool:
        """
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