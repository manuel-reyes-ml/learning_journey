"""Spell-checker orchestrator — wires all components together.

Coordinates dictionary loading, text processing, spell checking,
and benchmark reporting. This module depends on ABSTRACTIONS
(``DictionaryProtocol``), not concrete implementations
(``HashTableDictionary``). The concrete class is injected by
the caller (``__main__.py``).

This is the Dependency Inversion Principle in action:
    - speller.py says "give me anything with load/check/size"
    - __main__.py says "here's a HashTableDictionary"
    - speller.py never imports dictionary.py

CS50 Output Format
-------------------
The output must match CS50's ``speller.c`` exactly::

    MISSPELLED WORDS

    [list of misspelled words, one per line]

    WORDS MISSPELLED:     [count]
    WORDS IN DICTIONARY:  [count]
    WORDS IN TEXT:        [count]
    TIME IN load:         [seconds]
    TIME IN check:        [seconds]
    TIME IN size:         [seconds]
    TIME IN TOTAL:        [seconds]

Module Dependencies
-------------------
    config.py         → (none currently, but available for constants)
    protocols.py      → DictionaryProtocol (interface contract)
    benchmarks.py     → timer(), timed(), BenchmarkResult
    text_processor.py → extract_words() (word generator)
"""

# =============================================================================
# IMPORTS
# =============================================================================

from __future__ import annotations

from dataclasses import dataclass, field, KW_ONLY
from pathlib import Path
import logging
from collections import namedtuple
from typing import Final

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

__all__ = [
    "SpellerResult",
    "run_speller",
]


# =============================================================================
# CONSTANTS
# =============================================================================

COL: Final[int] = 22
REPORT = namedtuple("REPORT", ["main", "misspelled"])


# =============================================================================
# RESULT CONTAINER
# =============================================================================

# frozen=True makes instances immutable.
# slots=True prevents dynamic attribute creation and
# reduces memory fooprint.
# Together they create a truly locked-down data container.
@dataclass(frozen=True, slots=True)
class SpellerResult: 
    """Immutable container for the complete spell-check result.

    Holds all data needed to produce the CS50-format output report.
    Using a dataclass instead of returning a tuple or dict because:
    - Named fields are self-documenting (result.misspelled vs result[0])
    - Type hints catch errors at compile time
    - frozen=True prevents accidental mutation after creation
    - The caller decides HOW to display results (print, log, write to file)

    This is the same pattern you'll use in future projects:
    - DataVault:    AnalysisResult (query, response, tokens, latency)
    - PolicyPulse:  RetrievalResult (query, chunks, confidence, source)
    - FormSense:    ExtractionResult (fields, confidence, routing)
    - AFC:          BacktestResult (trades, returns, sharpe, drawdown)

    Parameters
    ----------
    misspelled_words : list[str]
        Words not found in the dictionary, in original case.
    words_misspelled : int
        Count of misspelled words.
    words_in_dictionary : int
        Total words loaded in dictionary.
    words_in_text : int
        Total words processed from text file.
    benchmarks : dict[str, BenchmarkResult]
        Timing results keyed by operation name.
    """

    _: KW_ONLY      # Everything after is keyword-only
    ops_name: str
    misspelled_words: list[str]
    words_misspelled: int
    words_in_dictionary: int
    words_in_text: int
    benchmarks: dict[str, BenchmarkResult] = field(default_factory=dict)
    
    @property  # access time_total as an attribute not time_total()
    def time_total(self) -> float:
        """Calculate total time across all benchmarked operations.

        Uses a generator expression inside sum() — no intermediate list.
        This is the same pattern as:
            sum(sale.amount for sale in sales)  # Stage 1 DataVault
            sum(score for score in model.evaluate())  # Stage 3 ML

        Returns
        -------
        float
            Sum of all benchmark elapsed_seconds values.
        """
        return sum(b.elapsed_seconds for b in self.benchmarks.values())
    
    
    def format_report(self, *, log_misspelled: bool = False) -> REPORT:
        """Format results to match CS50 speller.c output exactly.

        Returns a string rather than printing directly because:
        - Testable: assert result.format_report() == expected_output
        - Flexible: caller decides destination (stdout, file, log)
        - Composable: can be included in larger reports

        This pattern is called "command-query separation":
        - format_report() QUERIES the data (returns string, no side effects)
        - The caller COMMANDS what to do with it (print, write, send)

        Returns
        -------
        str
            Formatted report matching CS50's exact output format.
        """
        lines: list[str] = []
        
        # Header
        lines.append(f"\nMISSPELLED WORDS -- {self.ops_name} --\n")
        
        # .get() with a default BenchmarkResult avoids KeyError if
        # a benchmark wasn´t recorded (defensive prorgramming)
        data_load = self.benchmarks.get("load")
        data_check = self.benchmarks.get("check")
        data_size = self.benchmarks.get("size")
        
        # SAFER — access by key name (works regardless of how many items)
        txt_file = data_check.metadata.get("input_file") if data_check else None
        
        # Statistics (CS50 uses %-20s style alignment with 5 spaces)
        lines.append(f"{'WORDS MISSPELLED:':<{COL}}{self.words_misspelled}")
        lines.append(f"{'WORDS IN DICTIONARY:':<{COL}}{self.words_in_dictionary}")
        lines.append(f"{'WORDS IN TEXT:':<{COL}}{self.words_in_text}")
        #                  ↑             ↑↑
        #                  │             ││
        #               the text         │└── 22 characters total width
        #                                └─── < means left-align (pad RIGHT with spaces)
        
        ## The Three Alignment Specifiers

        # f"{'text':<20}"     left-align    → 'text                '
        # f"{'text':>20}"     right-align   → '                text'
        # f"{'text':^20}"     center        → '        text        '
        
        # Text file specs: name and path
        lines.append(
            f"{'CHECKED FILE:':<{COL}}{txt_file.fname}"
            if txt_file else
            f"{'CHECKED FILE:':<{COL}}-- file not registered --"
        )
        lines.append(
            f"{'FILE PATH:':<{COL}}{txt_file.fpath}"
            if txt_file else
            f"{'FILE PATH:':<{COL}}-- file not registered --"
        )
        
        # Benchmark timings
        lines.append(
            f"{'TIME IN load:':<{COL}}{data_load.elapsed_seconds:.2f}"
            if data_load else
            f"{'TIME IN load:':<{COL}}0.00"
        )
        lines.append(
            f"{'TIME IN check:':<{COL}}{data_check.elapsed_seconds:.2f}"
            if data_check else
            f"{'TIME IN check:':<{COL}}0.00"
        )
        lines.append(
            f"{'TIME IN size:':<{COL}}{data_size.elapsed_seconds:.2f}"
            if data_size else
            f"{'TIME IN size:':<{COL}}0.00"
        )
        lines.append(f"{'TIME IN TOTAL:':<{COL}}{self.time_total:.2f}\n")
        
        # Report to show in console
        main_report = "\n".join(lines)
        
        # Misspelled words list to log
        misspelled_report = (
            "\n".join(self.misspelled_words) 
            if log_misspelled else None
        )
        
        return REPORT(main_report, misspelled_report)
    

