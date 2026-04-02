"""Dictionary loader for the speller batch pipeline.

Separates dictionary loading from spell-checking so the expensive
``load()`` operation runs exactly once per backend per program
execution, regardless of how many text files are processed.

Without this separation, a batch of N files would reload 143K words
N times — once per ``run_speller()`` call.  With it, the dictionary
loads once and the loaded instance is passed to every ``run_speller()``
call in the batch loop.

Single responsibility
---------------------
This module does one thing: time the ``load()`` call and return the
loaded dictionary alongside its :class:`~speller.benchmarks.BenchmarkResult`.
Path validation and error display are the caller's responsibility
(``__main__.py``).

Roadmap relevance
-----------------
The same "load once, iterate N times" pattern applies to every
Stage 2+ project with an expensive initialisation step:

- PolicyPulse:  ChromaDB client loaded once, N documents ingested.
- FormSense:    Gemini Vision client loaded once, N forms processed.
- AFC:          Database connection opened once, N SEC filings parsed.
"""

# =============================================================================
# IMPORTS
# =============================================================================

from __future__ import annotations

import logging
from pathlib import Path

from speller.benchmarks import timer, BenchmarkResult
from speller.protocols import DictionaryProtocol

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

__all__ = ["load_dictionary"]


# =============================================================================
# CORE FUNCTION
# =============================================================================

# STEP: Load dictionary (timed)
def load_dictionary(
    *,
    dictionary: DictionaryProtocol,
    dict_path: str | Path,
) -> tuple[DictionaryProtocol, BenchmarkResult]:
    """Load a dictionary backend and return it with its timing result.

    Times the ``load()`` call using the :func:`~speller.benchmarks.timer`
    context manager.  Raises :exc:`SystemExit` immediately if loading
    fails — spell-checking cannot proceed without a dictionary, and
    this is a fatal condition that belongs at the program boundary.

    Parameters
    ----------
    dictionary : DictionaryProtocol
        An unloaded dictionary instance satisfying
        :class:`~speller.protocols.DictionaryProtocol`.
        Created by the caller via ``data.dict_class()`` in the
        composition root (``__main__.py``).
    dict_path : str or Path
        Path to the word-list file to load.  Passed to
        ``dictionary.load()`` as a string.

    Returns
    -------
    tuple[DictionaryProtocol, BenchmarkResult]
        A 2-tuple of:

        - The same ``dictionary`` instance, now populated with words.
        - A :class:`~speller.benchmarks.BenchmarkResult` for the
          ``"load"`` operation, ready to be stored in ``benchmarks``.

    Raises
    ------
    SystemExit
        If ``dictionary.load()`` returns ``False``.  This is a fatal
        error — the program cannot spell-check without a dictionary.
        The caller (``__main__.py``) catches ``SystemExit`` and maps
        it to :attr:`~speller.config.ExitCode.LOAD_FAILED`.

    Examples
    --------
    ::

        loaded_dict, load_result = load_dictionary(
            dictionary=HashTableDictionary(),
            dict_path="dictionaries/large",
        )
        benchmarks["load"] = load_result
        # loaded_dict is now ready for run_speller()

    Notes
    -----
    Why return the dictionary instance alongside the benchmark?
        The caller needs both: the loaded instance to pass to
        ``run_speller()``, and the timing result to include in the
        batch benchmark report.  A 2-tuple keeps the call site clean
        with unpacking: ``loaded_dict, load_result = load_dictionary(...)``.

    Why ``SystemExit`` instead of ``ValueError``?
        Dictionary load failure is fatal for the entire batch — there
        is no point skipping individual files if the word list cannot
        be loaded.  ``ValueError`` is reserved for per-file errors
        (encoding issues, empty files) that allow the batch to continue.
        ``SystemExit`` surfaces at ``main()``'s ``except SystemExit``
        handler and terminates the program cleanly.
    """
    # timer() context manager wraps the load call.
    # After the 'with' block, t["result"] contains the BenchmarkResult.
    with timer("load") as t:
        # dictionary.load() works with ANY implementation
        # Dependency injection in action
        loaded = dictionary.load(str(dict_path))
    
    if not loaded:
        logger.error("Could not load dictionary: %s", dict_path)
        raise SystemExit(f"Could not load {dict_path}.")
    
    logger.info(
        "Dictionary loaded: %d words",
        len(dictionary),
    )
    return dictionary, t["result"]
