"""
python_recursion_reference.py
==============================

Personal reference: Recursive functions in Python — how they work,
when to use them, and production-grade patterns.

Topics covered
--------------
1. What is recursion — the mental model
2. The two required parts — base case + recursive case
3. The call stack — how Python tracks recursive calls
4. Counting patterns — simple countdown and countup
5. Accumulating patterns — sum, factorial, fibonacci
6. Tree recursion — binary trees and family trees
7. Timing recursive functions — the public/private split
8. Recursion vs iteration — when to use which
9. Common pitfalls and gotchas
10. Production patterns from your roadmap

Why this matters for your roadmap
----------------------------------
- Stage 1: Your CS50 Inheritance project uses recursion to build
  a family tree (create_family) and to traverse it (print_family).
  Your free_family equivalent demonstrates recursive cleanup.
  Tree traversal is a fundamental CS50 concept you'll need for
  all future data structure work.
- Stage 2: Directory traversal (os.walk, pathlib.rglob), JSON/XML
  parsing of nested data, and recursive SQL CTEs (Common Table
  Expressions) all use recursive thinking. Airflow DAG dependency
  resolution is inherently recursive.
- Stage 3: Decision trees (Random Forest, XGBoost) are built using
  recursive splitting. Divide-and-conquer algorithms (merge sort,
  quicksort) are recursive. Backtracking algorithms for optimization.
- Stage 4-5: LangGraph agent loops, recursive RAG (query refinement),
  recursive summarization of long documents, and tree-of-thought
  prompting all leverage recursive patterns.

How to use this file
---------------------
Run it directly to see all output::

    $ python 25_python_recursion_reference.py

Or import individual sections to experiment in a REPL.

References
----------
.. [1] Python docs — Recursion limit: https://docs.python.org/3/library/sys.html#sys.setrecursionlimit
.. [2] CS50 Week 5 — Data Structures: https://cs50.harvard.edu/x/psets/5/inheritance/
.. [3] Real Python — Thinking Recursively: https://realpython.com/python-thinking-recursively/
.. [4] Fluent Python, Ch. 17 — Iterators & Generators (Ramalho)
"""

from __future__ import annotations

from dataclasses import dataclass, field
from functools import wraps, lru_cache
from typing import Any, Callable, Final
import random
import time
import sys


# =============================================================================
# SECTION 1: WHAT IS RECURSION — THE MENTAL MODEL
# =============================================================================
#
# Recursion is when a function CALLS ITSELF with a smaller version of
# the same problem, until it hits a case so simple it can answer
# without calling itself again.
#
# MENTAL MODEL — Russian Nesting Dolls:
# ┌──────────────────────────────────────────────────────────────────┐
# │                                                                  │
# │  Think of recursion like opening Russian nesting dolls:          │
# │                                                                  │
# │  ┌─────────────────────────────────────────────┐                │
# │  │ Open doll 5 (biggest)                       │                │
# │  │  ┌────────────────────────────────────────┐ │                │
# │  │  │ Open doll 4                            │ │                │
# │  │  │  ┌─────────────────────────────────┐   │ │                │
# │  │  │  │ Open doll 3                     │   │ │                │
# │  │  │  │  ┌──────────────────────────┐   │   │ │                │
# │  │  │  │  │ Open doll 2              │   │   │ │                │
# │  │  │  │  │  ┌───────────────────┐   │   │   │ │                │
# │  │  │  │  │  │ Doll 1 (SOLID!)   │   │   │   │ │                │
# │  │  │  │  │  │ BASE CASE — STOP  │   │   │   │ │                │
# │  │  │  │  │  └───────────────────┘   │   │   │ │                │
# │  │  │  │  └──────────────────────────┘   │   │ │                │
# │  │  │  └─────────────────────────────────┘   │ │                │
# │  │  └────────────────────────────────────────┘ │                │
# │  └─────────────────────────────────────────────┘                │
# │                                                                  │
# │  You keep opening dolls (recursive calls) until you reach       │
# │  the smallest one (base case), then you close them back         │
# │  up (return values back up the chain).                          │
# └──────────────────────────────────────────────────────────────────┘
#
# KEY TERMS:
#   BASE CASE     — the simplest version of the problem that can
#                   be solved directly without further recursion
#   RECURSIVE CASE — breaks the problem into a SMALLER version
#                    and calls itself with that smaller input
#   CALL STACK    — Python's memory structure that tracks which
#                   function is currently running and what to
#                   return to when it finishes
#
# =============================================================================


