"""Provider registry for the llm_api_smoke_test package.

Provides the infrastructure for a **plugin-style registry**: new
provider adapters are added to the system by decorating a class with
:func:`register_class` — no changes to ``__main__.py``, ``runner.py``,
``batch_runner.py``, or ``providers.py``'s Protocol definitions are
required.

Two-axis indexing — name × kind
-------------------------------
Each provider name (``"anthropic"``, ``"gemini"``) maps to a single
:class:`ProviderList` that bundles BOTH the sync and async variants.
The decorator distinguishes between them via the ``kind`` parameter
(``"sync"`` or ``"async"``).  This lets the composition root in
``__main__.py`` choose between sync and async execution paths from
the same CLI name without a separate registry for each.

Immutability
------------
:class:`DictInfo` and :class:`ProviderList` are both frozen
dataclasses.  Updates use :func:`dataclasses.replace` to produce a
new :class:`ProviderList` with one field changed, then reassign
back to ``dicts[name]``.  This keeps the registry safe from
accidental mutation while still allowing the two decorator calls
(sync, then async, in some order at import time) to converge on a
fully-populated bucket.

Components
----------
:class:`DictInfo`
    Metadata container pairing a registry key with a concrete
    provider class, its display name, description, and accumulated
    run results.
:class:`ProviderList`
    Per-name bundle of sync + async :class:`DictInfo` instances.
    Either slot may be ``None`` if only one variant was registered.
:data:`dicts`
    Module-level ``dict[str, ProviderList]`` — the registry itself.
    Populated at import time when ``providers.py`` executes its
    ``@register_class`` decorators.
:func:`register_class`
    Decorator factory.  ``@register_class("key", "sync"/"async", "...")``
    upserts the decorated class into :data:`dicts` without modifying
    the class itself.

Roadmap relevance
-----------------
First implemented for the speller package's dictionary backends; now
extended here to support the sync/async dual-registration shape.
Stage 2+ will reuse the same shape for ``VectorStore`` (PolicyPulse),
``ExtractionBackend`` (FormSense), and ``DataSource`` (AFC) registries
whenever a single conceptual backend has multiple variant
implementations.
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
    """Typed mapping for one provider's accumulated smoke-test outcomes.

    Stored on :attr:`DictInfo.results` keyed by an arbitrary label
    (typically the prompt string or a per-run identifier).  Using a
    ``TypedDict`` rather than a frozen dataclass because the dict
    container is convenient for JSON serialisation in benchmark
    reports.

    Keys
    ----
    successes : list of SmokeTestResult
        Provider calls that completed and returned a parsed result.
    failures : list of (str, Exception)
        Tuples of ``(provider_class_name, exception)`` for calls
        that raised.  Captured rather than re-raised so a batch run
        can continue past a single provider's outage.
    """
    
    successes: list[SmokeTestResult]
    failures: list[CallFailure]
    

@dataclass(frozen=True)
class DictInfo:
    """Metadata container for one registered LLM provider variant.

    Pairs a provider class (sync OR async, not both) with its display
    name, description, and a mutable results dict that accumulates
    :class:`RunResults` across smoke-test runs within a single
    program execution.

    Two ``DictInfo`` instances exist per provider name — one for the
    sync variant and one for the async variant — bundled together
    inside a :class:`ProviderList`.

    The dataclass itself is ``frozen``, but ``results`` is an
    intentionally mutable inner ``dict`` — updated in place during
    each ``main()`` iteration.  This is the same "frozen container,
    mutable history" pattern used by ``speller.register.DictInfo``.

    Parameters
    ----------
    provider_class : type[LLMProvider | AsyncLLMProvider]
        The class itself, not an instance.  Callers instantiate it
        via ``info.provider_class(settings)`` in the composition
        root.  ``type[X]`` means "the class object for X" — pyright
        knows the call produces an ``LLMProvider`` (or async)
        instance.
    class_name : str
        Display name derived from ``provider_class.__name__``
        (e.g. ``"AsyncAnthropicProvider"``).  Distinct from the
        registry key (``"anthropic"``): the key is for CLI lookup;
        the name is for human-readable output.
    description : str
        One-line description used in CLI help and benchmark reports.
        Falls back to ``provider_class.__doc__`` if not supplied
        explicitly.
    results : dict of {str : RunResults}, optional
        Accumulated outcomes keyed by run label.  Empty by default;
        populated during ``main()`` execution.
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
    """Sync + async pair of :class:`DictInfo` for one provider name.

    One ``ProviderList`` lives in :data:`dicts` per provider name
    (``"anthropic"``, ``"gemini"``).  Either slot may be ``None`` if
    only one variant has been registered — typical during partial
    registration at import time before both decorator calls have run.

    ``frozen=True`` makes this safe to share across modules without
    fear of accidental mutation; ``slots=True`` reduces memory
    footprint.  Updates go through :func:`dataclasses.replace` in
    :func:`register_class.decorator`.

    Attributes
    ----------
    async_provider : DictInfo or None, optional
        Metadata for the async variant (e.g. ``AsyncAnthropicProvider``).
        ``None`` if no async variant has been registered.
    sync_provider : DictInfo or None, optional
        Metadata for the sync variant (e.g. ``AnthropicProvider``).
        ``None`` if no sync variant has been registered.

    Examples
    --------
    >>> dicts["anthropic"].sync_provider.provider_class
    <class 'llm_api_smoke_test.providers.AnthropicProvider'>
    >>> dicts["anthropic"].async_provider.provider_class
    <class 'llm_api_smoke_test.providers.AsyncAnthropicProvider'>

    Notes
    -----
    Why both as ``DictInfo | None`` instead of requiring both?
        Decorators fire in source order at import time.  When the
        first ``@register_class("anthropic", "sync", ...)`` runs,
        the async slot doesn't have a value yet — so the initial
        :class:`ProviderList` must be constructable with ``None``.
        The second decorator call replaces ``async_provider`` and
        leaves ``sync_provider`` intact.
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
    """Decorator factory that upserts a provider class into :data:`dicts`.

    Returns a decorator that inserts the decorated class into the
    ``kind``-typed slot of ``dicts[name]`` (creating the
    :class:`ProviderList` if absent), then returns the class
    **unchanged**.  Because the class is returned as-is,
    ``@functools.wraps`` is unnecessary — there is no wrapper
    function whose metadata needs copying.

    Parameters
    ----------
    name : str
        Registry key for CLI lookup (e.g. ``"anthropic"``, ``"gemini"``).
        Multiple ``@register_class`` calls may share a name — each one
        populates a different ``kind`` slot of the same
        :class:`ProviderList`.
    kind : Literal["sync", "async"]
        Which slot of :class:`ProviderList` to populate.
        ``Literal`` typing means Pyright catches misspellings
        (``kind="syn"``) at edit time.
    description : str, optional
        One-line description for CLI help and benchmark output.
        Falls back to ``provider_class.__doc__`` if empty.

    Returns
    -------
    RegDecorator
        A callable that accepts a ``type[LLMProvider | AsyncLLMProvider]``
        and returns it unchanged after registering it.

    Examples
    --------
    ::

        @register_class("anthropic", "sync", "Anthropic sync LLM provider.")
        class AnthropicProvider:
            ...

        @register_class("anthropic", "async", "Anthropic async LLM provider.")
        class AsyncAnthropicProvider:
            ...

        bundle = dicts["anthropic"]
        sync_cls  = bundle.sync_provider.provider_class    # AnthropicProvider
        async_cls = bundle.async_provider.provider_class   # AsyncAnthropicProvider

    Notes
    -----
    Adding a new provider requires exactly three things:

    1. Create classes satisfying
       :class:`~llm_api_smoke_test.providers.LLMProvider`
       and/or :class:`~llm_api_smoke_test.providers.AsyncLLMProvider`.
    2. Decorate each with ``@register_class("key", "sync"/"async", "...")``.
    3. Ensure ``providers.py`` is imported before :data:`dicts` is
       read — handled automatically because ``__main__.py`` imports
       ``providers`` inside its import guard.

    Why ``Literal["sync", "async"]`` instead of a free-text description match?
        An earlier draft inferred kind from the description string via
        ``"sync" in description``.  That broke because ``"sync"`` is a
        substring of ``"async"`` — every async provider was registered
        as sync.  Explicit ``Literal`` typing eliminates the ambiguity
        AND lets Pyright catch typos at edit time.
    """
    
    def decorator(provider_class: SyncAsyncProvider) -> SyncAsyncProvider:
        """Insert ``provider_class`` into :data:`dicts` and return it unchanged.

        Builds a :class:`DictInfo` for the class, looks up the existing
        :class:`ProviderList` for ``name`` (or creates an empty one),
        then uses :func:`dataclasses.replace` to produce a new
        :class:`ProviderList` with the ``kind``-typed slot populated.
        The new instance is assigned back to ``dicts[name]``.

        Parameters
        ----------
        provider_class : type[LLMProvider | AsyncLLMProvider]
            The concrete provider class being registered.

        Returns
        -------
        type[LLMProvider | AsyncLLMProvider]
            The same class passed in, unmodified.  ``@functools.wraps``
            unnecessary — no wrapper function substituted.

        Notes
        -----
        Why ``dicts.get()`` instead of ``dicts.setdefault()``?
            Both work for the frozen-replace flow because the assignment
            on the next line overwrites the dict slot regardless.
            ``get()`` is fractionally cleaner: ``setdefault()`` would
            insert a fresh empty :class:`ProviderList` as a side effect
            that is then immediately replaced — wasted work.

        Why ``**{field_name: info}``?
            ``replace()`` accepts field updates as keyword arguments,
            but ``field_name`` is a string variable — Python can't
            interpolate it into a keyword name directly.  Building a
            dict and unpacking with ``**`` is the standard idiom for
            passing keyword arguments whose names are computed at
            runtime.
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