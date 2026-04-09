"""Timing utilities for spell-checker operations.
 
Provides two complementary timing interfaces:
 
``timer()``
    A ``@contextmanager`` that wraps any code block and writes a
    :class:`BenchmarkResult` into a mutable dict container after the
    block completes.  Used in ``speller.py`` for cumulative loop
    timing — e.g. the per-word ``check()`` loop — where a decorator
    cannot be applied.
 
``timed()``
    A decorator factory that wraps a single function call and attaches
    the :class:`BenchmarkResult` to ``func.benchmark``.  Best for
    one-shot operations such as ``load()`` and ``size()``.
 
Both interfaces produce :class:`BenchmarkResult` instances (frozen
dataclasses) so callers always receive the same structured data
regardless of which interface was used.
 
Design notes
------------
``timer()`` yields a *mutable* ``dict`` before timing is complete.
The caller receives a reference to that dict; after the ``with`` block
ends the result is written back into it.  This is the canonical
pattern used by pytest fixtures, FastAPI dependencies, and SQLAlchemy
session managers — yield setup data, populate results post-yield.
 
``timed()`` preserves the decorated function\'s full type signature via
``ParamSpec`` and ``TypeVar``, so pyright sees the real parameter and
return types rather than ``Any``.
 
Roadmap relevance
-----------------
The ``timer`` / ``BenchmarkResult`` pair reappears in every Stage 1+
project:
 
- DataVault:    LLM API call latency.
- PolicyPulse:  retrieval latency per RAG chunk batch.
- AFC:          per-bar execution time in the backtesting loop.
 
References
----------
.. [1] PEP 343 — The "with" Statement
   https://peps.python.org/pep-0343/
.. [2] PEP 612 — Parameter Specification Variables (ParamSpec)
   https://peps.python.org/pep-0612/
.. [3] contextlib — Utilities for with-statement contexts
   https://docs.python.org/3/library/contextlib.html
"""

# =============================================================================
# IMPORTS
# =============================================================================

from __future__ import annotations

from dataclasses import dataclass, field, KW_ONLY

# Runtime collection types → collections.abc
from collections.abc import Generator, Callable
from collections import namedtuple

# Type system concepts → typing
from typing import Any, ParamSpec, TypeVar

from contextlib import contextmanager
from pathlib import Path
from functools import wraps
import logging
import time

## Simple Decision Rule
# "Is it a CONTAINER or CALLABLE type?"
#     YES → from collections.abc  (Generator, Iterator, Callable, Sequence, Mapping)

# "Is it a TYPE SYSTEM concept?"
#     YES → from typing  (Protocol, TypeVar, ParamSpec, Any, Final, TypedDict)


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
    "BenchmarkResult",
    "timer",
    "timed",
]


# =============================================================================
# MODULE CONFIGURATION
# =============================================================================
# =====================================================
# Constants
# =====================================================

FDATA = namedtuple("FDATA", ["fname", "fpath"])


# =====================================================
# Type Variables % Aliases
# =====================================================

# Define types locally if only used in the module

# Type variables for preserving decorated function signatures
# P captures the function's parameter types as a group
# T captures the function's return type
# Together they ensure the decorator doesn't erase type info
P = ParamSpec("P")
T = TypeVar("T")

# Container type for the timer context manager
type TimerContainer = dict[str, Any]

# 'Any' since the container is empty during the
# 'with' block and only has data after.


# =====================================================
# Dataclass Frozen Constants
# ===================================================== 

# Use @dataclass for internal logic, Pydantic BaseModel
# at services boundaries (API, user validation).

