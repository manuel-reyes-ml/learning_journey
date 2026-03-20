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

__all__ = []



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
                    
        except OSError as e:
            # OSError catches file permission errors, encoding errors, etc.
            # More specific than bare Exception, broader than FileNotFoundError.
            logger.error("Failed to read dictionary '%s': %s", path, e)
            return False
        
        self._loaded = True
        logger.info(
            "Loaded %d words from '%s'",
            len(self._words),
            path.name,
        )
        return True
        