"""Tests for speller.speller module.
 
Tests the run_speller() orchestrator and SpellerResult dataclass.
This is where DEPENDENCY INJECTION pays off — we inject MockDictionary
and FailingDictionary (from conftest.py) instead of using real files.
 
No real dictionary files needed. No slow I/O. Fast, deterministic,
isolated tests. This is the testing pattern for every future project:
- DataVault:   MockLLMProvider → test analysis pipeline
- PolicyPulse: MockVectorStore → test RAG retrieval
- FormSense:   MockExtractor → test form processing
- AFC:         MockDataSource → test backtesting engine
 
Architecture note
-----------------
run_speller(*, dictionary, text_path, benchmarks=None) -> SpellerResult
 
run_speller() receives a PRE-LOADED dictionary — it does NOT call
load() itself. Dictionary loading was separated into load_dictionary.py.
This means:
 
- run_speller() benchmarks: "check" and "size" only by default
- "load" only appears if the CALLER pre-populates the benchmarks dict
  before passing it to run_speller() — matching main()'s batch pattern:
 
      benchmarks["load"] = load_result        # from load_dictionary()
      result = run_speller(                   # adds "check" and "size"
          dictionary=loaded_dict,
          text_path=text_path,
          benchmarks=benchmarks,
      )
 
- FailingDictionary (load returns False) must be tested against
  load_dictionary(), NOT run_speller()
 
Pytest Patterns Used
--------------------
- Dependency injection (MockDictionary via conftest.py fixtures)
- Testing frozen dataclass properties (@property)
- Testing named tuple returns (REPORT namedtuple)
- pytest.raises() with SystemExit (in TestLoadDictionary)
- Combining fixtures (mock + temp files)
- pytest.mark.integration for real-file tests
"""

from __future__ import annotations

from pathlib import Path
from pydoc import text
import pytest

from speller.benchmarks import BenchmarkResult
from speller.protocols import DictionaryProtocol
from speller.register import dicts
from speller.speller import REPORT, SpellerResult, run_speller

# MockDictionary and FailingDictionary are in conftest.py.
# pytest auto-discovers them — no import needed for fixtures,
# but we DO import the classes directly when constructing instances
# inline (e.g. MockDictionary(words={...}) inside a test body).
from tests.conftest import FailingDictionary, MockDictionary


# =============================================================================
# OVERRIDE confest.py fixtures (for this file only)
# =============================================================================

# When the thing that varies is the object under test (the dictionary backend), parametrize
# the fixture that produces it. Every test that uses that fixture automatically runs once
# per backend — zero changes to the test methods themselves.
@pytest.fixture(params=list(dicts.keys()))
def empty_dictionary(request: pytest.FixtureRequest) -> DictionaryProtocol:
    #                 ↑
    # pytest sees this parameter name "request" and injects
    # its own FixtureRequest object automatically — same way
    # it injects tmp_path or capsys by name
    """Unloaded instance of every registered backend.

    params=list(dicts.keys()) makes pytest run every test that uses
    this fixture once per registered backend key ("hash", "list",
    "sorted", "dict"). request.param holds the current key.

    This locally overrides the conftest.py fixture of the same name
    for this file only — conftest remains unchanged.
    """
    return dicts[request.param].dict_class()
    #                ↑
    # First run:  request.param == "hash"   → HashTableDictionary()
    # Second run: request.param == "list"   → ListDictionary()
    # Third run:  request.param == "sorted" → SortedListDictionary()
    # Fourth run: request.param == "dict"   → DictDictionary()
    

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

