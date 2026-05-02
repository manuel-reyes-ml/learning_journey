"""
contextmanager_decorators_reference.py
=======================================

Personal reference: Python's ``@contextmanager`` decorator and
how decorators compose with context managers to build reusable tools.

Topics covered
--------------
1. Context managers — what they are, ``__enter__``/``__exit__`` protocol
2. ``@contextmanager`` — generator shortcut for context managers
3. Execution flow — step-by-step what happens at each line
4. Why yield a mutable container — the reference pattern
5. Decorators recap — two-layer vs three-layer
6. Wrapping a context manager inside a decorator
7. Common patterns and real-world usage
8. Gotchas and pitfalls

Why this matters for your roadmap (v8.1 GenAI-First)
-----------------------------------------------------
- Stage 1: Speller benchmarks (this project), file I/O safety,
  DataVault LLM client connections, PolicyPulse ChromaDB sessions
- Stage 2: Database connections (``with psycopg2.connect() as conn``),
  AWS sessions (``with boto3.resource('s3') as s3``),
  Airflow task context managers
- Stage 3: MLflow experiment tracking (``with mlflow.start_run()``),
  PyTorch device context (``with torch.no_grad()``),
  training loop timing
- Stage 4: LangChain callback managers, LangGraph state managers,
  LLM streaming contexts, agent execution spans
- Stage 5: Production LLMOps — distributed tracing, span management,
  resource cleanup in multi-agent systems

How to use this file
---------------------
Run it directly to see all demonstrations::

    $ python contextmanager_decorators_reference.py

Or import specific sections::

    >>> from contextmanager_decorators_reference import section_3_execution_flow

Author: Manuel Reyes — CS50 / Stage 1 Learning Reference
Version: 1.0.0 — March 2026

References
----------
.. [1] Python Docs — contextlib.contextmanager
   https://docs.python.org/3/library/contextlib.html#contextlib.contextmanager
.. [2] Python Docs — With Statement Context Managers
   https://docs.python.org/3/reference/datamodel.html#context-managers
.. [3] PEP 343 — The "with" Statement
   https://peps.python.org/pep-0343/
.. [4] Real Python — Context Managers and the "with" Statement
   https://realpython.com/python-with-statement/
"""
from __future__ import annotations

import logging
import time
from contextlib import contextmanager
from dataclasses import dataclass
from functools import wraps
from typing import Any, Callable, Generator


# =========================================================================
# SECTION 1: WHAT IS A CONTEXT MANAGER?
# =========================================================================
# A context manager is any object that implements two methods:
#   __enter__()  — runs when the `with` block STARTS
#   __exit__()   — runs when the `with` block ENDS (even if an error occurs)
#
# The `with` statement guarantees __exit__ is called, which makes it
# perfect for resource cleanup: files, connections, locks, timers.
#
# MENTAL MODEL — The Bouncer Pattern:
# ====================================
#
#   with open("file.txt") as f:       # Bouncer opens the door (__enter__)
#       data = f.read()               # You're inside the club (your code)
#                                     # Bouncer closes the door (__exit__)
#                                     # Door closes EVEN IF you cause trouble
#                                     # (even if an exception is raised)
#
# WHY THIS MATTERS:
# Without `with`, you must manually close resources:
#
#   f = open("file.txt")     # ← what if .read() crashes?
#   data = f.read()          # ← exception here means f.close() never runs
#   f.close()                # ← resource leak!
#
# With `with`, cleanup is GUARANTEED:
#
#   with open("file.txt") as f:
#       data = f.read()      # ← even if this crashes, __exit__ still runs
#                             # ← file is always properly closed
# =========================================================================

