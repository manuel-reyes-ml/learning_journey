"""
Python Import & Execution System — Complete Reference Guide.

A deep-dive into how Python finds, loads, compiles, and executes
modules and packages. Covers the full lifecycle from ``python``
command to running code, including ``sys.modules`` caching,
``__name__`` assignment, bytecode compilation, and the
``__main__.py`` entry point pattern.

This file is structured as a runnable reference — each section
prints demonstrations you can execute to see the behavior live.

Usage
-----
Run the full guide::

    $ python python_import_system_guide.py

Or import specific sections for interactive exploration::

    >>> from 21_python_import_system import demonstrate_sys_modules

Author
------
Manuel Reyes — CS50 / Stage 1 Learning Reference

Version
-------
1.0.0 — March 2026

References
----------
.. [1] Python Docs — The Import System
   https://docs.python.org/3/reference/import.html
.. [2] Python Docs — ``__main__`` — Top-level code environment
   https://docs.python.org/3/library/__main__.html
.. [3] PEP 328 — Imports: Multi-Line and Absolute/Relative
   https://peps.python.org/pep-0328/
.. [4] PEP 302 — New Import Hooks
   https://peps.python.org/pep-0302/
"""

from __future__ import annotations

import sys


# =============================================================================
# SECTION 1: WHAT HAPPENS WHEN YOU RUN `python something.py`
# =============================================================================

def section_1_execution_lifecycle() -> None:
    """
    Explain the complete lifecycle when Python executes a file.

    When you type ``python something.py``, Python performs these
    steps in exact order:

    STEP 1 — INTERPRETER STARTUP
        Python initializes its runtime: sets up memory management,
        creates built-in types (int, str, list), and initializes
        the ``sys`` module with default values.

    STEP 2 — ``sys.path`` CONSTRUCTION
        Python builds the module search path list::

            sys.path = [
                "",                    # Current directory (or script directory)
                "/usr/lib/python3.12", # Standard library
                "/usr/lib/python3.12/lib-dynload",
                "/home/user/.local/lib/python3.12/site-packages",  # pip packages
            ]

        The FIRST entry is always the script's directory (or ""
        for the current working directory if running interactively).

    STEP 3 — COMPILE TO BYTECODE
        Python compiles the .py source into bytecode (.pyc). This is
        an intermediate representation that the Python Virtual Machine
        (PVM) can execute. Cached in ``__pycache__/`` directories::

            something.py  →  __pycache__/something.cpython-312.pyc

        If the .pyc is newer than the .py, Python skips recompilation.

    STEP 4 — ``__name__`` ASSIGNMENT
        THIS IS THE CRITICAL STEP. Python assigns the module's
        ``__name__`` attribute based on HOW the file was invoked:

        - ``python something.py``     → ``__name__ = "__main__"``
        - ``import something``        → ``__name__ = "something"``
        - ``from pkg import something`` → ``__name__ = "pkg.something"``

    STEP 5 — EXECUTE TOP-LEVEL CODE
        Python runs EVERY line at the top level of the file, from
        top to bottom. This includes:
        - Import statements (which trigger their own import cycles)
        - Class and function DEFINITIONS (but not their bodies)
        - Global variable assignments
        - Any bare code (print statements, function calls, etc.)

    STEP 6 — ``sys.modules`` CACHING
        After execution, the module object is stored in
        ``sys.modules["something"]``. Future imports of the same
        module return this cached object WITHOUT re-executing.
    """
    print("=" * 70)
    print("SECTION 1: EXECUTION LIFECYCLE")
    print("=" * 70)
    print("""
    python something.py
        │
        ▼
    ┌─────────────────────────────┐
    │ 1. Interpreter Startup      │  Initialize runtime, built-ins
    └──────────────┬──────────────┘
                   │
                   ▼
    ┌─────────────────────────────┐
    │ 2. Build sys.path           │  Script dir + stdlib + site-packages
    └──────────────┬──────────────┘
                   │
                   ▼
    ┌─────────────────────────────┐
    │ 3. Compile to Bytecode      │  .py → .pyc (cached in __pycache__/)
    └──────────────┬──────────────┘
                   │
                   ▼
    ┌─────────────────────────────┐
    │ 4. Set __name__             │  "__main__" if run directly
    │                             │  "module_name" if imported
    └──────────────┬──────────────┘
                   │
                   ▼
    ┌─────────────────────────────┐
    │ 5. Execute Top-Level Code   │  Every line runs top-to-bottom
    └──────────────┬──────────────┘
                   │
                   ▼
    ┌─────────────────────────────┐
    │ 6. Cache in sys.modules     │  Future imports skip re-execution
    └─────────────────────────────┘
    """)


