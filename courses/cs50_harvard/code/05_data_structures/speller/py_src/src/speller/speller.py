"""
"""

# =============================================================================
# IMPORTS
# =============================================================================

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
import logging

from speller.benchmarks import BenchmarkResult, timer, timed
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
    
    misspelled_words: list[str]
    words_misspelled: int
    words_in_dictionary: int
    words_in_text: int
    benchmarks: dict[str, BenchmarkResult] = field(default_factory=dict)
    
    @property
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
        