def section_1_context_manager_basics() -> None:
    """Demonstrate the context manager protocol with a class-based example.

    A context manager is a class with ``__enter__`` and ``__exit__`` methods.
    The ``with`` statement calls them automatically.
    """
    print("\n" + "=" * 60)
    print("SECTION 1: Context Manager Basics (Class-Based)")
    print("=" * 60)

    # --- Example 1: Class-based context manager (the verbose way) ---
    class ManualTimer:
        """Times a code block using the class-based protocol.

        This is the MANUAL way to write a context manager.
        Section 2 shows the shortcut with @contextmanager.
        """

        def __init__(self, label: str) -> None:
            self.label = label
            self.elapsed: float = 0.0

        def __enter__(self):
            """Called when `with` block starts.

            Returns
            -------
            self
                The value assigned to `as X` in `with ... as X`.
            """
            self.start = time.perf_counter()
            print(f"  __enter__: Timer '{self.label}' started")
            return self  # ← this becomes the `as t` variable

        def __exit__(self, exc_type, exc_val, exc_tb):
            """Called when `with` block ends (even on exceptions).

            Parameters
            ----------
            exc_type : type or None
                Exception class if an error occurred, else None.
            exc_val : BaseException or None
                Exception instance if an error occurred, else None.
            exc_tb : TracebackType or None
                Traceback if an error occurred, else None.

            Returns
            -------
            bool
                False = let exceptions propagate (almost always correct).
                True  = swallow the exception (DANGEROUS — hides bugs).
            """
            self.elapsed = time.perf_counter() - self.start
            print(f"  __exit__:  Timer '{self.label}' stopped: {self.elapsed:.6f}s")
            return False  # ← don't swallow exceptions

    # Usage
    print("\nUsing class-based ManualTimer:")
    with ManualTimer("demo") as t:
        # Simulate some work
        total = sum(range(100_000))
    print(f"  Result: {t.elapsed:.6f}s elapsed, sum = {total}")

    # --- The execution order ---
    print("\nExecution order:")
    print("  1. ManualTimer('demo') → __init__() creates the object")
    print("  2. `with` calls __enter__() → returns self → assigned to `t`")
    print("  3. Your code runs (sum calculation)")
    print("  4. Block ends → __exit__() called → elapsed calculated")
    print("  5. `t.elapsed` is now available")


# =========================================================================
# SECTION 2: @contextmanager — THE SHORTCUT
# =========================================================================
# Writing __enter__ and __exit__ is verbose. Python's contextlib module
# provides @contextmanager, which converts a GENERATOR FUNCTION into a
# context manager using a single `yield`.
#
# MENTAL MODEL — Before/Yield/After:
# ====================================
#
#   @contextmanager
#   def my_context():
#       # BEFORE yield  → this is __enter__
#       setup_stuff()
#
#       yield value     → this is what `as X` receives
#
#       # AFTER yield   → this is __exit__
#       cleanup_stuff()
#
# HOW IT WORKS UNDER THE HOOD:
# ==============================
# @contextmanager wraps your generator in a class that:
#   1. Calls next() on your generator → runs to `yield` → acts as __enter__
#   2. Sends the yielded value to `as X`
#   3. Calls next() again when block ends → resumes after yield → acts as __exit__
#   4. Handles exceptions by throwing them into the generator
#
# COMPARISON:
#
#   Class-based:                    @contextmanager:
#   ─────────────────────          ─────────────────────
#   class Timer:                    @contextmanager
#       def __init__(self):         def timer(label):
#           self.label = ...            start = perf_counter()
#       def __enter__(self):            yield {}
#           self.start = ...            elapsed = perf_counter() - start
#           return self
#       def __exit__(self, ...):
#           self.elapsed = ...
#
#   8+ lines                        4 lines (same behavior!)
# =========================================================================