# =============================================================================
# SECTION 2: THE __name__ VARIABLE
# =============================================================================

def section_2_name_variable() -> None:
    """
    Demonstrate how ``__name__`` changes based on execution context.

    ``__name__`` is Python's way of telling a module HOW it was
    invoked. This is the mechanism behind the famous
    ``if __name__ == "__main__"`` guard.

    Scenario A — Run Directly
        ``python my_module.py``
        Python sets ``__name__ = "__main__"`` because this file
        is the TOP-LEVEL script (the "main" program).

    Scenario B — Imported
        ``import my_module``
        Python sets ``__name__ = "my_module"`` because the file
        is being loaded as a LIBRARY, not as the entry point.

    Scenario C — Inside a Package
        ``from py_src import bmp_filters``
        Python sets ``__name__ = "py_src.bmp_filters"`` — the
        FULLY QUALIFIED dotted name within the package hierarchy.

    Why This Matters for Logging
        In your BMP project, you use ``logging.getLogger(__name__)``.
        When ``bmp_filters.py`` is imported as part of the ``py_src``
        package, ``__name__`` becomes ``"py_src.bmp_filters"``, which
        automatically places it UNDER the ``py_src`` parent logger.
        This is why all child loggers inherit the configuration
        you set up in ``setup_logging()`` on the ``"py_src"`` logger.
    """
    print("=" * 70)
    print("SECTION 2: THE __name__ VARIABLE")
    print("=" * 70)

    # Live demonstration
    print(f"\n  This file's __name__ right now: '{__name__}'")
    print(f"  (If you see '__main__', you ran this file directly)")
    print(f"  (If you see a module name, you imported it)")

    print("""
    ┌─────────────────────────────────────────────────────┐
    │ HOW YOU RUN IT          │ __name__ VALUE             │
    ├─────────────────────────┼────────────────────────────┤
    │ python my_module.py     │ "__main__"                 │
    │ import my_module        │ "my_module"                │
    │ from pkg import mod     │ "pkg.mod"                  │
    │ python -m pkg.mod       │ "__main__"  ← WATCH OUT!   │
    │ python -m pkg           │ "__main__"  (runs __main__.py)│
    └─────────────────────────┴────────────────────────────┘

    YOUR BMP PROJECT LOGGER HIERARCHY:

    logging.getLogger("py_src")             ← package logger (setup_logging)
        ├── logging.getLogger("py_src.bmp_io")      ← child (inherits!)
        ├── logging.getLogger("py_src.bmp_filters")  ← child (inherits!)
        └── logging.getLogger("py_src.bmp_main")     ← child (inherits!)
    """)


# =============================================================================
# SECTION 3: sys.modules — THE IMPORT CACHE
# =============================================================================

