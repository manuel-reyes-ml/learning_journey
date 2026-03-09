"""
python_datamodel_functools_reference.py
========================================

Personal reference: Python's function data model attributes and functools.wraps.

Topics covered
--------------
1. Function Objects — functions are objects with attributes
2. __name__ vs __qualname__ — identity and nesting context
3. __doc__ — docstrings as attributes
4. __dict__, __module__, __annotations__ — other function metadata
5. __defaults__, __kwdefaults__ — default argument introspection
6. Closures & __closure__ — how closures capture variables
7. functools.wraps — preserving metadata in decorators
8. functools.partial — pre-filling arguments (factory alternative)
9. functools.update_wrapper — manual metadata transfer
10. Production Patterns — real-world applications in your roadmap

Why this matters for your roadmap
----------------------------------
- Stage 1: Your BMP filter factory creates closures that lose their identity.
  Understanding __name__, __qualname__, and functools.wraps fixes this.
- Stage 2+: LangChain decorators, Airflow task decorators, FastAPI route
  decorators, and pytest fixtures ALL rely on functools.wraps. If you don't
  understand the data model, debugging decorator-heavy frameworks is a
  nightmare.
- Stage 4-5: Building your own decorators for logging, retries, caching,
  and authentication in agentic AI systems.

How to use this file
---------------------
Run it directly to see all output::

    $ python 22_python_datamodel_functools_reference.py

Or import individual sections to experiment in a REPL.

References
----------
.. [1] Python Data Model: https://docs.python.org/3/reference/datamodel.html
.. [2] functools docs: https://docs.python.org/3/library/functools.html
.. [3] PEP 3155 — Qualified name: https://peps.python.org/pep-3155/
.. [4] Fluent Python, Ch. 7 — Closures & Decorators (Ramalho)
.. [5] Effective Python, Item 38 — functools.wraps (Slatkin)
"""

from __future__ import annotations
from functools import wraps, partial, update_wrapper
from typing import Callable, Any
import inspect
import logging


# =============================================================================
# SECTION 1: FUNCTIONS ARE OBJECTS
# =============================================================================
#
# In Python, functions are first-class objects. This means:
#   1. They can be assigned to variables
#   2. They can be passed as arguments
#   3. They can be returned from other functions
#   4. They have ATTRIBUTES (just like any other object)
#
# This is different from languages like Java or C where functions
# are NOT objects. Python's design is what makes decorators, closures,
# and higher-order functions possible.
#
# MENTAL MODEL:
# ┌─────────────────────────────────────────────────┐
# │  def greet(name):                               │
# │      """Say hello."""                            │
# │      return f"Hello, {name}"                     │
# │                                                  │
# │  Python creates a FUNCTION OBJECT:               │
# │  ┌──────────────────────────────────┐            │
# │  │ greet (function object)          │            │
# │  │ ├── __name__    = "greet"        │            │
# │  │ ├── __qualname__ = "greet"       │            │
# │  │ ├── __doc__     = "Say hello."   │            │
# │  │ ├── __module__  = "__main__"     │            │
# │  │ ├── __annotations__ = {...}      │            │
# │  │ ├── __defaults__ = None          │            │
# │  │ ├── __closure__  = None          │            │
# │  │ ├── __dict__    = {}             │            │
# │  │ └── __code__    = <code object>  │            │
# │  └──────────────────────────────────┘            │
# └─────────────────────────────────────────────────┘
#
# =============================================================================


def section_1_functions_are_objects() -> None:
    """
    Demonstrate that functions are objects with attributes.

    Shows how to inspect a function's built-in attributes using
    ``dir()`` and direct attribute access. Every function in Python
    automatically gets these attributes at creation time.
    """
    def greet(name: str) -> str:
        """Say hello to someone."""
        return f"Hello, {name}"

    print("=" * 70)
    print("SECTION 1: FUNCTIONS ARE OBJECTS")
    print("=" * 70)

    # Functions have a type — they're instances of the 'function' class
    print(f"\ntype(greet)        = {type(greet)}")
    # Output: <class 'function'>

    # You can list ALL attributes of a function object
    # Filter to just the dunder (double underscore) attributes
    func_attrs = [attr for attr in dir(greet) if attr.startswith("__")]
    print(f"\nFunction attributes ({len(func_attrs)} total):")
    for attr in func_attrs:
        print(f"  {attr}")

    # You can even add CUSTOM attributes to functions
    # (this is how some decorator patterns store state)
    greet.call_count = 0    # type: ignore[attr-defined]
    greet.call_count += 1   # type: ignore[attr-defined]
    print(f"\nCustom attribute:   greet.call_count = {greet.call_count}")

    # Functions can be assigned to variables (first-class objects)
    say_hi = greet
    print(f"\nsay_hi('World')    = {say_hi('World')}")
    print(f"say_hi is greet    = {say_hi is greet}")  # Same object!