# =============================================================================
# CORE FUNCTION
# =============================================================================

# CORRECT -  return data, let caller decide presentation.
# This is command-query separation — a function either computes and returns
# data (query), or performs an action (command), but not both. run_speller()
# is a query. Printing is a command that __main__.py handles.
def run_speller(
    *,
    dictionary: DictionaryProtocol,
    text_path: str | Path,
    dict_path: str | Path,
    ops_name: str,
) -> SpellerResult:  # pure computation, testable
    """Run the spell checker — orchestrates all components.

    This function:
    1. Loads the dictionary (timed)
    2. Extracts words from text (generator — streaming)
    3. Checks each word against the dictionary (timed cumulatively)
    4. Gets dictionary size (timed)
    5. Packages everything into a SpellerResult

    Parameters
    ----------
    dictionary : DictionaryProtocol
        Any object satisfying the DictionaryProtocol interface.
        Injected by __main__.py — this function doesn't know or care
        whether it's a HashTableDictionary, a DatabaseDictionary,
        or a MockDictionary for testing.
    text_path : str or Path
        Path to the text file to spell-check.
    dict_path : str or Path
        Path to the dictionary file to load.

    Returns
    -------
    SpellerResult
        Frozen dataclass containing all results and benchmarks.
        The caller decides how to display it (format_report(), logging, etc.)

    Raises
    ------
    SystemExit
        If the dictionary fails to load (cannot proceed without it).

    Notes
    -----
    Why accept DictionaryProtocol (not HashTableDictionary)?
        Dependency injection — this function works with ANY dictionary
        backend. For testing, you pass a MockDictionary. For Stage 2,
        you could pass a DatabaseDictionary. No changes to speller.py.

    Why return SpellerResult (not print directly)?
        - Testable: assert result.words_misspelled == 30
        - Composable: caller can log, print, write to file, or ignore
        - No side effects: pure function (given same inputs → same output)
        - This is command-query separation — compute and return, let the
          caller decide what to do with the results

    Why not use @timed decorator for check?
        check() is called thousands of times (once per word). We need
        the CUMULATIVE time, not individual call times. The timer()
        context manager wraps the entire check loop to capture total time.
        @timed is for one-shot operations like load() and size().
    """
    benchmarks: dict[str, BenchmarkResult] = {}
    
    logger.debug("Running Speller with '%s'", ops_name)
    
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
    
    logger.info(
        "Dictionary loaded: %d words in '%s'", 
        len(dictionary),  # NOTE: Try Pythonic exp (dunder)
        ops_name,
    ) 
    
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
    
    with timer("check", input_file=text_path) as t:
        for word in extract_words(text_path):
            words_in_text +=1
            
            if word not in dictionary: #NOTE: Try Pythonic exp (dunder)
                misspelled_words.append(word)
                
    benchmarks["check"] = t["result"]
    
    # =================================================================
    # STEP 3: Get dictionary size (timed)
    # =================================================================
    with timer("size") as t:
        words_in_dictionary = len(dictionary) #NOTE: Try Pythonic exp (dunder)
        
    benchmarks["size"] = t["result"] 
    
    # =================================================================
    # STEP 4: Package results
    # =================================================================
    result = SpellerResult(
        ops_name=ops_name,
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
    