def section_3_sys_modules() -> None:
    """
    Demonstrate how ``sys.modules`` prevents double-execution.

    ``sys.modules`` is a dictionary that Python uses as a CACHE
    for all imported modules. The key insight:

        **Python NEVER executes a module twice.**

    When you write ``import os``, Python checks
    ``sys.modules["os"]`` first. If it exists, Python returns
    the cached module object immediately — no file reading, no
    compilation, no execution.

    This is both a feature and the source of the bug you hit:

    The Double-Import Problem (your RuntimeWarning)
        When you ran ``python -m py_src.bmp_main``:

        1. Python sees ``py_src.bmp_main`` → imports ``py_src`` first
        2. ``py_src/__init__.py`` runs → ``from .bmp_main import main``
        3. Now ``py_src.bmp_main`` is in ``sys.modules`` (imported!)
        4. Python then tries to EXECUTE ``bmp_main`` as ``__main__``
        5. CONFLICT: module already in sys.modules but being re-executed

        The fix (``__main__.py``) ensures the entry point and the
        module are DIFFERENT files, so no conflict.
    """
    print("=" * 70)
    print("SECTION 3: sys.modules — THE IMPORT CACHE")
    print("=" * 70)

    # Show some cached modules
    print(f"\n  Total cached modules: {len(sys.modules)}")
    print(f"\n  Sample entries in sys.modules:")

    sample_modules = ["sys", "os", "pathlib", "logging", "__main__"]
    for name in sample_modules:
        if name in sys.modules:
            mod = sys.modules[name]
            file_attr = getattr(mod, "__file__", "built-in")
            print(f"    sys.modules['{name}'] → {file_attr}")

    print("""
    HOW IMPORT CACHING WORKS:

    import os           # FIRST TIME
        │
        ├── Check sys.modules["os"]  → NOT FOUND
        ├── Search sys.path for os.py
        ├── Compile os.py → bytecode
        ├── Execute os.py top-level code
        ├── Store result: sys.modules["os"] = <module 'os'>
        └── Return the module object

    import os           # SECOND TIME (same process)
        │
        ├── Check sys.modules["os"]  → FOUND!
        └── Return cached object immediately (NO re-execution)

    YOUR BUG EXPLAINED:

    python -m py_src.bmp_main
        │
        ├── Step 1: Import package 'py_src'
        │   └── Runs __init__.py → "from .bmp_main import main"
        │       └── bmp_main.py EXECUTES (as import)
        │           └── sys.modules["py_src.bmp_main"] = <module>
        │
        ├── Step 2: Execute py_src.bmp_main as __main__
        │   └── BUT... it's already in sys.modules!
        │   └── RuntimeWarning: found in sys.modules before execution
        │
        FIX: python -m py_src  (uses __main__.py instead)
        │
        ├── Step 1: Import package 'py_src'
        │   └── Runs __init__.py → "from .bmp_main import main"
        │       └── bmp_main.py EXECUTES (as import) ← only once
        │
        ├── Step 2: Execute py_src/__main__.py as __main__
        │   └── __main__.py is a DIFFERENT file ← no conflict!
        │   └── It just calls main() from the already-imported bmp_main
        │
        └── Clean execution, no warning
    """)


# =============================================================================
# SECTION 4: MODULES vs PACKAGES
# =============================================================================

def section_4_modules_vs_packages() -> None:
    """
    Explain the difference between modules and packages.

    Module
        A single ``.py`` file. When imported, becomes an object
        in ``sys.modules``. Can contain functions, classes,
        variables, and executable code.

    Package
        A DIRECTORY containing an ``__init__.py`` file. A package
        is also a module (it gets an entry in ``sys.modules``),
        but it can contain sub-modules and sub-packages.

    Regular Package (what you have)
        A directory with ``__init__.py``. This file runs when the
        package is imported and defines the package's public API.

    Namespace Package (advanced, Python 3.3+)
        A directory WITHOUT ``__init__.py``. Allows splitting a
        package across multiple directories. Rarely used in
        application code.

    Special Files
        ``__init__.py``  — Runs on package import, defines public API
        ``__main__.py``  — Runs when package is invoked with ``-m``
        ``__all__``      — Variable listing public exports
    """
    print("=" * 70)
    print("SECTION 4: MODULES vs PACKAGES")
    print("=" * 70)
    print("""
    MODULE = single .py file
    PACKAGE = directory with __init__.py

    YOUR BMP PROJECT STRUCTURE:

    filter-more/                    ← Project root (BASE_DIR)
    ├── images/                     ← Input BMP files
    └── py_src/                     ← PACKAGE (has __init__.py)
        ├── __init__.py             ← Package definition + public API
        ├── __main__.py             ← Entry point: python -m py_src
        ├── bmp_config.py           ← MODULE: types, constants
        ├── bmp_logger.py           ← MODULE: logging setup
        ├── bmp_filters.py          ← MODULE: filter functions
        ├── bmp_io.py               ← MODULE: read/write BMP
        ├── bmp_main.py             ← MODULE: CLI orchestration
        ├── logs/                   ← Generated log files
        └── filtered_imgs/          ← Generated output images

    IMPORT RESOLUTION ORDER:

    from .bmp_io import read_bmp
         │
         ├── "." means "current package" (py_src/)
         ├── Python looks for py_src/bmp_io.py
         ├── Compiles and executes it
         └── Extracts 'read_bmp' from the module namespace

    WHAT __init__.py DOES:

    # py_src/__init__.py
    from .bmp_main import main    ← Runs when "import py_src" happens
    __all__ = ["main"]            ← Defines: from py_src import *

    This means users can write:
        from py_src import main   ← Clean public API
    Instead of:
        from py_src.bmp_main import main  ← Internal structure exposed
    """)