# =============================================================================
# SECTION 2: __name__ vs __qualname__
# =============================================================================
#
# __name__     = The SIMPLE name of the function (just the identifier)
# __qualname__ = The QUALIFIED name showing the full nesting path
#
# WHY BOTH EXIST:
# __name__ was the original attribute (Python 2). But when you have
# nested functions, closures, or methods, __name__ alone is ambiguous.
# PEP 3155 (Python 3.3) introduced __qualname__ to solve this.
#
# VISUAL GUIDE:
# ┌───────────────────────────────────────────────────────────┐
# │  Context                  │ __name__    │ __qualname__    │
# │───────────────────────────│─────────────│─────────────────│
# │  def foo():               │ "foo"       │ "foo"           │
# │  class A:                 │             │                 │
# │      def bar(self):       │ "bar"       │ "A.bar"         │
# │  def outer():             │             │                 │
# │      def inner():         │ "inner"     │ "outer.<locals> │
# │                           │             │  .inner"        │
# │  factory() -> closure     │ "closure"   │ "factory.       │
# │                           │             │  <locals>.      │
# │                           │             │  closure"       │
# └───────────────────────────────────────────────────────────┘
#
# The <locals> marker tells Python (and YOU in a traceback) that
# this function was defined INSIDE another function's local scope.
#
# =============================================================================


def section_2_name_vs_qualname() -> None:
    """
    Show the difference between __name__ and __qualname__ in various contexts.

    Demonstrates how nesting depth affects qualified names, which is
    critical for debugging closures and factory-created functions.
    """
    print("\n" + "=" * 70)
    print("SECTION 2: __name__ vs __qualname__")
    print("=" * 70)

    # ── Case 1: Top-level function ──────────────────────────────
    # Both are identical for module-level functions
    def top_level():
        pass

    print(f"\n── Case 1: Top-level function ──")
    print(f"  __name__    = {top_level.__name__!r}")
    print(f"  __qualname__ = {top_level.__qualname__!r}")
    # __name__    = 'top_level'
    # __qualname__ = 'section_2_name_vs_qualname.<locals>.top_level'
    # NOTE: Even this is nested because we're inside section_2_name_vs_qualname!

    # ── Case 2: Nested function (closure pattern) ───────────────
    def outer():
        def inner():
            pass
        return inner

    inner_func = outer()
    print(f"\n── Case 2: Nested function ──")
    print(f"  __name__    = {inner_func.__name__!r}")
    print(f"  __qualname__ = {inner_func.__qualname__!r}")
    # __name__    = 'inner'
    # __qualname__ = 'section_2_name_vs_qualname.<locals>.outer.<locals>.inner'

    # ── Case 3: Class method ────────────────────────────────────
    class Processor:
        def run(self) -> None:
            pass

    print(f"\n── Case 3: Class method ──")
    print(f"  __name__    = {Processor.run.__name__!r}")
    print(f"  __qualname__ = {Processor.run.__qualname__!r}")
    # __name__    = 'run'
    # __qualname__ = 'section_2_name_vs_qualname.<locals>.Processor.run'

    # ── Case 4: Factory-created functions (YOUR BMP scenario) ───
    # This is exactly what happens with create_brightness_filter
    def create_filter(value: int) -> Callable:
        def adjust(data: list) -> list:
            return [x + value for x in data]
        return adjust

    brighten = create_filter(50)
    darken = create_filter(-50)

    print(f"\n── Case 4: Factory-created (THE PROBLEM) ──")
    print(f"  brighten.__name__    = {brighten.__name__!r}")
    print(f"  darken.__name__      = {darken.__name__!r}")
    print(f"  brighten.__qualname__ = {brighten.__qualname__!r}")
    # PROBLEM: Both say "adjust" — indistinguishable in logs/tracebacks!

    # ── Case 5: Factory with manual __name__ fix (THE SOLUTION) ─
    def create_filter_fixed(value: int, name: str) -> Callable:
        def adjust(data: list) -> list:
            return [x + value for x in data]

        # Manually set identity attributes
        adjust.__name__ = name
        adjust.__qualname__ = f"create_filter_fixed.<locals>.{name}"
        adjust.__doc__ = f"Adjust pixel values by {value} units."
        return adjust

    brighten_v2 = create_filter_fixed(50, "brighten")
    darken_v2 = create_filter_fixed(-50, "darken")

    print(f"\n── Case 5: Factory with __name__ fix (THE SOLUTION) ──")
    print(f"  brighten_v2.__name__    = {brighten_v2.__name__!r}")
    print(f"  darken_v2.__name__      = {darken_v2.__name__!r}")
    print(f"  brighten_v2.__qualname__ = {brighten_v2.__qualname__!r}")
    print(f"  darken_v2.__qualname__   = {darken_v2.__qualname__!r}")

    # ── WHY THIS MATTERS: Logging and Tracebacks ────────────────
    # When Python shows an error, it uses __qualname__ in the traceback:
    #
    #   File "bmp_filters.py", line 42, in adjust       <-- USELESS
    #   File "bmp_filters.py", line 42, in brighten      <-- USEFUL
    #
    # When you log with __name__, the same problem appears:
    #   logger.info(f"Applying {func.__name__}...")
    #   "Applying adjust..."    <-- Which one?!
    #   "Applying brighten..."  <-- Clear!

    print(f"\n── Why it matters: simulated logging ──")
    for func in [brighten, darken]:
        print(f"  Applying {func.__name__}...")  # Both say "adjust" 😕

    for func in [brighten_v2, darken_v2]:
        print(f"  Applying {func.__name__}...")  # "brighten", "darken" 😊