class TestFormatReport:
    """Test SpellerResult.format_report() output.

    format_report(*, log_misspelled=False) -> REPORT

    Returns a REPORT namedtuple with two fields:
    - main:        the full CS50-format summary string (always populated)
    - misspelled:  newline-joined word list, or None when not requested
    """
    
    @pytest.fixture
    def result_with_benchmarks(self) -> SpellerResult:
        """SpellerResult with all three benchmark keys for report testing."""
        return SpellerResult(
            misspelled_words=["xyz", "abc"],
            words_misspelled=2,
            words_in_dictionary=10,
            words_in_text=100,
            benchmarks={
                "load": BenchmarkResult(
                    operation="load", elapsed_seconds=0.12
                ),
                "check": BenchmarkResult(
                    operation="check", elapsed_seconds=0.34
                ),
                "size": BenchmarkResult(
                    operation="size", elapsed_seconds=0.001
                ),
            },
        )
        
    def test_report_returns_report_namedtuple(
        self, result_with_benchmarks: SpellerResult
    ) -> None:
        """format_report() returns a REPORT namedtuple, not a plain str.

        REPORT has two fields: .main (str) and .misspelled (str | None).
        This separation keeps the console summary distinct from the
        optional misspelled-words file content.
        """
        report = result_with_benchmarks.format_report()
        assert isinstance(report, REPORT)
        assert isinstance(report.main, str)
        
    def test_report_contains_statistics(
        self, result_with_benchmarks: SpellerResult
    ) -> None:
        """Report includes all required statistics lines."""
        report = result_with_benchmarks.format_report()
        
        assert "TIME IN load:" in report.main
        assert "TIME IN check:" in report.main
        assert "TIME IN size:" in report.main
        assert "TIME IN TOTAL:" in report.main
        
    def test_report_contains_timings(
        self, result_with_benchmarks: SpellerResult
    ) -> None:
        """Report includes all timing lines."""
        report = result_with_benchmarks.format_report()
        
    def test_report_contains_header(
        self, result_with_benchmarks: SpellerResult
    ) -> None:
        """Report starts with MISSPELLED WORDS header."""
        report = result_with_benchmarks.format_report()
        assert "MISSPELLED WORDS" in report.main
        
    def test_misspelled_none_by_default(
        self, result_with_benchmarks: SpellerResult
    ) -> None:
        """misspelled field is None when log_misspelled=False (default)."""
        report = result_with_benchmarks.format_report(log_misspelled=False)
        assert report.misspelled is None
        
    def test_misspelled_populated_when_requested(
        self, result_with_benchmarks: SpellerResult
    ) -> None:
       """misspelled field contains words when log_misspelled=True."""
       report = result_with_benchmarks.format_report(log_misspelled=True)
       assert report.misspelled is not None
       assert "xyz"  in report.misspelled
       assert "abc" in report.misspelled
       
    def test_report_with_no_benchmarks(self) -> None:
        """Report handles missing benchmarks gracefully (shows 0.00)."""
        result = SpellerResult(
            misspelled_words=[],
            words_misspelled=0,
            words_in_dictionary=0,
            words_in_text=0,
        )
        report = result.format_report()
        assert "0.00" in report.main
        
        
# =============================================================================
# RUN_SPELLER — THE ORCHESTRATOR
# =============================================================================