def section_2_contextmanager_decorator() -> None:
    """Demonstrate @contextmanager as a shortcut for context managers.

    Converts a generator function with a single ``yield`` into a
    full context manager — no class needed.
    """
    print("\n" + "=" * 60)
    print("SECTION 2: @contextmanager — The Generator Shortcut")
    print("=" * 60)

    # --- Example 1: Simple timer with @contextmanager ---
    @contextmanager
    def simple_timer(label: str) -> Generator[dict[str, Any], None, None]:
        """Time a block of code.

        Yields
        ------
        dict[str, Any]
            Mutable container — access ``result["elapsed"]`` after block.
        """
        container: dict[str, Any] = {}

        # === BEFORE yield === (__enter__ equivalent)
        start = time.perf_counter()
        print(f"  [before yield] Timer '{label}' started")

        # === yield === (control passes to the `with` block)
        yield container  # ← this dict becomes the `as t` variable

        # === AFTER yield === (__exit__ equivalent)
        elapsed = time.perf_counter() - start
        container["elapsed"] = elapsed
        print(f"  [after yield]  Timer '{label}' stopped: {elapsed:.6f}s")

    # Usage
    print("\nUsing @contextmanager-based simple_timer:")
    with simple_timer("sum_demo") as t:
        print("  [inside with]  Running sum calculation...")
        total = sum(range(100_000))

    print(f"  [after with]   Elapsed: {t['elapsed']:.6f}s, sum = {total}")

    # --- Execution order visualization ---
    print("\n  Step-by-step execution:")
    print("  ┌─ simple_timer('sum_demo') called")
    print("  │  ├─ container = {} created")
    print("  │  ├─ start = perf_counter()")
    print("  │  └─ yield container → PAUSES here, sends {} to `as t`")
    print("  │")
    print("  │  ┌─ YOUR CODE runs inside `with` block")
    print("  │  │  total = sum(range(100_000))")
    print("  │  └─ block ends")
    print("  │")
    print("  │  ├─ Generator RESUMES after yield")
    print("  │  ├─ elapsed = perf_counter() - start")
    print("  │  └─ container['elapsed'] = elapsed")
    print("  └─ done — t['elapsed'] is now accessible")


# =========================================================================
# SECTION 3: EXECUTION FLOW — DETAILED STEP-BY-STEP
# =========================================================================
# This section traces EVERY step of what Python does when you use
# @contextmanager + `with`. Understanding this flow is critical
# for debugging and for composing context managers with decorators.
#
# KEY INSIGHT: yield is a PAUSE BUTTON
# =====================================
#
# A normal function runs start-to-finish. A generator function
# PAUSES at each `yield` and RESUMES when next() is called.
#
# @contextmanager exploits this:
#   next() call #1 → runs to yield    → __enter__
#   next() call #2 → resumes to end   → __exit__
#
# The `with` statement orchestrates these two next() calls.
#
# ASCII EXECUTION TIMELINE:
# ==========================
#
#   Time →
#   │
#   ├── with timer("load") as t:     Python calls timer("load")
#   │   │                             ↓
#   │   │                             generator starts running
#   │   │                             ↓
#   │   │                             start = perf_counter()
#   │   │                             ↓
#   │   │                             yield container ──→ PAUSE
#   │   │                                    │
#   │   │                                    ↓
#   │   │                             t = container (the `as` target)
#   │   │
#   │   ├── dictionary.load(path)     YOUR CODE runs
#   │   │
#   │   └── (block ends)              Python calls next() on generator
#   │                                 ↓
#   │                                 generator RESUMES after yield
#   │                                 ↓
#   │                                 elapsed = perf_counter() - start
#   │                                 ↓
#   │                                 container["result"] = BenchmarkResult(...)
#   │                                 ↓
#   │                                 generator ends → __exit__ complete
#   │
#   ├── print(t["result"])            You access the stored result
# =========================================================================

def section_3_execution_flow() -> None:
    """Trace every step of @contextmanager execution with print statements."""
    print("\n" + "=" * 60)
    print("SECTION 3: Execution Flow — Watching Every Step")
    print("=" * 60)

    @contextmanager
    def traced_timer(label: str) -> Generator[dict[str, Any], None, None]:
        """A timer that prints at every execution phase."""
        container: dict[str, Any] = {}

        print(f"  ① Generator starts — label='{label}'")
        print(f"  ② Before yield — recording start time")
        start = time.perf_counter()

        print(f"  ③ yield container — PAUSING generator, sending {{}} to caller")
        yield container
        print(f"  ⑥ Generator RESUMES — block has finished")

        elapsed = time.perf_counter() - start
        container["elapsed"] = elapsed
        print(f"  ⑦ After yield — elapsed = {elapsed:.6f}s, stored in container")
        print(f"  ⑧ Generator ends — context manager __exit__ complete")

    print("\nCalling: with traced_timer('demo') as t:")
    with traced_timer("demo") as t:
        print(f"  ④ Inside `with` block — t is: {t}")
        print(f"  ⑤ Running user code... (simulating work)")
        _ = sum(range(50_000))

    print(f"  ⑨ After `with` — t is now: {t}")
    print(f"  ⑩ Accessing result: t['elapsed'] = {t['elapsed']:.6f}s")