# =============================================================================
# SECTION 3: __doc__ — DOCSTRINGS AS ATTRIBUTES
# =============================================================================
#
# When you write a triple-quoted string as the first statement in a
# function, class, or module, Python stores it as __doc__.
#
# WHO READS __doc__:
#   - help()          → Built-in help system
#   - IDE tooltips    → Cursor, VS Code hover
#   - Sphinx          → Documentation generators
#   - inspect.getdoc  → Programmatic access
#   - pydoc           → Command-line documentation
#
# KEY INSIGHT: __doc__ is a regular string attribute. You can read it,
# reassign it, and even set it on functions that don't have docstrings.
#
# =============================================================================


def section_3_doc_attribute() -> None:
    """
    Show how __doc__ works, how to read it, and how to set it dynamically.

    Particularly relevant for factory-created functions where the
    inner function's docstring is generic or empty.
    """
    print("\n" + "=" * 70)
    print("SECTION 3: __doc__ — DOCSTRINGS AS ATTRIBUTES")
    print("=" * 70)

    # ── Reading __doc__ ─────────────────────────────────────────
    def documented_function(x: int) -> int:
        """
        Double the input value.

        Parameters
        ----------
        x : int
            Value to double.

        Returns
        -------
        int
            The doubled value.
        """
        return x * 2

    print(f"\n── Reading __doc__ ──")
    doc_preview = repr(documented_function.__doc__)[:80]
    print(f"  documented_function.__doc__ =")
    print(f"  {doc_preview}...")

    # help() reads from __doc__
    # Uncomment to see full help output:
    # help(documented_function)

    # ── Functions without docstrings ────────────────────────────
    def no_docs(x):
        return x

    print(f"\n── No docstring ──")
    print(f"  no_docs.__doc__ = {no_docs.__doc__!r}")
    # None — help() will show nothing useful

    # ========================================================================
    # repr() and f-string flags
    # ========================================================================
    # '!r' it's a format flag inside f-strings that calls repr() on the value instead of str().
    # The difference:
    name = "blur"

    print(f"{name}")       # blur        ← str() — human-friendly
    print(f"{name!r}")     # 'blur'      ← repr() — shows the quotes
    
    # str() gives you what a human wants to read. repr() gives you what a developer needs to
    # debug — it shows the object's type unambiguously. The distinction matters most
    # with strings and None:
    value = "blur"
    empty = ""
    nothing = None

    # Without !r — ambiguous in logs
    print(f"filter = {value}")      # filter = blur
    print(f"filter = {empty}")      # filter =         ← is it empty or None?
    print(f"filter = {nothing}")    # filter = None     ← string "None" or actual None?

    # With !r — unambiguous
    print(f"filter = {value!r}")    # filter = 'blur'   ← clearly a string
    print(f"filter = {empty!r}")    # filter = ''       ← clearly empty string
    print(f"filter = {nothing!r}")  # filter = None     ← clearly NoneType
    
    # I use it in the reference files for exactly this reason — when printing
    # function attributes like __name__ or __doc__, you need to see whether
    # the value is a string, None, or empty. Without !r, None and the string
    # "None" look identical in output.
    
    # There are three format flags total: !r for repr(), !s for str()
    # (the default, so you never need it), and !a for ascii() (rarely
    # used — escapes non-ASCII characters).
    # ========================================================================
    # ========================================================================
    

    # ── Setting __doc__ dynamically (factory pattern) ───────────
    def create_multiplier(factor: int) -> Callable[[int], int]:
        def multiply(x: int) -> int:
            return x * factor
        # Dynamically set a meaningful docstring
        multiply.__doc__ = (
            f"Multiply input by {factor}.\n\n"
            f"Parameters\n"
            f"----------\n"
            f"x : int\n"
            f"    Value to multiply.\n\n"
            f"Returns\n"
            f"-------\n"
            f"int\n"
            f"    x * {factor}\n"
        )
        return multiply

    double = create_multiplier(2)
    triple = create_multiplier(3)

    print(f"\n── Dynamically set __doc__ ──")
    print(f"  double.__doc__ (first 40 chars) = {double.__doc__[:40]!r}")
    print(f"  triple.__doc__ (first 40 chars) = {triple.__doc__[:40]!r}")

    # ── inspect.getdoc() — cleaned version ──────────────────────
    # inspect.getdoc() strips leading whitespace from docstrings
    # and handles inherited docstrings from parent classes.
    print(f"\n── inspect.getdoc() vs raw __doc__ ──")
    clean_doc = inspect.getdoc(documented_function)
    print(f"  Raw __doc__ starts with whitespace: {documented_function.__doc__[:20]!r}")
    print(f"  inspect.getdoc() is clean:          {clean_doc[:30]!r}" if clean_doc else "")


# =============================================================================
# SECTION 4: OTHER FUNCTION ATTRIBUTES
# =============================================================================
#
# Beyond __name__, __qualname__, and __doc__, functions carry:
#
# __module__      → Which module defined this function (string)
# __annotations__ → Type hints as a dict (PEP 3107)
# __defaults__    → Tuple of default values for positional params
# __kwdefaults__  → Dict of default values for keyword-only params
# __dict__        → Custom attributes you attach (like call_count)
# __code__        → The compiled bytecode object
#
# =============================================================================