class TestRunSpeller:
    """Test run_speller() using injected mock dictionaries.

    THIS IS THE DEPENDENCY INJECTION PAYOFF.

    run_speller(*, dictionary, text_path, benchmarks=None) accepts
    DictionaryProtocol — it doesn't know or care that we're passing
    a MockDictionary. The function works identically with:
    - MockDictionary       (tests — fast, deterministic, no file I/O)
    - HashTableDictionary  (production — real dictionary files)
    - DatabaseDictionary   (Stage 2 — PostgreSQL-backed)

    No changes to run_speller() code. Ever.

    What run_speller() does NOT do:
    - It does NOT call dictionary.load() — loading is the caller's job
      (done in load_dictionary.py before the batch loop in main())
    - Therefore "load" does NOT appear in result.benchmarks by default
    - Only "check" and "size" are benchmarked inside run_speller()
    """
    
    def test_basic_spell_check(
        self,
        mock_dictionary: MockDictionary,
        sample_text_file: Path,
    ) -> None:
        """run_speller returns a SpellerResult with correct structure."""
        result = run_speller(
            dictionary=mock_dictionary,
            text_path=sample_text_file,
        )
        
        assert isinstance(result, SpellerResult)
        assert result.words_in_text > 0
        assert isinstance(result.words_misspelled, int)
        
    def test_all_words_found(self, tmp_path: Path) -> None:
        """When all words are in the dictionary, nothing is misspelled."""
        text_file = tmp_path / "test_txt"
        text_file.write_text("cat dog", encoding="utf-8")
       
        result = run_speller(
           dictionary=MockDictionary(words={"cat", "dog"}),
           text_path=text_file,
        )
        
        assert result.words_misspelled == 0
        assert result.misspelled_words == []
        assert result.words_in_text == 2
        
    def test_misspelled_words_detected(self, tmp_path: Path) -> None:
        """Words not in dictionary appear in misspelled_words list."""
        text_file = tmp_path / "test.txt"
        text_file.write_text("cat xyz dog qqq", encoding="utf-8")
        
        result = run_speller(
            dictionary=MockDictionary(words={"cat", "dog"}),
            text_path=text_file,
        )
        
        assert result.words_misspelled == 2
        assert "xyz" in result.misspelled_words
        assert "qqq" in result.misspelled_words
        
    def test_check_and_size_benchmarks_recorded(
        self,
        mock_dictionary: MockDictionary,
        sample_text_file: Path,
    ) -> None:
        """run_speller records 'check' and 'size' benchmarks only.

        run_speller() does NOT call load() — that responsibility
        belongs to load_dictionary.py (called once before the batch
        loop in main()). Therefore only 'check' and 'size' appear
        in benchmarks by default.
        """
        result = run_speller(
            dictionary=mock_dictionary,
            text_path=sample_text_file,
        ) 
     
        assert "check" in result.benchmarks
        assert "size" in result.benchmarks
        assert "load" not in result.benchmarks  # load is caller's job
        
        for benchmark in result.benchmarks.values():
            assert isinstance(benchmark, BenchmarkResult)
            assert benchmark.elapsed_seconds >= 0
            
    def test_caller_provided_benchmarks_are_merged(
        self,
        mock_dictionary: MockDictionary,
        sample_text_file: Path,
    ) -> None:
        """Pre-populated benchmarks dict is extended, not replaced.

        This mirrors main()'s batch loop pattern:
            benchmarks["load"] = load_result        # load_dictionary()
            result = run_speller(                   # adds "check", "size"
                dictionary=loaded_dict,
                text_path=text_path,
                benchmarks=benchmarks,
            )
            # result.benchmarks now has all three: load, check, size
        """
        load_benchmark = BenchmarkResult(operation="load", elapsed_seconds=0.05)
        
        result = run_speller(
            dictionary=mock_dictionary,
            text_path=sample_text_file,
            benchmarks={"load": load_benchmark},
        )
        
        assert "load" in result.benchmarks
        assert "check" in result.benchmarks
        assert "size" in result.benchmarks
        assert result.benchmarks["load"].elapsed_seconds == 0.05
        
    def test_dictionary_size_reported(
        self,
        mock_dictionary: MockDictionary,
        sample_text_file: Path,
    ) -> None:
        """words_in_dictionary matches the mock dictionary size."""
        result = run_speller(
            dictionary=mock_dictionary,
            text_path=sample_text_file,
        )
        
        assert result.words_in_dictionary == mock_dictionary.size()
        
    def test_keyword_only_arguments(self) -> None:
        """run_speller requires keyword arguments (* in signature).

        The * in 'def run_speller(*, dictionary, text_path, ...)'
        forces ALL arguments to be keyword-only. Any positional
        call raises TypeError — this prevents argument-order bugs.
        """
        with pytest.raises(TypeError):
            run_speller(
                MockDictionary(),  # type: ignore[misc] - positional - should fail
                "texts/cat.txt",
            )
        
    def test_preserves_original_case_in_misspelled(
        self, tmp_path: Path
    ) -> None:
        """Misspelled words retain their original case.

        text_processor yields "Bingley" (original case).
        dictionary.check() normalizes to "bingley" for lookup.
        The misspelled list should contain "Bingley", not "bingley".
        """
        text_file = tmp_path / "test.txt"
        text_file.write_text("Hello Bingley world", encoding="utf-8")
        
        result = run_speller(
            dictionary=MockDictionary(words={"hello", "world"}),
            text_path=text_file,
        )
        
        assert "Bingley" in result.misspelled_words
        
    def test_benchmarks_none_creates_fresh_dict(
        self,
        mock_dictionary: MockDictionary,
        tmp_path: Path,
    ) -> None:
        """benchmarks=None (default) creates a new dict each call.

        The None sentinel avoids the mutable default argument footgun
        where a shared {} would accumulate state across batch iterations.
        Two consecutive calls must produce independent result objects.
        """
        text_file = tmp_path / "test.txt"
        text_file.write_text("cat dog", encoding="utf-8")
        
        result_a = run_speller(dictionary=mock_dictionary, text_path=text_file)
        result_b = run_speller(dictionary=mock_dictionary, text_path=text_file)
        
        assert result_a is not result_b
        assert result_a.benchmarks is not result_b.benchmarks
        
        