# =========================================================================
# SECTION 4: WHY YIELD A MUTABLE CONTAINER?
# =========================================================================
# Problem: We yield BEFORE the timed block runs, but need to store
# the result AFTER it completes.
#
# We can't yield a frozen dataclass — can't mutate it after yielding.
# We can't yield a float — immutable, reassignment creates a new object.
#
# Solution: Yield a MUTABLE CONTAINER (dict or list).
#
# MENTAL MODEL — The Mailbox Pattern:
# =====================================
#
#   yield container   →  You hand someone an EMPTY MAILBOX
#                        They hold the mailbox (same object, same address)
#                        Their code runs
#                        You put a LETTER in the mailbox (after yield resumes)
#                        They can now read the letter from their mailbox
#
# WHY A DICT WORKS (Python reference semantics):
#
#   container = {}           # Object lives at memory address 0xABC
#   yield container          # Caller gets a REFERENCE to 0xABC
#                            # Caller's `t` variable points to 0xABC
#   container["result"] = x  # We write to the SAME object at 0xABC
#                            # Caller's `t` still points to 0xABC
#                            # So t["result"] sees our write!
#
# WHY A FLOAT WOULD FAIL:
#
#   elapsed = 0.0            # Float at address 0xDEF
#   yield elapsed            # Caller gets 0.0 (the VALUE, not a reference)
#   elapsed = 1.23           # Creates NEW float at address 0xFFF
#                            # Caller's variable still holds 0.0!
# =========================================================================

def section_4_mutable_container() -> None:
    """Demonstrate why mutable containers are needed with yield."""
    print("\n" + "=" * 60)
    print("SECTION 4: Why Yield a Mutable Container")
    print("=" * 60)

    # --- Example 1: WRONG — yielding an immutable value ---
    @contextmanager
    def broken_timer(label: str) -> Generator[float, None, None]:
        """BROKEN: yielding a float doesn't work for post-yield updates."""
        elapsed = 0.0
        start = time.perf_counter()
        yield elapsed  # ← caller gets 0.0 (a copy of the value)
        elapsed = time.perf_counter() - start  # ← new float, caller never sees it
        # The caller's variable still holds 0.0!

    print("\n❌ BROKEN — yielding a float:")
    with broken_timer("oops") as t:
        _ = sum(range(50_000))
    print(f"  t = {t}  ← still 0.0! The update never reached the caller.")

    # --- Example 2: CORRECT — yielding a mutable dict ---
    @contextmanager
    def working_timer(label: str) -> Generator[dict[str, Any], None, None]:
        """CORRECT: yielding a dict — both sides reference the same object."""
        container: dict[str, Any] = {}  # mutable!
        start = time.perf_counter()
        yield container  # ← caller gets a REFERENCE to this same dict
        elapsed = time.perf_counter() - start
        container["elapsed"] = elapsed  # ← writes to the SAME dict object

    print("\n✅ CORRECT — yielding a dict:")
    with working_timer("good") as t:
        _ = sum(range(50_000))
    print(f"  t = {t}  ← dict was updated after yield!")
    print(f"  t['elapsed'] = {t['elapsed']:.6f}s")

    # --- Example 3: Also works with a list ---
    @contextmanager
    def list_timer(label: str) -> Generator[list[Any], None, None]:
        """Also valid: yield a list as the mutable container."""
        container: list[Any] = []  # mutable!
        start = time.perf_counter()
        yield container
        elapsed = time.perf_counter() - start
        container.append(elapsed)  # ← appends to the SAME list

    print("\n✅ ALSO CORRECT — yielding a list:")
    with list_timer("list") as t:
        _ = sum(range(50_000))
    print(f"  t = {t}  ← list was updated after yield!")
    print(f"  t[0] = {t[0]:.6f}s")