def section_4_other_attributes() -> None:
    """
    Explore the lesser-known function attributes.

    These become important when building introspection tools,
    debugging decorators, or understanding framework internals.
    """
    print("\n" + "=" * 70)
    print("SECTION 4: OTHER FUNCTION ATTRIBUTES")
    print("=" * 70)

    def process_data(
        data: list[int],
        scale: float = 1.0,
        offset: int = 0,
        *,                        # Everything after * is keyword-only
        verbose: bool = False,
        log_level: str = "INFO",
    ) -> list[float]:
        """Scale and offset a list of integers."""
        return [x * scale + offset for x in data]

    # ── __module__ ──────────────────────────────────────────────
    # Tells you WHERE the function was defined
    print(f"\n── __module__ ──")
    print(f"  process_data.__module__ = {process_data.__module__!r}")
    # When running directly: '__main__'
    # When imported: 'my_package.my_module'

    # This is how logging.getLogger(__name__) works!
    # __name__ of the MODULE (not function) becomes the logger hierarchy.

    # ── __annotations__ ─────────────────────────────────────────
    # Type hints stored as a dictionary
    print(f"\n── __annotations__ ──")
    for param, hint in process_data.__annotations__.items():
        print(f"  {param}: {hint}")
    # data: list[int]
    # scale: float
    # offset: int
    # verbose: bool
    # log_level: str
    # return: list[float]

    # ── __defaults__ ────────────────────────────────────────────
    # Default values for POSITIONAL parameters (tuple)
    print(f"\n── __defaults__ (positional param defaults) ──")
    print(f"  process_data.__defaults__ = {process_data.__defaults__}")
    # (1.0, 0) — matches scale=1.0, offset=0

    # ── __kwdefaults__ ──────────────────────────────────────────
    # Default values for KEYWORD-ONLY parameters (dict)
    print(f"\n── __kwdefaults__ (keyword-only param defaults) ──")
    print(f"  process_data.__kwdefaults__ = {process_data.__kwdefaults__}")
    # {'verbose': False, 'log_level': 'INFO'}

    # ── __dict__ ────────────────────────────────────────────────
    # Custom attributes (empty by default)
    print(f"\n── __dict__ (custom attributes) ──")
    print(f"  Before: process_data.__dict__ = {process_data.__dict__}")
    process_data.version = "1.0"  # type: ignore[attr-defined]
    print(f"  After:  process_data.__dict__ = {process_data.__dict__}")

    # ── __code__ (advanced) ─────────────────────────────────────
    # The compiled bytecode object — rarely accessed directly
    # but useful for deep introspection
    print(f"\n── __code__ (bytecode metadata) ──")
    code = process_data.__code__
    print(f"  co_varnames  = {code.co_varnames}")   # All local variable names
    print(f"  co_argcount  = {code.co_argcount}")    # Number of positional args
    print(f"  co_filename  = {code.co_filename!r}")  # Source file


# =============================================================================
# SECTION 5: CLOSURES & __closure__
# =============================================================================
#
# A CLOSURE is a function that captures variables from its enclosing
# scope. The captured variables are stored in __closure__ as a tuple
# of "cell" objects.
#
# VISUAL:
# ┌─────────────────────────────────────────────────┐
# │  def make_adder(n):          # Enclosing scope  │
# │      ┌────────────────────┐                     │
# │      │ n = 10  (captured) │ ← "free variable"   │
# │      └────────┬───────────┘                     │
# │               │                                 │
# │      def adder(x):           # Inner function   │
# │          return x + n        # Uses 'n' from    │
# │                              # enclosing scope  │
# │      return adder                               │
# │                                                  │
# │  add10 = make_adder(10)                          │
# │  add10.__closure__[0].cell_contents == 10        │
# └─────────────────────────────────────────────────┘
#
# WHY THIS MATTERS:
# Your create_brightness_filter IS a closure. The 'adjustment'
# parameter is a free variable captured by the inner function.
# Understanding __closure__ lets you inspect what values were
# captured — invaluable for debugging.
#
# =============================================================================


def section_5_closures() -> None:
    """
    Demonstrate closures, free variables, and __closure__ introspection.

    Shows how your BMP brightness factory creates closures and
    how to inspect the captured values.
    """
    print("\n" + "=" * 70)
    print("SECTION 5: CLOSURES & __closure__")
    print("=" * 70)

    # ── Basic closure ───────────────────────────────────────────
    def make_adder(n: int) -> Callable[[int], int]:
        """Create a function that adds n to its argument."""
        def adder(x: int) -> int:
            return x + n    # 'n' is a FREE VARIABLE (not local, not global)
        return adder

    add10 = make_adder(10)
    add99 = make_adder(99)

    print(f"\n── Basic closure ──")
    print(f"  add10(5)  = {add10(5)}")   # 15
    print(f"  add99(1)  = {add99(1)}")   # 100

    # ── Inspecting __closure__ ──────────────────────────────────
    print(f"\n── Inspecting __closure__ ──")
    print(f"  add10.__closure__       = {add10.__closure__}")
    # Tuple of cell objects

    # Each cell has a .cell_contents attribute with the actual value
    if add10.__closure__:
        for i, cell in enumerate(add10.__closure__):
            print(f"  add10.__closure__[{i}].cell_contents = {cell.cell_contents}")
    # Output: 10

    # ── Free variables (what was captured) ──────────────────────
    # __code__.co_freevars lists the NAMES of captured variables
    print(f"\n── Free variable names ──")
    print(f"  add10.__code__.co_freevars = {add10.__code__.co_freevars}")
    # ('n',)

    # ── Non-closure functions have __closure__ = None ───────────
    def regular_func(x: int) -> int:
        return x + 1

    print(f"\n── Non-closure comparison ──")
    print(f"  regular_func.__closure__ = {regular_func.__closure__}")
    # None — no captured variables

    # ── YOUR BMP PATTERN: Brightness filter closure ─────────────
    # This mirrors create_brightness_filter exactly
    def create_brightness(adjustment: int, name: str) -> Callable:
        def adjust_brightness(pixels: list) -> list:
            return [max(0, min(255, p + adjustment)) for p in pixels]

        adjust_brightness.__name__ = name
        adjust_brightness.__qualname__ = f"create_brightness.<locals>.{name}"
        return adjust_brightness

    brighten = create_brightness(50, "brighten")
    darken = create_brightness(-50, "darken")

    print(f"\n── Your BMP pattern: closure inspection ──")
    print(f"  brighten.__name__    = {brighten.__name__!r}")
    print(f"  darken.__name__      = {darken.__name__!r}")

    # Inspect what values each closure captured
    if brighten.__closure__:
        for i, cell in enumerate(brighten.__closure__):
            var_name = brighten.__code__.co_freevars[i]
            print(f"  brighten captured: {var_name} = {cell.cell_contents!r}")

    if darken.__closure__:
        for i, cell in enumerate(darken.__closure__):
            var_name = darken.__code__.co_freevars[i]
            print(f"  darken captured:   {var_name} = {cell.cell_contents!r}")


