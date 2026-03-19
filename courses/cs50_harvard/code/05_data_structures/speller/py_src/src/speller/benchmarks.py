"""
"""

# =============================================================================
# IMPORTS
# =============================================================================

from __future__ import annotations
from dataclasses import dataclass, field, KW_ONLY
from contextlib import contextmanager
from typing import Any, Generator
from functools import wraps
import logging
import time


# =============================================================================
# LOGGER SETUP
# =============================================================================

logger = logging.getLogger(__name__)


# =============================================================================
# EXPORTS
# =============================================================================

__all__ = []


# =============================================================================
# MODULE CONFIGURATION
# =============================================================================
# =====================================================
# Dataclass Frozen Constants
# ===================================================== 

# Use @dataclass for internal logic, Pydantic BaseModel
# at services boundaries (API, user validation).
@dataclass(frozen=True, slots=True)
class BenchmarkResult:
    """
    """
    _: KW_ONLY              # Everything after is keyword-only
    operation: str          
    elapsed_seconds: float  
    metadata: dict[str, Any] = field(default_factory=dict)
    
    # __str__ is called by output func (logging, print)
    def __str__(self) -> str:
        """
        """
        return f"{self.operation}: {self.elapsed_seconds:2f}s"


# =====================================================
# Decorators
# ===================================================== 

@contextmanager
def timer(operation_name: str) -> Generator[dict[str, Any], None, None]:
    """
    """
    # Mutable container - we yield this before timing is done, then we
    # fill it in AFTER the block completes.
    # The caller holds a reference to this same dict object
    container: dict[str, Any] = {}
    
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
    

def timed(operation_name: str):
    """
    """
    # LAYER 1: receives the parameter (operation_name)
    # Returns the actual decorator function
    def decorator(func):
        # LAYER 2: receives the function being decorated
        # Returns the wrapper that replaces the original function
        
        @wraps(func)  # Preserve func.__name__, __.doc__, etc.
        def wrapper(*args: Any, **kwargs: Any):
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