# =========================================================================
# SECTION 5: DECORATORS RECAP — TWO-LAYER vs THREE-LAYER
# =========================================================================
# Before showing how to wrap a context manager in a decorator,
# let's review the two decorator patterns.
#
# TWO-LAYER — decorator WITHOUT parameters:
# ===========================================
#
#   def my_decorator(func):          # Layer 1: receives FUNCTION
#       @wraps(func)
#       def wrapper(*args, **kwargs): # Layer 2: receives ARGUMENTS
#           print("before")
#           result = func(*args, **kwargs)
#           print("after")
#           return result
#       return wrapper
#
#   @my_decorator        # ← no parentheses, no parameters
#   def greet(name):
#       print(f"Hello, {name}")
#
# THREE-LAYER — decorator WITH parameters:
# ==========================================
#
#   def my_decorator(label):          # Layer 1: receives PARAMETER
#       def decorator(func):          # Layer 2: receives FUNCTION
#           @wraps(func)
#           def wrapper(*args, **kwargs): # Layer 3: receives ARGUMENTS
#               print(f"[{label}] before")
#               result = func(*args, **kwargs)
#               print(f"[{label}] after")
#               return result
#           return wrapper
#       return decorator
#
#   @my_decorator("greet")   # ← parentheses WITH parameter
#   def greet(name):
#       print(f"Hello, {name}")
#
# WHAT PYTHON DOES:
#
#   Two-layer:   greet = my_decorator(greet)
#   Three-layer: greet = my_decorator("greet")(greet)
#                        ↑ returns decorator  ↑ called with function
# =========================================================================

def section_5_decorator_recap() -> None:
    """Review two-layer and three-layer decorator patterns."""
    print("\n" + "=" * 60)
    print("SECTION 5: Decorators Recap — 2-Layer vs 3-Layer")
    print("=" * 60)

    # --- Two-layer: no parameters ---
    def log_call(func: Callable) -> Callable:
        """Two-layer decorator — no parameters."""
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            print(f"  [log_call] Calling {func.__name__}")
            result = func(*args, **kwargs)
            print(f"  [log_call] {func.__name__} returned {result}")
            return result
        return wrapper

    @log_call
    def add(a: int, b: int) -> int:
        """Add two numbers."""
        return a + b

    print("\nTwo-layer decorator (no parameters):")
    print(f"  add.__name__ = '{add.__name__}'  ← preserved by @wraps")
    result = add(3, 4)
    print(f"  Final result: {result}")

    # --- Three-layer: with parameters ---
    def log_call_with_label(label: str) -> Callable:
        """Three-layer decorator — with parameter."""
        def decorator(func: Callable) -> Callable:
            @wraps(func)
            def wrapper(*args: Any, **kwargs: Any) -> Any:
                print(f"  [{label}] Calling {func.__name__}")
                result = func(*args, **kwargs)
                print(f"  [{label}] {func.__name__} returned {result}")
                return result
            return wrapper
        return decorator

    @log_call_with_label("MATH")
    def multiply(a: int, b: int) -> int:
        """Multiply two numbers."""
        return a * b

    print("\nThree-layer decorator (with parameter 'MATH'):")
    print(f"  multiply.__name__ = '{multiply.__name__}'  ← preserved by @wraps")
    result = multiply(3, 4)
    print(f"  Final result: {result}")

    # --- What Python actually does ---
    print("\n  What Python does behind the scenes:")
    print("  Two-layer:   add      = log_call(add)")
    print("  Three-layer: multiply = log_call_with_label('MATH')(multiply)")
    print("                         ↑ returns decorator func ↑ called with fn")


# =========================================================================
# SECTION 6: WRAPPING A CONTEXT MANAGER IN A DECORATOR
# =========================================================================
# This is the KEY pattern used in benchmarks.py.
#
# The idea: build the timing logic ONCE in a context manager,
# then reuse it in a decorator. DRY — Don't Repeat Yourself.
#
# VISUAL — How timed() wraps timer():
# =====================================
#
#   @timed("load")
#   def load_dict(path):
#       return True
#
#   # When load_dict(path) is called, this happens:
#
#   ┌─ wrapper(path) is called
#   │
#   │  ┌─ with timer("load") as t:     ← opens context manager
#   │  │   │
#   │  │   │  ┌─ start = perf_counter()
#   │  │   │  └─ yield container → PAUSE
#   │  │   │
#   │  │   ├─ result = func(path)       ← calls original load_dict
#   │  │   │         = True
#   │  │   │
#   │  │   └─ block ends → generator resumes
#   │  │      elapsed = perf_counter() - start
#   │  │      container["result"] = BenchmarkResult(...)
#   │  │
#   │  └─ t["result"] is now populated
#   │
#   │  wrapper.benchmark = t["result"]  ← stored on function object
#   │  return result                    ← returns True (unchanged)
#   └─ done
# =========================================================================