# =============================================================================
# SECTION 6: functools.wraps — THE DECORATOR'S BEST FRIEND
# =============================================================================
#
# PROBLEM: When you decorate a function, the wrapper REPLACES the
# original. All metadata (__name__, __qualname__, __doc__, etc.)
# now belongs to the wrapper, not the original function.
#
# WITHOUT functools.wraps:
# ┌─────────────────────────────────────┐
# │  @my_decorator                      │
# │  def greet(name):                   │
# │      """Say hello."""               │
# │      return f"Hello, {name}"        │
# │                                     │
# │  greet.__name__ = "wrapper"  😕     │
# │  greet.__doc__  = None       😕     │
# │  help(greet)    = useless    😕     │
# └─────────────────────────────────────┘
#
# WITH functools.wraps:
# ┌─────────────────────────────────────┐
# │  @my_decorator                      │
# │  def greet(name):                   │
# │      """Say hello."""               │
# │      return f"Hello, {name}"        │
# │                                     │
# │  greet.__name__ = "greet"    ✅     │
# │  greet.__doc__  = "Say..."   ✅     │
# │  help(greet)    = correct    ✅     │
# │  greet.__wrapped__ = <orig>  ✅     │
# └─────────────────────────────────────┘
#
# WHAT functools.wraps COPIES (from wrapped → wrapper):
#   __module__
#   __name__
#   __qualname__
#   __annotations__
#   __doc__
#   __dict__        (merged, not replaced)
#   __wrapped__     (reference to the original function — BONUS)
#
# =============================================================================


def section_6_functools_wraps() -> None:
    """
    Compare decorators with and without functools.wraps.

    This is the most critical section for production Python.
    Every decorator you write should use @wraps(func).
    """
    print("\n" + "=" * 70)
    print("SECTION 6: functools.wraps")
    print("=" * 70)

    # ── BAD: Decorator WITHOUT @wraps ───────────────────────────
    def bad_logger(func: Callable) -> Callable:
        """Log function calls (broken metadata)."""
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            print(f"  [LOG] Calling {func.__name__}")
            return func(*args, **kwargs)
        return wrapper

    @bad_logger
    def add_bad(a: int, b: int) -> int:
        """Add two numbers together."""
        return a + b

    print(f"\n── WITHOUT @wraps (BAD) ──")
    print(f"  add_bad.__name__    = {add_bad.__name__!r}")       # 'wrapper' 😕
    print(f"  add_bad.__doc__     = {add_bad.__doc__!r}")         # None 😕
    print(f"  add_bad.__module__  = {add_bad.__module__!r}")
    print(f"  hasattr(__wrapped__) = {hasattr(add_bad, '__wrapped__')}")  # False
    print(f"  add_bad(2, 3)       = ", end="")
    result = add_bad(2, 3)
    print(result)

    # ── GOOD: Decorator WITH @wraps ─────────────────────────────
    def good_logger(func: Callable) -> Callable:
        """Log function calls (preserved metadata)."""
        @wraps(func)    # ← This one line fixes everything
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            print(f"  [LOG] Calling {func.__name__}")
            return func(*args, **kwargs)
        return wrapper

    @good_logger
    def add_good(a: int, b: int) -> int:
        """Add two numbers together."""
        return a + b

    print(f"\n── WITH @wraps (GOOD) ──")
    print(f"  add_good.__name__    = {add_good.__name__!r}")      # 'add_good' ✅
    print(f"  add_good.__doc__     = {add_good.__doc__!r}")        # 'Add...' ✅
    print(f"  add_good.__module__  = {add_good.__module__!r}")
    print(f"  hasattr(__wrapped__) = {hasattr(add_good, '__wrapped__')}")  # True ✅
    print(f"  add_good(2, 3)       = ", end="")
    result = add_good(2, 3)
    print(result)

    # ── __wrapped__: Access the ORIGINAL function ───────────────
    # @wraps adds a __wrapped__ attribute pointing to the original
    # This lets you bypass the decorator entirely (useful for testing)
    print(f"\n── __wrapped__ (bypass decorator) ──")
    print(f"  add_good.__wrapped__          = {add_good.__wrapped__!r}")
    print(f"  add_good.__wrapped__(2, 3)    = {add_good.__wrapped__(2, 3)}")
    # No "[LOG]" printed — we called the original directly!

    # ── REAL-WORLD: Timing decorator ────────────────────────────
    import time

    def timer(func: Callable) -> Callable:
        """Measure and print execution time."""
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            start = time.perf_counter()
            result = func(*args, **kwargs)
            elapsed = time.perf_counter() - start
            print(f"  {func.__name__} took {elapsed:.6f}s")
            return result
        return wrapper

    @timer
    def slow_sum(n: int) -> int:
        """Sum integers from 0 to n."""
        return sum(range(n))

    print(f"\n── Real-world: @timer decorator ──")
    print(f"  slow_sum.__name__ = {slow_sum.__name__!r}")  # 'slow_sum' ✅
    print(f"  Result: {slow_sum(1_000_000)}")

    # ── STACKING decorators (order matters!) ────────────────────
    # Decorators apply bottom-up: closest to the function first
    @timer
    @good_logger
    def multiply(a: int, b: int) -> int:
        """Multiply two numbers."""
        return a * b

    print(f"\n── Stacked decorators ──")
    print(f"  multiply.__name__ = {multiply.__name__!r}")
    print(f"  Result: ", end="")
    print(multiply(6, 7))
    # Order: timer wraps (good_logger wraps multiply)
    # So timer measures the TOTAL time including logging


