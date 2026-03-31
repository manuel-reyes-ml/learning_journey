"""Text processor for extracting words from text files.

Implements the exact word extraction logic from CS50's ``speller.c``
as a Python generator. Yields words one at a time using constant
memory, regardless of file size.

This is a STATE MACHINE — it reads characters one at a time and
transitions between states based on what it encounters:

    SEEKING  →  found alpha char  →  BUILDING
    BUILDING →  found delimiter   →  yield word, back to SEEKING
    BUILDING →  found digit       →  consume alnum, discard, SEEKING
    BUILDING →  word too long     →  consume alpha, discard, SEEKING

C → Python Mapping
-------------------
    C (speller.c)                    Python (text_processor.py)
    ──────────────────               ──────────────────────────
    fread(&c, 1, 1, file)           content[pos]
    char word[LENGTH + 1]           word_chars: list[str]
    isalpha(c)                      char.isalpha()
    isdigit(c)                      char.isdigit()
    isalnum(c)                      char.isalnum()
    word[index] = '\\0'; words++    yield "".join(word_chars)

Module Dependencies
-------------------
    config.py → MAX_WORD_LENGTH (45, matches C's #define LENGTH 45)
"""

# =============================================================================
# IMPORTS
# =============================================================================

from __future__ import annotations

# Runtime collection types → collections.abc
from collections.abc import Iterator
import logging

from speller.config import MAX_WORD_LENGTH

# No ImportError sys.exit() on regular module so the
# error propagates to the caller (__main__.py).

## Simple Decision Rule
# "Is it a CONTAINER or CALLABLE type?"
#     YES → from collections.abc  (Generator, Iterator, Callable, Sequence, Mapping)

# "Is it a TYPE SYSTEM concept?"
#     YES → from typing  (Protocol, TypeVar, ParamSpec, Any, Final, TypedDict)


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

__all__ = ["extract_words"]


# =============================================================================
# INTERNAL HELPER FUNCTIONS
# =============================================================================

# The underscore prefix signals "internal to this module — not part of the public
# API." These functions aren't in __all__, so from speller.text_processor
# import * won't export them.

def _consume_alpha(content: str, pos: int, length: int) -> int:
    """Advance pos past remaining alphabetical characters.

    Replicates the C pattern::

        while (fread(&c, 1, 1, file) && isalpha(c));

    In C, this inner fread loop consumes the terminating non-alpha
    character too (the outer fread reads the char AFTER it). We
    replicate this by advancing one position past the last alpha.

    Parameters
    ----------
    content : str
        The full text content.
    pos : int
        Current position (should be first char to check).
    length : int
        Total length of content.

    Returns
    -------
    int
        New position pointing past all consumed alpha characters
        AND the terminating non-alpha character (matching C behavior).
    """
    while pos < length and content[pos].isalpha():
        pos += 1
        
    # Skip the terminating non-alpha character (matches C's fread
    # consumption: the inner loop reads the terminator, then the
    # outer loop's fread reads the NEXT char, so the terminator 
    # is effectively consumed/lost).
    if pos < length:
        pos += 1
    
    return pos


def _consume_alnum(content: str, pos: int, length: int) -> int:
    """Advance pos past remaining alphanumeric characters.

    Replicates the C pattern::

        while (fread(&c, 1, 1, file) && isalnum(c));

    Same terminator-consumption behavior as ``_consume_alpha``.

    Parameters
    ----------
    content : str
        The full text content.
    pos : int
        Current position (should be first char to check).
    length : int
        Total length of content.

    Returns
    -------
    int
        New position pointing past all consumed alnum characters
        AND the terminating character.
    """
    while pos < length and content[pos].isalnum():
        pos += 1
    
    if pos < length:
        pos += 1
        
    return pos


# =============================================================================
# CORE FUNCTIONS
# =============================================================================