# =============================================================================
# SECTION 5: IMPORT TYPES — ABSOLUTE vs RELATIVE
# =============================================================================

def section_5_import_types() -> None:
    """
    Explain absolute vs relative imports and when to use each.

    Absolute Import
        Uses the full path from the project root or an installed
        package. Always starts from a top-level package name::

            import py_src.bmp_config
            from py_src.bmp_filters import grayscale

    Relative Import
        Uses dots to navigate relative to the CURRENT module's
        position within the package. Only works INSIDE packages::

            from .bmp_config import Pixel       # Same directory
            from ..utils import helper          # Parent directory

        Single dot (``.``) = current package directory
        Double dot (``..``) = parent package directory

    Rules
        - Relative imports ONLY work inside packages (need __init__.py)
        - A file run as ``__main__`` CANNOT use relative imports
          (because it has no package context — this is another
          reason ``__main__.py`` exists!)
        - PEP 8 recommends absolute imports for clarity, but
          relative imports are fine within a package's own modules
    """
    print("=" * 70)
    print("SECTION 5: ABSOLUTE vs RELATIVE IMPORTS")
    print("=" * 70)
    print("""
    ABSOLUTE IMPORTS (full path from top):

        import os                              # stdlib
        import py_src.bmp_config               # your package
        from py_src.bmp_filters import blur    # specific function

    RELATIVE IMPORTS (dots = navigate from current file):

        from .bmp_config import Pixel          # "." = same directory
        from .bmp_io import read_bmp           # "." = same directory
        from ..utils import helper             # ".." = parent directory

    DOT NOTATION EXPLAINED:

    py_src/
    ├── __init__.py
    ├── bmp_main.py        ← You are HERE
    ├── bmp_config.py
    └── sub_package/
        ├── __init__.py
        └── helper.py

    FROM bmp_main.py:
        from .bmp_config import Pixel     # "." = py_src/ (same level)
        from .sub_package import helper   # "." = py_src/ then into sub

    FROM sub_package/helper.py:
        from ..bmp_config import Pixel    # ".." = up to py_src/
        from . import another_helper      # "." = sub_package/

    WHY YOUR try/except PATTERN EXISTS:

        try:
            from .bmp_config import Pixel   # Works when imported as package
        except ImportError as e:
            sys.exit(f"Error: {e}")         # Fails if run directly

    This catches the case where someone accidentally runs:
        python bmp_filters.py              # No package context!
    Instead of:
        python -m py_src blur -i image.bmp # Correct way
    """)


# =============================================================================
# SECTION 6: THE __main__.py PATTERN
# =============================================================================