def section_6_context_manager_in_decorator() -> None:
    """Demonstrate wrapping a context manager inside a decorator."""
    print("\n" + "=" * 60)
    print("SECTION 6: Context Manager Inside a Decorator")
    print("=" * 60)

    # --- Step 1: The context manager (foundation) ---
    @contextmanager
    def timer_cm(label: str) -> Generator[dict[str, Any], None, None]:
        """Context manager that times a code block."""
        container: dict[str, Any] = {}
        start = time.perf_counter()
        print(f"  [timer_cm] Started timing '{label}'")
        yield container
        elapsed = time.perf_counter() - start
        container["elapsed"] = elapsed
        print(f"  [timer_cm] Finished timing '{label}': {elapsed:.6f}s")

    # --- Step 2: The decorator that WRAPS the context manager ---
    def timed_decorator(label: str) -> Callable:
        """Three-layer decorator that reuses timer_cm inside."""
        def decorator(func: Callable) -> Callable:
            @wraps(func)
            def wrapper(*args: Any, **kwargs: Any) -> Any:
                print(f"  [wrapper]  Opening timer_cm for '{label}'")

                # HERE IS THE KEY: reuse the context manager
                with timer_cm(label) as t:
                    result = func(*args, **kwargs)

                # Store result on the wrapper function
                wrapper.benchmark = t["elapsed"]  # type: ignore[attr-defined]
                print(f"  [wrapper]  Stored benchmark: {t['elapsed']:.6f}s")
                return result

            wrapper.benchmark = None  # type: ignore[attr-defined]
            return wrapper
        return decorator

    # --- Usage: as context manager (flexible, block-level) ---
    print("\n--- Usage 1: Context manager (block-level timing) ---")
    with timer_cm("direct") as t:
        total = sum(range(100_000))
    print(f"  After block: elapsed = {t['elapsed']:.6f}s, sum = {total}")

    # --- Usage: as decorator (function-level timing) ---
    print("\n--- Usage 2: Decorator (function-level timing) ---")

    @timed_decorator("compute")
    def compute_sum(n: int) -> int:
        """Sum numbers from 0 to n-1."""
        return sum(range(n))

    result = compute_sum(100_000)
    print(f"  Return value: {result}  (unchanged by decorator)")
    print(f"  Benchmark:    {compute_sum.benchmark:.6f}s")  # type: ignore[attr-defined]
    print(f"  __name__:     '{compute_sum.__name__}'  (preserved by @wraps)")


# =========================================================================
# SECTION 7: COMMON PATTERNS AND REAL-WORLD USAGE
# =========================================================================
# These patterns appear in professional Python code and in frameworks
# you'll use across your roadmap stages.
# =========================================================================

