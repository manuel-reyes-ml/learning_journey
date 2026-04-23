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
import itertools
from pathlib import Path
import logging
from collections.abc import Iterator
from rich.console import Console
from typing import Final, NamedTuple

from speller.benchmarks import BenchmarkResult, timer
from speller.protocols import DictionaryProtocol
from speller.text_processor import extract_words

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

__all__ = [
    "SpellerResult",
    "run_speller",
    "Report",
    "get_console",
]


# =============================================================================
# CONSTANTS
# =============================================================================

COL: Final[int] = 22


# =============================================================================
# RESULT CONTAINER
# =============================================================================

# The class-based form gives you typed fields that Pyright can validate at every
# access site, docstring support, default values, and it follows PEP 8 class
# naming, (Report not REPORT). This lets you introduce optional fields without
# breaking call sites, which is useful during staged migrations.
#
# Notice how Report.misspelled can now have a default of None — the current code
# passes None for this field in several places but the functional namedtuple can't
# express that without a workaround.
class Report(NamedTuple):
    """Formatted spell-check report."""
    
    main: str
    misspelled: str | None = None
    

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

    # Required fields (no default) must come first
    # Optional fields with defaults afterwards
    _: KW_ONLY      # Everything after is keyword-only
    misspelled_words: list[str]
    words_misspelled: int
    words_in_dictionary: int
    words_in_text: int
    
    ops_name: str = ""
    description: str = ""
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
    
    
    def format_report(self, *, log_misspelled: bool = False) -> Report:
        """Format results to match CS50 speller.c output exactly.

        Returns a :class:`REPORT` namedtuple rather than printing
        directly — the caller decides the output destination (stdout,
        log file, test assertion).  This is command-query separation:
        ``format_report()`` *queries* the data; the caller *commands*
        what to do with the result.

        Parameters
        ----------
        log_misspelled : bool, optional
            If ``True``, the returned :attr:`REPORT.misspelled` field
            contains a newline-joined string of all misspelled words
            for writing to a file.  If ``False`` (default),
            :attr:`REPORT.misspelled` is ``None``.

        Returns
        -------
        REPORT
            Named tuple with two fields:

            - ``main`` — the full CS50-format summary string, always
              populated.
            - ``misspelled`` — newline-joined misspelled word list, or
              ``None`` when ``log_misspelled=False``.

        Notes
        -----
        Returning ``REPORT`` instead of a plain ``str`` separates the
        console summary from the optional misspelled-words file content.
        :func:`~speller.__main__._print_reports` handles both fields.
        """
        lines: list[str] = []
        
        # Header
        lines.append(f"\n[bold cyan]MISSPELLED WORDS -- {self.ops_name} --[/bold cyan]")
        
        # Description
        lines.append(f"\n[cyan]{self.description}[/cyan]\n")
        
        # .get() with a default BenchmarkResult avoids KeyError if
        # a benchmark wasn´t recorded (defensive prorgramming)
        # data_load = self.benchmarks.get("load")
        data_check = self.benchmarks.get("check")
        # data_size = self.benchmarks.get("size")
        
        # SAFER — access by key name (works regardless of how many items)
        txt_file = data_check.metadata.get("input_file") if data_check else None
        
         # Color choice — red for misspelled if any, green if zero
        misspelled_color = "red" if self.words_misspelled > 0 else "green"
        
        # Statistics (CS50 uses %-20s style alignment with 5 spaces)
        lines.append(
            f"[cyan]{'WORDS MISSPELLED:':<{COL}}[/cyan]"
            f"[bold {misspelled_color}]{self.words_misspelled:,}[/bold {misspelled_color}]"
        )
        lines.append(f"[cyan]{'WORDS IN DICTIONARY:':<{COL}}[/cyan][bold]{self.words_in_dictionary:,}[/bold]")
        lines.append(f"[cyan]{'WORDS IN TEXT:':<{COL}}[/cyan][bold]{self.words_in_text:,}[/bold]")
        #                  ↑             ↑↑                         ↑  
        #                  │             ││                         |__ means apply separator: 100,000
        #               the text         │└── 22 characters total width
        #                                └─── < means left-align (pad RIGHT with spaces)
        
        ## The Three Alignment Specifiers

        # f"{'text':<20}"     left-align    → 'text                '
        # f"{'text':>20}"     right-align   → '                text'
        # f"{'text':^20}"     center        → '        text        '
        
        # Text file specs: name and path
        # [yellow] for the filename follows the Unix convention for identifiers/links/files
        lines.append(
            f"[cyan]{'CHECKED FILE:':<{COL}}[/cyan][yellow]{txt_file.fname}[/yellow]"
            if txt_file else
            f"[cyan]{'CHECKED FILE:':<{COL}}[cyan][dim italic]-- file not registered --[/dim italic]"
        )
        # [dim green] for the path mirrors how most shells color directory paths
        # Gives users a visual cue they already recognize from other terminal tools
        lines.append(
            f"[cyan]{'FILE PATH:':<{COL}}[/cyan][dim green]{txt_file.fpath.parent}/[/dim green]"
            if txt_file else
            f"[cyan]{'FILE PATH:':<{COL}}[/cyan][dim italic]-- file not registered --[/dim italic]"
        )
        
        # Benchmark timings
        for op, benchmark in self.benchmarks.items():
            label = f"TIME in {op}:"
            lines.append(
                f"[dim cyan]{label:<{COL}}[/dim cyan][dim]{benchmark.elapsed_seconds:.2f}[/dim]"
                if benchmark else
                f"[dim cyan]{label:<{COL}}[/dim cyan][dim]0.00[/dim]"
            )
        
        # --- Old Benchmark timings -------------------------------       
        # lines.append(
        #     f"{'TIME IN load:':<{COL}}{data_load.elapsed_seconds:.2f}"
        #     if data_load else
        #     f"{'TIME IN load:':<{COL}}0.00"
        # )
        # lines.append(
        #     f"{'TIME IN check:':<{COL}}{data_check.elapsed_seconds:.2f}"
        #     if data_check else
        #     f"{'TIME IN check:':<{COL}}0.00"
        # )
        # lines.append(
        #     f"{'TIME IN size:':<{COL}}{data_size.elapsed_seconds:.2f}"
        #    if data_size else
        #     f"{'TIME IN size:':<{COL}}0.00"
        # )
        
        lines.append(
            f"[bold cyan]{'TIME IN TOTAL:':<{COL}}[/bold cyan]"
            f"[bold]{self.time_total:.2f}[/bold]\n")
        
        # Report to show in console
        main_report = "\n".join(lines)
        
        # Misspelled words list to log
        misspelled_report = (
            "\n".join(self.misspelled_words) 
            if log_misspelled else None
        )
        
        return Report(main_report, misspelled_report)