def section_6_main_py_pattern() -> None:
    """
    Explain the ``__main__.py`` entry point pattern in detail.

    When you run ``python -m package_name``, Python looks for
    ``package_name/__main__.py`` and executes it as the entry
    point. This is the standard pattern for executable packages.

    Why It Exists
        Without ``__main__.py``, you'd need to run a specific
        module: ``python -m py_src.bmp_main``. But this causes
        the double-import problem because Python must import
        the package first (running ``__init__.py``), and your
        ``__init__.py`` imports from ``bmp_main``.

    The Pattern
        ``__main__.py`` should be THIN — just a trampoline that
        calls the real entry point::

            # py_src/__main__.py
            import sys
            from .bmp_main import main
            sys.exit(main())

    Real-World Examples
        Python's own standard library uses this pattern:
        - ``python -m http.server``  → ``http/__main__.py``
        - ``python -m json.tool``    → ``json/__main__.py``
        - ``python -m pip install``  → ``pip/__main__.py``
        - ``python -m pytest``       → ``pytest/__main__.py``
    """
    print("=" * 70)
    print("SECTION 6: THE __main__.py PATTERN")
    print("=" * 70)
    print("""
    THREE WAYS TO RUN PYTHON CODE:

    1. Run a script directly:
       $ python bmp_main.py
       → __name__ = "__main__"
       → No package context (relative imports FAIL)
       → Uses: if __name__ == "__main__"

    2. Run a MODULE inside a package:
       $ python -m py_src.bmp_main
       → __name__ = "__main__"
       → BUT py_src/__init__.py runs first and imports bmp_main
       → CONFLICT: bmp_main already in sys.modules!
       → RuntimeWarning appears

    3. Run a PACKAGE (the correct way):
       $ python -m py_src
       → Looks for py_src/__main__.py
       → __init__.py runs first (imports bmp_main normally)
       → __main__.py runs as "__main__" (separate file!)
       → NO CONFLICT

    THE FIX — SEPARATION OF CONCERNS:

    ┌─────────────────────────────────────────────────────┐
    │  __main__.py    →  HOW to start (thin trampoline)   │
    │  bmp_main.py    →  WHAT to do (all the logic)       │
    │  __init__.py    →  Public API (from py_src import…)  │
    └─────────────────────────────────────────────────────┘

    # __main__.py (3 lines — intentionally minimal)
    import sys
    from .bmp_main import main
    sys.exit(main())

    # bmp_main.py (all your logic, NO "if __name__" guard)
    def main(argv=None):
        ...
        return ExitCode.SUCCESS

    # __init__.py (public API)
    from .bmp_main import main
    __all__ = ["main"]

    EXECUTION FLOW (clean, no conflicts):

    $ python -m py_src blur -i image.bmp
        │
        ▼
    Python finds py_src/ package
        │
        ├── Runs __init__.py
        │   └── from .bmp_main import main
        │       └── bmp_main.py loads into sys.modules["py_src.bmp_main"]
        │
        ├── Runs __main__.py as "__main__"
        │   └── from .bmp_main import main  ← already cached, no re-exec!
        │   └── sys.exit(main())            ← calls the function
        │
        └── main() runs your CLI pipeline
    """)


# =============================================================================
# SECTION 7: IMPORT ORDER OF EXECUTION
# =============================================================================

