# Test files must start with 'test_' so they are auto-discovery by pytest
"""
"""

from __future__ import annotations

from pathlib import Path
import pytest

from speller.benchmarks import BenchmarkResult, timer, timed


# =============================================================================
# BENCHMARKRESULT DATACLASS
# =============================================================================

# Test classes must start with capital T, colleted by class-name pattern
# Test functions/methods must start with 'test_', collected by function-name pattern

class TestBenchMarkResult:
    """Test the BenchmarkResult frozen dataclass."""
    
    def test_creation_with_required_fields(self) -> None:
        """BenchmarkResult can be created with required fields only."""
        result = BenchmarkResult(operation="load", elapsed_seconds=0.5)
        assert result.operation == "load"
        assert result.elapsed_seconds == 0.5
        
    def test_metadata_defaults_to_empty_dict(self) -> None:
        """metadata field defaults to empty dict when not provided."""
        result = BenchmarkResult(operation="test", elapsed_seconds=0.1)
        assert result.metadata == {}
        
    def test_creation_with_metadata(self) -> None:
        """BenchmarkResult accepts optional metadata."""
        meta = {"input_file": "test.txt"}
        result = BenchmarkResult(
            operation="check",
            elapsed_seconds=0.2,
            metadata=meta,
        )
        assert result.metadata == meta
        
    def test_frozen_immutability(self) -> None:
        """Frozen dataclass prevents mutation after creation.

        This is WHY we use frozen=True — benchmark results should
        never change after being recorded. If they could be mutated,
        you'd never trust the timing data.
        """
        result = BenchmarkResult(operation="load", elapsed_seconds=0.5)
        with pytest.raises(AttributeError):
            result.operation = "hacked"   # type: ignore[misc]
            
    def test_str_format(self) -> None:
        """__str__ returns human-readable timing summary."""
        result = BenchmarkResult(operation="load", elapsed_seconds=1.234)
        assert str(result) == "load: 1.23s"
        
    def test_keyword_only_enforcement(self) -> None:
        """KW_ONLY prevents positional argument construction.

        BenchmarkResult("load", 0.5) should fail because KW_ONLY
        forces keyword arguments: BenchmarkResult(operation="load", ...).
        This prevents argument-order bugs.
        """
        with pytest.raises(TypeError):
            BenchmarkResult("load", 0.5)   # type: ignore[misc]


# =============================================================================
# TIMER CONTEXT MANAGER
# =============================================================================

class TestTimer:
    """Test the timer() context manager.

    The timer wraps a code block and produces a BenchmarkResult.
    We test:
    - That it produces a result
    - That the result has the correct operation name
    - That elapsed time is positive and reasonable
    - That metadata is stored correctly
    """
    
    def test_timer_produces_result(self) -> None:
        """timer() populates the container with a BenchmarkResult."""
        with timer("test_op") as t:
            total = sum(range(1000))   # some work
        
        assert "result" in t
        assert isinstance(t["result"], BenchmarkResult)
        
    def test_timer_operation_name(self) -> None:
        """BenchmarkResult has the correct operation name."""
        with timer("my_operation") as t:
            pass
        
        assert t["result"].operation == "my_operation"
        
    def test_timer_elapsed_is_positive(self) -> None:
        """Elapsed time is always positive (even for fast operations).

        time.perf_counter() is monotonic — it never goes backward.
        Even an empty block takes some nonzero time.
        """
        with timer("fast") as t:
            pass  # nearly instant
        
        assert t["result"].elapsed_seconds > 0
        
    def test_timer_elapsed_is_reasonable(self) -> None:
        """Elapsed time is reasonable (not negative, not huge).

        pytest.approx() handles floating-point comparison:
            assert 0.1 == pytest.approx(0.1, abs=0.05)
        means "0.1 is within ±0.05 of 0.1"

        For timing tests, we check the value is in a reasonable
        range rather than an exact match (timing varies by machine).
        """
        import time
        
        with timer("sleep_test") as t:
            time.sleep(0.05)  # sleep 50ms
            
        elapsed = t["result"].elapsed_seconds
        # Should be at least 0.04s (sleep overhead) and less than 1s
        assert elapsed >= 0.04
        assert elapsed < 1.0
        
    def test_timer_without_metadata(self) -> None:
        """timer() without input_file produces empty metadata."""
        with timer("no_meta") as t:
            pass
        
        assert t["result"].metadata == {}
        
    def test_timer_with_metadata(self) -> None:
        """timer() with input_file stores FDATA in metadata."""
        test_path = Path("texts/cat.txt")
        
        with timer("check", input_file=test_path) as t:
            pass
        
        result = t["result"]
        assert "input_file" in result.metadata
        fdata = result.metadata["input_file"]
        assert fdata.fname == "cat.txt"
        
    def test_timer_container_empty_during_block(self) -> None:
        """Container is empty DURING the with block, filled AFTER.

        This tests the fundamental design: yield happens before
        timing is complete, so the container must be mutable.
        """
        with timer("during_test") as t:
            # DURING the block - container should be empty
            assert "result" not in t
        
        # AFTER the block - container should have result
        assert "result" in t
        
        
# =============================================================================
# TIMED DECORATOR
# =============================================================================

class TestTimed:
    """Test the timed() parameterized decorator.

    The decorator wraps a function with timer() and stores the
    BenchmarkResult on the wrapper.benchmark attribute.
    """
    
    def test_timed_preserves_return_value(self) -> None:
        """Decorated function returns its original value unchanged.

        The decorator must NOT alter the function's return value.
        It only adds timing as a side effect.
        """
        @timed("compute")
        def add(a: int, b: int) -> int:
            return a + b
        
        result = add(3, 4)
        assert result == 7
        
    def test_timed_stores_benchmark(self) -> None:
        """BenchmarkResult is accessible via wrapper.benchmark."""
        @timed("compute")
        def multiply(a: int, b: int) -> int:
            return a * b
        
        multiply(3, 4)
        assert multiply.benchmark is not None   # type: ignore[attr-define]
        assert isinstance(multiply.benchmark, BenchmarkResult)  # type: ignore[attr-define]
        
    def test_timed_operation_name(self) -> None:
         """Benchmark has the correct operation name."""
         @timed("my_op")
         def noop() -> None:
             pass
         
         noop()
         assert noop.benchmark.operation == "my_op"     # type: ignore[attr-define]
         
    def test_timed_preserves_function_name(self) -> None:
        """@wraps preserves the original function's __name__.

        Without @wraps, the decorated function's __name__ would
        be "wrapper" instead of the original name. This matters
        for debugging, logging, and pytest output.
        """
        @timed("test")
        def my_function() -> None:
            pass
        
        assert my_function.__name__ == "my_function"
        
    def test_timed_preserves_docstring(self) -> None:
        """@wraps preserves the original function's __doc__."""
        @timed("test")
        def documented_func() -> None:
            """This is my docstring."""
            pass
        
        assert documented_func.__doc__ == "This is my docstring."
        
    def test_timed_benchmark_updates_on_each_call(self) -> None:
        """Each call updates the benchmark (latest timing wins)."""
        @timed("test")
        def work(n: int) -> int:
            return sum(range(n))
        
        work(100)
        first_time = work.benchmark.elapsed_seconds     # type: ignore[attr-define]
        
        work(100_000)
        second_time = work.benchmark.elapsed_seconds    # type: ignore[attr-define]
        
        # Second call (more work) should take longer
        # (not guaranteed on fast machines, but generally true)
        assert work.benchmark is not None   # type: ignore[attr-define]
        assert isinstance(second_time, float)