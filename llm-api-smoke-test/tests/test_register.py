"""Tests for llm_api_smoke_test.register.
 
Covers the plugin-registry mechanics:
- :class:`DictInfo` — frozen container
- :class:`ProviderList` — sync/async pair
- :func:`register_class` — decorator factory, sync/async kind dispatch
- :data:`dicts` — module-level registry state
 
Why test the registry?
----------------------
The registry is the package's central wiring point.  A subtle bug
(wrong key, missing slot, frozen-vs-mutable confusion) silently
breaks the entire CLI.  Tests pin the contract so refactors don't
regress.
"""

# =============================================================================
# IMPORTS
# =============================================================================

from __future__ import annotations

from dataclasses import FrozenInstanceError

import pytest

from llm_api_smoke_test.register import (
    DictInfo,
    ProviderList,
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
        with pytest.raises((TypeError, AttributeError, FrozenInstanceError)):
            bundle.bogus_attr = "fail"  # type: ignore[misc, attr-defined]
            
            
# =============================================================================
# register_class decorator — the main attraction
# =============================================================================

class TestRegisterClass:
    """Tests for the register_class decorator factory.
    
    These tests use a LOCAL registry-like dict — they don't pollute
    the global ``dicts`` module-level registry, because mutating
    module state from tests creates ordering dependencies.
    """
 
    # The 'monkeypatch' fixture is pytest's built-in tool for safely
    # replacing module-level state during a test.  After the test ends,
    # everything is restored — even on failure.
    @pytest.fixture
    def clean_registry(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Replace dicts with an empty dict for the duration of one test.
        
        Why?  The real ``dicts`` is populated at import time when
        providers.py loads.  If tests mutated it directly, test order
        would matter (test A leaves garbage that fails test B).
        monkeypatch.setattr swaps the reference and restores after.
        """
        # Replace 'dicts' on the register module with an empty dict.
        # The decorator looks up 'dicts' via module global — swapping
        # the module attribute is what affects the decorator's behaviour.
        monkeypatch.setattr("llm_api_smoke_test.register.dicts", {})
        
    def test_registers_sync_provider(self, clean_registry: None) -> None:
        """@register_class('key', 'sync', ...) populates sync_provider."""
        # Import dicts FRESH after monkeypatch — module attribute is
        # now an empty dict.
        from llm_api_smoke_test.register import dicts as test_dicts
        
        # Apply the decorator manually — same effect as @register_class
        # on a class definition.
        decorator = register_class("testkey", "sync", "test sync provider")
        decorator(FakeRegistryProvider)  # type: ignore[arg-type]
        
        # The registry now has an entry
        assert "testkey" in test_dicts
        bundle = test_dicts["testkey"]
        
        # Sync slot populated, async still None.
        assert bundle.sync_provider is not None
        assert bundle.sync_provider.provider_class is FakeRegistryProvider
        assert bundle.sync_provider.class_name == "FakeRegistryProvider"
        assert bundle.async_provider is None
        
    def test_registers_async_provider(self, clean_registry: None) -> None:
        """@register_class('key', 'async', ...) populates async_provider."""
        from llm_api_smoke_test.register import dicts as test_dicts
        
        register_class("testkey", "async", "test async")(
            FakeAsyncRegistryProvider   # type: ignore[arg-type]
        )
        
        bundle = test_dicts["testkey"]
        assert bundle.async_provider is not None
        assert bundle.sync_provider is None
        
    def test_both_kinds_under_one_key(self, clean_registry: None) -> None:
        """Two decorators on the same key populate both slots.
        
        This is the core behaviour of the sync/async dual-registration.
        Test it explicitly because it relies on the dataclasses.replace
        round-trip, which is non-obvious.
        """
        from llm_api_smoke_test.register import dicts as test_dicts
        
        # First decorator - sync.
        register_class("testkey", "sync", "sync v")(
            FakeRegistryProvider    # type: ignore[arg-type]
        )
        
        # Second decorator - async, SAME key.
        register_class("testkey", "async", "async v")(
            FakeAsyncRegistryProvider   # type: ignore[arg-type]
        )
        
        bundle = test_dicts["testkey"]
        
        # BOTH slots populated.
        assert bundle.sync_provider is not None
        assert bundle.async_provider is not None
        
        # Verify they hold the right classes.
        assert bundle.sync_provider.provider_class is FakeRegistryProvider
        assert bundle.async_provider.provider_class is FakeAsyncRegistryProvider
        
    def test_decorator_return_class_unchanged(self, clean_registry: None) -> None:
        """The decorated class must come out IDENTICAL — no wrapping."""
        # IS check — same object identity, not just equal.
        result = register_class("k", "async")(FakeRegistryProvider)  # type: ignore[arg-type]
        assert result is FakeRegistryProvider
        
    def test_description_falls_back_to_docstring(
        self, clean_registry: None
    ) -> None:
        """Empty description → uses provider_class.__doc__ instead."""
        from llm_api_smoke_test.register import dicts as test_dicts
        
        class DocumentedProvider:
            """Docstring used as fallback description."""
            def __init__(self, setting) -> None: pass
            
        # Empty description argument.
        register_class("doc_test", "sync", "")(
            DocumentedProvider   # type: ignore[arg-type]
        )
        
        info = test_dicts["doc_test"].sync_provider
        assert info is not None
        # Falls back to __doc__ - Pydantic-style fallback.
        assert "Docstring used" in info.description
        
        
# =============================================================================
# Module-level dicts — the REAL registry, after providers.py imports
# =============================================================================

class TestLiveRegistry:
    """Inspect the actual dicts populated at package import time.
    
    These tests DON'T mutate the registry — they only read it.  Safe
    to run in any order, no monkeypatch needed.
    """
    
    def test_anthropic_is_registered(self) -> None:
        """Both sync and async Anthropic providers must be present
        after importing providers.py.
        """
        # The mere act of importing register triggers providers.py
        # imports indirectly — which runs the @register_class
        # decorators at module load. 
        from llm_api_smoke_test import providers  # noqa: F401
        
        assert "anthropic" in dicts
        bundle = dicts["anthropic"]
        
        assert bundle.sync_provider is not None
        assert bundle.async_provider is not None
        
    def test_gemini_is_registered(self) -> None:
        """Same coverage as above for Gemini."""
        from llm_api_smoke_test import providers  # noqa: F401
        
        assert "gemini" in dicts
        bundle = dicts["gemini"]
        
        assert bundle.sync_provider is not None
        assert bundle.async_provider is not None