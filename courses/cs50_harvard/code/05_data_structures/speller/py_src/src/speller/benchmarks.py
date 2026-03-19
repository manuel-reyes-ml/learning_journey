"""
"""

# =============================================================================
# IMPORTS
# =============================================================================

from __future__ import annotations

from dataclasses import dataclass, field, KW_ONLY
from typing import Any, Generator, Callable
from contextlib import contextmanager
from functools import wraps
import logging
import time


# =============================================================================
# LOGGER SETUP
# =============================================================================

# '__name__' will automatically be name 'speller.benchmarks'
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
# Type Aliases
# =====================================================

# Define types locally if only used in the module

# Syntax: Callable[[INPUT_TYPES], RETURN_TYPE]
#   - Input parameters in a list
type Wrapped = Callable[[Any], Any]
type Decorator = Callable[[Callable], Wrapped]
type DictMetaData = dict[str, BenchmarkResult]


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
    """
    """
    _: KW_ONLY        # Everything after is keyword-only
    operation: str          
    elapsed_seconds: float  
    metadata: DictMetaData = field(default_factory=dict)
    
    # __str__ is called by output func (logging, print)
    def __str__(self) -> str:
        """
        """
        return f"{self.operation}: {self.elapsed_seconds:2f}s"


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
def timer(operation_name: str) -> Generator[DictMetaData, None, None]:
    """
    """
    # Mutable container - we yield this before timing is done, then we
    # fill it in AFTER the block completes.
    # The caller holds a reference to this same dict object
    container: DictMetaData = {}
    
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
    )
    
    logger.debug(
        "Timer '%s' completed: %.6fs",
        operation_name,
        elapsed,
    )
    

def timed(operation_name: str) -> Decorator:
    """
    """
    # LAYER 1: receives the parameter (operation_name)
    # Returns the actual decorator function
    def decorator(func: Callable) -> Wrapped:
        # LAYER 2: receives the function being decorated
        # Returns the wrapper that replaces the original function
        
        @wraps(func)  # Preserve func.__name__, .__doc__, etc.
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            # LAYER 3: receives the arguments when the function is called
            # This is what actually runs when you call load_dictionary(path)
            
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