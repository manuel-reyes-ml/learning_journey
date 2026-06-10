"""
"""

# =============================================================================
# IMPORTS
# =============================================================================

from __future__ import annotations

from dataclasses import FrozenInstanceError
from typing import Protocol

import pytest

from llm_api_smoke_test.register import (
    DictInfo,
    ProviderList,
    RunResults,
    dicts,
    register_class,
)

# =============================================================================
# Test-only fake provider classes
# =============================================================================
 
# We define minimal classes here — NOT in conftest — because these are
# specific to registry tests.  They don't even need to implement smoke_test;
# the registry just stores classes.

class FakeRegistryProvider:
    """Stand-in class for register_class tests — no real Protocol needed."""
    
    def __init__(self, settings) -> None:
        self._settings = settings
        
        
class FakeAsyncRegistryProvider:
    """Async sibling of FakeRegistryProvider — same minimal shape."""
    
    def __init__(self, settings) -> None:
        self._settings = settings
        
        
# =============================================================================
# DictInfo — the small frozen container
# =============================================================================

class TestDictInfo:
    """DictInfo is a frozen dataclass — verify the contract."""
    
    def test_construction_minimal(self) -> None:
        """All required keyword-only fields work."""
        info = DictInfo(
            provider_class=FakeRegistryProvider,  # type: ignore[arg-type]
            class_name="FakeRegistryProvider",
            description="A test fake",
        )
        
        assert info.provider_class is FakeRegistryProvider
        assert info.class_name == "FakeRegistryProvider"
        assert info.description == "A test fake"
        # results defaults to empty dict.
        assert info.results == {}
        
    def test_results_default_is_unique_per_instance(self) -> None:
        """default_factory=dict produces a FRESH dict per instance.
        
        This is the classic mutable-default-argument trap.  A naïve
        ``= {}`` default would be SHARED across all instances —
        every DictInfo would alias the same dict.  default_factory
        fixes it.
        """
        a = DictInfo(
            provider_class=FakeRegistryProvider,  # type: ignore[arg-type]
            class_name="A",
            description="a",
        )
        b = DictInfo(
            provider_class=FakeRegistryProvider,  # type: ignore[arg-type]
            class_name="B",
            description="b",
        )
        
        # IS NOT — different object identity, not just equal value.
        assert a.results is not b.results
        
    def test_is_frozen(self) -> None:
        """frozen=True must prevent attribute reassignment."""
        info = DictInfo(
            provider_class=FakeRegistryProvider,  # type: ignore[arg-type]
            class_name="Test",
            description="test",
        )
        
        # FrozenInstanceError is the specific exception dataclass raises.
        with pytest.raises(FrozenInstanceError):
            info.class_name = "Mutated"  # type: ignore[misc]
            
        
# =============================================================================
# ProviderList — sync + async bundle
# =============================================================================

