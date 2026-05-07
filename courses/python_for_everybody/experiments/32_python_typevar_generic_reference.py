"""
31_python_typevar_generic_reference.py
=======================================

Personal reference: TypeVar and Generic — how Python's type system
expresses "the type varies, but consistently" for both functions and
class hierarchies.

Topics covered
--------------
1.  The Problem — Why TypeVar exists (Any erases type information)
2.  TypeVar Basics — placeholder types for functions
3.  TypeVar with bound= — constrain to a class family
4.  TypeVar with constraints — constrain to an explicit closed set
5.  bound= vs constraints — which to use and when
6.  Generic[T] for classes — parameterizing a class over a type
7.  Generic in class hierarchies — the _BaseDictionary[WordContainer] pattern
8.  Multiple TypeVars — Generic[K, V] and Pipeline[I, O]
9.  Generic + Protocol — combining structural typing with generics
10. Variance — covariant, contravariant, invariant (awareness note)
11. Common Pitfalls and Gotchas
12. Decision Guide and Cheat Sheet

Why this matters for your roadmap (v8.1 GenAI-First)
------------------------------------------------------
- Stage 1 (Speller):     _BaseDictionary[WordContainer] — your actual code
                          TypeVar("WordContainer", set[str], list[str])
                          Solves the mypy invariance error with _words
- Stage 1 (DataVault):   LLMProvider[ResponseT] — response type varies by provider
                          AnalysisResult[T] — generic result containers
- Stage 1 (PolicyPulse): VectorStore[ChunkT] — chunk type varies by embedder
                          Retriever[ResultT] — result type varies by strategy
- Stage 1 (FormSense):   ExtractionResult[FieldT] — field type varies by form
- Stage 1 (AFC):         DataSource[RecordT] — record type varies by provider
                          BacktestResult[SignalT] — signal type varies by model
- Stage 2 (Data Eng):    Pipeline[InputT, OutputT] — typed ETL stages
                          BatchProcessor[T] — generic batch windows
- Stage 3 (ML):          ModelWrapper[InputT, PredT] — typed model interfaces
- Stage 4 (LLM):         Tool[InputT, OutputT] — typed LangChain/MCP tools
                          Memory[StateT] — typed agent memory
- Stage 5 (Senior):      All of the above combined in production systems

How to use this file
---------------------
Run it directly to see all output::

    $ python 31_python_typevar_generic_reference.py

Or import individual sections to experiment in a REPL::

    >>> from 31_python_typevar_generic_reference import section_2_typevar_basics

Author: Manuel Reyes — CS50 Speller / Stage 1 Learning Reference
Version: 1.0.0 — March 2026

References
----------
.. [1] PEP 484 — Type Hints
   https://peps.python.org/pep-0484/
.. [2] PEP 695 — Type Parameter Syntax (Python 3.12+)
   https://peps.python.org/pep-0695/
.. [3] Python Docs — typing.TypeVar
   https://docs.python.org/3/library/typing.html#typing.TypeVar
.. [4] Python Docs — typing.Generic
   https://docs.python.org/3/library/typing.html#typing.Generic
.. [5] mypy — Generics
   https://mypy.readthedocs.io/en/stable/generics.html
.. [6] mypy — Variance
   https://mypy.readthedocs.io/en/stable/generics.html#variance-of-generic-types
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, TypeVar, Generic


# =============================================================================
# SECTION 1: THE PROBLEM — Why TypeVar Exists
# =============================================================================
# ┌─────────────────────────────────────────────────────────────────┐
# │              THE PROBLEM: Any ERASES type information           │
# │─────────────────────────────────────────────────────────────────│
# │                                                                 │
# │  GOAL: Write first_item() that works for any list type          │
# │  and returns the SAME type as the list elements.                │
# │                                                                 │
# │  ATTEMPT 1: Hardcode a type → only works for one type           │
# │    def first_item(items: list[int]) -> int: ...                 │
# │                                                                 │
# │  ATTEMPT 2: Use Any → loses ALL type information                │
# │    def first_item(items: list[Any]) -> Any: ...                 │
# │    result = first_item([1, 2, 3])                               │
# │    result.upper()   ← pyright: OK  (it's Any — no checking)     │
# │    # RUNTIME ERROR: int has no .upper()                         │
# │                                                                 │
# │  SOLUTION: TypeVar → tracks "whatever type flows in flows out"  │
# │    T = TypeVar("T")                                             │
# │    def first_item(items: list[T]) -> T: ...                     │
# │    result = first_item([1, 2, 3])    # T resolves to int        │
# │    result.upper()   ← pyright: ERROR (int has no .upper()) ✓    │
# │                                                                 │
# │  KEY INSIGHT: TypeVar is a TYPE-LEVEL variable.                 │
# │  Just like x = 5 is a value variable, T = TypeVar("T")         │
# │  is a variable that holds a TYPE at type-check time.            │
# └─────────────────────────────────────────────────────────────────┘

def section_1_the_problem() -> None:
    """Show why Any is insufficient and TypeVar is needed."""
    print("=" * 70)
    print("SECTION 1: THE PROBLEM — Any erases type information")
    print("=" * 70)

    # --- 1a: Hardcoded type — works but rigid ---
    print("\n--- 1a: Hardcoded type (works but rigid) ---")

    def first_int(items: list[int]) -> int:
        return items[0]

    print(f"  first_int([10, 20, 30]) → {first_int([10, 20, 30])}")
    print("  Problem: Can't use with strings, Paths, DataFrames...")

    # --- 1b: Any — flexible but dangerous ---
    print("\n--- 1b: Using Any (flexible but type-safety gone) ---")

    def first_any(items: list[Any]) -> Any:
        return items[0]

    result = first_any([1, 2, 3])
    print(f"  first_any([1, 2, 3]) → {result}  (type: {type(result).__name__})")
    print("  pyright thinks result is 'Any' — no checking at all.")
    print("  result.upper() would pass type-check but CRASH at runtime.")

    # --- 1c: TypeVar — flexible AND type-safe ---
    print("\n--- 1c: TypeVar (flexible AND type-safe) ---")

    T = TypeVar("T")  # T is a placeholder: "some type, to be determined"

    def first_item(items: list[T]) -> T:
        # T is resolved per call site:
        # first_item([1, 2, 3])     → T = int,  return type = int
        # first_item(["a", "b"])    → T = str,  return type = str
        # first_item([Path("x")])   → T = Path, return type = Path
        return items[0]

    print(f"  first_item([10, 20, 30])   → {first_item([10, 20, 30])}")
    print(f"  first_item(['a', 'b'])     → {first_item(['a', 'b'])}")
    print(f"  first_item([True, False])  → {first_item([True, False])}")
    print()
    print("  pyright knows each return type exactly:")
    print("  first_item([1,2,3]).upper()  ← ERROR: int has no .upper() ✓")
    print("  first_item(['a']).upper()    ← OK: str has .upper() ✓")

    print()


# =============================================================================
# SECTION 2: TYPEVAR BASICS — Placeholder Types for Functions
# =============================================================================
# ┌─────────────────────────────────────────────────────────────────┐
# │              TYPEVAR: How it works at each call site            │
# │─────────────────────────────────────────────────────────────────│
# │                                                                 │
# │  T = TypeVar("T")   ← declare once at module level             │
# │                                                                 │
# │  def identity(x: T) -> T:   ← T is the SAME type in & out     │
# │      return x                                                   │
# │                                                                 │
# │  identity(42)    → T binds to int   → returns int              │
# │  identity("hi")  → T binds to str   → returns str              │
# │  identity(3.14)  → T binds to float → returns float            │
# │                                                                 │
# │  RULE: T binds ONCE per call, then stays consistent.           │
# │  If T = int here, EVERY use of T in that call is int.          │
# │                                                                 │
# │  TWO TypeVars for two independent types:                        │
# │  K = TypeVar("K")                                               │
# │  V = TypeVar("V")                                               │
# │  def make_pair(key: K, val: V) -> tuple[K, V]:                 │
# │      return (key, val)                                          │
# │                                                                 │
# │  make_pair("name", 42)  → K=str, V=int → tuple[str, int]       │
# └─────────────────────────────────────────────────────────────────┘

def section_2_typevar_basics() -> None:
    """Demonstrate TypeVar mechanics for functions."""
    print("=" * 70)
    print("SECTION 2: TYPEVAR BASICS — Placeholder types for functions")
    print("=" * 70)

    T = TypeVar("T")
    K = TypeVar("K")
    V = TypeVar("V")

    # --- 2a: Identity function — T in, T out ---
    print("\n--- 2a: Identity function (T in → T out) ---")

    def identity(x: T) -> T:
        # T binds to whatever type is passed in.
        # pyright knows the return type is EXACTLY what was passed.
        return x

    print(f"  identity(42)     → {identity(42)!r:<10} (int)")
    print(f"  identity('hello')→ {identity('hello')!r:<10} (str)")
    print(f"  identity(3.14)   → {identity(3.14)!r:<10} (float)")

    # --- 2b: T keeps the same type throughout ONE call ---
    print("\n--- 2b: T is consistent WITHIN one call ---")

    def swap_pair(a: T, b: T) -> tuple[T, T]:
        # Both a AND b must be the same type T.
        # swap_pair(1, 2)        → T=int, both args are int ✓
        # swap_pair(1, "hello")  → pyright ERROR: T can't be int AND str ✓
        return (b, a)

    print(f"  swap_pair(1, 2)            → {swap_pair(1, 2)}")
    print(f"  swap_pair('cat', 'dog')    → {swap_pair('cat', 'dog')}")
    print("  swap_pair(1, 'hello')      → pyright ERROR (T can't be two types)")

    # --- 2c: Two TypeVars for two independent types ---
    print("\n--- 2c: Two TypeVars (K, V) for independent types ---")

    def make_pair(key: K, val: V) -> tuple[K, V]:
        # K and V are INDEPENDENT — each resolves separately.
        # make_pair("name", 42) → K=str, V=int
        return (key, val)

    print(f"  make_pair('name', 42)       → {make_pair('name', 42)}")
    print(f"  make_pair(True, [1,2,3])    → {make_pair(True, [1, 2, 3])}")

    # --- 2d: TypeVar in container operations ---
    print("\n--- 2d: TypeVar preserves type through container operations ---")

    def last_item(items: list[T]) -> T:
        return items[-1]

    def wrap_in_list(item: T) -> list[T]:
        # Returns a list of the SAME type as the input.
        return [item]

    print(f"  last_item([10, 20, 30])     → {last_item([10, 20, 30])!r}")
    print(f"  last_item(['x', 'y', 'z'])  → {last_item(['x', 'y', 'z'])!r}")
    print(f"  wrap_in_list(42)            → {wrap_in_list(42)}")
    print(f"  wrap_in_list('hello')       → {wrap_in_list('hello')}")

    print()


# =============================================================================
# SECTION 3: TYPEVAR WITH bound= — Constrain to a Class Family
# =============================================================================
# ┌─────────────────────────────────────────────────────────────────┐
# │              bound= : "T must be a subclass of X"              │
# │─────────────────────────────────────────────────────────────────│
# │                                                                 │
# │  T = TypeVar("T")               # ANY type                      │
# │  T = TypeVar("T", bound=Animal) # Animal OR any subclass        │
# │                                                                 │
# │  OPEN hierarchy — subclasses are automatically valid:           │
# │    bound=Animal                                                 │
# │         Animal  ← valid                                         │
# │         ├── Dog ← valid (subclass)                              │
# │         └── Cat ← valid (subclass)                              │
# │         int     ← INVALID (not in Animal family)                │
# │                                                                 │
# │  WHY bound= matters:                                            │
# │  Without bound, T can be ANYTHING — pyright won't let you       │
# │  call .speak() on T because T might be int.                     │
# │  With bound=Animal, pyright knows T has .speak() because        │
# │  Animal and all its subclasses have .speak().                   │
# │                                                                 │
# │  bound= is the answer to: "I need any type from this family     │
# │  AND I need to call methods defined on the base class."         │
# └─────────────────────────────────────────────────────────────────┘

def section_3_bound() -> None:
    """Demonstrate TypeVar with bound= for class family constraints."""
    print("=" * 70)
    print("SECTION 3: TypeVar WITH bound= — constrain to a class family")
    print("=" * 70)

    # --- 3a: Without bound — can't call methods ---
    print("\n--- 3a: Without bound (can't call T-specific methods) ---")

    class Animal:
        def speak(self) -> str:
            return "..."

    class Dog(Animal):
        def speak(self) -> str:
            return "Woof"

    class Cat(Animal):
        def speak(self) -> str:
            return "Meow"

    T = TypeVar("T")

    def make_speak_bad(animal: T) -> str:
        # pyright ERROR: T might be int, str, Path — no .speak() guaranteed
        # return animal.speak()   ← type error
        return "can't call .speak() — T is unconstrained"

    print(f"  make_speak_bad(Dog()) → '{make_speak_bad(Dog())}'")
    print("  pyright would error on animal.speak() — T is unconstrained")

    # --- 3b: With bound= — methods are guaranteed ---
    print("\n--- 3b: With bound=Animal (methods are guaranteed) ---")

    AnyAnimal = TypeVar("AnyAnimal", bound=Animal)
    # AnyAnimal can be: Animal, Dog, Cat, or any future subclass
    # It CANNOT be: int, str, list — they're not in the Animal family

    def make_speak(animal: AnyAnimal) -> str:
        # pyright KNOWS animal has .speak() because AnyAnimal is bound to Animal
        return animal.speak()

    print(f"  make_speak(Dog())  → '{make_speak(Dog())}'")
    print(f"  make_speak(Cat())  → '{make_speak(Cat())}'")
    print(f"  make_speak(Animal()) → '{make_speak(Animal())}'")
    print("  make_speak(42)     → pyright ERROR: int not in Animal family ✓")

    # --- 3c: bound= preserves the SUBTYPE — key insight ---
    print("\n--- 3c: bound= preserves the concrete subtype ---")

    def clone_animal(animal: AnyAnimal) -> AnyAnimal:
        # Returns the SAME concrete type as the input — not just Animal.
        # clone_animal(Dog()) → return type is Dog, not just Animal.
        # This matters when you need the concrete interface, not just the base.
        print(f"    Cloning a {type(animal).__name__}...")
        return animal

    dog = Dog()
    result = clone_animal(dog)
    print(f"  clone_animal(Dog()) → {type(result).__name__}")
    print("  pyright knows result is Dog (not just Animal) — subtype preserved")

    # --- 3d: Real roadmap example — bound to a base class ---
    print("\n--- 3d: Roadmap example — bound=_BaseDictionary ---")
    print("  # From your speller codebase (Stage 2+ pattern):")
    print()
    print("  DictT = TypeVar('DictT', bound=_BaseDictionary)")
    print()
    print("  def benchmark_all(dicts: list[DictT], text: str) -> list[DictT]:")
    print("      for d in dicts:")
    print("          d.load('dictionaries/large')  # .load() guaranteed ✓")
    print("          d.check('hello')              # .check() guaranteed ✓")
    print("      return dicts  # returns same concrete type as input ✓")

    print()


# =============================================================================
# SECTION 4: TYPEVAR WITH CONSTRAINTS — Explicit Closed Set
# =============================================================================
# ┌─────────────────────────────────────────────────────────────────┐
# │         constraints: "T must be EXACTLY one of these"           │
# │─────────────────────────────────────────────────────────────────│
# │                                                                 │
# │  T = TypeVar("T", set[str], list[str])                          │
# │  # T can ONLY be set[str] or list[str]. Nothing else.           │
# │                                                                 │
# │  CLOSED set — no subclasses, no unrelated types:                │
# │    set[str]  ← valid                                            │
# │    list[str] ← valid                                            │
# │    dict[str] ← INVALID (not in the list)                        │
# │    FrozenSet  ← INVALID (subclass, but still not in the list)   │
# │                                                                 │
# │  This is EXACTLY why your speller uses constraints:             │
# │  WordContainer = TypeVar("WordContainer", set[str], list[str])  │
# │                                                                 │
# │  _BaseDictionary(ABC, Generic[WordContainer]):                  │
# │      self._words: WordContainer = self._create_container()      │
# │                                                                 │
# │  HashTableDictionary(_BaseDictionary[set[str]]):                │
# │      self._words  →  set[str]   → .add() is valid ✓            │
# │                                                                 │
# │  ListDictionary(_BaseDictionary[list[str]]):                    │
# │      self._words  →  list[str]  → .append() is valid ✓         │
# └─────────────────────────────────────────────────────────────────┘

def section_4_constraints() -> None:
    """Demonstrate TypeVar with explicit type constraints."""
    print("=" * 70)
    print("SECTION 4: TypeVar WITH CONSTRAINTS — explicit closed set")
    print("=" * 70)

    # --- 4a: Constraints in action ---
    print("\n--- 4a: TypeVar with constraints ---")

    # WordContainer can ONLY be set[str] OR list[str] — nothing else.
    # This is the actual TypeVar from your speller/dictionaries.py.
    WordContainer = TypeVar("WordContainer", set[str], list[str])

    print("  WordContainer = TypeVar('WordContainer', set[str], list[str])")
    print()
    print("  Valid:   set[str]   ← one of the two allowed types")
    print("  Valid:   list[str]  ← one of the two allowed types")
    print("  Invalid: dict[str]  ← not in the constraint list")
    print("  Invalid: frozenset  ← subclass, but constraints ignore inheritance")

    # --- 4b: Constraints vs unconstrained in a function ---
    print("\n--- 4b: Constraints in a function ---")

    def count_words(container: WordContainer) -> int:
        # pyright knows container is EITHER set[str] OR list[str].
        # Both support len() — this is safe.
        return len(container)

    print(f"  count_words({{'hello', 'world'}})  → {count_words({'hello', 'world'})}")
    print(f"  count_words(['cat', 'dog', 'cat'])   → {count_words(['cat', 'dog', 'cat'])}")
    print("  count_words({'key': 'val'})          → pyright ERROR: dict not allowed ✓")

    # --- 4c: Why constraints are needed for the speller _words attribute ---
    print("\n--- 4c: WHY constraints solve the _words mypy problem ---")
    print()
    print("  WITHOUT Generic[WordContainer]:")
    print("  class _BaseDictionary:")
    print("      self._words: set[str] | list[str]  ← UNION type")
    print()
    print("  class HashTableDictionary(_BaseDictionary):")
    print("      def _add_word(self, word):")
    print("          self._words.add(word)   ← ERROR: list[str] has no .add()")
    print("          # pyright can't narrow the union inside the method")
    print()
    print("  WITH Generic[WordContainer]:")
    print("  class _BaseDictionary(ABC, Generic[WordContainer]):")
    print("      self._words: WordContainer  ← UNRESOLVED placeholder")
    print()
    print("  class HashTableDictionary(_BaseDictionary[set[str]]):")
    print("      # WordContainer = set[str] for THIS class")
    print("      def _add_word(self, word):")
    print("          self._words.add(word)   ← OK: _words IS set[str] ✓")

    print()


# =============================================================================
# SECTION 5: bound= vs CONSTRAINTS — Which to Use and When
# =============================================================================
# ┌─────────────────────────────────────────────────────────────────┐
# │              bound=  vs  constraints — the decision             │
# │─────────────────────────────────────────────────────────────────│
# │                                                                 │
# │  bound=X                                                        │
# │  ────────                                                        │
# │  "T must be X or any subclass of X"                             │
# │  OPEN: future subclasses automatically valid                    │
# │  Use when: all types share a base class with useful methods     │
# │  Use when: you need to call base-class methods on T             │
# │  Example: bound=Animal → can call .speak() on T                 │
# │           bound=_BaseDictionary → can call .load(), .check()   │
# │                                                                 │
# │  TypeVar("T", A, B)                                             │
# │  ──────────────────                                              │
# │  "T must be EXACTLY A or EXACTLY B — nothing else"              │
# │  CLOSED: explicit list, inheritance NOT included                │
# │  Use when: types are unrelated (no shared base with methods)    │
# │  Use when: you want to restrict to specific concrete types      │
# │  Example: TypeVar("T", set[str], list[str])                     │
# │           TypeVar("T", str, bytes)                              │
# │                                                                 │
# │  MENTAL TEST:                                                   │
# │  "Are there methods I need to call on T?"                       │
# │      YES → use bound= (the base class guarantees them)          │
# │  "Is this a closed list of unrelated concrete types?"           │
# │      YES → use constraints                                      │
# └─────────────────────────────────────────────────────────────────┘

def section_5_bound_vs_constraints() -> None:
    """Compare bound= and constraints with concrete examples."""
    print("=" * 70)
    print("SECTION 5: bound= vs CONSTRAINTS — which to use and when")
    print("=" * 70)

    # --- 5a: bound= when you need to call methods ---
    print("\n--- 5a: bound= when you need to CALL METHODS on T ---")

    class Shape:
        def area(self) -> float:
            return 0.0

    class Circle(Shape):
        def __init__(self, radius: float) -> None:
            self.radius = radius

        def area(self) -> float:
            return 3.14159 * self.radius ** 2

    class Rectangle(Shape):
        def __init__(self, w: float, h: float) -> None:
            self.w = w
            self.h = h

        def area(self) -> float:
            return self.w * self.h

    AnyShape = TypeVar("AnyShape", bound=Shape)

    def largest(shapes: list[AnyShape]) -> AnyShape:
        # bound=Shape guarantees .area() exists on every item.
        # Returns the SAME concrete type as the input elements.
        return max(shapes, key=lambda s: s.area())

    shapes = [Circle(3.0), Circle(1.0), Circle(5.0)]
    result = largest(shapes)
    print(f"  largest([Circle(3), Circle(1), Circle(5)]) → Circle(r={result.radius})")
    print("  pyright knows result is Circle (not just Shape) — bound= preserves subtype")

    # --- 5b: Constraints when types are unrelated ---
    print("\n--- 5b: Constraints when types are UNRELATED ---")

    # set[str] and list[str] share no useful base class with .add()/.append().
    # We want EXACTLY one of these two — not frozenset, not dict, not deque.
    WordContainer = TypeVar("WordContainer", set[str], list[str])

    def empty_container(c: WordContainer) -> WordContainer:
        # Returns an empty container of the SAME concrete type.
        # For set[str]  → returns set()
        # For list[str] → returns list()
        return type(c)()  # type: ignore[return-value]

    word_set: set[str] = {"cat", "dog"}
    word_list: list[str] = ["cat", "dog"]
    print(f"  empty_container({{'cat','dog'}}) → {empty_container(word_set)!r}")
    print(f"  empty_container(['cat','dog']) → {empty_container(word_list)!r}")

    # --- 5c: The decision table ---
    print("\n--- 5c: Decision table ---")
    print()
    print("  Situation                                  → Use")
    print("  ─────────────────────────────────────────────────────")
    print("  Need to call methods defined on base class → bound=")
    print("  Types share a meaningful common ancestor   → bound=")
    print("  Future subclasses should work automatically→ bound=")
    print("  Types are unrelated (set vs list)          → constraints")
    print("  Want an explicit closed list of types      → constraints")
    print("  Exactly two concrete types, no more        → constraints")
    print()
    print("  YOUR SPELLER:")
    print("  set[str] and list[str] have no shared ancestor with")
    print("  .add() or .append() — constraints is the correct choice.")

    print()


# =============================================================================
# SECTION 6: Generic[T] FOR CLASSES — Parameterizing a Class
# =============================================================================
# ┌─────────────────────────────────────────────────────────────────┐
# │              Generic[T]: "this class is parameterised"          │
# │─────────────────────────────────────────────────────────────────│
# │                                                                 │
# │  T binds ONCE per INSTANCE (not per method call).               │
# │  Every method on that instance sees the same T.                 │
# │                                                                 │
# │  class Box(Generic[T]):        ← class is parameterised         │
# │      def __init__(self, v: T): ← T resolved at instantiation    │
# │          self.value: T = v                                      │
# │      def get(self) -> T:       ← same T as __init__             │
# │          return self.value                                      │
# │                                                                 │
# │  int_box = Box(42)           → T = int for THIS instance        │
# │  str_box = Box("hello")      → T = str for THIS instance        │
# │                                                                 │
# │  int_box.get()   → int  (pyright knows this)                    │
# │  str_box.get()   → str  (pyright knows this)                    │
# │                                                                 │
# │  FUNCTION TypeVar: T resolves per CALL                          │
# │  CLASS TypeVar:    T resolves per INSTANCE                      │
# └─────────────────────────────────────────────────────────────────┘

def section_6_generic_classes() -> None:
    """Demonstrate Generic[T] for class parameterisation."""
    print("=" * 70)
    print("SECTION 6: Generic[T] FOR CLASSES — parameterizing a class")
    print("=" * 70)

    T = TypeVar("T")

    # --- 6a: Simple Box[T] --- 
    print("\n--- 6a: Box[T] — the canonical Generic example ---")

    class Box(Generic[T]):
        """A container holding exactly one value of type T."""

        def __init__(self, value: T) -> None:
            # T is resolved ONCE when Box(42) or Box("hello") is called.
            # Every subsequent method sees the same T for this instance.
            self.value: T = value

        def get(self) -> T:
            return self.value

        def transform(self, func: Any) -> Any:
            # In a fully typed version: Callable[[T], V] -> Box[V]
            # Simplified here for clarity
            return Box(func(self.value))

        def __repr__(self) -> str:
            return f"Box({self.value!r})"

    int_box = Box(42)
    str_box = Box("hello")
    print(f"  int_box = Box(42)      → {int_box}  (T = int)")
    print(f"  str_box = Box('hello') → {str_box}  (T = str)")
    print(f"  int_box.get()          → {int_box.get()!r}  (pyright: int)")
    print(f"  str_box.get()          → {str_box.get()!r}  (pyright: str)")

    # --- 6b: T is consistent across ALL methods of one instance ---
    print("\n--- 6b: T is consistent across ALL methods ---")

    class Stack(Generic[T]):
        """LIFO stack that holds items of type T."""

        def __init__(self) -> None:
            self._items: list[T] = []

        def push(self, item: T) -> None:
            self._items.append(item)

        def pop(self) -> T:
            return self._items.pop()

        def peek(self) -> T:
            return self._items[-1]

        def size(self) -> int:
            return len(self._items)

    int_stack: Stack[int] = Stack()
    int_stack.push(10)
    int_stack.push(20)
    int_stack.push(30)
    print(f"  int_stack: push 10, 20, 30")
    print(f"  int_stack.peek() → {int_stack.peek()!r}  (pyright: int)")
    print(f"  int_stack.pop()  → {int_stack.pop()!r}   (pyright: int)")
    print(f"  int_stack.push('hello') → pyright ERROR: str not int ✓")

    # --- 6c: How T resolves per instance (not per class) ---
    print("\n--- 6c: T resolves PER INSTANCE, not per class ---")

    path_stack: Stack[str] = Stack()
    path_stack.push("src/speller.py")
    path_stack.push("src/dictionaries.py")

    print(f"  int_stack holds ints  → int_stack.pop() returns int")
    print(f"  path_stack holds strs → path_stack.pop() returns str")
    print(f"  Both are Stack, but T is different per instance.")
    print(f"  path_stack.pop() → {path_stack.pop()!r}  (pyright: str)")

    # --- 6d: The explicit type annotation style ---
    print("\n--- 6d: Explicit vs inferred parameterisation ---")
    print("  # Inferred — pyright resolves T from the argument:")
    print("  box = Box(42)                    # T inferred as int")
    print()
    print("  # Explicit — you declare T upfront (better for clarity):")
    print("  box: Box[int] = Box(42)          # T explicitly declared")
    print("  stack: Stack[str] = Stack()      # T declared, no initial items")

    print()


# =============================================================================
# SECTION 7: Generic IN CLASS HIERARCHIES — Your Speller Pattern
# =============================================================================
# ┌─────────────────────────────────────────────────────────────────┐
# │     Generic[W] in inheritance: the _BaseDictionary pattern      │
# │─────────────────────────────────────────────────────────────────│
# │                                                                 │
# │  W = TypeVar("W", set[str], list[str])                          │
# │                                                                 │
# │  class _BaseDictionary(ABC, Generic[W]):                        │
# │      self._words: W        ← W is unresolved (a promise)       │
# │      def _add_word(self, word: str) → None: ...  (abstract)    │
# │                                                                 │
# │  class HashTableDictionary(_BaseDictionary[set[str]]):          │
# │      # W = set[str] here   ↑↑↑↑↑↑↑↑                           │
# │      # pyright substitutes set[str] for W everywhere            │
# │      self._words: set[str]   ← resolved ✓                      │
# │      def _add_word(self, word):                                 │
# │          self._words.add(word)  ← .add() exists on set ✓       │
# │                                                                 │
# │  class ListDictionary(_BaseDictionary[list[str]]):              │
# │      # W = list[str] here  ↑↑↑↑↑↑↑↑                           │
# │      self._words: list[str]  ← resolved ✓                      │
# │      def _add_word(self, word):                                 │
# │          self._words.append(word) ← .append() exists on list ✓ │
# │                                                                 │
# │  KEY: The base class NEVER commits to a concrete type.          │
# │  The subclass SPECIALISES by filling in W.                      │
# │  This is SPECIALISATION, not NARROWING — no invariance error.   │
# └─────────────────────────────────────────────────────────────────┘

def section_7_generic_hierarchy() -> None:
    """Demonstrate Generic[W] in the _BaseDictionary class hierarchy."""
    print("=" * 70)
    print("SECTION 7: Generic IN CLASS HIERARCHIES — the speller pattern")
    print("=" * 70)

    # This is a simplified but faithful reproduction of your actual
    # speller/dictionaries.py structure.
    WordContainer = TypeVar("WordContainer", set[str], list[str])

    # --- 7a: The base class — Generic[WordContainer] ---
    print("\n--- 7a: Base class with Generic[WordContainer] ---")

    class _BaseWordStore(ABC, Generic[WordContainer]):
        """
        Generic[WordContainer] means: this class is parameterised.
        WordContainer is NOT resolved here — it's a PROMISE.
        Each subclass fills it in when it declares its specialisation.
        """

        def __init__(self) -> None:
            # self._words is typed as WordContainer — still unresolved.
            # pyright stores this as "some future set[str] or list[str]".
            self._words: WordContainer = self._create_container()
            self._count: int = 0

        @abstractmethod
        def _create_container(self) -> WordContainer:
            """Return the empty container. Subclass decides which type."""
            ...

        @abstractmethod
        def _add_word(self, word: str) -> None:
            """Add word to container. Subclass decides how."""
            ...

        def load(self, words: list[str]) -> None:
            """Shared algorithm — same for all subclasses."""
            for word in words:
                self._add_word(word.lower())
                self._count += 1
            print(f"    Loaded {self._count} words into {type(self).__name__}")

        def size(self) -> int:
            return len(self._words)

        def __repr__(self) -> str:
            return f"{type(self).__name__}(words={self._count:,})"

    print("  _BaseWordStore(ABC, Generic[WordContainer]) defined.")
    print("  WordContainer is unresolved — base class makes no commitment.")

    # --- 7b: First specialisation — W = set[str] ---
    print("\n--- 7b: HashTable subclass — W is resolved to set[str] ---")

    class HashTableStore(_BaseWordStore[set[str]]):
        # Writing _BaseWordStore[set[str]] tells pyright:
        # "For THIS class, WordContainer = set[str]"
        # pyright substitutes set[str] everywhere WordContainer appears.

        def _create_container(self) -> set[str]:
            # Return type matches WordContainer = set[str] ✓
            return set()

        def _add_word(self, word: str) -> None:
            # pyright knows self._words is set[str] here.
            # .add() exists on set[str] → no error ✓
            self._words.add(word)

        def check(self, word: str) -> bool:
            return word.lower() in self._words

    h = HashTableStore()
    h.load(["cat", "dog", "bird"])
    print(f"  h = HashTableStore() → {h}")
    print(f"  h.check('cat')  → {h.check('cat')}")
    print(f"  h.check('fish') → {h.check('fish')}")
    print("  self._words is set[str] → .add() valid ✓")

    # --- 7c: Second specialisation — W = list[str] ---
    print("\n--- 7c: List subclass — W is resolved to list[str] ---")

    class ListStore(_BaseWordStore[list[str]]):
        # _BaseWordStore[list[str]] → WordContainer = list[str] here

        def _create_container(self) -> list[str]:
            # Return type matches WordContainer = list[str] ✓
            return []

        def _add_word(self, word: str) -> None:
            # pyright knows self._words is list[str] here.
            # .append() exists on list[str] → no error ✓
            self._words.append(word)

        def check(self, word: str) -> bool:
            return word.lower() in self._words

    lst = ListStore()
    lst.load(["cat", "dog", "bird"])
    print(f"  lst = ListStore() → {lst}")
    print(f"  lst.check('dog')  → {lst.check('dog')}")
    print("  self._words is list[str] → .append() valid ✓")

    # --- 7d: Why specialisation ≠ narrowing (the invariance insight) ---
    print("\n--- 7d: WHY this avoids the invariance error ---")
    print()
    print("  WRONG approach (Protocol on mutable attribute):")
    print("  class _BaseWordStore:")
    print("      _words: WordStore  ← committed to WordStore")
    print("  class HashTableStore(_BaseWordStore):")
    print("      _words: set[str]   ← pyright: invariance violation!")
    print("      # Base says 'WordStore', subclass says 'set[str]'")
    print("      # Mutable variables must match EXACTLY (invariance)")
    print()
    print("  CORRECT approach (Generic[W]):")
    print("  class _BaseWordStore(ABC, Generic[W]):")
    print("      _words: W          ← base NEVER commits")
    print("  class HashTableStore(_BaseWordStore[set[str]]):")
    print("      _words: set[str]   ← W is SPECIALISED, not overridden ✓")
    print("      # This is filling in W, not changing an existing type")

    print()


# =============================================================================
# SECTION 8: MULTIPLE TypeVars — Generic[K, V] and Pipeline[I, O]
# =============================================================================
# ┌─────────────────────────────────────────────────────────────────┐
# │         Multiple TypeVars: each resolves independently          │
# │─────────────────────────────────────────────────────────────────│
# │                                                                 │
# │  K = TypeVar("K")                                               │
# │  V = TypeVar("V")                                               │
# │                                                                 │
# │  class Pair(Generic[K, V]):                                     │
# │      key: K                                                     │
# │      value: V                                                   │
# │                                                                 │
# │  Pair[str, int]   → key is str, value is int                   │
# │  Pair[int, float] → key is int, value is float                 │
# │                                                                 │
# │  ROADMAP: Pipeline[InputT, OutputT] is how you'll type          │
# │  ETL stages in Stage 2 — each stage transforms I → O.          │
# │                                                                 │
# │  class Pipeline(Generic[I, O]):                                 │
# │      def run(self, data: I) -> O: ...                           │
# └─────────────────────────────────────────────────────────────────┘

def section_8_multiple_typevars() -> None:
    """Demonstrate Generic with multiple TypeVar parameters."""
    print("=" * 70)
    print("SECTION 8: MULTIPLE TypeVars — Generic[K, V] and Pipeline[I, O]")
    print("=" * 70)

    K = TypeVar("K")
    V = TypeVar("V")
    I = TypeVar("I")  # Input
    O = TypeVar("O")  # Output  # noqa: E741

    # --- 8a: Pair[K, V] ---
    print("\n--- 8a: Pair[K, V] — two independent type parameters ---")

    class Pair(Generic[K, V]):
        """A key-value pair where key and value can be any types."""

        def __init__(self, key: K, value: V) -> None:
            self.key: K = key
            self.value: V = value

        def swap(self) -> "Pair[V, K]":
            # Returns a new Pair with key and value swapped.
            # The types SWAP too: Pair[str, int] → Pair[int, str]
            return Pair(self.value, self.key)

        def __repr__(self) -> str:
            return f"Pair(key={self.key!r}, value={self.value!r})"

    p1: Pair[str, int] = Pair("age", 35)
    p2: Pair[str, list[str]] = Pair("tags", ["python", "ml", "finance"])
    print(f"  Pair('age', 35)          → {p1}")
    print(f"  Pair('tags', [...])      → {p2}")
    print(f"  p1.swap()                → {p1.swap()}")
    print("  p1.key is str, p1.value is int — tracked independently ✓")

    # --- 8b: Pipeline[I, O] — Stage 2 ETL pattern ---
    print("\n--- 8b: Pipeline[I, O] — Stage 2 ETL pattern ---")

    class Pipeline(Generic[I, O]):
        """A data transformation step: takes type I, returns type O."""

        def __init__(self, name: str) -> None:
            self.name = name

        def run(self, data: I) -> O:
            # Subclasses implement the actual transformation.
            # The type system tracks: what goes in (I) and comes out (O).
            raise NotImplementedError

        def __repr__(self) -> str:
            return f"Pipeline[{self.name}]"

    # Concrete stage: str → list[str]  (e.g. CSV line → fields)
    class ParseCSVRow(Pipeline[str, list[str]]):
        """Takes a CSV row string, returns list of field strings."""

        def run(self, data: str) -> list[str]:
            return [field.strip() for field in data.split(",")]

    # Concrete stage: list[str] → dict[str, str] (e.g. fields → record)
    class FieldsToRecord(Pipeline[list[str], dict[str, str]]):
        """Takes field list, returns a labeled record dict."""

        def __init__(self, headers: list[str]) -> None:
            super().__init__("fields_to_record")
            self.headers = headers

        def run(self, data: list[str]) -> dict[str, str]:
            return dict(zip(self.headers, data))

    parse = ParseCSVRow("parse_csv")
    label = FieldsToRecord(["name", "age", "city"])

    raw = "Alice, 35, New York"
    fields = parse.run(raw)
    record = label.run(fields)

    print(f"  ParseCSVRow.run('{raw}')")
    print(f"    → {fields}")
    print(f"  FieldsToRecord.run({fields})")
    print(f"    → {record}")
    print()
    print("  pyright tracks: ParseCSVRow is Pipeline[str, list[str]]")
    print("  pyright tracks: FieldsToRecord is Pipeline[list[str], dict[str,str]]")
    print("  Stage 2 ETL: each pipeline stage has typed I/O contracts ✓")

    # --- 8c: Roadmap relevance ---
    print("\n--- 8c: Multiple TypeVars in your v8.1 projects ---")
    print()
    print("  DataVault:   LLMProvider[ResponseT]")
    print("               → T is the provider's response object type")
    print()
    print("  PolicyPulse: Retriever[QueryT, ChunkT]")
    print("               → Q is query type, C is retrieved chunk type")
    print()
    print("  AFC:         DataSource[RecordT, FilterT]")
    print("               → R is the record type, F is the filter type")
    print()
    print("  Stage 2 ETL: Pipeline[InputT, OutputT]")
    print("               → each DAG task has a typed contract")

    print()


# =============================================================================
# SECTION 9: Generic + Protocol — Structural Typing meets Generics
# =============================================================================
# ┌─────────────────────────────────────────────────────────────────┐
# │         Generic Protocol: structural AND parameterised          │
# │─────────────────────────────────────────────────────────────────│
# │                                                                 │
# │  from typing import Protocol                                    │
# │                                                                 │
# │  T_co = TypeVar("T_co", covariant=True)  ← read-only output    │
# │                                                                 │
# │  class Readable(Protocol[T_co]):                                │
# │      def read(self) -> T_co: ...                                │
# │                                                                 │
# │  Any class with a .read() method satisfies Readable[X]          │
# │  WHERE X is the return type of .read().                         │
# │                                                                 │
# │  This is how collections.abc works:                             │
# │  Iterator[T_co] — any class with __next__() -> T satisfies it   │
# └─────────────────────────────────────────────────────────────────┘

def section_9_generic_protocol() -> None:
    """Demonstrate combining Generic with Protocol."""
    print("=" * 70)
    print("SECTION 9: Generic + Protocol — structural typing meets generics")
    print("=" * 70)

    from typing import Protocol

    # --- 9a: A Generic Protocol ---
    print("\n--- 9a: Generic Protocol for a typed provider interface ---")

    T_co = TypeVar("T_co", covariant=True)  # covariant: OK for read-only output

    class Provider(Protocol[T_co]):
        """Any object with a .fetch() method returning T."""
        def fetch(self) -> T_co: ...

    # A stock price provider
    class StockPriceProvider:
        """Returns float — satisfies Provider[float] structurally."""
        def fetch(self) -> float:
            return 182.35  # simulated AAPL price

    # An SEC filing provider
    class SECFilingProvider:
        """Returns str — satisfies Provider[str] structurally."""
        def fetch(self) -> str:
            return "10-K filing content..."

    def display_data(provider: Provider[Any]) -> None:
        data = provider.fetch()
        print(f"    Fetched: {data!r} (type: {type(data).__name__})")

    print("  StockPriceProvider satisfies Provider[float]:")
    display_data(StockPriceProvider())
    print("  SECFilingProvider satisfies Provider[str]:")
    display_data(SECFilingProvider())
    print()
    print("  Neither class inherits from Provider — pure structural typing.")
    print("  This is how your v8.1 DataSource protocol will work in AFC.")

    # --- 9b: collections.abc as Generic Protocols ---
    print("\n--- 9b: collections.abc — Generic Protocols you already use ---")
    print()
    print("  Iterator[T_co]   — any class with __next__() -> T")
    print("  Iterable[T_co]   — any class with __iter__() -> Iterator[T]")
    print("  Sequence[T_co]   — any class supporting len() + indexing")
    print("  Mapping[K, V_co] — any class supporting key lookup")
    print()
    print("  Your extract_words() uses Iterator[str]:")
    print("  def extract_words(filepath) -> Iterator[str]:")
    print("    This says 'I return something that yields str values'")
    print("    list, generator, any __next__() -> str all satisfy this.")

    # --- 9c: Roadmap connection ---
    print("\n--- 9c: Generic Protocols in your v8.1 projects ---")
    print()
    print("  PolicyPulse:")
    print("    class VectorStore(Protocol[ChunkT]):")
    print("        def search(self, query: str) -> list[ChunkT]: ...")
    print("    # ChromaDB, Pinecone, in-memory — all satisfy structurally")
    print()
    print("  DataVault:")
    print("    class LLMProvider(Protocol[ResponseT]):")
    print("        def complete(self, prompt: str) -> ResponseT: ...")
    print("    # Gemini, OpenAI, Claude — each has its own ResponseT")

    print()


# =============================================================================
# SECTION 10: VARIANCE — Covariant, Contravariant, Invariant
# =============================================================================
# ┌─────────────────────────────────────────────────────────────────┐
# │              VARIANCE: an awareness note                        │
# │─────────────────────────────────────────────────────────────────│
# │                                                                 │
# │  This is the TYPE-THEORY reason behind the invariance error     │
# │  you hit when you tried WordStore Protocol on _words.           │
# │                                                                 │
# │  INVARIANT (default for TypeVar, all mutable containers)        │
# │    list[Dog] is NOT a list[Animal]  ← strict: exact match only  │
# │    Because: a list[Animal] could hold a Cat, breaking list[Dog] │
# │    All mutable class attributes are invariant.                  │
# │                                                                 │
# │  COVARIANT (covariant=True, read-only outputs)                  │
# │    Tuple[Dog] IS a Tuple[Animal]  ← Dog is a subtype of Animal  │
# │    Because: tuples are immutable — you can only READ from them   │
# │    Iterator[Dog] satisfies Iterator[Animal] (output only)       │
# │    Use for: return types, read-only protocol outputs             │
# │                                                                 │
# │  CONTRAVARIANT (contravariant=True, write-only inputs)          │
# │    Callable[[Animal], ...] satisfies Callable[[Dog], ...]       │
# │    Because: if you handle any Animal, you can handle a Dog       │
# │    Use for: function parameters, write-only protocol inputs      │
# │                                                                 │
# │  PRACTICAL RULE for Stage 1:                                    │
# │  Use covariant=True only in Protocols for read-only outputs.    │
# │  Leave everything else invariant (the default).                  │
# │  Stage 2+ will introduce Contravariant where needed.            │
# └─────────────────────────────────────────────────────────────────┘

def section_10_variance() -> None:
    """Explain variance as an awareness note for Stage 1+."""
    print("=" * 70)
    print("SECTION 10: VARIANCE — covariant, contravariant, invariant")
    print("=" * 70)

    # --- 10a: Invariance — the default ---
    print("\n--- 10a: Invariance (default) — exact type match required ---")
    print()
    print("  class Animal: ...")
    print("  class Dog(Animal): ...")
    print()
    print("  dogs: list[Dog] = [Dog()]")
    print("  animals: list[Animal] = dogs   ← pyright ERROR (invariant)")
    print()
    print("  WHY? A list[Animal] could hold a Cat:")
    print("  animals.append(Cat())  ← now dogs contains a Cat!")
    print("  dogs[1].fetch()        ← RuntimeError: Cat has no .fetch()")
    print()
    print("  Mutability requires exact type match (invariance).")
    print("  This is the rule that rejected 'self._words: WordStore'")
    print("  when you tried the Protocol approach on _BaseDictionary.")

    # --- 10b: Covariance — read-only is safe ---
    print("\n--- 10b: Covariance (covariant=True) — for read-only outputs ---")
    print()

    T_co = TypeVar("T_co", covariant=True)

    class ReadOnly(Generic[T_co]):
        """Immutable container — only supports reading, not writing."""

        def __init__(self, value: T_co) -> None:
            self._value = value

        def get(self) -> T_co:
            return self._value

    print("  class ReadOnly(Generic[T_co]):  # covariant")
    print("      def get(self) -> T_co: ...")
    print()
    print("  ReadOnly[Dog] IS a ReadOnly[Animal]   ← safe because read-only")
    print("  You can only GET from ReadOnly — you can't add a Cat to it.")
    print()
    print("  Rule: covariant=True when T only appears in RETURN positions.")
    print("  Most common: return types, Iterator outputs, Producer types.")

    # --- 10c: Contravariance --- 
    print("\n--- 10c: Contravariance (contravariant=True) — for inputs ---")
    print()
    print("  T_contra = TypeVar('T_contra', contravariant=True)")
    print()
    print("  class Handler(Protocol[T_contra]):")
    print("      def handle(self, item: T_contra) -> None: ...")
    print()
    print("  Handler[Animal] IS a Handler[Dog]  ← safe because write-only")
    print("  If you handle ANY Animal, you can certainly handle a Dog.")
    print()
    print("  Rule: contravariant=True when T only appears in PARAMETER positions.")
    print("  Most common: callback parameters, Consumer types.")

    # --- 10d: Practical Stage 1 rule ---
    print("\n--- 10d: Practical rule for Stage 1 ---")
    print()
    print("  Stage 1: use covariant=True in Protocols for read-only outputs.")
    print("  Leave everything else as the default (invariant).")
    print()
    print("  When you'll need contravariance:")
    print("  Stage 2+ when building typed callback systems or event handlers.")
    print()
    print("  Memory aid:")
    print("  INvariant   = IN and OUT  (mutable — must match exactly)")
    print("  COvariant   = OUT only    (read-only — subtype flows UP)")
    print("  CONTRAvariant = IN only   (write-only — subtype flows DOWN)")

    print()


# =============================================================================
# SECTION 11: COMMON PITFALLS AND GOTCHAS
# =============================================================================

def section_11_pitfalls() -> None:
    """Cover the most common TypeVar and Generic mistakes."""
    print("=" * 70)
    print("SECTION 11: COMMON PITFALLS AND GOTCHAS")
    print("=" * 70)

    # --- 11a: TypeVar must be defined at module level ---
    print("\n--- 11a: TypeVar must be defined at MODULE level ---")
    print()
    print("  WRONG — defined inside a function:")
    print("  def my_func():")
    print("      T = TypeVar('T')   ← NEW T per call, not reused")
    print("      def identity(x: T) -> T: ...")
    print()
    print("  CORRECT — defined at module level:")
    print("  T = TypeVar('T')       ← defined ONCE, reused everywhere")
    print("  def identity(x: T) -> T: ...")

    # --- 11b: TypeVar string name must match variable name ---
    print("\n--- 11b: The string name must match the variable name ---")
    print()
    print("  WRONG:")
    print("  T = TypeVar('MyType')  ← variable is T, string is MyType")
    print()
    print("  CORRECT:")
    print("  T = TypeVar('T')       ← both are T ✓")
    print("  WordContainer = TypeVar('WordContainer')  ← both match ✓")

    # --- 11c: Can't use `type` statement with TypeVar ---
    print("\n--- 11c: Python 3.12 `type` statement and TypeVar ---")
    print()
    print("  Python 3.12 introduced the `type` statement for aliases:")
    print("  type RegDecorator = Callable[...]   ← works for simple aliases")
    print()
    print("  BUT: ParamSpec and TypeVar CANNOT be used with `type`.")
    print("  The `type` statement creates isolated scope — breaks TypeVar flow.")
    print()
    print("  WRONG:")
    print("  T = TypeVar('T')")
    print("  type Container = list[T]   ← T is out of scope inside `type`")
    print()
    print("  CORRECT:")
    print("  from typing import TypeAlias")
    print("  T = TypeVar('T')")
    print("  Container: TypeAlias = list[T]   ← TypeAlias works ✓")
    print()
    print("  YOUR CODE uses `type` correctly — only for non-TypeVar aliases:")
    print("  type RegDecorator = Callable[[type[DictionaryProtocol]], ...]  ✓")
    print("  type TimerContainer = dict[str, Any]  ✓")

    # --- 11d: TypeVar constraints vs Union ---
    print("\n--- 11d: TypeVar constraints ≠ Union ---")
    print()
    print("  UNION: can hold BOTH types at once")
    print("  def f(x: set[str] | list[str]) → can mix types in one call")
    print("  f({'a'}) and f(['a']) — each call is independent")
    print()
    print("  TypeVar CONSTRAINTS: T resolves to ONE type per call")
    print("  T = TypeVar('T', set[str], list[str])")
    print("  def f(x: T) -> T — if T=set[str], return must be set[str]")
    print()
    print("  The key difference: constraints LINK input and output types.")
    print("  A union does not — f could take set[str] and return list[str].")

    # --- 11e: Generic class attribute typing ---
    print("\n--- 11e: Class attributes vs instance attributes with Generic ---")
    print()
    print("  Class attributes (shared across instances) are NOT generic:")
    print("  class Box(Generic[T]):")
    print("      count: int = 0        ← OK: not parameterised")
    print("      label: ClassVar[str]  ← OK: ClassVar")
    print("      value: T              ← instance attribute — OK ✓")
    print()
    print("  Don't try to make class-level attributes generic —")
    print("  T doesn't exist at the class level, only at the instance level.")

    # --- 11f: TypeVar in Protocol attributes ---
    print("\n--- 11f: Protocol attributes and variance ---")
    print()
    print("  If a Protocol has a mutable attribute:")
    print("  class HasWords(Protocol):")
    print("      words: list[str]   ← mutable attribute")
    print()
    print("  Subclasses must match EXACTLY (invariance).")
    print("  You cannot say words: list[str] | set[str] in the Protocol.")
    print("  This is the invariance rule — use Generic[W] instead.")

    print()


# =============================================================================
# SECTION 12: DECISION GUIDE AND CHEAT SHEET
# =============================================================================
#
# ┌──────────────────────────────────────────────────────────────────┐
# │                TypeVar / Generic DECISION GUIDE                  │
# │──────────────────────────────────────────────────────────────────│
# │  Situation                              │ Use                    │
# │─────────────────────────────────────────│────────────────────────│
# │  Function takes X, returns same X       │ T = TypeVar("T")       │
# │  Need methods of a base class on T      │ bound=BaseClass        │
# │  Exactly 2-3 unrelated concrete types   │ TypeVar("T", A, B)     │
# │  Class holds value that varies by use   │ Generic[T]             │
# │  Subclass specialises parent's type     │ Parent[ConcreteType]   │
# │  Two independent varying types          │ Generic[K, V]          │
# │  Typed ETL/pipeline stages              │ Generic[I, O]          │
# │  Protocol + varying output type         │ Protocol[T_co]         │
# │  Protocol + varying input type          │ Protocol[T_contra]     │
# │  Mutable attribute with varying type    │ Generic[W] (not Union) │
# └──────────────────────────────────────────────────────────────────┘
#
# ┌──────────────────────────────────────────────────────────────────┐
# │                TYPEVAR CHEAT SHEET                               │
# │──────────────────────────────────────────────────────────────────│
# │  # Unconstrained — any type                                      │
# │  T = TypeVar("T")                                                │
# │                                                                  │
# │  # Upper bound — T must be SomeBase or subclass                  │
# │  T = TypeVar("T", bound=SomeBase)                                │
# │                                                                  │
# │  # Constraints — T must be exactly A or exactly B                │
# │  T = TypeVar("T", A, B)                                          │
# │                                                                  │
# │  # Covariant — for read-only outputs in Protocols                │
# │  T_co = TypeVar("T_co", covariant=True)                          │
# │                                                                  │
# │  # Contravariant — for write-only inputs in Protocols            │
# │  T_contra = TypeVar("T_contra", contravariant=True)              │
# │                                                                  │
# │  # Multiple independent TypeVars                                 │
# │  K = TypeVar("K")                                                │
# │  V = TypeVar("V")                                                │
# └──────────────────────────────────────────────────────────────────┘
#
# ┌──────────────────────────────────────────────────────────────────┐
# │                GENERIC CLASS CHEAT SHEET                         │
# │──────────────────────────────────────────────────────────────────│
# │  from typing import TypeVar, Generic                             │
# │                                                                  │
# │  T = TypeVar("T")                                                │
# │                                                                  │
# │  # Basic Generic class                                           │
# │  class Box(Generic[T]):                                          │
# │      def __init__(self, value: T) -> None:                       │
# │          self.value: T = value                                   │
# │      def get(self) -> T:                                         │
# │          return self.value                                       │
# │                                                                  │
# │  # Generic + ABC (Template Method pattern)                       │
# │  W = TypeVar("W", set[str], list[str])                           │
# │  class Base(ABC, Generic[W]):                                    │
# │      def __init__(self) -> None:                                 │
# │          self._data: W = self._make()                            │
# │      @abstractmethod                                             │
# │      def _make(self) -> W: ...                                   │
# │                                                                  │
# │  class SetBacked(Base[set[str]]):   # W = set[str]               │
# │      def _make(self) -> set[str]: return set()                   │
# │                                                                  │
# │  class ListBacked(Base[list[str]]): # W = list[str]              │
# │      def _make(self) -> list[str]: return []                     │
# └──────────────────────────────────────────────────────────────────┘
#
# ┌──────────────────────────────────────────────────────────────────┐
# │          bound= vs CONSTRAINTS CHEAT SHEET                       │
# │──────────────────────────────────────────────────────────────────│
# │                                                                  │
# │  bound=X                          constraints: A, B              │
# │  ──────────────────────────────   ──────────────────────────────  │
# │  "X or any subclass of X"         "exactly A or exactly B"       │
# │  OPEN hierarchy                   CLOSED list                    │
# │  Future subclasses: automatic     Future subclasses: NO          │
# │  Call X methods on T: YES ✓       Call methods: only shared      │
# │  Use when: types share a base     Use when: unrelated types      │
# │                                                                  │
# │  Example:                         Example:                       │
# │  bound=Animal                     TypeVar("W", set[str], list[str])│
# │  → Dog, Cat, and any future       → ONLY set[str] or list[str]   │
# │    Animal subclass                                               │
# └──────────────────────────────────────────────────────────────────┘
#
# ┌──────────────────────────────────────────────────────────────────┐
# │             YOUR SPELLER TYPEVAR MAP                             │
# │──────────────────────────────────────────────────────────────────│
# │  Location          │ TypeVar                 │ Resolves to        │
# │────────────────────│─────────────────────────│────────────────────│
# │  dictionaries.py   │ WordContainer           │ set[str] or        │
# │  (your code ✓)     │ TypeVar("WordContainer",│ list[str] per      │
# │                    │   set[str], list[str])   │ subclass           │
# │  benchmarks.py     │ P = ParamSpec("P")      │ decorated func     │
# │  (your code ✓)     │ T = TypeVar("T")        │ params / return    │
# └──────────────────────────────────────────────────────────────────┘
#
# ┌──────────────────────────────────────────────────────────────────┐
# │            v8.1 ROADMAP TypeVar PREVIEW                          │
# │──────────────────────────────────────────────────────────────────│
# │  Project       │ TypeVar          │ Pattern                      │
# │────────────────│──────────────────│──────────────────────────────│
# │  DataVault     │ ResponseT        │ LLMProvider[ResponseT]        │
# │  PolicyPulse   │ ChunkT           │ VectorStore[ChunkT]           │
# │  AFC           │ RecordT, SignalT  │ DataSource[RecordT]           │
# │  Stage 2 ETL   │ InputT, OutputT  │ Pipeline[InputT, OutputT]     │
# │  Stage 3 ML    │ InputT, PredT    │ ModelWrapper[InputT, PredT]   │
# │  Stage 4 LLM   │ StateT           │ Memory[StateT]                │
# └──────────────────────────────────────────────────────────────────┘
#
# ┌──────────────────────────────────────────────────────────────────┐
# │                  IMPORT CHEAT SHEET                              │
# │──────────────────────────────────────────────────────────────────│
# │  from typing import TypeVar         # type-level variable        │
# │  from typing import Generic         # parameterise a class       │
# │  from typing import TypeAlias       # named alias (not TypeVar)  │
# │  from abc import ABC, abstractmethod# Generic + ABC together     │
# │                                                                  │
# │  # Python 3.12+ syntax (PEP 695) — for type aliases ONLY:       │
# │  type MyAlias = list[str]           # OK — no TypeVar involved   │
# │  type RegDecorator = Callable[...]  # OK — no TypeVar involved   │
# │  # Do NOT use `type` with TypeVar or ParamSpec                   │
# └──────────────────────────────────────────────────────────────────┘
#
# =============================================================================


# =============================================================================
# MAIN EXECUTION
# =============================================================================

if __name__ == "__main__":
    section_1_the_problem()
    section_2_typevar_basics()
    section_3_bound()
    section_4_constraints()
    section_5_bound_vs_constraints()
    section_6_generic_classes()
    section_7_generic_hierarchy()
    section_8_multiple_typevars()
    section_9_generic_protocol()
    section_10_variance()
    section_11_pitfalls()

    print("=" * 70)
    print("REFERENCE COMPLETE — See Section 12 (cheat sheets) in source code")
    print("=" * 70)
