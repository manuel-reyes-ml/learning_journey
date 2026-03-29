"""Dictionary backend registry for the speller package.
 
Provides the infrastructure for a **plugin-style registry**: new
dictionary backends are added to the system by decorating a class with
:func:`register_class` — no changes to ``__main__.py``, ``speller.py``,
or ``protocols.py`` are required.
 
Components
----------
:class:`DictInfo`
    Metadata container pairing a registry key with a concrete
    :class:`~speller.protocols.DictionaryProtocol` class, a display
    name, a description, and accumulated
    :class:`~speller.speller.SpellerResult` objects from benchmark runs.
 
:data:`dicts`
    Module-level ``dict[str, DictInfo]`` — the registry itself.
    Populated at import time when ``dictionaries.py`` executes and its
    ``@register_class`` decorators run.
 
:func:`register_class`
    Decorator factory.  ``@register_class("key", "description")``
    inserts the decorated class into :data:`dicts` without modifying
    the class itself.
 
Execution order
---------------
1. ``speller/__init__.py`` imports ``dictionaries`` as a side effect.
2. ``dictionaries.py`` executes top-to-bottom — all ``@register_class``
   calls run.
3. Each call writes a :class:`DictInfo` entry into :data:`dicts`.
4. By the time ``__main__.py`` reads :data:`dicts`, it is fully
   populated.
 
Roadmap relevance
-----------------
The same registry scales to every future Stage 1+ project:
 
- DataVault:   ``LLMProvider`` registry  (``"gemini"``, ``"openai"``)
- PolicyPulse: ``VectorStore`` registry  (``"chroma"``, ``"pinecone"``)
- FormSense:   ``ExtractionBackend``     (``"gemini-vision"``, ``"custom"``)
- AFC:         ``DataSource``            (``"sec"``, ``"news"``)
"""

# =============================================================================
# IMPORTS
# =============================================================================

from __future__ import annotations

from dataclasses import dataclass, KW_ONLY, field
import logging
from typing import Callable

from speller.protocols import DictionaryProtocol
from speller.speller import SpellerResult


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

__all__ = [
    "DictInfo",
    "dicts",
    "register_class",
]


# =============================================================================
# MODULE CONFIGURATION
# =============================================================================
# =====================================================
# Type Aliases
# =====================================================

type RegDecorator = Callable[[type[DictionaryProtocol]], type[DictionaryProtocol]]


# =====================================================
# Dict Metadata Configuration
# =====================================================

@dataclass
class DictInfo:
    """Metadata container for a registered dictionary backend.
 
    Stores the class object (not an instance), display name, description,
    and a mutable results dict that accumulates
    :class:`~speller.speller.SpellerResult` objects across benchmark
    runs within a single program execution.
 
    Not frozen because ``results`` is intentionally mutable — updated
    in-place during each ``run_speller()`` call in the ``main()`` loop.
 
    Parameters
    ----------
    dict_class : type[DictionaryProtocol]
        The class itself, not an instance.  Callers instantiate it via
        ``data.dict_class()`` in the composition root.
        ``type[X]`` means "the class object for X" — pyright knows
        ``data.dict_class()`` produces a ``DictionaryProtocol`` instance.
    name : str
        Display name derived from ``dict_class.__name__``
        (e.g. ``"HashTableDictionary"``).  Distinct from the registry
        key (e.g. ``"hash"``): the key is for CLI lookup; the name is
        for human-readable output and benchmark reports.
    description : str
        One-line description used in CLI help text and benchmark reports.
        Falls back to ``dict_class.__doc__`` if not supplied explicitly.
    results : dict of {str : SpellerResult}, optional
        Accumulated results keyed by label (e.g. ``"speller_result"``).
        Empty by default; populated during ``main()`` execution.
 
    Examples
    --------
    >>> info = dicts["hash"]
    >>> instance = info.dict_class()      # HashTableDictionary()
    >>> info.name
    \'HashTableDictionary\'
    """
    
    # Required fields (no default) must come first
    _: KW_ONLY  # Everything after this is keyword-only
    dict_class: type[DictionaryProtocol]
    name: str
    description: str
    # Optional fields with defaults afterwards
    results: dict[str, SpellerResult] = field(default_factory=dict)

# Tells pyright this is an INSTANCE
#   dict_class: DictionaryProtocol          # an object with .load(), .check()

# Tells pyright this is a CLASS
#   dict_class: type[DictionaryProtocol]    # a class you can call with ()

# type[X] means "the class itself, not an instance of it." Pyright knows
# dict_class() is valid because you're calling a class constructor, which
# returns an instance of DictionaryProtocol.


# =====================================================
# Constants
# =====================================================

dicts: dict[str, DictInfo] = {}  # now DictInfo is defined above


# =============================================================================
# DICTIONARY REGISTRY
# =============================================================================

# A decorator factory is just a function that takes custom parameters 
# and generates a decorator.
def register_class(name: str, description: str = "") -> RegDecorator:
    """Decorator factory that registers a dictionary class in :data:`dicts`.
 
    Returns a decorator that inserts the decorated class into :data:`dicts`
    under ``name``, then returns the class **unchanged**.  Because the
    class is returned as-is, ``@functools.wraps`` is unnecessary —
    there is no wrapper function whose metadata needs copying.
 
    Parameters
    ----------
    name : str
        Registry key for CLI lookup (e.g. ``"hash"``, ``"sorted"``).
        Must be unique across all registered backends.
    description : str, optional
        One-line description for CLI help and benchmark output.
        Falls back to ``dict_class.__doc__`` if empty.
 
    Returns
    -------
    RegDecorator
        A callable that accepts a ``type[DictionaryProtocol]`` and
        returns it unchanged after registering it.
 
    Examples
    --------
    ::
 
        @register_class("hash", "O(1) average lookup via Python set.")
        class HashTableDictionary(_BaseDictionary[set[str]]):
            ...
 
        dicts["hash"].dict_class()   # → HashTableDictionary()
 
    Notes
    -----
    Adding a new backend requires exactly three things:
 
    1. Create a class satisfying
       :class:`~speller.protocols.DictionaryProtocol`.
    2. Decorate it with ``@register_class("key", "description")``.
    3. Ensure its module is imported before :data:`dicts` is read —
       handled automatically by the ``__init__.py`` side-effect import.
    """
    def decorator(dict_class: type[DictionaryProtocol]) -> type[DictionaryProtocol]:
        dicts[name] = DictInfo(
            dict_class=dict_class,
            name=dict_class.__name__,
            description=description or dict_class.__doc__ or "",
        )
        return dict_class  # Return unchanged class
        # class goes in, class comes out. The class' __name__, __doc__, __qualname__
        # are all intact because you never created a replacement. Nothing to fix,
        # so @wraps would do nothing useful.
    return decorator

# Instantiate by key - calling a class creates an instance
# dictionary = dicts["hash"].dict_class() -> HashTableDictionary()