# =============================================================================
# LOAD_DICTIONARY — ERROR PATH TESTING
# =============================================================================

class TestLoadDictionary:
    """Test load_dictionary() with a FailingDictionary.

    FailingDictionary.load() always returns False, simulating a
    corrupted or unreadable dictionary file at the load step.

    The SystemExit for load failure belongs here — in load_dictionary()
    — not in run_speller(), because run_speller() never calls load().
    Testing it in the right place keeps each component's contract clear.
    """
    
    def test_failing_dictionary_raises_system_exit(
        self,
        failing_dictionary: FailingDictionary,
        sample_dict_file: Path,
    ) -> None:
        """load_dictionary() raises SystemExit when load() returns False.

        This is NEGATIVE TESTING — verifying that error paths work
        correctly is just as important as testing happy paths.

        FailingDictionary.load() always returns False, triggering the
        SystemExit inside load_dictionary(). main() catches it and maps
        it to ExitCode.LOAD_FAILED.
        """
        from speller.load_dictionary import load_dictionary
        
        with pytest.raises(SystemExit):
            load_dictionary(
                dictionary=failing_dictionary,
                dict_path=sample_dict_file,
            )
            
    def test_successful_load_returns_tuple(
        self,
        mock_dictionary: MockDictionary,
        sample_dict_file: Path,
    ) -> None:
        """load_dictionary() returns (dictionary, BenchmarkResult) on success.

        The 2-tuple keeps the call site clean with unpacking:
            loaded_dict, load_result = load_dictionary(...)
        """
        from speller.load_dictionary import load_dictionary
        
        loaded_dict, load_result = load_dictionary(
            dictionary=mock_dictionary,
            dict_path=sample_dict_file,
        )
        
        assert loaded_dict is mock_dictionary
        assert isinstance(load_result, BenchmarkResult)
        assert load_result.operation == "load"
        assert load_result.elapsed_seconds >= 0
        

# =============================================================================
# INTEGRATION — REAL FILES
# =============================================================================

class TestRunSpellerIntegration:
    """Integration tests with real HashTableDictionary and text files.

    These tests exercise the full pipeline: real dictionary loading,
    real text processing, real spell checking. They're slower but
    catch integration bugs that mock-based tests miss.

    The load step mirrors main()'s batch pattern exactly:
        loaded_dict, load_result = load_dictionary(dictionary=..., dict_path=...)
        benchmarks = {"load": load_result}
        result = run_speller(dictionary=loaded_dict, text_path=..., benchmarks=benchmarks)
    """
    
    @pytest.mark.integration
    def test_cat_txt_zero_misspelled(
        self,
        empty_dictionary: DictionaryProtocol,
        large_dict_path: Path,
        texts_dir: Path,
    ) -> None:
        """cat.txt should have 0 misspelled words with the large dictionary.

        The simplest validation: "A cat is not a caterpillar"
        — all 6 words are in the large dictionary.
        """
        from speller.load_dictionary import load_dictionary
        
        text_path = texts_dir / "cat.txt"
        if not text_path.exists():
            pytest.skip(f"Text file not found: {text_path}")
        
        loaded_dict, load_result = load_dictionary(
            dictionary=empty_dictionary,
            dict_path=large_dict_path,
        )
        
        result = run_speller(
            dictionary=loaded_dict,
            text_path=text_path,
            benchmarks={"load": load_result},
        )
        
        assert result.words_misspelled == 0
        assert result.words_in_text == 6
        assert result.words_in_dictionary == 143091
        # All three benchmarks present when load_dictionary is used
        assert "load" in result.benchmarks
        assert "check" in result.benchmarks
        assert "size" in result.benchmarks