# frozen=True makes instances immutable.
# slots=True prevents dynamic attribute creation and
# reduces memory fooprint.
# Together they create a truly locked-down data container.
@dataclass(frozen=True, slots=True)
class BenchmarkResult:
    """Immutable container for a single timed operation.
 
    Produced by :func:`timer` (accessed as ``t["result"]``) and stored
    on a decorated function as ``func.benchmark`` after :func:`timed`
    completes.  ``frozen=True`` and ``slots=True`` make this the same
    locked-down pattern used by :class:`~speller.speller.SpellerResult`.
 
    Parameters
    ----------
    operation : str
        Human-readable label for the timed operation
        (e.g. ``"load"``, ``"check"``, ``"size"``).
    elapsed_seconds : float
        Wall-clock duration measured with :func:`time.perf_counter`.
        Always monotonic — never jumps backward during NTP sync.
    metadata : dict of {str : Any}, optional
        Arbitrary key/value context attached at call time.
        :func:`timer` stores ``{"input_file": FDATA(name, path)}``
        when ``input_file`` is provided.
 
    Examples
    --------
    >>> with timer("load") as t:
    ...     pass
    >>> result = t["result"]
    >>> print(result)
    load: 0.00s
    >>> isinstance(result.elapsed_seconds, float)
    True
    """
    
    _: KW_ONLY        # Everything after is keyword-only
    operation: str          
    elapsed_seconds: float  
    metadata: dict[str, Any] = field(default_factory=dict)
    
    # __str__ is called by output func (logging, print)
    def __str__(self) -> str:
        """Return a concise human-readable summary.
 
        Called automatically by ``print()``, ``str()``, and logging
        formatters.  Matches the style used in CS50\'s speller.c report
        (``"load: 0.14s"``).
 
        Returns
        -------
        str
            ``"<operation>: <elapsed>s"`` rounded to two decimal places.
 
        Examples
        --------
        >>> result = BenchmarkResult(operation="load", elapsed_seconds=0.1423)
        >>> str(result)
        \'load: 0.14s\'
        """
        return f"{self.operation}: {self.elapsed_seconds:.2f}s"


# =====================================================
# Decorators
# ===================================================== 

# Generator[dict[str, Any], None, None]
#          ↑               ↑     ↑
#          what yield      what   what
#          sends OUT       you    return
#                          send() gives back
#                          IN
# SendType = The caller can send() a value into the generator, and
#       it arrives as the return value of the yield expression.
# ReturnType = When the generator finishes (hits return), the value
#       gets stuffed inside StopIteration exception. 
# The caller can catch it:
# try:
#     next(gen)       # generator is exhausted
# except StopIteration as e:
#     print(e.value)  # ← the return value lives here

# Iterator is the simpler type — it only specifies what comes out

# A context manager is any object that implements two methods:
#   __enter__()  — runs when the `with` block STARTS
#   __exit__()   — runs when the `with` block ENDS (even if an error occurs)
#
# The `with` statement guarantees __exit__ is called, which makes it
# perfect for resource cleanup: files, connections, locks, timers.
@contextmanager
def timer(
    operation_name: str,
    *,
    input_file: str | Path | None = None,
) -> Generator[TimerContainer, None, None]:
    """Context manager that times the enclosed code block.
 
    Yields an empty ``dict`` container before the block runs.  After
    the ``with`` block exits, writes a :class:`BenchmarkResult` into
    ``container["result"]``.  The caller holds a reference to the same
    dict throughout, so the result is accessible after the block even
    though it did not exist at yield time.
 
    Parameters
    ----------
    operation_name : str
        Label for this timing event (e.g. ``"load"``, ``"check"``).
    input_file : str or Path or None, optional
        When provided, stored in ``result.metadata["input_file"]`` as
        ``FDATA(fname, fpath)`` for report generation.
 
    Yields
    ------
    TimerContainer
        Empty ``dict`` at yield time.  After the block ends it
        contains ``{"result": BenchmarkResult}``.
 
    Examples
    --------
    Basic timing::
 
        with timer("load") as t:
            dictionary.load(path)
        print(t["result"])           # load: 0.08s
 
    With file metadata::
 
        with timer("check", input_file=text_path) as t:
            for word in extract_words(text_path):
                dictionary.check(word)
        meta = t["result"].metadata["input_file"]
        print(meta.fname)            # "austen.txt"
 
    Notes
    -----
    Why ``time.perf_counter()`` instead of ``time.time()``?
        ``perf_counter`` is monotonic — it never decreases during NTP
        clock adjustments.  ``time.time()`` can jump backward, making
        benchmark results unreliable in long-running processes.
 
    Why yield a mutable ``dict`` instead of a frozen dataclass?
        The ``yield`` happens *before* the timed block runs; the result
        only exists *after* it ends.  A frozen dataclass cannot be
        mutated post-yield.  Yielding a plain ``dict`` and writing into
        it after the block is the minimal pattern that works — the same
        approach used by pytest fixtures and SQLAlchemy session managers.
    """
    path = Path(input_file) if isinstance(input_file, str) else input_file
    
    # Mutable container - we yield this before timing is done, then we
    # fill it in AFTER the block completes.
    # The caller holds a reference to this same dict object
    container: TimerContainer = {}
    
    # ===__enter__ phase ===
    # perf_counter() is monotonic (never goes backward) and high-resolution.
    # time.time() can jump backward during NTP sync - neer use it for benchmarks.
    start = time.perf_counter()
    
    logger.debug("Starting timer for '%s'", operation_name)
    
    # === yield phase ===
    # Control passes to the caller's 'with' block.
    # Everything between 'yield' and the next line runs the caller's code.
    yield container
    
    # === __exit__ phase ===
    # The caller's 'with' block has finished. Calculate elapsed time.
    elapsed = time.perf_counter() - start
    
    # Store the result in the mutable container.
    # The caller can access it because they hold a reference to the same dict
    container["result"] = BenchmarkResult(
        operation=operation_name,
        elapsed_seconds=elapsed,
        metadata={
            "input_file": FDATA(path.name, path)
        } if path else {},
    )
    
    logger.debug(
        "Timer '%s' completed: %.6fs",
        operation_name,
        elapsed,
    )
    
    