def section_1_what_is_recursion() -> None:
    """
    Demonstrate the simplest possible recursive function and
    compare it to its iterative equivalent.
    """
    print("=" * 70)
    print("SECTION 1: WHAT IS RECURSION — THE MENTAL MODEL")
    print("=" * 70)

    # ── Simplest recursion: countdown ────────────────────────────
    def countdown(n: int) -> None:
        """Count down from n to 1, then print 'Done!'"""
        # BASE CASE — the recursion STOPS here
        if n == 0:
            print("    Done!")
            return

        # DO WORK at this level
        print(f"    {n}")

        # RECURSIVE CASE — call yourself with SMALLER input
        countdown(n - 1)

    print("\n── Recursive countdown ──")
    countdown(5)

    # ── Same thing iteratively (for comparison) ──────────────────
    print("\n── Iterative equivalent ──")
    for i in range(5, 0, -1):
        print(f"    {i}")
    print("    Done!")

    print("\n── Key insight ──")
    print(f"  Both produce the same output, but the recursive version")
    print(f"  doesn't need a loop variable — the function parameter")
    print(f"  'n' shrinks by 1 each call, acting as the counter.")


# =============================================================================
# SECTION 2: THE TWO REQUIRED PARTS
# =============================================================================
#
# Every recursive function MUST have both parts:
#
# ┌──────────────────────────────────────────────────────────────────┐
# │                                                                  │
# │  def recursive_function(problem):                                │
# │                                                                  │
# │      # 1. BASE CASE — when to STOP                              │
# │      if problem is simple enough:                                │
# │          return answer directly                                  │
# │                                                                  │
# │      # 2. RECURSIVE CASE — break it down                        │
# │      smaller_problem = make_problem_smaller(problem)             │
# │      return recursive_function(smaller_problem)                  │
# │                                                                  │
# │  WITHOUT base case → RecursionError (infinite calls)             │
# │  WITHOUT recursive case → just a regular function                │
# │  WITHOUT shrinkage → RecursionError (never reaches base case)    │
# │                                                                  │
# └──────────────────────────────────────────────────────────────────┘
#
# THE SHRINKAGE RULE:
# Every recursive call MUST make the problem SMALLER in some way.
# If the input doesn't shrink, you'll never reach the base case.
#
#   countdown(5) → countdown(4) → countdown(3) → ... → countdown(0)  ✅
#   countdown(5) → countdown(5) → countdown(5) → ...  (INFINITE!)    ❌
#
# =============================================================================


def section_2_two_required_parts() -> None:
    """
    Show what happens with and without proper base cases.

    Demonstrates the three failure modes: no base case,
    no shrinkage, and base case that's never reached.
    """
    print("\n" + "=" * 70)
    print("SECTION 2: THE TWO REQUIRED PARTS")
    print("=" * 70)

    # ── Correct: both parts present ──────────────────────────────
    def sum_to(n: int) -> int:
        """Sum integers from 1 to n using recursion."""
        if n == 1:           # BASE CASE: simplest problem
            return 1
        return n + sum_to(n - 1)  # RECURSIVE: n + sum of rest

    print("\n── Correct recursion: sum_to(5) ──")
    print(f"  sum_to(5) = 5 + 4 + 3 + 2 + 1 = {sum_to(5)}")

    # ── Trace the calls step by step ─────────────────────────────
    print("\n── Trace (unwinding the calls) ──")
    print(f"  sum_to(5)")
    print(f"    = 5 + sum_to(4)")
    print(f"    = 5 + (4 + sum_to(3))")
    print(f"    = 5 + (4 + (3 + sum_to(2)))")
    print(f"    = 5 + (4 + (3 + (2 + sum_to(1))))")
    print(f"    = 5 + (4 + (3 + (2 + 1)))          ← base case hit!")
    print(f"    = 5 + (4 + (3 + 3))")
    print(f"    = 5 + (4 + 6)")
    print(f"    = 5 + 10")
    print(f"    = 15")

    # ── What happens without a base case ─────────────────────────
    print("\n── Without base case (DON'T RUN — just for illustration) ──")
    print(f"  def broken(n):          # No base case!")
    print(f"      return n + broken(n - 1)")
    print(f"  broken(5) → broken(4) → broken(3) → ... → broken(-9999)")
    print(f"  RecursionError: maximum recursion depth exceeded")
    print(f"  Python's default limit: {sys.getrecursionlimit()} calls")

    # ── "Trust the recursion" rule ───────────────────────────────
    print("\n── The 'trust the recursion' rule ──")
    print(f"  When writing sum_to(n), ASSUME sum_to(n-1) works.")
    print(f"  Don't trace every level mentally — just trust that")
    print(f"  the function correctly handles smaller inputs, and")
    print(f"  focus on what the CURRENT level needs to do.")


