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

class TestProviderList:
    """ProviderList bundles sync/async DictInfo — verify the slots."""
    
    def test_default_construction_has_both_none(self) -> None:
        """Both slots default to None — letting decorators populate
        them one at a time at import time.
        """ 
        bundle = ProviderList()
        
        assert bundle.sync_provider is None
        assert bundle.async_provider is None
        
    def test_construction_with_sync_only(self) -> None:
        """Partial construction works — async slot stays None."""
        sync_info = DictInfo(
            provider_class=FakeRegistryProvider,  # type: ignore[arg-type]
            class_name="FakeSync",
            description="sync",
        )
        
        bundle = ProviderList(sync_provider=sync_info)
        
        assert bundle.sync_provider is sync_info
        assert bundle.async_provider is None
        
    def test_is_frozen_with_slots(self) -> None:
        """ProviderList is frozen + slotted — both attributes
        of the contract are tested here.
        """
        bundle = ProviderList()
        
        # frozen rejection
        with pytest.raises(FrozenInstanceError):
            bundle.sync_provider = "anything"  # type: ignore[misc]
            
        # slots - cannot add arbitrary attributes either
        with pytest.raises((AttributeError, FrozenInstanceError)):
            bundle.bogus_attr = "fail"  # type: ignore[misc, attr-defined]
            
            
# =============================================================================
# register_class decorator — the main attraction
# =============================================================================