def section_7_common_patterns() -> None:
    """Show real-world context manager patterns from your roadmap."""
    print("\n" + "=" * 60)
    print("SECTION 7: Common Patterns and Real-World Usage")
    print("=" * 60)

    # --- Pattern 1: Temporary state change (restore after) ---
    # Used in: test fixtures, Streamlit session state, config overrides
    @contextmanager
    def temporary_log_level(
        logger: logging.Logger,
        level: int,
    ) -> Generator[None, None, None]:
        """Temporarily change log level, restore when done.

        Usage
        -----
        ::

            with temporary_log_level(logger, logging.DEBUG):
                logger.debug("This will print")
            # Level is restored to original after the block

        Real-world: Streamlit debug mode, test verbose output,
        DataVault LLM call tracing
        """
        original_level = logger.level
        logger.setLevel(level)
        yield  # ← yield None when caller doesn't need a value
        logger.setLevel(original_level)  # ← always restores

    demo_logger = logging.getLogger("demo")
    demo_logger.setLevel(logging.WARNING)

    print("\nPattern 1: Temporary state change")
    print(f"  Before: logger level = {demo_logger.level} (WARNING)")
    with temporary_log_level(demo_logger, logging.DEBUG):
        print(f"  During: logger level = {demo_logger.level} (DEBUG)")
    print(f"  After:  logger level = {demo_logger.level} (WARNING restored)")

    # --- Pattern 2: Exception-safe cleanup ---
    # Used in: database connections, file handles, network sockets
    @contextmanager
    def managed_connection(name: str) -> Generator[dict[str, Any], None, None]:
        """Simulate a database connection with guaranteed cleanup.

        Real-world equivalents:
        - psycopg2.connect()   (Stage 2: PostgreSQL)
        - boto3.resource()     (Stage 2: AWS)
        - chromadb.Client()    (Stage 1: PolicyPulse)
        - mlflow.start_run()   (Stage 3: ML experiment tracking)
        """
        conn = {"name": name, "open": True}
        print(f"  [connect]    Opened connection '{name}'")
        try:
            yield conn  # ← caller uses the connection
        except Exception as e:
            print(f"  [error]      Error in '{name}': {e}")
            raise  # ← re-raise so caller can handle it
        finally:
            # finally ALWAYS runs — even if an exception occurred
            conn["open"] = False
            print(f"  [cleanup]    Closed connection '{name}' (guaranteed)")

    print("\nPattern 2: Exception-safe cleanup (happy path)")
    with managed_connection("db") as conn:
        print(f"  [user code]  Using connection: {conn}")
    print(f"  After block: conn['open'] = {conn['open']}")

    print("\nPattern 2: Exception-safe cleanup (error path)")
    try:
        with managed_connection("db_error") as conn:
            print(f"  [user code]  About to crash...")
            raise ValueError("Simulated database error!")
    except ValueError:
        print(f"  [caught]     ValueError caught outside `with` block")
        print(f"  [verify]     conn['open'] = {conn['open']}  ← still cleaned up!")

    # --- Pattern 3: Accumulating timer (loop usage) ---
    # Used in: Speller's check() hot loop
    @contextmanager
    def accumulating_timer(
        label: str,
        accumulator: dict[str, float],
    ) -> Generator[None, None, None]:
        """Add elapsed time to a running total.

        Used when timing MANY calls to the same operation
        and you want the cumulative time.

        This is exactly how Speller times check() —
        thousands of calls, one total.
        """
        start = time.perf_counter()
        yield
        elapsed = time.perf_counter() - start
        accumulator[label] = accumulator.get(label, 0.0) + elapsed

    print("\nPattern 3: Accumulating timer (loop usage — Speller's check() pattern)")
    totals: dict[str, float] = {}
    words = ["hello", "world", "python", "speller", "test"]
    for word in words:
        with accumulating_timer("check", totals):
            # Simulate dictionary lookup
            _ = word.lower() in {"hello", "world", "python"}
    print(f"  Checked {len(words)} words")
    print(f"  Total check time: {totals['check']:.6f}s (accumulated)")

    # --- Pattern 4: yield None — when caller doesn't need a value ---
    print("\nPattern 4: yield None (no value needed)")
    print("  Some context managers yield nothing — they just do setup/teardown:")
    print("  • with torch.no_grad():       ← disables gradient computation")
    print("  • with mlflow.start_run():     ← starts experiment tracking")
    print("  • with temporary_log_level():  ← changes log level temporarily")
    print("  These yield None (or just `yield` with no value)")


# =========================================================================
# SECTION 8: GOTCHAS AND PITFALLS
# =========================================================================
# Common mistakes when using @contextmanager and decorators together.
# =========================================================================