# =============================================================================
# SECTION 3: THE CALL STACK — HOW PYTHON TRACKS CALLS
# =============================================================================
#
# When Python calls a function, it creates a STACK FRAME that stores:
#   - The function name
#   - The values of all local variables
#   - Where to return to when the function finishes
#
# Recursive calls CREATE NEW FRAMES on top of the stack:
#
# ┌──────────────────────────────────────────────────────────────────┐
# │                                                                  │
# │  factorial(4) creates this call stack:                           │
# │                                                                  │
# │  CALL PHASE (building up):        RETURN PHASE (unwinding):     │
# │                                                                  │
# │  ┌──────────────────┐             ┌──────────────────┐          │
# │  │ factorial(1) = 1 │  ←base      │ factorial(1) = 1 │ → 1     │
# │  ├──────────────────┤             ├──────────────────┤          │
# │  │ factorial(2) = ? │             │ factorial(2) = 2 │ → 2*1=2 │
# │  ├──────────────────┤             ├──────────────────┤          │
# │  │ factorial(3) = ? │             │ factorial(3) = 6 │ → 3*2=6 │
# │  ├──────────────────┤             ├──────────────────┤          │
# │  │ factorial(4) = ? │  ←start     │ factorial(4) =24 │ → 4*6=24│
# │  └──────────────────┘             └──────────────────┘          │
# │                                                                  │
# │  Stack grows UP during calls, then shrinks DOWN during returns. │
# │  Each frame is independent — factorial(3)'s 'n' is 3, while    │
# │  factorial(2)'s 'n' is 2. They don't share variables.          │
# └──────────────────────────────────────────────────────────────────┘
#
# =============================================================================


def section_3_call_stack() -> None:
    """
    Visualize the call stack with a traced recursive function.

    Uses indentation to show stack depth, making the push/pop
    behavior visible.
    """
    print("\n" + "=" * 70)
    print("SECTION 3: THE CALL STACK — HOW PYTHON TRACKS CALLS")
    print("=" * 70)

    # ── Traced factorial — shows the stack visually ──────────────
    def factorial_traced(n: int, depth: int = 0) -> int:
        """Factorial with visual call stack tracing."""
        indent = "  " * depth
        print(f"  {indent}→ factorial({n}) called")

        if n <= 1:
            print(f"  {indent}← factorial({n}) returns 1  [BASE CASE]")
            return 1

        result = n * factorial_traced(n - 1, depth + 1)
        print(f"  {indent}← factorial({n}) returns {result}")
        return result

    print("\n── Traced factorial(5) — watch the stack ──")
    answer = factorial_traced(5)
    print(f"\n  Final answer: {answer}")

    # ── Stack depth = number of recursive calls ──────────────────
    print("\n── Stack depth matters ──")
    print(f"  Python's recursion limit: {sys.getrecursionlimit()}")
    print(f"  factorial(5):    depth 5   (fine)")
    print(f"  factorial(100):  depth 100 (fine)")
    print(f"  factorial(1000): depth 1000 (gets close to limit!)")
    print(f"  factorial(10000): RecursionError!")
    print(f"  This is why deep recursion needs iteration instead.")


# =============================================================================
# SECTION 4: COUNTING PATTERNS
# =============================================================================


def section_4_counting_patterns() -> None:
    """
    Show the fundamental counting-based recursive patterns.

    These are the building blocks for more complex recursion.
    """
    print("\n" + "=" * 70)
    print("SECTION 4: COUNTING PATTERNS")
    print("=" * 70)

    # ── Pattern 1: Countdown (shrink to base) ────────────────────
    def countdown_list(n: int) -> list[int]:
        """Return [n, n-1, ..., 1] using recursion."""
        if n == 0:
            return []
        return [n] + countdown_list(n - 1)

    print("\n── Countdown (parameter shrinks) ──")
    print(f"  countdown_list(5): {countdown_list(5)}")

    # ── Pattern 2: Countup (build from base) ─────────────────────
    def countup_list(n: int) -> list[int]:
        """Return [1, 2, ..., n] using recursion."""
        if n == 0:
            return []
        return countup_list(n - 1) + [n]
        # Notice: recursive call FIRST, then append current
        # This reverses the order compared to countdown

    print("\n── Countup (build from base upward) ──")
    print(f"  countup_list(5): {countup_list(5)}")

    # ── Pattern 3: Repeat n times ────────────────────────────────
    def repeat(value: str, n: int) -> str:
        """Repeat a value n times using recursion."""
        if n == 0:
            return ""
        return value + repeat(value, n - 1)

    print("\n── Repeat pattern ──")
    print(f"  repeat('Ha', 3):    '{repeat('Ha', 3)}'")
    print(f"  repeat('Great-', 2): '{repeat('Great-', 2)}'")
    print(f"  ^ This is exactly how your Inheritance label works!")