# Syntax: Callable[[INPUT_TYPES], RETURN_TYPE]
#   - Input parameters in a list
def timed(operation_name: str) -> Callable[[Callable[P, T]], Callable[P, T]]:
    """Decorator factory that times a single function call.
 
    Wraps the decorated function in a :func:`timer` context manager.
    After each call, attaches the :class:`BenchmarkResult` to the
    wrapper as ``func.benchmark``.  Uses ``ParamSpec`` and ``TypeVar``
    to preserve the original function\'s complete type signature —
    pyright sees the real parameter and return types, not ``Any``.
 
    Parameters
    ----------
    operation_name : str
        Label passed to :func:`timer` (e.g. ``"load"``).
 
    Returns
    -------
    Callable[[Callable[P, T]], Callable[P, T]]
        A decorator that accepts a function and returns a
        type-preserving wrapper with an additional ``.benchmark``
        attribute initialised to ``None`` before the first call.
 
    Examples
    --------
    ::
 
        @timed("load")
        def load_dictionary(path: str) -> bool:
            ...
 
        result = load_dictionary("dictionaries/large")  # bool preserved
        print(load_dictionary.benchmark)  # BenchmarkResult(operation="load", ...)
 
    Notes
    -----
    Why not use ``@timed`` for ``check()`` in ``speller.py``?
        ``check()`` runs once per word — potentially hundreds of
        thousands of times per text file.  Per-call decorator overhead
        would dominate the measurement.  Use :func:`timer` to wrap the
        *entire loop* for cumulative time instead.
 
    Why three nested functions?
        A parameterised decorator requires two evaluation steps:
 
        1. ``timed("load")``         → returns ``decorator``
        2. ``decorator(func)``       → returns ``wrapper``
        3. ``wrapper(*args, ...)``   → runs func and stores timing
 
        A decorator without parameters only needs two layers.
    """