# =============================================================================
# SECTION 7: functools.partial — FACTORY ALTERNATIVE
# =============================================================================
#
# partial() creates a new callable with some arguments pre-filled.
# It's an ALTERNATIVE to writing a closure/factory function.
#
# YOUR BMP SCENARIO — Two approaches:
#
# Approach A (closure factory — what you have):
#   def create_brightness_filter(adjustment):
#       def adjust(pixels):
#           return [clamp(p + adjustment) for p in pixels]
#       return adjust
#   brighten = create_brightness_filter(50)
#
# Approach B (partial — simpler for straightforward cases):
#   def adjust_brightness(pixels, adjustment):
#       return [clamp(p + adjustment) for p in pixels]
#   brighten = partial(adjust_brightness, adjustment=50)
#
# WHEN TO USE WHICH:
# - partial: When you just need to pre-fill arguments
# - closure: When you need custom logic, state, or __name__ control
#
# Your BMP factory is the right choice because you also want to
# register the function, set __name__, and maintain the same
# FilterFunc signature.
#
# =============================================================================


def section_7_functools_partial() -> None:
    """
    Show functools.partial as an alternative to closure factories.

    Compares both approaches so you can choose the right one
    for each situation in your projects.
    """
    print("\n" + "=" * 70)
    print("SECTION 7: functools.partial")
    print("=" * 70)

    # ── Basic partial usage ─────────────────────────────────────
    def multiply(a: int, b: int) -> int:
        """Multiply two numbers."""
        return a * b

    double = partial(multiply, b=2)
    triple = partial(multiply, b=3)

    print(f"\n── Basic partial ──")
    print(f"  double(5) = {double(5)}")  # 10
    print(f"  triple(5) = {triple(5)}")  # 15

    # ── Inspecting partial objects ──────────────────────────────
    print(f"\n── Partial introspection ──")
    print(f"  double.func     = {double.func!r}")      # Original function
    print(f"  double.args     = {double.args}")         # Positional pre-fills
    print(f"  double.keywords = {double.keywords}")     # Keyword pre-fills

    # ── IMPORTANT: partial objects DON'T have __name__ ──────────
    # This is a key difference from closures!
    print(f"\n── partial vs closure: __name__ ──")
    print(f"  hasattr(double, '__name__') = {hasattr(double, '__name__')}")
    # False! partial objects aren't functions, they're partial objects.
    # This is why your closure factory is BETTER for the FILTERS registry —
    # you need __name__ for the dispatch dictionary key.

    # ── Comparison: closure vs partial ──────────────────────────
    # Closure approach
    def make_multiplier(factor: int) -> Callable[[int], int]:
        def multiplier(x: int) -> int:
            return x * factor
        multiplier.__name__ = f"multiply_by_{factor}"
        return multiplier

    # Partial approach
    def base_multiply(x: int, factor: int = 1) -> int:
        return x * factor

    closure_double = make_multiplier(2)
    partial_double = partial(base_multiply, factor=2)

    print(f"\n── Side-by-side comparison ──")
    print(f"  Closure: closure_double(10) = {closure_double(10)}")
    print(f"  Partial: partial_double(10) = {partial_double(10)}")
    print(f"  Closure __name__: {closure_double.__name__!r}")
    print(f"  Partial type:     {type(partial_double).__name__!r}")

    # ── Where partial SHINES: simplifying repeated calls ────────
    # Common in data engineering — pre-configuring readers/writers
    import json

    # Instead of always writing json.dumps(data, indent=2, sort_keys=True):
    pretty_json = partial(json.dumps, indent=2, sort_keys=True)

    data = {"name": "Manuel", "stage": 1, "active": True}
    print(f"\n── Practical partial: pre-configured json.dumps ──")
    print(f"  {pretty_json(data)}")