def section_7_import_execution_order() -> None:
    """
    Trace the exact execution order for your BMP package.

    When ``python -m py_src blur -i tower.bmp`` runs, here is
    the precise order Python executes code, showing how the
    import chain cascades through your modules.
    """
    print("=" * 70)
    print("SECTION 7: YOUR PACKAGE — EXACT EXECUTION ORDER")
    print("=" * 70)
    print("""
    $ python -m py_src blur -i tower.bmp

    STEP 1: Python finds py_src/ and runs __init__.py
    ──────────────────────────────────────────────────
    __init__.py line: from .bmp_main import main
        │
        └── This triggers import of bmp_main.py...

    STEP 2: bmp_main.py top-level code runs
    ──────────────────────────────────────────────────
    Line 31: from .bmp_io import read_bmp, write_bmp
        │
        └── This triggers import of bmp_io.py...

            STEP 2a: bmp_io.py top-level code runs
            ──────────────────────────────────────
            Line 33: from .bmp_config import (bmp_constants, ...)
                │
                └── This triggers import of bmp_config.py...

                    STEP 2a-i: bmp_config.py top-level code runs
                    ────────────────────────────────────────────
                    - All type aliases defined
                    - All dataclasses defined
                    - bmp_dirs = BmpDirectories() instantiated
                    - bmp_constants = BmpConstants() instantiated
                    - ExitCode, Pixel, etc. defined
                    - ColoredFormatter class defined
                    - Module cached in sys.modules["py_src.bmp_config"]
                    └── DONE, returns to bmp_io.py

            - _padding_calculator defined
            - read_bmp defined
            - write_bmp defined
            - logger = logging.getLogger("py_src.bmp_io")
            - Module cached in sys.modules["py_src.bmp_io"]
            └── DONE, returns to bmp_main.py

    Line 33: from .bmp_logger import setup_logging
        │
        └── bmp_logger.py loads (bmp_config already cached — NOT re-executed)
            - setup_logging defined
            - Module cached in sys.modules["py_src.bmp_logger"]
            └── DONE

    Line 34: from .bmp_config import (DictDispatch, ...)
        │
        └── bmp_config.py already in sys.modules — INSTANT return!

    Line 43: from .bmp_filters import (grayscale, ...)
        │
        └── bmp_filters.py loads
            - from .bmp_config import ... (already cached — instant)
            - grayscale, reflect, blur, edges defined
            - Module cached in sys.modules["py_src.bmp_filters"]
            └── DONE

    Line 71: FUNCS = {"grayscale": grayscale, ...}  ← dict dispatch created
    Line 79: setup_logging()                         ← loggers configured
    Line 83: logger = logging.getLogger("py_src.bmp_main")
    - Module cached in sys.modules["py_src.bmp_main"]
    └── DONE, returns to __init__.py

    STEP 3: __init__.py finishes
    ──────────────────────────────────────────────────
    __all__ = ["main"]  defined
    - Package cached in sys.modules["py_src"]

    STEP 4: __main__.py runs
    ──────────────────────────────────────────────────
    from .bmp_main import main  ← already cached, instant!
    sys.exit(main())            ← YOUR PROGRAM STARTS HERE

    KEY INSIGHT: By the time main() is called, ALL modules
    are already imported, compiled, and cached. The entire
    import chain happens ONCE, in dependency order.
    """)


# =============================================================================
# SECTION 8: COMMON PITFALLS
# =============================================================================

def section_8_common_pitfalls() -> None:
    """
    Document common import mistakes and how to avoid them.
    """
    print("=" * 70)
    print("SECTION 8: COMMON PITFALLS & SOLUTIONS")
    print("=" * 70)
    print("""
    PITFALL 1: CIRCULAR IMPORTS
    ──────────────────────────────────────────────────
    # module_a.py
    from module_b import func_b    # Triggers import of module_b
    def func_a(): ...

    # module_b.py
    from module_a import func_a    # module_a isn't done yet!
    def func_b(): ...              # ImportError: cannot import 'func_a'

    FIX: Move shared types to a config module (what you did with bmp_config!)
    Your architecture already avoids this: bmp_config has NO imports
    from other py_src modules, so it sits at the bottom of the
    dependency chain and can be imported by everyone safely.

    PITFALL 2: RUNNING A PACKAGE MODULE DIRECTLY
    ──────────────────────────────────────────────────
    $ python py_src/bmp_main.py     # WRONG
    → ImportError: attempted relative import with no known parent package

    FIX: Always use -m flag:
    $ python -m py_src              # CORRECT (uses __main__.py)

    PITFALL 3: MODULE-LEVEL SIDE EFFECTS
    ──────────────────────────────────────────────────
    # BAD: This runs every time the module is imported!
    print("Module loaded!")             # Side effect
    connection = connect_to_database()  # Expensive side effect

    # GOOD: Wrap in a function, call explicitly
    def init():
        print("Module loaded!")
        return connect_to_database()

    FIX: Your setup_logging() call at module level in bmp_main.py
    is acceptable because bmp_main is the orchestration module,
    not a library. But if bmp_filters.py had setup_logging() at
    module level, importing it would configure logging as a side
    effect — which is why only bmp_main calls it.

    PITFALL 4: SHADOWING STDLIB MODULES
    ──────────────────────────────────────────────────
    # If you create a file named "logging.py" in your project:
    import logging  # Imports YOUR logging.py, not Python's!

    FIX: Never name your files after stdlib modules.
    Common traps: email.py, test.py, string.py, types.py, io.py

    PITFALL 5: FORGETTING __init__.py
    ──────────────────────────────────────────────────
    py_src/
    ├── bmp_main.py
    └── bmp_config.py      # No __init__.py!

    from py_src import bmp_main  # ImportError: No module named 'py_src'

    FIX: Always include __init__.py in package directories
    (even if empty — though yours has useful content).
    """)