#                                  ↑        ↑               ↑
#                                  |        |               |
#                                  |        input func      output func
#                                  |        (same types)    (same types)
#                                  |
#                                  returns a decorator
#
# In English: "timed() returns a function that takes a
#              Callable[P, T] and returns a Callable[P, T]"
#
# Which means: "whatever goes in comes out with the same types"

    # LAYER 1: receives the parameter (operation_name)
    # Returns the actual decorator function
    
    def decorator(func: Callable[P, T]) -> Callable[P, T]:
        """Wrap ``func`` with timing logic and return the wrapper.

        Parameters
        ----------
        func : Callable[P, T]
            The function to wrap.  Its full type signature is captured
            via ``ParamSpec`` ``P`` and ``TypeVar`` ``T``.

        Returns
        -------
        Callable[P, T]
            A wrapper with the same signature as ``func`` plus a
            ``.benchmark`` attribute initialised to ``None``.
        """
        # LAYER 2: receives the function being decorated
        # Returns the wrapper that replaces the original function
        
        @wraps(func)  # Preserve func.__name__, .__doc__, etc.
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
            """Execute ``func`` inside a :func:`timer` block.

            Returns
            -------
            T
                The original return value of ``func``, unchanged.

            Notes
            -----
            After each call, ``wrapper.benchmark`` is updated to the
            :class:`BenchmarkResult` for that invocation.
            """
            # LAYER 3: receives the arguments when the function is called
            # This is what actually runs when you call load_dictionary(path)
        #                   ↑                 ↑
        #                   positional args   keyword args
        #                   from P            from P
        # If the original function is:
        #   def load_dictionary(path: str, verbose: bool = False) -> bool

        # Then P.args captures: (str,)
        # And P.kwargs captures: {verbose: bool}
        # And T captures: bool    
            
            # Reuse the timer() context manager - DRY principle
            # The timing logic exists in one place (timer), not duplicated here
            with timer(operation_name) as t:
                result = func(*args, **kwargs)  # Call the original function
            
            # Store the BenchmarkResult on the wrapper function object
            # Functions are objects in Python - you can set attributes on them.
            # This is how the caller accesses the timing data after the call.
            wrapper.benchmark = t["result"]  # type: ignore[attr-defined]
            
            # Return the original function's return value unchanged.
            # The caller doesn't know or care that timing happened.
            return result
        
        # Initialize .benchmark to None before any call is made
        wrapper.benchmark = None  # type: ignore[attr-defined]
        
        return wrapper
    return decorator


# =========================================================================
# SECTION 2: timer() — Context Manager (THE FOUNDATION)
# =========================================================================
#
# HOW @contextmanager WORKS
# =========================
#
# Normally, to create a context manager you write a class with
# __enter__ and __exit__ methods:
#
#   class Timer:
#       def __enter__(self):
#           self.start = time.perf_counter()
#           return self
#       def __exit__(self, *exc):
#           self.elapsed = time.perf_counter() - self.start
#           return False
#
# That's 8+ lines of boilerplate. @contextmanager lets you write
# the SAME thing as a generator function with a single `yield`:
#
#   @contextmanager
#   def timer(name):
#       start = time.perf_counter()     ← __enter__ (before yield)
#       yield container                  ← the value `with ... as X` receives
#       elapsed = time.perf_counter()    ← __exit__ (after yield)
#
# The @contextmanager decorator converts your generator into a proper
# context manager. It:
#   1. Calls your function up to `yield`     → this is __enter__
#   2. Sends the yielded value to `as X`     → this is the return value
#   3. Resumes after `yield` when the block ends → this is __exit__
#
# EXECUTION FLOW (step by step)
# ==============================
#
#   with timer("load") as t:       # 1. Python calls timer("load")
#                                   # 2. Function runs until yield
#                                   # 3. t = the yielded dict {}
#       dictionary.load(path)       # 4. YOUR CODE runs here
#                                   # 5. Block ends → function resumes after yield
#                                   # 6. elapsed is calculated
#                                   # 7. BenchmarkResult stored in t["result"]
#   print(t["result"])              # 8. You access the result
#
# WHY yield a DICT (mutable container)?
# ======================================
#
# Problem: yield happens BEFORE the timed block runs, but we need
# to store the result AFTER it completes. We can't yield a frozen
# dataclass because we can't mutate it after yielding.
#
# Solution: yield a mutable dict. We fill it in AFTER the block:
#
#   yield container        ← empty dict goes to caller
#   ...timing happens...
#   container["result"] =  ← we can still write to it because
#                             the caller has a REFERENCE to the
#                             same dict object (Python passes by
#                             reference for mutable objects)
#
# This is the same pattern used in pytest fixtures, FastAPI
# dependencies, and SQLAlchemy session managers.
# =========================================================================