# =============================================================================
# SECTION 5: ACCUMULATING PATTERNS
# =============================================================================


def section_5_accumulating() -> None:
    """
    Show recursive accumulation: combining results as calls return.
    """
    print("\n" + "=" * 70)
    print("SECTION 5: ACCUMULATING PATTERNS")
    print("=" * 70)

    # ── Sum of a list ────────────────────────────────────────────
    def recursive_sum(items: list[int]) -> int:
        """Sum a list recursively."""
        if not items:           # Empty list — base case
            return 0
        return items[0] + recursive_sum(items[1:])
        # Take first item + sum of the rest

    print("\n── Recursive sum ──")
    data = [10, 20, 30, 40, 50]
    print(f"  recursive_sum({data}): {recursive_sum(data)}")

    # ── Fibonacci (classic but SLOW) ─────────────────────────────
    def fibonacci(n: int) -> int:
        """Nth Fibonacci number (naive recursive — exponential time!)."""
        if n <= 1:
            return n
        return fibonacci(n - 1) + fibonacci(n - 2)

    print("\n── Fibonacci (naive — O(2^n) — DON'T use in production) ──")
    for i in range(10):
        print(f"  fib({i}) = {fibonacci(i)}", end="  ")
    print()

    # ── Fibonacci with memoization (FAST) ────────────────────────
    @lru_cache(maxsize=None)
    def fibonacci_fast(n: int) -> int:
        """Nth Fibonacci with memoization — O(n) time."""
        if n <= 1:
            return n
        return fibonacci_fast(n - 1) + fibonacci_fast(n - 2)

    print("\n── Fibonacci with @lru_cache (O(n) — production ready) ──")
    print(f"  fib(50) = {fibonacci_fast(50)}")
    print(f"  Cache info: {fibonacci_fast.cache_info()}")
    print(f"  Without cache, fib(50) would take ~113 TRILLION operations!")

    # ── String reversal ──────────────────────────────────────────
    def reverse_string(s: str) -> str:
        """Reverse a string recursively."""
        if len(s) <= 1:
            return s
        return reverse_string(s[1:]) + s[0]

    print(f"\n── String reversal ──")
    print(f"  reverse('hello'): '{reverse_string('hello')}'")
    print(f"  reverse('ABO'):   '{reverse_string('ABO')}'")


# =============================================================================
# SECTION 6: TREE RECURSION — BINARY TREES AND FAMILY TREES
# =============================================================================
#
# Tree recursion is when a function makes TWO (or more) recursive
# calls per invocation. This creates a tree-shaped call pattern.
#
# YOUR INHERITANCE PROJECT is tree recursion:
# ┌──────────────────────────────────────────────────────────────────┐
# │                                                                  │
# │  create_family(3) — builds a binary tree:                        │
# │                                                                  │
# │              create_family(3)     ← CHILD                       │
# │              /                \                                   │
# │      create_family(2)   create_family(2)   ← PARENTS            │
# │       /          \        /          \                            │
# │    cf(1)       cf(1)   cf(1)       cf(1)   ← GRANDPARENTS       │
# │   (base)      (base)  (base)      (base)     (4 base cases)     │
# │                                                                  │
# │  Total calls: 2^0 + 2^1 + 2^2 = 1 + 2 + 4 = 7                 │
# │  General formula: 2^generations - 1                              │
# │                                                                  │
# │  The tree BUILDS from leaves up (grandparents first).           │
# │  But PRINTS from root down (child first).                       │
# └──────────────────────────────────────────────────────────────────┘
#
# =============================================================================

# -- Data structures for family tree demonstration --

ALLELES: Final[tuple[str, ...]] = ("A", "B", "O")


@dataclass
class Person:
    """A person in a family tree with blood type alleles."""
    parents: list[Person | None] = field(default_factory=lambda: [None, None])
    alleles: tuple[str, ...] = field(default_factory=tuple)


