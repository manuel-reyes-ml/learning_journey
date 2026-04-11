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