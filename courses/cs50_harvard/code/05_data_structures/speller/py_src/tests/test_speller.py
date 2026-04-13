"""
"""

from __future__ import annotations

from pathlib import Path
import pytest

from speller.benchmarks import BenchmarkResult
from speller.speller import REPORT, SpellerResult, run_speller

# MockDictionary and FailingDictionary are in conftest.py.
# pytest auto-discovers them — no import needed for fixtures,
# but we DO import the classes directly when constructing instances
# inline (e.g. MockDictionary(words={...}) inside a test body).
from tests.conftest import FailingDictionary, MockDictionary


# =============================================================================
# SPELLERRESULT DATACLASS
# =============================================================================

class TestSpellerResult:
    """Test the SpellerResult frozen dataclass.
 
    SpellerResult holds all data produced by run_speller():
    - misspelled_words, words_misspelled, words_in_dictionary, words_in_text
    - ops_name, description (set by main() after run_speller() returns)
    - benchmarks (timing data keyed by operation name)
    """
    
    @pytest.fixture
    def sample_result(self) -> SpellerResult:
        """Create a SpellerResult with known values for testing.
 
        This is a LOCAL fixture — defined inside the test class
        because only this class needs it. Fixtures can live at
        three levels:
        1. conftest.py   → shared across ALL test files
        2. Test module   → shared across classes in this file
        3. Test class    → shared across methods in this class
 
        Choose the narrowest scope that covers all users.
        """
        return SpellerResult(
            misspelled_words=["Bingley", "Netherfield", "Longbourn"],
            words_misspelled=3,
            words_in_dictionary=143091,
            words_in_text=125203,
            benchmarks={
                "load": BenchmarkResult(
                    operation="load", elapsed_seconds=0.05
                ),
                "check": BenchmarkResult(
                    operation="check", elapsed_seconds=0.15
                ),
                "size": BenchmarkResult(
                    operation="size", elapsed_seconds=0.001
                ),
            },
        )
        
    def test_creation(self, sample_result: SpellerResult) -> None:
        """SpellerResult stores all provided values."""
        assert sample_result.words_misspelled == 3
        assert sample_result.words_in_dictionary == 143091
        assert sample_result.words_in_text == 125203
        assert len(sample_result.misspelled_words) == 3
        
    def test_frozen_immutability(self, sample_result: SpellerResult) -> None:
        """SpellerResult is immutable after creation."""
        with pytest.raises(AttributeError):
            sample_result.words_misspelled = 999  # type: ignore[misc]
            
    def test_keyword_only(self) -> None:
        """SpellerResult requires keyword arguments (KW_ONLY).
 
        Positional construction is blocked to prevent argument-order
        bugs when the dataclass has many fields of the same type.
        """
        with pytest.raises(TypeError):
            SpellerResult([], 0, 0, 0)  # type: ignore[misc]
            
    def test_optional_fields_default(self) -> None:
        """ops_name, description, and benchmarks have safe defaults.
 
        run_speller() returns a result with ops_name="" and description="".
        main() updates them via dataclasses.replace() after the call.
        """
        result = SpellerResult(
            misspelled_words=[],
            words_misspelled=0,
            words_in_dictionary=0,
            words_in_text=0,
        )
        assert result.ops_name == ""
        assert result.description == ""
        assert result.benchmarks == {}
        
    def test_time_total_property(self, sample_result: SpellerResult) -> None:
        """time_total sums all benchmark elapsed times.
 
        @property makes it accessible as result.time_total (no parens).
        Computed from benchmarks dict — never stored, never stale.
        """
        expected = 0.05 + 0.15 + 0.001
        assert sample_result.time_total == pytest.approx(expected)
        
    def test_time_total_empty_benchmarks(self) -> None:
        """time_total returns 0.0 when no benchmarks exist."""
        result = SpellerResult(
            misspelled_words=[],
            words_misspelled=0,
            words_in_dictionary=0,
            words_in_text=0,
        )
        assert result.time_total == 0.0
        
    def test_benchmarks_default_to_empty(self) -> None:
        """benchmarks field defaults to empty dict via default_factory."""
        result = SpellerResult(
            misspelled_words=[],
            words_misspelled=0,
            words_in_dictionary=0,
            words_in_text=0,
        )
        assert result.benchmarks == {}


# =============================================================================
# FORMAT REPORT
# =============================================================================