# =============================================================================
# INTERNAL HELPER FUNCTIONS
# =============================================================================

def get_console() -> Console:
    """
    """
    # Output goes to stderr to match your logging pattern (keeps stdout clean
    # for programmatic piping)
    return Console(stderr=False)


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
    benchmarks: dict[str, BenchmarkResult] | None = None,  # <- None sentinel
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
        A pre-loaded dictionary instance satisfying
        :class:`~speller.protocols.DictionaryProtocol`.
        Injected by ``__main__.py`` after :func:`~speller.load_dictionary.load_dictionary`
        has already called ``load()`` — this function performs no loading.
        Works with any backend: ``HashTableDictionary``, ``DatabaseDictionary``
        (Stage 2), ``MockDictionary`` (testing).
    text_path : str or Path
        Path to the text file to spell-check.
    benchmarks : dict of {str : BenchmarkResult} or None, optional
        Timing results accumulated so far (e.g. ``{"load": result}``
        from :func:`~speller.load_dictionary.load_dictionary`).
        ``None`` (default) creates a fresh ``{}`` each call — avoids
        the mutable default argument footgun where a shared ``{}``
        would carry state across batch iterations.

    Returns
    -------
    SpellerResult
        Frozen dataclass containing all results and benchmarks.
        The caller decides how to display it
        (``format_report()``, logging, write to file).

    Raises
    ------
    ValueError
        If the text file cannot be decoded as UTF-8
        (``UnicodeDecodeError`` is re-raised with context preserved).
        If the file is empty or contains no extractable words
        (``StopIteration`` is suppressed — implementation detail).
        The caller (``main()``) catches ``ValueError`` per file and
        continues the batch; other files are not affected.

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
    path = Path(text_path) if isinstance(text_path, str) else text_path
    
    if benchmarks is None:
        benchmarks = {}  # new dict created fresh each call
    
    # =================================================================
    # STEP 1: Load dictionary (timed)
    # =================================================================
    # Dictionary load needs to run only once for the batch txt file(s)
    # A separate function is implemented in load_dictionary module
    
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
    
    with timer("check", input_file=path) as t:
        # The exception pattern keeps the boundary clean. Raises ValueError because something
        # went wrong in its domain-bad encoding, empty file. main() catches it and translates
        # it to an ExitCode at the CLI boundary. That translation is exatly main()'s job.
        try:
            content = path.read_text(encoding="utf-8")
            words: Iterator[str] = extract_words(content, path.name)
            first = next(words)
        except UnicodeDecodeError as e:
            # from e - the original exception adds diagnostic value. Keep it visible.
            # UnicodeDecodeError is not a normal exception — it has a rigid C-level
            # constructor signature that requires exactly 5 positional arguments:
            raise UnicodeDecodeError(
                e.encoding, e.object, e.start, e.end,
                f"Cannot decode '{path.name}': {e.reason}",
            ) from e
        
        # StopIteration is Python internals signal, not a real error.
        # Shows an Iterator or Generator was exhausted.
        except StopIteration:
            # from None - the original exception is an implementation detail
            # or internal signal. Hide it.
            raise ValueError(f"No valid words in '{path.name}'") from None
        
        for word in itertools.chain([first], words):
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