def section_6_tree_recursion() -> None:
    """
    Demonstrate tree recursion with the family tree pattern.

    This is the exact pattern from your CS50 Inheritance project,
    simplified for teaching purposes.
    """
    print("\n" + "=" * 70)
    print("SECTION 6: TREE RECURSION — BINARY TREES AND FAMILY TREES")
    print("=" * 70)

    # ── The family tree builder (your Inheritance pattern) ───────
    random.seed(42)  # Deterministic for demonstration

    def build_person(generations: int) -> Person:
        """
        Recursively build a family tree.

        Base case (generations == 1): Oldest generation gets random alleles.
        Recursive case: Create two parents, then inherit from them.
        """
        person = Person()

        if generations == 1:
            # BASE CASE: oldest generation — random alleles
            person.alleles = (random.choice(ALLELES), random.choice(ALLELES))
        else:
            # RECURSIVE CASE: this person has parents
            parent_0 = build_person(generations - 1)  # ← first recursive call
            parent_1 = build_person(generations - 1)  # ← second recursive call
            person.parents = [parent_0, parent_1]
            person.alleles = (
                random.choice(parent_0.alleles),
                random.choice(parent_1.alleles),
            )

        return person

    # ── The family tree printer (your print_family pattern) ──────
    def print_person(person: Person | None, generation: int = 0) -> None:
        """
        Recursively print a family tree with indentation.

        Base case: person is None (no more ancestors).
        Recursive case: print this person, then recurse into parents.
        """
        if person is None:
            return

        indent = "  " * (generation * 2)

        # Determine label based on generation depth
        if generation == 0:
            label = "Child"
        elif generation == 1:
            label = "Parent"
        else:
            label = "Great-" * (generation - 2) + "Grandparent"

        allele_str = "".join(person.alleles)
        print(f"  {indent}{label} (Gen {generation}): blood type {allele_str}")

        # Two recursive calls — one for each parent
        print_person(person.parents[0], generation + 1)
        print_person(person.parents[1], generation + 1)

    print("\n── Building family tree (3 generations) ──")
    family = build_person(3)
    print_person(family)

    # ── Counting nodes in a tree ─────────────────────────────────
    def count_people(person: Person | None) -> int:
        """Count all people in a family tree recursively."""
        if person is None:
            return 0
        return 1 + count_people(person.parents[0]) + count_people(person.parents[1])

    print(f"\n── Tree statistics ──")
    print(f"  Total people: {count_people(family)}")
    print(f"  Formula: 2^3 - 1 = {2**3 - 1}")

    # ── Two directions of tree recursion ─────────────────────────
    print(f"\n── Two directions of tree recursion ──")
    print(f"  BUILD:  create_family counts DOWN  (3 → 2 → 1)")
    print(f"          Builds from LEAVES up (grandparents first)")
    print(f"  PRINT:  print_family counts UP    (0 → 1 → 2)")
    print(f"          Prints from ROOT down (child first)")
    print(f"  Same structure, opposite traversal directions.")


# =============================================================================
# SECTION 7: TIMING RECURSIVE FUNCTIONS
# =============================================================================
#
# PROBLEM: If you decorate a recursive function with @timer,
# EVERY recursive call gets timed individually:
#
# ┌──────────────────────────────────────────────────────────────────┐
# │                                                                  │
# │  @timer                                                          │
# │  def build_person(generations):                                  │
# │      ...                                                         │
# │      parent_0 = build_person(generations - 1)  ← timer fires!  │
# │      parent_1 = build_person(generations - 1)  ← timer fires!  │
# │                                                                  │
# │  Output: 7 timing messages for 3 generations (one per person)   │
# │                                                                  │
# │  SOLUTION: Public/private split pattern                          │
# │                                                                  │
# │  @timer                                                          │
# │  def create_family(generations):    ← timed ONCE                │
# │      return _build_person(generations)                           │
# │                                                                  │
# │  def _build_person(generations):    ← recursive, NOT timed      │
# │      ...                                                         │
# │      parent_0 = _build_person(generations - 1)  ← no timer     │
# │                                                                  │
# │  Output: 1 timing message (total time for entire tree)          │
# └──────────────────────────────────────────────────────────────────┘
#
# =============================================================================


def section_7_timing() -> None:
    """
    Demonstrate the public/private split pattern for timing
    recursive functions. This is the exact pattern used in
    your Inheritance project.
    """
    print("\n" + "=" * 70)
    print("SECTION 7: TIMING RECURSIVE FUNCTIONS")
    print("=" * 70)

    # ── Simple timer decorator ───────────────────────────────────
    def timer(func: Callable) -> Callable:
        """Measure execution time of a function."""
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            start = time.perf_counter()
            result = func(*args, **kwargs)
            elapsed = time.perf_counter() - start
            print(f"    {func.__name__} took {elapsed:.6f}s")
            return result
        return wrapper

    # ── BAD: timer on recursive function ─────────────────────────
    call_count = 0

    @timer
    def factorial_timed_bad(n: int) -> int:
        """Each recursive call triggers the timer."""
        nonlocal call_count
        call_count += 1
        if n <= 1:
            return 1
        return n * factorial_timed_bad(n - 1)

    print("\n── BAD: @timer on recursive function ──")
    call_count = 0
    factorial_timed_bad(5)
    print(f"  Timer fired {call_count} times! (one per recursive call)")

    # ── GOOD: public/private split ───────────────────────────────
    def _factorial_worker(n: int) -> int:
        """Private recursive worker — no timer overhead."""
        if n <= 1:
            return 1
        return n * _factorial_worker(n - 1)

    @timer
    def factorial_timed_good(n: int) -> int:
        """Public entry point — timed once."""
        return _factorial_worker(n)

    print("\n── GOOD: Public/private split pattern ──")
    result = factorial_timed_good(5)
    print(f"  Result: {result}")
    print(f"  Timer fired exactly ONCE (total time for all recursion)")

    # ── Your Inheritance project uses this exact pattern ─────────
    print("\n── Your Inheritance project pattern ──")
    print(f"  @timer")
    print(f"  def create_family(generations):    ← public, timed once")
    print(f"      return _build_person(generations)")
    print(f"")
    print(f"  def _build_person(generations):    ← private, recursive")
    print(f"      ...recursive logic here...")