# =============================================================================
# SECTION 8: functools.update_wrapper — MANUAL METADATA TRANSFER
# =============================================================================
#
# @wraps(func) is actually syntactic sugar for update_wrapper().
# They do the same thing, but update_wrapper gives you more control.
#
# @wraps(func)  ←→  update_wrapper(wrapper, wrapped=func)
#
# You would use update_wrapper directly when:
# 1. You're not using a decorator pattern (e.g., factory functions)
# 2. You need to customize WHICH attributes get copied
# 3. You're building a class-based decorator
#
# =============================================================================


def section_8_update_wrapper() -> None:
    """
    Show update_wrapper for cases where @wraps doesn't fit.

    Relevant for your factory pattern where the inner function
    isn't wrapping another function — it's a new function entirely.
    """
    print("\n" + "=" * 70)
    print("SECTION 8: functools.update_wrapper")
    print("=" * 70)

    # ── @wraps is shorthand for update_wrapper ──────────────────
    # These two are equivalent:
    #
    #   @wraps(original)
    #   def wrapper(...):
    #       ...
    #
    #   def wrapper(...):
    #       ...
    #   update_wrapper(wrapper, original)

    # ── update_wrapper with a class-based decorator ─────────────
    # Sometimes you want a decorator that's a CLASS, not a function.
    # @wraps doesn't work as neatly here — use update_wrapper.

    class CountCalls:
        """Decorator class that counts how many times a function is called."""

        def __init__(self, func: Callable) -> None:
            update_wrapper(self, func)    # Copy func's metadata to self
            self.func = func
            self.count = 0

        def __call__(self, *args: Any, **kwargs: Any) -> Any:
            self.count += 1
            return self.func(*args, **kwargs)

    @CountCalls
    def say_hello(name: str) -> str:
        """Greet someone by name."""
        return f"Hello, {name}!"

    say_hello("Manuel")
    say_hello("World")

    print(f"\n── Class-based decorator with update_wrapper ──")
    print(f"  say_hello.__name__  = {say_hello.__name__!r}")    # 'say_hello' ✅
    print(f"  say_hello.__doc__   = {say_hello.__doc__!r}")      # 'Greet...' ✅
    print(f"  say_hello.count     = {say_hello.count}")           # 2
    print(f"  say_hello.__wrapped__ = {say_hello.__wrapped__!r}") # Original func ✅

    # ── Selective attribute copying ─────────────────────────────
    # update_wrapper has 'assigned' and 'updated' parameters
    # Default assigned: ('__module__', '__name__', '__qualname__',
    #                     '__annotations__', '__doc__')
    # Default updated:  ('__dict__',)
    #
    # You can customize what gets copied:
    print(f"\n── Customizing what gets copied ──")
    print(f"  Default assigned attrs: {update_wrapper.__defaults__}")
    # Shows the FUNCTOOLS_WRAPS_ASSIGNMENTS and FUNCTOOLS_WRAPS_UPDATES


# =============================================================================
# SECTION 9: PRODUCTION PATTERNS — YOUR ROADMAP
# =============================================================================
#
# Pattern 1: Register + Wrap (your BMP filter registry)
# Pattern 2: Retry decorator with @wraps (Stage 2 API calls)
# Pattern 3: Logging decorator preserving signatures
# Pattern 4: Factory + registration + metadata (complete solution)
#
# =============================================================================