def extract_words(content: str, path_name: str) -> Iterator[str]:
    """Extract words from a text file, matching CS50 speller.c behavior.

    Yields words one at a time using the generator pattern (constant
    memory for output, regardless of how many words the file contains).
    The full file content IS loaded into memory for character-level
    access — acceptable for CS50's text files. For truly streaming
    input (Stage 2 multi-GB files), you'd use chunked reading.

    Word extraction rules (matching speller.c exactly)
    ---------------------------------------------------
    1. Words consist of alphabetical characters and apostrophes
    2. Apostrophes are only valid MID-WORD (not at the start)
    3. Words containing ANY digit are skipped entirely
    4. Words longer than MAX_WORD_LENGTH (45) are skipped entirely
    5. Everything else (spaces, punctuation, newlines) is a delimiter

    Parameters
    ----------
    filepath : str or Path
        Path to the text file to process.

    Yields
    ------
    str
        Each valid word found in the text, preserving original case.
        Case normalization happens in dictionary.check(), not here.
        This matches speller.c where words are passed as-is to check().

    Raises
    ------
    FileNotFoundError
        If the text file does not exist.
    OSError
        If the text file cannot be read.

    Examples
    --------
    >>> list(extract_words("texts/cat.txt"))
    ['A', 'cat', 'is', 'not', 'a', 'caterpillar']

    Notes
    -----
    Why preserve original case?
        In CS50's speller.c, the word is printed in its original case
        when misspelled ("Bingley", not "bingley"). The check() function
        handles case-insensitive comparison. Separating extraction from
        normalization follows the single-responsibility principle.

    Why a generator (yield) instead of a list?
        - Constant memory: yields one word at a time, doesn't store all words
        - Composable: can chain with other generators (filter, transform)
        - Lazy: only extracts the next word when asked for it
        - This is the same streaming pattern used in LangChain for LLM tokens,
          PolicyPulse for RAG chunks, and PySpark for partition streaming

    Why load the full file with read() instead of reading char by char?
        - ``f.read(1)`` in a loop is extremely slow in Python (function call
          overhead per character, no buffering benefit)
        - ``f.read()`` loads the file once, then indexing ``content[pos]`` is
          a fast O(1) array access
        - CS50's test files are small (< 2MB). For Stage 2 multi-GB files,
          you'd read in fixed-size chunks instead
    """
    logger.debug("Extracting words from '%s'", path_name)
    
    length = len(content)
    pos = 0
    
    while pos < length:
        char = content[pos]
        
        # =============================================================
        # STATE: SEEKING — looking for the start of a word
        # =============================================================
        
        # --- Digit outside a word: consume remaining alnum, skip ---
        # Matches C: else if (isdigit(c)) { while(fread...isalnum); }
        # Example: "123abc" -> '1' triggers, consumes "23abc", skips all
        if char.isdigit():
            pos = _consume_alnum(content, pos + 1, length)
            continue
        
        # --- Non-alphabetical: skip (spaces, punctuation, etc.) ---
        if not char.isalpha():
            pos += 1
            continue
        
        # =============================================================
        # STATE: BUILDING — char is alphabetical, start building a word
        # =============================================================
        
        word_chars: list[str] = []
        valid = True
        
        while pos < length:
            char = content[pos]
            
            # --- Alphabetical character: append to word buffer ---
            if char.isalpha():
                word_chars.append(char)
                pos += 1
                
                # --- Too long: consume remaining alpha, discard ---
                # Matches C: if (index > LENGHT) { while(fread...isalpha); }
                if len(word_chars) > MAX_WORD_LENGTH:
                    pos = _consume_alpha(content, pos, length)
                    valid = False
                    break
                
            # --- Apostrophe mid-word: include in word ---
            # Matches C: (c == '\'' && index > 0)
            # word_chars being non-emty = index > 0
            elif char == "'" and word_chars:
                word_chars.append(char)
                pos += 1
                
            # --- Digit mid-word: consume remaining alnum, discard ---
            # Matches C: else if (isdigit(c)) { while(fread...isalnum); }
            # Example: "abc123def!" -> 'a','b','c' built, '1' triggers,
            #           consumes "23ded", '!' is consumed too, word discarded
            elif char.isdigit():
                pos = _consume_alnum(content, pos + 1, length)
                valid = False
                break
            
            # --- Any other character: word is completed ---
            # Matches C: else if (index > 0) { word[index] = '\0'; }
            else:
                break
            
        # Yield the word if it passed all validation
        if valid and word_chars:
            yield "".join(word_chars)
            
    logger.debug("Finished extracting words from '%s'", path_name)
    

# This is the first **state machine** in your portfolio.
# The function has two implicit states:

# ┌──────────┐    found alpha     ┌──────────┐
# │          │ ──────────────────→ │          │
# │ SEEKING  │                    │ BUILDING │
# │          │ ←────────────────── │          │
# └──────────┘  yield or discard  └──────────┘

# The outer while loop is in SEEKING state — scanning for the start
# of a word. Once it finds an alphabetical character, it enters the inner
# while loop (BUILDING state) — accumulating characters until the word ends,
# is too long, or contains a digit.

# You'll use state machines again in FormSense (parsing form fields), AFC
# (parsing SEC filings), and Stage 4 (LangGraph agent state transitions).