# =============================================================================
# SECTION 8: RECURSION VS ITERATION
# =============================================================================
#
# WHEN TO USE RECURSION:
# ┌──────────────────────────────────────────────────────────────────┐
# │  Use recursion when:                                             │
# │  ✅ The problem has a natural TREE structure                     │
# │  ✅ The problem is defined recursively (factorial, Fibonacci)    │
# │  ✅ You're traversing nested data (JSON, XML, file trees)       │
# │  ✅ The code is cleaner/clearer than iteration                  │
# │                                                                  │
# │  Use iteration when:                                             │
# │  ✅ The problem is FLAT (processing a list sequentially)         │
# │  ✅ Depth could exceed ~1000 (Python's recursion limit)         │
# │  ✅ Performance is critical (function call overhead)             │
# │  ✅ You're just counting or accumulating a single value          │
# └──────────────────────────────────────────────────────────────────┘
#
# =============================================================================


def section_8_recursion_vs_iteration() -> None:
    """
    Compare recursive and iterative solutions side by side.

    Shows when each approach is preferable.
    """
    print("\n" + "=" * 70)
    print("SECTION 8: RECURSION VS ITERATION")
    print("=" * 70)

    # ── Side-by-side: factorial ──────────────────────────────────
    def factorial_recursive(n: int) -> int:
        if n <= 1:
            return 1
        return n * factorial_recursive(n - 1)

    def factorial_iterative(n: int) -> int:
        result = 1
        for i in range(2, n + 1):
            result *= i
        return result

    print("\n── Factorial: recursive vs iterative ──")
    print(f"  Recursive: {factorial_recursive(10)}")
    print(f"  Iterative: {factorial_iterative(10)}")
    print(f"  For flat accumulation → iterative is simpler")

    # ── Side-by-side: flatten nested list ────────────────────────
    def flatten_recursive(nested: list) -> list:
        """Flatten arbitrarily nested lists."""
        result = []
        for item in nested:
            if isinstance(item, list):
                result.extend(flatten_recursive(item))  # ← recurse
            else:
                result.append(item)
        return result

    nested = [1, [2, [3, 4], 5], [6, 7], 8]
    print(f"\n── Flatten nested list: recursion WINS ──")
    print(f"  Input:  {nested}")
    print(f"  Output: {flatten_recursive(nested)}")
    print(f"  Iterative version would need a manual stack — messier.")

    # ── Side-by-side: directory traversal ────────────────────────
    print(f"\n── Directory traversal (Stage 2 pattern) ──")
    print(f"  Recursive: natural fit — directories contain directories")
    print(f"  Python's os.walk() and pathlib.rglob() use recursion")
    print(f"  internally, even though they expose iterative APIs.")

    # ── The decision table ───────────────────────────────────────
    print(f"\n── Decision table ──")
    print(f"  ┌────────────────────────────┬─────────────────────┐")
    print(f"  │ Problem type               │ Prefer              │")
    print(f"  ├────────────────────────────┼─────────────────────┤")
    print(f"  │ Family tree / binary tree   │ Recursion           │")
    print(f"  │ Nested JSON/XML             │ Recursion           │")
    print(f"  │ File system traversal       │ Recursion           │")
    print(f"  │ Sum/count a flat list       │ Iteration (for loop)│")
    print(f"  │ Process rows in DataFrame   │ Vectorized (pandas) │")
    print(f"  │ Very deep structures (>1K)  │ Iteration + stack   │")
    print(f"  └────────────────────────────┴─────────────────────┘")


# =============================================================================
# SECTION 9: COMMON PITFALLS AND GOTCHAS
# =============================================================================


