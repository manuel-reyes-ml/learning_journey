"""
"""

# =============================================================================
# IMPORTS
# =============================================================================

from __future__ import annotations

import logging
from pathlib import Path

from speller.benchmarks import timer, BenchmarkResult
from speller.speller import DictionaryProtocol

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
# CORE FUNCTION
# =============================================================================

# STEP: Load dictionary (timed)
def load_dictionary(
    *,
    dictionary: DictionaryProtocol,
    dict_path: str | Path,
) -> tuple[DictionaryProtocol, BenchmarkResult]:
    """
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