# =========================================================================
# SECTION 3: timed() — Decorator (WRAPS the Context Manager)
# =========================================================================
#
# HOW THE THREE-LAYER DECORATOR WORKS
# =====================================
#
# A decorator with parameters needs THREE nested functions:
#
#   timed("load")                → returns `decorator`   (layer 1: receives NAME)
#   decorator(load_dictionary)   → returns `wrapper`     (layer 2: receives FUNCTION)
#   wrapper(*args, **kwargs)     → calls func + times it (layer 3: receives ARGUMENTS)
#
# Why three layers? Because Python evaluates decorators in two steps:
#
#   @timed("load")           # Step 1: Python calls timed("load") → gets `decorator`
#   def load_dict(path):     # Step 2: Python calls decorator(load_dict) → gets `wrapper`
#       ...
#
# After decoration, `load_dict` IS `wrapper`. When you call `load_dict(path)`,
# you're actually calling `wrapper(path)`, which:
#   1. Opens the timer context manager
#   2. Calls the original load_dict inside the timed block
#   3. Stores the BenchmarkResult on wrapper.benchmark
#   4. Returns the original function's return value unchanged
#
# VISUAL FLOW
# ============
#
#   @timed("load")
#   def load_dict(path):
#       return True
#
#   # What Python actually does:
#   #   temp = timed("load")          → temp is `decorator`
#   #   load_dict = temp(load_dict)   → load_dict is now `wrapper`
#
#   result = load_dict("large")
#   #   → wrapper("large") is called
#   #   → wrapper opens: with timer("load") as t:
#   #   → wrapper calls: original_load_dict("large")
#   #   → wrapper stores: wrapper.benchmark = t["result"]
#   #   → wrapper returns: True (the original return value)
#
#   print(result)                    # True (unchanged)
#   print(load_dict.benchmark)       # BenchmarkResult(operation="load", ...)
#
# WHY @wraps(func)?
# ==================
#
# Without @wraps, the wrapper replaces the original function's metadata:
#   load_dict.__name__  → "wrapper"  (WRONG — confuses debuggers and loggers)
#   load_dict.__doc__   → wrapper's docstring (WRONG — hides original docs)
#
# With @wraps(func), the wrapper COPIES the original's metadata:
#   load_dict.__name__  → "load_dict"  (CORRECT)
#   load_dict.__doc__   → original docstring (CORRECT)
#
# @wraps also preserves __module__, __qualname__, __annotations__,
# and __dict__, which matters for mypy, pytest, and Sphinx docs.
# =========================================================================


# @timed("load")
#def load_dictionary(path: str) -> bool:
#    return True

# Your code expects bool, but mypy can't verify because
# the decorator's return type is Any
# result: str = load_dictionary("large")  # ← mypy says "fine!" (it's not)

# The decorator erased the original function's type information. After decoration, `mypy` thinks `load_dictionary` returns `Any` instead of `bool`.

## What `TypeVar` and `ParamSpec` Solve

# They let the decorator **preserve** the original function's exact types — parameters AND return type flow through unchanged:

# BEFORE (Any):
#   load_dictionary: (*Any) -> Any          ← type info lost

# AFTER (ParamSpec + TypeVar):
#   load_dictionary: (path: str) -> bool    ← type info preserved

## How They Work
#┌─────────────────────────────────────────────────────────────────┐
#│              TypeVar and ParamSpec                               │
#│─────────────────────────────────────────────────────────────────│
#│                                                                  │
#│  TypeVar("T")  — captures ONE type and reuses it                 │
#│                                                                  │
#│    T = TypeVar("T")                                              │
#│    def identity(x: T) -> T: ...                                  │
#│                                                                  │
#│    identity(42)     → mypy knows return is int                   │
#│    identity("hi")   → mypy knows return is str                   │
#│    T "binds" to whatever type flows in, then flows out           │
#│                                                                  │
#│  ParamSpec("P")  — captures ALL parameters as a group            │
#│                                                                  │
#│    P = ParamSpec("P")                                            │
#│    def wrapper(*args: P.args, **kwargs: P.kwargs): ...           │
#│                                                                  │
#│    If original func is (path: str, verbose: bool) -> bool        │
#│    Then P captures (path: str, verbose: bool) as a unit          │
#│    P.args = the positional args                                  │
#│    P.kwargs = the keyword args                                   │
#│                                                                  │
#│  Together they let decorators say:                               │
#│    "I take a function with parameters P returning T,             │
#│     and I return a function with the SAME parameters P           │
#│     returning the SAME type T"                                   │
#└─────────────────────────────────────────────────────────────────┘