def section_9_pitfalls() -> None:
    """
    Show the most common recursion bugs and how to avoid them.
    """
    print("\n" + "=" * 70)
    print("SECTION 9: COMMON PITFALLS AND GOTCHAS")
    print("=" * 70)

    # ── Pitfall 1: Forgetting the base case ──────────────────────
    print("\n── Pitfall 1: Missing or unreachable base case ──")
    print(f"  def broken(n):              ← no base case!")
    print(f"      return n + broken(n-1)  ← calls forever")
    print(f"  Fix: ALWAYS write the base case FIRST, test it, then")
    print(f"  add the recursive case.")

    # ── Pitfall 2: Base case never reached ───────────────────────
    print(f"\n── Pitfall 2: Input doesn't shrink ──")
    print(f"  def broken(n):       ← n never changes!")
    print(f"      if n == 0:")
    print(f"          return 0")
    print(f"      return broken(n)  ← same n forever")
    print(f"  Fix: Ensure EVERY recursive call passes a SMALLER input.")

    # ── Pitfall 3: Modifying shared mutable state ────────────────
    print(f"\n── Pitfall 3: Mutating shared state ──")
    shared_list: list[int] = []

    def bad_collect(n: int) -> None:
        """Mutates a shared list — all calls see same list."""
        if n == 0:
            return
        shared_list.append(n)  # Shared state — risky
        bad_collect(n - 1)

    bad_collect(3)
    print(f"  Shared list after bad_collect(3): {shared_list}")
    print(f"  Fix: Return new values instead of mutating shared state.")
    print(f"  Each recursive call should be independent.")

    # ── Pitfall 4: Stack overflow on deep recursion ──────────────
    print(f"\n── Pitfall 4: Exceeding recursion limit ──")
    print(f"  Python default limit: {sys.getrecursionlimit()}")
    print(f"  Your family tree with 3 generations: 7 calls (fine)")
    print(f"  A family tree with 12 generations: 4095 calls (CRASH)")
    print(f"  Fix: For deep structures, convert to iteration with")
    print(f"  an explicit stack (list used as LIFO).")

    # ── Pitfall 5: Exponential time without memoization ──────────
    print(f"\n── Pitfall 5: Exponential time (duplicate work) ──")
    print(f"  Naive fibonacci(30) makes ~2.7 BILLION calls")
    print(f"  fibonacci(50) would take ~36 YEARS on a laptop")
    print(f"  Fix: Use @lru_cache to memoize (cache results).")
    print(f"  Or convert to iterative with two variables.")

    # ── Pitfall 6: Decorating recursive functions ────────────────
    print(f"\n── Pitfall 6: @timer on a recursive function ──")
    print(f"  @timer fires on EVERY recursive call, not just once.")
    print(f"  Fix: Public/private split pattern (Section 7).")
    print(f"  Your Inheritance project already does this correctly!")


# =============================================================================
# SECTION 10: PRODUCTION PATTERNS FROM YOUR ROADMAP
# =============================================================================


def section_10_production_patterns() -> None:
    """
    Real-world recursive patterns directly applicable to your projects.
    """
    print("\n" + "=" * 70)
    print("SECTION 10: PRODUCTION PATTERNS — YOUR ROADMAP")
    print("=" * 70)

    # ── Pattern 1: Recursive data cleanup (Inheritance) ──────────
    print("\n── Pattern 1: Recursive cleanup (Stage 1 — Inheritance) ──")
    print(f"  In C: free_family() recursively frees malloc'd memory")
    print(f"  In Python: garbage collector handles this, but the")
    print(f"  pattern teaches you recursive traversal + cleanup:")

    def free_family(person: Person | None) -> int:
        """Recursively 'free' a family tree. Returns count freed."""
        if person is None:
            return 0
        # Free children (parents) BEFORE freeing the parent
        count = free_family(person.parents[0])
        count += free_family(person.parents[1])
        person.parents = [None, None]
        person.alleles = ()
        return count + 1

    random.seed(42)
    family = Person()
    family.alleles = ("A", "O")  # Minimal tree for demo
    freed = free_family(family)
    print(f"  Freed {freed} person(s)")

    # ── Pattern 2: Nested JSON traversal (Stage 2) ───────────────
    print(f"\n── Pattern 2: Nested JSON traversal (Stage 2 — ETL) ──")

    def find_keys(data: dict | list | Any, target_key: str) -> list:
        """Recursively find all values for a key in nested JSON."""
        results = []
        if isinstance(data, dict):
            for key, value in data.items():
                if key == target_key:
                    results.append(value)
                results.extend(find_keys(value, target_key))
        elif isinstance(data, list):
            for item in data:
                results.extend(find_keys(item, target_key))
        return results

    nested_json = {
        "name": "Root",
        "children": [
            {"name": "Child 1", "children": [{"name": "Grandchild"}]},
            {"name": "Child 2"},
        ],
    }
    names = find_keys(nested_json, "name")
    print(f"  All 'name' values: {names}")

    # ── Pattern 3: Recursive SQL CTE concept (Stage 2) ──────────
    print(f"\n── Pattern 3: Recursive SQL CTEs (Stage 2 — SQL) ──")
    print(f"  WITH RECURSIVE org_chart AS (")
    print(f"      SELECT id, name, manager_id   -- base case")
    print(f"      FROM employees WHERE manager_id IS NULL")
    print(f"      UNION ALL")
    print(f"      SELECT e.id, e.name, e.manager_id  -- recursive case")
    print(f"      FROM employees e JOIN org_chart o ON e.manager_id = o.id")
    print(f"  )")
    print(f"  Same pattern: base case + recursive case + shrinkage!")

    # ── Pattern 4: Tree-of-thought (Stage 4) ─────────────────────
    print(f"\n── Pattern 4: Tree-of-Thought prompting (Stage 4 — LLM) ──")
    print(f"  LLM explores multiple reasoning paths recursively:")
    print(f"  1. Generate N candidate thoughts (branches)")
    print(f"  2. Evaluate each branch (score)")
    print(f"  3. Recurse deeper on the best branches")
    print(f"  4. Base case: reached max depth or found answer")
    print(f"  Same tree recursion as your family tree!")