# =============================================================================
# SHORT REFERENCE GUIDES
# =============================================================================

# __main__.py is the COMPOSITION ROOT — the one place that picks the concrete class
#   from speller.dictionary import HashTableDictionary
#   from speller.speller import run_speller

# dictionary = HashTableDictionary()     # concrete choice HERE
# result = run_speller(dictionary, ...)  # injected via Protocol

# Why this matters: when you write tests, you inject a MockDictionary
# with predictable behavior. When you build Stage 2's database-backed
# dictionary, you swap the implementation in __main__.py — speller.py
# doesn't change at all.


# =====================================================
# Chained Raise Exceptions
# =====================================================

# from e  — confusing to the caller
# StopIteration
# The above exception was the direct cause of the following exception:
# ValueError: No valid words in 'empty.txt'

# from None — clean
# ValueError: No valid words in 'empty.txt'

# The mechanical detail
# Both work by setting dunder attributes on the raised exception:
#   raise ValueError("msg") from e     # sets __cause__ = e,    __suppress_context__ = True
#   raise ValueError("msg") from None  # sets __cause__ = None, __suppress_context__ = True
#   raise ValueError("msg")            # sets __cause__ = None, __suppress_context__ = False
                                       # Python still shows __context__ (implicit chaining)

# That third case is the subtle one — a bare raise ValueError("msg") inside an except block still
# chains implicitly via __context__, showing the original exception with "During handling of the above
# exception, another exception occurred." from None is the only way to fully suppress that.

# The decision rule
#   from e — the original exception adds diagnostic value. Keep it visible.
#   from None — the original exception is an implementation detail or internal signal. Hide it.
#   bare raise — fine for quick scripts, but in production code you're leaving implicit chaining
#   on that may or may not be useful depending on context.


# =====================================================
# UnicodeDecodeError details
# =====================================================

# UnicodeDecodeError inherits from UnicodeError, which stores all 5 constructor arguments as
# attributes. reason is the human-readable explanation of why the decode failed:

# except UnicodeDecodeError as e:
#     print(e.encoding)  # "utf-8"
#     print(e.object)    # b'\xff\xfe...'  ← the raw bytes that failed
#     print(e.start)     # 0              ← index where the bad byte starts
#     print(e.end)       # 1              ← index where the bad byte ends
#     print(e.reason)    # "invalid start byte"  ← the WHY