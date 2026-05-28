"""
"""

# =============================================================================
# IMPORTS
# =============================================================================

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field, KW_ONLY, replace
from typing import Literal, TypedDict

from llm_api_smoke_test.providers import (
    AsyncLLMProvider,
    LLMProvider,
    SmokeTestResult,
)

from llm_api_smoke_test.runner import CallFailure

# No ImportError sys.exit() on regular module so the
# error propagates to the caller (__main__.py).

# =============================================================================
# EXPORTS
# =============================================================================

__all__ = ["register_class"]


# =============================================================================
# MODULE CONFIGURATION
# =============================================================================
# =====================================================
# Type Aliases
# =====================================================

# Literal -> ProviderKind is only 'sync' or 'async' only
type ProviderKind = Literal["sync", "async"]

type SyncAsyncProvider = type[LLMProvider | AsyncLLMProvider]
type RegDecorator = Callable[[SyncAsyncProvider], SyncAsyncProvider]


# =====================================================
# Dict Metadata Configuration
# =====================================================

class RunResults(TypedDict):
    """
    """
    
    successes: list[SmokeTestResult]
    failures: list[CallFailure]
    

@dataclass(frozen=True)
class DictInfo:
    """
    """
    
    # Required fields (no default) must come first
    _:  KW_ONLY  # Everything after this is keyword-only
    provider_class: SyncAsyncProvider
    class_name: str
    description: str
    
    # Optional fields with defaults afterwards
    results: dict[str, RunResults] = field(default_factory=dict)
    
# Tells pyright this is an INSTANCE
#   dict_class: DictionaryProtocol          # an object with .load(), .check()

# Tells pyright this is a CLASS
#   dict_class: type[DictionaryProtocol]    # a class you can call with ()

# type[X] means "the class itself, not an instance of it." Pyright knows
# dict_class() is valid because you're calling a class constructor, which
# returns an instance of DictionaryProtocol.


@dataclass(frozen=True, slots=True)
class ProviderList:
    """
    """
    
    _: KW_ONLY  # After this is keyword only
    
    # Default makes them optional
    async_provider: DictInfo | None = None
    sync_provider: DictInfo | None = None


# =====================================================
# Constants
# =====================================================

dicts: dict[str, ProviderList] = {}


# =============================================================================
# DICTIONARY REGISTRY
# =============================================================================

# A decorator factory is just a function that takes custom parameters
# and generates a decorator.
def register_class(
    name: str, 
    kind: ProviderKind,  # explicit only -> kind="sync" / kind="async"
    description: str = "",
) -> RegDecorator:
    """
    """
    
    def decorator(provider_class: SyncAsyncProvider) -> SyncAsyncProvider:
        """
        """
        info = DictInfo(
            provider_class=provider_class,
            class_name=provider_class.__name__,
            description=description or provider_class.__doc__ or "",
        )
        
        # Get-or-create the ProviderList for this name
        # bucket = dicts.setdefault(name, ProviderList())
        
        # match kind:
        #     case "sync":
        #         bucket.sync_provider = info
        #     case _:  # "async" - mypy/pyright narrows it because of Literal
        #         bucket.async_provider = info
        
        bucket = dicts.get(name, ProviderList())
        field_name = f"{kind}_provider"  # "sync_provider" or "async_provider"
        
        # Return a new object replacing specified fields with new values.
        # This is especially useful for frozen classes
        #
        # The ** operator unpacks the dict — it turns each key-value pair
        # into a key=value keyword argument at the call site.
        # What we want — replace the field named "sync_provider"
        #   replace(bucket, sync_provider=info)          # ✅ works
        # But field_name is a string variable — we can't write replace(bucket, field_name=info)
        # because Python would treat field_name literally as a keyword called "field_name",
        # not as a variable to interpolate.
        #
        # The **{field_name: info} pattern is the workaround: build the kwargs dict programmatically,
        # then unpack:
        #   Step 1: Build the dict       → {"sync_provider": info}
        #   Step 2: Unpack with **       → replace(bucket, sync_provider=info)
        #
        # General rule: * spreads sequences into positional args; ** spreads dicts into keyword args.
        # Same syntax on both sides of the function call (sender unpacks; receiver collects).
        dicts[name] = replace(bucket, **{field_name: info}) 
        
        # RECEIVER — function definition collects loose args INTO a container
        #   def func(*args, **kwargs):
                # args   = tuple of positional args
                # kwargs = dict of keyword args
        #       print(args, kwargs)
        #
        # SENDER — call site spreads a container OUT INTO loose args
        #   my_list = [1, 2, 3]
        #   my_dict = {"a": 10, "b": 20}
        #   func(*my_list, **my_dict)
        #   Equivalent to: func(1, 2, 3, a=10, b=20)
        #
        # The dict gets unpacked at the call site, then the receiver collects them back into a dict.
        # Looks redundant, but it isn't — the value at the call site is a real dict variable, while
        # the receiver gets loose keyword arguments that happen to be collected into a dict.
        # The transformation is meaningful when you're forwarding kwargs through layers.
    
        return provider_class  # Return unchanged class
        # class goes in, class comes out. The class' __name__, __doc__, __qualname__
        # are all intact because you never created a replacement. Nothing to fix,
        # so @wraps would do nothing useful.
        
    return decorator

# Instantiate by key - calling a class creates an instance
# dictionary = dicts["hash"].dict_class() -> HashTableDictionary()

# d = {"a": 1}

# --- get() ---
# val = d.get("b", 999)
# print(val)   # 999
# print(d)     # {"a": 1}             ← dict UNCHANGED

# --- setdefault() ---
# val = d.setdefault("b", 999)
# print(val)   # 999
# print(d)     # {"a": 1, "b": 999}   ← dict NOW HAS "b": 999
#
# After setdefault, the next call returns the existing value and does nothing:
# val = d.setdefault("b", 12345)
# print(val)   # 999  ← existing value, NOT 12345
# print(d)     # {"a": 1, "b": 999}
# That's the whole story. setdefault = "give me the value at key; if there isn't one,
# store this default first and give me that."
#
# Summary:
#   1. Both return the value or a default if missing — identical return value.
#   2. Only setdefault mutates the dict, inserting the default at key. get is pure-read.
#   3. In your registry, setdefault is the right call because two decorators must
#   operate on the same ProviderList instance — setdefault guarantees it.
#   4. Watch out for two traps: the default is always evaluated (even when unused),
#   and a shared mutable default is shared across all calls. Use defaultdict if
#   construction is expensive.