# =============================================================================
# SECTION 11: QUICK REFERENCE CHEAT SHEET
# =============================================================================
#
# ┌─────────────────────────────────────────────────────────────────┐
# │                   RECURSION TEMPLATE                            │
# │─────────────────────────────────────────────────────────────────│
# │  def solve(problem):                                            │
# │      # 1. BASE CASE — simplest version, solve directly          │
# │      if problem is trivial:                                     │
# │          return trivial_answer                                  │
# │                                                                 │
# │      # 2. RECURSIVE CASE — break down, call self                │
# │      smaller = make_smaller(problem)                            │
# │      sub_result = solve(smaller)                                │
# │      return combine(problem, sub_result)                        │
# └─────────────────────────────────────────────────────────────────┘
#
# ┌─────────────────────────────────────────────────────────────────┐
# │                    COMMON PATTERNS                              │
# │─────────────────────────────────────────────────────────────────│
# │  Linear (1 call):    factorial, sum, countdown                  │
# │  Tree (2+ calls):    family tree, fibonacci, merge sort         │
# │  Divide & conquer:   binary search, quicksort                   │
# │  Backtracking:       maze solving, N-queens, sudoku             │
# │  Accumulation:       collect results as you return              │
# │  Traversal:          print/visit every node in a tree           │
# └─────────────────────────────────────────────────────────────────┘
#
# ┌─────────────────────────────────────────────────────────────────┐
# │                    DEBUGGING CHECKLIST                          │
# │─────────────────────────────────────────────────────────────────│
# │  □ Does the base case handle ALL termination conditions?        │
# │  □ Does EVERY recursive call pass a SMALLER input?              │
# │  □ Is the base case reachable from the recursive case?          │
# │  □ Are you returning values (not just printing)?                │
# │  □ Are you using the returned value from recursive calls?       │
# │  □ Is depth safe? (< 1000 for Python's default limit)          │
# │  □ Is there duplicate work? (consider @lru_cache)               │
# │  □ Are you timing it correctly? (public/private split)          │
# └─────────────────────────────────────────────────────────────────┘
#
# ┌──────────────────────────────────────────────────────────────────┐
# │                   RECURSION LIMIT GUIDE                          │
# │──────────────────────────────────────────────────────────────────│
# │  Family tree (3 gen):    7 calls        ✅ Safe                 │
# │  Family tree (10 gen):   1023 calls     ⚠️ Near limit          │
# │  Family tree (12 gen):   4095 calls     ❌ RecursionError       │
# │  Factorial(100):         100 calls      ✅ Safe                 │
# │  Factorial(1000):        1000 calls     ⚠️ Borderline          │
# │  Naive fib(30):          ~2.7B calls    ❌ Heat death of sun    │
# │  Cached fib(30):         30 calls       ✅ @lru_cache saves     │
# │                                                                  │
# │  Python default limit: sys.getrecursionlimit() → 1000           │
# │  Can increase: sys.setrecursionlimit(5000) (use with caution)   │
# └──────────────────────────────────────────────────────────────────┘
#
# =============================================================================


# =============================================================================
# MAIN EXECUTION
# =============================================================================

if __name__ == "__main__":
    section_1_what_is_recursion()
    section_2_two_required_parts()
    section_3_call_stack()
    section_4_counting_patterns()
    section_5_accumulating()
    section_6_tree_recursion()
    section_7_timing()
    section_8_recursion_vs_iteration()
    section_9_pitfalls()
    section_10_production_patterns()

    print("\n" + "=" * 70)
    print("REFERENCE COMPLETE — See Section 11 (cheat sheet) in source code")
    print("=" * 70)