def section_8_gotchas() -> None:
    """Show common mistakes and how to avoid them."""
    print("\n" + "=" * 60)
    print("SECTION 8: Gotchas and Pitfalls")
    print("=" * 60)

    # --- Gotcha 1: Multiple yields ---
    print("\nGotcha 1: @contextmanager generators MUST yield exactly ONCE")
    print("  ❌ WRONG:")
    print("     @contextmanager")
    print("     def bad():")
    print("         yield 'first'   # works")
    print("         yield 'second'  # RuntimeError! Generator didn't stop!")
    print("")
    print("  ✅ CORRECT:")
    print("     @contextmanager")
    print("     def good():")
    print("         yield 'only_one'  # exactly one yield")

    # --- Gotcha 2: Forgetting @wraps in decorator ---
    print("\nGotcha 2: Always use @wraps(func) in decorators")

    def bad_decorator(func: Callable) -> Callable:
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            return func(*args, **kwargs)
        return wrapper  # ← no @wraps!

    def good_decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            return func(*args, **kwargs)
        return wrapper

    @bad_decorator
    def my_func_bad() -> str:
        """Important docstring."""
        return "hello"

    @good_decorator
    def my_func_good() -> str:
        """Important docstring."""
        return "hello"

    print(f"  Without @wraps: __name__ = '{my_func_bad.__name__}', "
          f"__doc__ = '{my_func_bad.__doc__}'")
    print(f"  With @wraps:    __name__ = '{my_func_good.__name__}', "
          f"__doc__ = '{my_func_good.__doc__}'")

    # --- Gotcha 3: Exception handling in @contextmanager ---
    print("\nGotcha 3: Use try/finally if cleanup MUST happen")
    print("  ❌ WRONG — cleanup skipped if exception occurs:")
    print("     @contextmanager")
    print("     def bad_cleanup():")
    print("         resource = acquire()")
    print("         yield resource")
    print("         release(resource)    # ← NEVER RUNS if exception in block!")
    print("")
    print("  ✅ CORRECT — try/finally guarantees cleanup:")
    print("     @contextmanager")
    print("     def good_cleanup():")
    print("         resource = acquire()")
    print("         try:")
    print("             yield resource")
    print("         finally:")
    print("             release(resource)  # ← ALWAYS runs")

    # --- Gotcha 4: Storing results on wrapper function ---
    print("\nGotcha 4: # type: ignore[attr-defined] for dynamic attributes")
    print("  When you do `wrapper.benchmark = result`, mypy complains because")
    print("  Callable doesn't have a .benchmark attribute. The comment")
    print("  # type: ignore[attr-defined] tells mypy 'I know, this is intentional'.")
    print("  This is a known pattern for function attributes in Python.")


# =========================================================================
# CHEAT SHEET — Quick Reference
# =========================================================================
#
# @contextmanager converts a generator to a context manager:
#   @contextmanager
#   def my_cm():
#       setup()       # __enter__
#       yield value   # value → `as X`
#       cleanup()     # __exit__
#
# Context manager with exception safety:
#   @contextmanager
#   def safe_cm():
#       resource = acquire()
#       try:
#           yield resource
#       finally:
#           release(resource)
#
# Two-layer decorator (no params):
#   def deco(func):
#       @wraps(func)
#       def wrapper(*args, **kwargs):
#           return func(*args, **kwargs)
#       return wrapper
#
# Three-layer decorator (with params):
#   def deco(param):
#       def decorator(func):
#           @wraps(func)
#           def wrapper(*args, **kwargs):
#               return func(*args, **kwargs)
#           return wrapper
#       return decorator
#
# Decorator wrapping context manager:
#   def timed(name):
#       def decorator(func):
#           @wraps(func)
#           def wrapper(*args, **kwargs):
#               with timer(name) as t:
#                   result = func(*args, **kwargs)
#               wrapper.benchmark = t["result"]
#               return result
#           return wrapper
#       return decorator
#
# Key rules:
#   • @contextmanager generators must yield EXACTLY once
#   • yield a MUTABLE container (dict/list) to share data post-yield
#   • Always @wraps(func) in decorators
#   • Use try/finally in context managers for guaranteed cleanup
#   • time.perf_counter() > time.time() for benchmarks
# =========================================================================


def main() -> None:
    """Run all sections sequentially."""
    print("=" * 60)
    print(" @contextmanager & Decorators — Complete Reference Guide")
    print(" Manuel Reyes — CS50 Stage 1 / GenAI-First Roadmap v8.1")
    print("=" * 60)

    section_1_context_manager_basics()
    section_2_contextmanager_decorator()
    section_3_execution_flow()
    section_4_mutable_container()
    section_5_decorator_recap()
    section_6_context_manager_in_decorator()
    section_7_common_patterns()
    section_8_gotchas()

    print("\n" + "=" * 60)
    print(" Reference guide complete. See CHEAT SHEET at bottom of file.")
    print("=" * 60)


if __name__ == "__main__":
    main()
