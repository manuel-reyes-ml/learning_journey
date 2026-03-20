"""
"""

# =============================================================================
# IMPORTS
# =============================================================================

from __future__ import annotations

from dataclasses import dataclass, field, KW_ONLY
from pathlib import Path
import logging

from speller.benchmarks import BenchmarkResult, timer
from speller.protocols import DictionaryProtocol
from speller.text_processor import extract_words

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


# =============================================================================
# RESULT CONTAINER
# =============================================================================

# frozen=True makes instances immutable.
# slots=True prevents dynamic attribute creation and
# reduces memory fooprint.
# Together they create a truly locked-down data container.
@dataclass(frozen=True, slots=True)
class SpellerResult: 
    """
    """
    _: KW_ONLY      # Everything after is keyword-only
    misspelled_words: list[str]
    words_misspelled: int
    words_in_dictionary: int
    words_in_text: int
    benchmarks: dict[str, BenchmarkResult] = field(default_factory=dict)
    
    @property  # access time_total as an attribute not time_total()
    def time_total(self) -> float:
        """
        """
        return sum(b.elapsed_seconds for b in self.benchmarks.values())
    
    
    def format_report(self) -> str:
        """
        """
        lines: list[str] = []
        
        # Header
        lines.append("\nMISSPELLED WORDS\n")
        
        # Misspelled words list
        for word in self.misspelled_words:
            lines.append(word)
            
        # Statistics (CS50 uses %-20s style alignment with 5 spaces)
        lines.append(f"\nWORDS MISSPELLED:     {self.words_misspelled}")
        lines.append(f"WORDS IN DICTIONARY:    {self.words_in_dictionary}")
        lines.append(f"WORDS IN TEXT:        {self.words_in_text}")
        
        # Benchmark timings
        # .get() with a default BenchmarkResult avoids KeyError if
        # a benchmark wasn´t recorded (defensive prorgramming)
        time_load = self.benchmarks.get("load")
        time_check = self.benchmarks.get("check")
        time_size = self.benchmarks.get("size")
        
        lines.append(
            "TIME IN load:     "
            f"{time_load.elapsed_seconds:.2f}" if time_load else
            "TIME IN load:     0.00"
        )
        lines.append(
            "TIME IN check:     "
            f"{time_check.elapsed_seconds:.2f}" if time_check else
            "TIME IN check:     0.00"
        )
        lines.append(
            "TIME IN size:     "
            f"{time_size.elapsed_seconds:.2f}" if time_size else
            "TIME IN size:     0.00"
        )
        lines.append(f"TIME IN TOTAL:     {self.time_total:.2f}\n")
        
        return "\n".join(lines)
    

# =============================================================================
# CORE FUNCTION
# =============================================================================

# CORRECT -  return data, let caller decide presentation.
# This is command-query separation — a function either computes and returns
# data (query), or performs an action (command), but not both. run_speller()
# is a query. Printing is a command that __main__.py handles.
def run_speller(
    dictionary: DictionaryProtocol,
    text_path: str | Path,
    dict_path: str | Path,
) -> SpellerResult:  # pure computation, testable
    """
    """
    benchmarks: dict[str, BenchmarkResult] = {}
    
    # =================================================================
    # STEP 1: Load dictionary (timed)
    # =================================================================
    # timer() context manager wraps the load call.
    # After the 'with' block, t["result"] contains the BenchmarkResult.
    with timer("load") as t:
        # dictionary.load() works with ANY implementation
        # Dependency injection in action
        loaded = dictionary.load(str(dict_path))
    
    benchmarks["load"] = t["result"]
    
    if not loaded:
        logger.error("Could not load dictionary: %s", dict_path)
        raise SystemExit(f"Could not load {dict_path}.")
    
    logger.info("Dictionary loaded: %d words", dictionary.size()) #NOTE: Try Pythonic exp (dunder)
    
    # =================================================================
    # STEP 2: Check words (timed cumulatively)
    # =================================================================
    # The timer wraps the ENTIRE loop — not individual check() calls.
    # This gives us total TIME IN check, matching CS50's output.
    #
    # extract_words() is a generator — it yields one word at a time.
    # No intermediate list is created. The flow is:
    #   generator yields word → we check it → generator yields next
    #
    # This is the streaming pipeline pattern:
    #   [file bytes] → extract_words → check → accumulate results
    misspelled_words: list[str] = []
    words_in_text = 0
    
    with timer("check") as t:
        for word in extract_words(text_path):
            words_in_text +=1
            
            if not dictionary.check(word): #NOTE: Try Pythonic exp (dunder)
                misspelled_words.append(word)
                
    benchmarks["check"] = t["result"]
    
    # =================================================================
    # STEP 3: Get dictionary size (timed)
    # =================================================================
    with timer("size") as t:
        words_in_dictionary = dictionary.size() #NOTE: Try Pythonic exp (dunder)
        
    benchmarks["size"] = t["result"] 
    
    # =================================================================
    # STEP 4: Package results
    # =================================================================
    result = SpellerResult(
        misspelled_words=misspelled_words,
        words_misspelled=len(misspelled_words),
        words_in_dictionary=words_in_dictionary,
        words_in_text=words_in_text,
        benchmarks=benchmarks,
    )
    
    logger.info(
        "Spell check complete: %d misspelled out of %d words",
        result.words_misspelled,
        result.words_in_text,
    )
    
    return result


# __main__.py is the COMPOSITION ROOT — the one place that picks the concrete class
#   from speller.dictionary import HashTableDictionary
#   from speller.speller import run_speller

# dictionary = HashTableDictionary()     # concrete choice HERE
# result = run_speller(dictionary, ...)  # injected via Protocol

# Why this matters: when you write tests, you inject a MockDictionary
# with predictable behavior. When you build Stage 2's database-backed
# dictionary, you swap the implementation in __main__.py — speller.py
# doesn't change at all.
    