# =============================================================================
# SECTION 9: QUICK REFERENCE TABLE
# =============================================================================

def section_9_quick_reference() -> None:
    """
    Print a quick reference summary of all import concepts.
    """
    print("=" * 70)
    print("SECTION 9: QUICK REFERENCE")
    print("=" * 70)
    print("""
    ┌─────────────────────┬────────────────────────────────────────────┐
    │ CONCEPT             │ WHAT IT DOES                               │
    ├─────────────────────┼────────────────────────────────────────────┤
    │ __name__            │ "__main__" if entry point, else module name│
    │ __init__.py         │ Makes directory a package; runs on import  │
    │ __main__.py         │ Runs when: python -m package_name          │
    │ __all__             │ Controls: from module import *             │
    │ __file__            │ Absolute path to the .py source file       │
    │ __package__         │ Dotted name of the containing package      │
    │ sys.modules         │ Cache dict of all imported modules         │
    │ sys.path            │ List of directories to search for modules  │
    │ __pycache__/        │ Directory storing compiled .pyc bytecode   │
    ├─────────────────────┼────────────────────────────────────────────┤
    │ IMPORT TYPE         │ SYNTAX                                     │
    ├─────────────────────┼────────────────────────────────────────────┤
    │ Absolute            │ from py_src.bmp_config import Pixel        │
    │ Relative (same dir) │ from .bmp_config import Pixel              │
    │ Relative (parent)   │ from ..utils import helper                 │
    │ Wildcard            │ from bmp_config import *  (uses __all__)   │
    ├─────────────────────┼────────────────────────────────────────────┤
    │ EXECUTION           │ COMMAND                                    │
    ├─────────────────────┼────────────────────────────────────────────┤
    │ Run script          │ python script.py                           │
    │ Run module          │ python -m package.module                   │
    │ Run package         │ python -m package  (needs __main__.py)     │
    │ Interactive          │ python → import module                    │
    └─────────────────────┴────────────────────────────────────────────┘

    DEPENDENCY CHAIN FOR YOUR BMP PROJECT:

    bmp_config.py    ← BOTTOM (no internal imports, imported by all)
        ▲
    bmp_logger.py    ← imports bmp_config
        ▲
    bmp_io.py        ← imports bmp_config
        ▲
    bmp_filters.py   ← imports bmp_config
        ▲
    bmp_main.py      ← imports everything above (TOP of chain)
        ▲
    __main__.py      ← imports main from bmp_main (entry point)
    __init__.py      ← imports main from bmp_main (public API)
    """)


# =============================================================================
# MAIN — RUN ALL SECTIONS
# =============================================================================

def main() -> None:
    """
    Run all sections of the import system guide.

    Prints each section sequentially with clear separators.
    Can also be imported and sections called individually::

        >>> from python_import_system_guide import section_3_sys_modules
        >>> section_3_sys_modules()
    """
    sections = [
        section_1_execution_lifecycle,
        section_2_name_variable,
        section_3_sys_modules,
        section_4_modules_vs_packages,
        section_5_import_types,
        section_6_main_py_pattern,
        section_7_import_execution_order,
        section_8_common_pitfalls,
        section_9_quick_reference,
    ]

    print("\n" + "=" * 70)
    print("  PYTHON IMPORT & EXECUTION SYSTEM — COMPLETE REFERENCE")
    print("  Manuel Reyes | CS50 / Stage 1 Learning Reference")
    print("=" * 70)

    for section_func in sections:
        print()
        section_func()

    print("\n" + "=" * 70)
    print("  END OF GUIDE — Save this file for future reference!")
    print("  Run: python python_import_system_guide.py")
    print("  Or:  from python_import_system_guide import section_3_sys_modules")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()