def section_9_production_patterns() -> None:
    """
    Real-world patterns combining data model knowledge with functools.

    Each pattern maps to a specific stage in your career roadmap.
    """
    print("\n" + "=" * 70)
    print("SECTION 9: PRODUCTION PATTERNS")
    print("=" * 70)

    # ── Pattern 1: Decorator Registry (your BMP pattern) ────────
    # This is exactly what register_filter does in bmp_filters.py
    REGISTRY: dict[str, Callable] = {}

    def register(func: Callable) -> Callable:
        """Register a function in the dispatch table by its __name__."""
        REGISTRY[func.__name__] = func
        return func  # Return unchanged — register is NOT a wrapper

    @register
    def grayscale(data: list) -> list:
        """Convert to grayscale."""
        return data

    @register
    def blur(data: list) -> list:
        """Apply box blur."""
        return data

    print(f"\n── Pattern 1: Decorator Registry ──")
    print(f"  REGISTRY keys = {list(REGISTRY.keys())}")
    print(f"  grayscale.__name__ = {grayscale.__name__!r}")
    # No @wraps needed here because register() returns the
    # ORIGINAL function unchanged — it's not a wrapper!

    # ── Pattern 2: Factory + Registration (your brightness fix) ─
    def create_brightness(adjustment: int, name: str) -> Callable:
        """
        Create and register a brightness adjustment filter.

        Parameters
        ----------
        adjustment : int
            Pixel value offset (-255 to 255).
        name : str
            Display name for the filter (used in registry and logs).

        Returns
        -------
        Callable
            A filter function with proper __name__ and __qualname__.
        """
        def adjust(data: list) -> list:
            return [max(0, min(255, p + adjustment)) for p in data]

        # Set identity (THE KEY LESSON from this entire reference)
        adjust.__name__ = name
        adjust.__qualname__ = f"create_brightness.<locals>.{name}"
        adjust.__doc__ = f"Adjust pixel brightness by {adjustment} units."
        return adjust

    # Create AND register in one step
    brighten = register(create_brightness(50, "brighten"))
    darken = register(create_brightness(-50, "darken"))

    print(f"\n── Pattern 2: Factory + Registration ──")
    print(f"  REGISTRY keys = {list(REGISTRY.keys())}")
    print(f"  brighten.__name__    = {brighten.__name__!r}")
    print(f"  darken.__name__      = {darken.__name__!r}")
    print(f"  brighten.__doc__     = {brighten.__doc__!r}")

    # ── Pattern 3: Retry Decorator (Stage 2 — API calls) ───────
    # When calling external APIs (Gemini, LangChain), you need retries.
    # @wraps is ESSENTIAL here or debugging becomes impossible.
    import time

    def retry(max_attempts: int = 3, delay: float = 0.1) -> Callable:
        """
        Decorator factory that retries a function on failure.

        Parameters
        ----------
        max_attempts : int
            Maximum number of retry attempts.
        delay : float
            Seconds to wait between retries.

        Returns
        -------
        Callable
            Decorator that wraps the target function with retry logic.
        """
        def decorator(func: Callable) -> Callable:
            @wraps(func)    # ← Preserves func's identity through the wrapper
            def wrapper(*args: Any, **kwargs: Any) -> Any:
                last_error: Exception | None = None
                for attempt in range(1, max_attempts + 1):
                    try:
                        return func(*args, **kwargs)
                    except Exception as e:
                        last_error = e
                        if attempt < max_attempts:
                            time.sleep(delay)
                raise last_error  # type: ignore[misc]
            return wrapper
        return decorator

    # Simulate an unreliable API call
    call_count = 0

    @retry(max_attempts=3, delay=0.01)
    def fetch_data(url: str) -> str:
        """Fetch data from an external API."""
        nonlocal call_count
        call_count += 1
        if call_count < 3:
            raise ConnectionError("Server busy")
        return f"Data from {url}"

    print(f"\n── Pattern 3: Retry Decorator (Stage 2) ──")
    print(f"  fetch_data.__name__  = {fetch_data.__name__!r}")     # 'fetch_data' ✅
    print(f"  fetch_data.__doc__   = {fetch_data.__doc__!r}")       # Preserved ✅
    print(f"  Result: {fetch_data('https://api.example.com')}")
    print(f"  Attempts needed: {call_count}")
    # Without @wraps, debugging "why did 'wrapper' fail?" is painful

    # ── Pattern 4: inspect.signature preservation ───────────────
    # @wraps also preserves the function signature for tools like
    # Sphinx, IDE autocomplete, and inspect.signature()

    print(f"\n── Bonus: Signature preservation ──")
    sig = inspect.signature(fetch_data)
    print(f"  inspect.signature(fetch_data) = {sig}")
    # (url: str) -> str  ← Shows ORIGINAL params, not (*args, **kwargs)


# =============================================================================
# SECTION 10: QUICK REFERENCE CHEAT SHEET
# =============================================================================
#
# ┌─────────────────────────────────────────────────────────────────┐
# │  ATTRIBUTE        │ WHAT IT IS              │ SET BY            │
# │───────────────────│─────────────────────────│───────────────────│
# │ __name__          │ Simple function name     │ def statement     │
# │ __qualname__      │ Full dotted path         │ def statement     │
# │ __doc__           │ Docstring                │ Triple-quote str  │
# │ __module__        │ Defining module          │ Python runtime    │
# │ __annotations__   │ Type hints dict          │ : syntax          │
# │ __defaults__      │ Positional defaults      │ def param=value   │
# │ __kwdefaults__    │ Keyword-only defaults    │ def *, param=val  │
# │ __dict__          │ Custom attributes        │ func.attr = val   │
# │ __closure__       │ Captured variables       │ Closure creation  │
# │ __wrapped__       │ Original function        │ @wraps            │
# │ __code__          │ Bytecode object          │ Compilation       │
# └─────────────────────────────────────────────────────────────────┘
#
# DECISION GUIDE:
# ┌──────────────────────────────────────────────────────────────┐
# │ Need to...                         │ Use                     │
# │────────────────────────────────────│─────────────────────────│
# │ Write a decorator                  │ @wraps(func)            │
# │ Pre-fill arguments                 │ functools.partial()     │
# │ Create variants with custom names  │ Closure + __name__      │
# │ Register functions by name         │ Decorator + __name__    │
# │ Build class-based decorator        │ update_wrapper()        │
# │ Inspect captured closure values    │ __closure__[i].cell_    │
# │                                    │   contents              │
# │ Bypass a decorator (testing)       │ func.__wrapped__()      │
# │ Check function's parameter types   │ __annotations__         │
# │ Get function signature             │ inspect.signature()     │
# └──────────────────────────────────────────────────────────────┘
#
# =============================================================================


# =============================================================================
# MAIN EXECUTION
# =============================================================================

if __name__ == "__main__":
    section_1_functions_are_objects()
    section_2_name_vs_qualname()
    section_3_doc_attribute()
    section_4_other_attributes()
    section_5_closures()
    section_6_functools_wraps()
    section_7_functools_partial()
    section_8_update_wrapper()
    section_9_production_patterns()

    print("\n" + "=" * 70)
    print("REFERENCE COMPLETE — See Section 10 (cheat sheet) in source code")
    print("=" * 70)
