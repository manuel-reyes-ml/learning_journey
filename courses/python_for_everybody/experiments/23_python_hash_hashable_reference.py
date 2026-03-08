"""
python_hash_hashable_reference.py
==================================

Personal reference: Python's hash system, hashable protocol, and
how it connects to dictionaries, sets, and data structures.

Topics covered
--------------
1. What is hash() — the fingerprint function
2. Why Python needs hashing — dictionary/set internals
3. Hashable vs unhashable — the mutability rule
4. The __hash__ and __eq__ contract
5. Hashing in your data structures — NamedTuple, dataclass, frozen
6. Custom __hash__ — when and how to implement it
7. Common pitfalls and gotchas
8. Production patterns from your roadmap

Why this matters for your roadmap
----------------------------------
- Stage 1: Your Pixel and ImageSize NamedTuples are hashable — that's
  why they work as dict keys and in sets. Your FilterInfo dataclass is
  NOT hashable (mutable) — that's fine because it's a dict value.
  Understanding this prevents silent bugs.
- Stage 2+: When building data pipelines, you'll use sets for
  deduplication, frozensets for immutable collections, and dicts
  everywhere. Knowing what can be a key and what can't saves hours
  of debugging TypeError: unhashable type.
- Stage 3-5: ML feature engineering, caching with @lru_cache (requires
  hashable args), and LangChain state management all depend on this.

How to use this file
---------------------
Run it directly to see all output::

    $ python python_hash_hashable_reference.py

Or import individual sections to experiment in a REPL.

References
----------
.. [1] Python Data Model: https://docs.python.org/3/reference/datamodel.html#object.__hash__
.. [2] Python Glossary — hashable: https://docs.python.org/3/glossary.html#term-hashable
.. [3] Fluent Python, Ch. 3 — Dicts and Sets (Ramalho)
.. [4] Effective Python, Item 43 — Custom Containers (Slatkin)
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import NamedTuple, Final
from functools import lru_cache


# =============================================================================
# SECTION 1: WHAT IS hash() — THE FINGERPRINT FUNCTION
# =============================================================================
#
# hash() is a built-in function that takes an object and returns
# a fixed integer. Think of it as a FINGERPRINT — a compact ID
# that represents the object.
#
# KEY PROPERTIES:
#   1. DETERMINISTIC — same object always returns the same integer
#      within a single Python session
#   2. FAST — computed in constant time O(1), regardless of
#      object size
#   3. ONE-WAY — you can't reconstruct the object from its hash
#   4. SESSION-DEPENDENT — hash("blur") may return different ints
#      across different Python sessions (security feature since 3.3)
#
# MENTAL MODEL:
# ┌──────────────────────────────────────────────────┐
# │  Object          hash()         Integer          │
# │  ──────          ──────         ───────          │
# │  "blur"     →    hash()    →   3487529384       │
# │  "blur"     →    hash()    →   3487529384  ✅   │
# │  "edges"    →    hash()    →   -238745102       │
# │  42         →    hash()    →   42               │
# │  (1, 2, 3)  →    hash()    →   529344067        │
# │  [1, 2, 3]  →    hash()    →   TypeError! ❌    │
# └──────────────────────────────────────────────────┘
#
# =============================================================================


def section_1_what_is_hash() -> None:
    """
    Demonstrate basic hash() behavior on different types.

    Shows that hash is deterministic within a session, works on
    immutable types, and fails on mutable types.
    """
    print("=" * 70)
    print("SECTION 1: WHAT IS hash() — THE FINGERPRINT FUNCTION")
    print("=" * 70)

    # ── Strings ─────────────────────────────────────────────────
    # Same string always produces the same hash (within one session)
    h1 = hash("blur")
    h2 = hash("blur")

    print(f"\n── Strings ──")
    print(f"  hash('blur')   = {h1}")
    print(f"  hash('blur')   = {h2}")
    print(f"  Same hash?       {h1 == h2}")  # Always True

    # Different strings produce different hashes (almost always)
    h3 = hash("edges")
    print(f"  hash('edges')  = {h3}")
    print(f"  'blur' == 'edges'? {h1 == h3}")  # False

    # ── Integers ────────────────────────────────────────────────
    # Small integers hash to themselves (CPython optimization)
    print(f"\n── Integers ──")
    print(f"  hash(0)   = {hash(0)}")
    print(f"  hash(1)   = {hash(1)}")
    print(f"  hash(42)  = {hash(42)}")
    print(f"  hash(-1)  = {hash(-1)}")  # Special case: -1 → -2 in CPython

    # ── Tuples ──────────────────────────────────────────────────
    # Tuples are hashable because they're immutable
    print(f"\n── Tuples ──")
    print(f"  hash((1, 2, 3))       = {hash((1, 2, 3))}")
    print(f"  hash(('a', 'b', 'c')) = {hash(('a', 'b', 'c'))}")

    # ── Booleans ────────────────────────────────────────────────
    # Bools are a subclass of int: True == 1, False == 0
    print(f"\n── Booleans (subclass of int) ──")
    print(f"  hash(True)  = {hash(True)}")
    print(f"  hash(False) = {hash(False)}")
    print(f"  hash(True) == hash(1)? {hash(True) == hash(1)}")  # True!

    # ── None ────────────────────────────────────────────────────
    print(f"\n── None ──")
    print(f"  hash(None) = {hash(None)}")

    # ── Mutable types FAIL ──────────────────────────────────────
    print(f"\n── Mutable types (UNHASHABLE) ──")
    for obj, name in [([1, 2], "list"), ({"a": 1}, "dict"), ({1, 2}, "set")]:
        try:
            hash(obj)
        except TypeError as e:
            print(f"  hash({name}) → TypeError: {e}")


# =============================================================================
# SECTION 2: WHY PYTHON NEEDS HASHING — DICT/SET INTERNALS
# =============================================================================
#
# Dictionaries and sets use a data structure called a HASH TABLE.
# The hash value is used as an INDEX to jump directly to the right
# slot in memory, instead of scanning every item.
#
# HOW dict["blur"] WORKS:
# ┌──────────────────────────────────────────────────────────────┐
# │                                                              │
# │  FILTERS["blur"]                                             │
# │                                                              │
# │  Step 1: Compute hash("blur") → 3487529384                  │
# │  Step 2: Convert to slot index → 3487529384 % table_size    │
# │  Step 3: Jump directly to that slot → O(1) lookup!          │
# │                                                              │
# │  WITHOUT hashing (scanning a list):                          │
# │  Step 1: Check index 0 → "grayscale"? No.                   │
# │  Step 2: Check index 1 → "reflect"? No.                     │
# │  Step 3: Check index 2 → "blur"? Yes! → O(n) lookup         │
# │                                                              │
# │  With 6 filters: barely noticeable difference.               │
# │  With 1 million entries: O(1) vs O(n) is HUGE.              │
# └──────────────────────────────────────────────────────────────┘
#
# This is why:
#   - dict KEYS must be hashable (they're used as slot indices)
#   - dict VALUES don't need to be hashable (they're just stored)
#   - set ITEMS must be hashable (a set IS a hash table of keys)
#
# =============================================================================


def section_2_why_hashing_matters() -> None:
    """
    Show the performance difference between hash-based and
    scan-based lookups, and demonstrate the key vs value rule.
    """
    print("\n" + "=" * 70)
    print("SECTION 2: WHY PYTHON NEEDS HASHING — DICT/SET INTERNALS")
    print("=" * 70)

    # ── Dict keys must be hashable, values don't ────────────────
    print(f"\n── Dict: keys vs values ──")

    # This works: string key (hashable), list value (unhashable is OK)
    valid_dict = {"filters": [1, 2, 3]}
    print(f"  String key, list value:  {valid_dict}  ✅")

    # This works: tuple key (hashable)
    coords = {(0, 0): "origin", (1, 2): "point_a"}
    print(f"  Tuple keys:              {coords}  ✅")

    # This FAILS: list key (unhashable)
    try:
        bad_dict = {[1, 2]: "value"}  # type: ignore[unhashable-type]
    except TypeError as e:
        print(f"  List as key:             TypeError: {e}  ❌")

    # ── Sets require hashable items ─────────────────────────────
    print(f"\n── Sets: all items must be hashable ──")

    valid_set = {"blur", "edges", "grayscale"}
    print(f"  Set of strings:  {valid_set}  ✅")

    try:
        bad_set = {[1, 2], [3, 4]}  # type: ignore[unhashable-type]
    except TypeError as e:
        print(f"  Set of lists:    TypeError: {e}  ❌")

    # ── Performance: dict lookup vs list scan ───────────────────
    import time

    # Build a large dict and list with the same data
    # 100_000 = 100,000 using underscore as a separator, readability convention (PEP 515)
    large_dict = {f"key_{i}": i for i in range(100_000)}
    large_list = [(f"key_{i}", i) for i in range(100_000)]

    # Dict lookup: O(1) — jumps directly to slot
    start = time.perf_counter()
    for _ in range(1000):
        _ = large_dict["key_99999"]
    dict_time = time.perf_counter() - start

    # List scan: O(n) — checks every pair
    start = time.perf_counter()
    for _ in range(1000):
        for k, v in large_list:
            if k == "key_99999":
                break
    list_time = time.perf_counter() - start

    print(f"\n── Performance: 1000 lookups in 100K entries ──")
    print(f"  Dict (hash-based): {dict_time:.4f}s")
    print(f"  List (scanning):   {list_time:.4f}s")
    print(f"  Dict is {list_time / dict_time:.0f}x faster")


# =============================================================================
# SECTION 3: HASHABLE vs UNHASHABLE — THE MUTABILITY RULE
# =============================================================================
#
# THE RULE:
# ┌──────────────────────────────────────────────────────────────┐
# │  If an object CAN CHANGE    → NOT hashable (mutable)        │
# │  If an object CANNOT CHANGE → hashable     (immutable)      │
# └──────────────────────────────────────────────────────────────┘
#
# WHY? If Python hashes [1, 2, 3] and stores it at slot 42,
# then you append 4 making it [1, 2, 3, 4], the hash changes.
# Python would look for it at a NEW slot and never find the
# original. The data structure is now silently corrupted.
#
# HASHABLE TYPES:           UNHASHABLE TYPES:
# ─────────────────         ──────────────────
# int, float, complex       list
# str                       dict
# bytes                     set
# tuple (if contents        bytearray
#   are all hashable)
# frozenset
# None, bool
# NamedTuple
# frozen dataclass
#
# =============================================================================


def section_3_hashable_vs_unhashable() -> None:
    """
    Comprehensive test of which built-in types are hashable.

    Includes the critical edge case: tuples containing mutable
    objects are NOT hashable even though tuples are immutable.
    """
    print("\n" + "=" * 70)
    print("SECTION 3: HASHABLE vs UNHASHABLE — THE MUTABILITY RULE")
    print("=" * 70)

    # ── Test every common type ──────────────────────────────────
    test_objects = [
        # (object, label, expected)
        (42,                    "int",              True),
        (3.14,                  "float",            True),
        ("blur",                "str",              True),
        (b"bytes",              "bytes",            True),
        (True,                  "bool",             True),
        (None,                  "None",             True),
        ((1, 2, 3),             "tuple(ints)",      True),
        (("a", "b"),            "tuple(strs)",      True),
        (frozenset({1, 2}),     "frozenset",        True),
        ([1, 2, 3],             "list",             False),
        ({"a": 1},              "dict",             False),
        ({1, 2, 3},             "set",              False),
        (bytearray(b"hi"),      "bytearray",        False),
    ]

    print(f"\n── Built-in types ──")
    for obj, label, expected in test_objects:
        try:
            h = hash(obj)
            status = "✅ hashable"
            result = True
        except TypeError:
            status = "❌ unhashable"
            result = False

        check = "✓" if result == expected else "UNEXPECTED!"
        print(f"  {label:<18} {status}  {check}")

    # ── CRITICAL EDGE CASE: tuple containing mutable objects ────
    # A tuple is immutable, but if it CONTAINS a mutable object,
    # the hash would depend on the mutable object's contents.
    # Python prevents this by making the whole tuple unhashable.
    print(f"\n── Edge case: tuple containing a list ──")

    safe_tuple = (1, 2, "hello")
    print(f"  (1, 2, 'hello')     → hash = {hash(safe_tuple)}  ✅")

    dangerous_tuple = (1, 2, [3, 4])
    try:
        hash(dangerous_tuple)
    except TypeError as e:
        print(f"  (1, 2, [3, 4])      → TypeError: {e}  ❌")
    # The TUPLE itself is immutable, but its third element (a list)
    # is mutable. Since the hash would depend on [3, 4]'s contents,
    # which could change, Python rejects the entire tuple.

    # ── frozenset: the hashable alternative to set ──────────────
    print(f"\n── frozenset: immutable set ──")
    fs = frozenset({1, 2, 3})
    print(f"  frozenset({{1, 2, 3}}) → hash = {hash(fs)}  ✅")
    print(f"  Can be a dict key:  {{{fs}: 'value'}}  ✅")

    # This is useful when you need a set AS a dictionary key:
    # e.g., mapping a combination of filters to a cached result
    cache: dict[frozenset[str], str] = {
        frozenset({"blur", "edges"}): "blur_edges_result",
        frozenset({"grayscale"}): "grayscale_result",
    }
    print(f"  Filter combo cache: {cache}")


# =============================================================================
# SECTION 4: THE __hash__ AND __eq__ CONTRACT
# =============================================================================
#
# Python's hashable protocol requires TWO methods:
#   __hash__()  → returns the integer hash value
#   __eq__()    → defines equality comparison (==)
#
# THE CONTRACT (must ALWAYS hold):
# ┌──────────────────────────────────────────────────────────────┐
# │  If a == b, then hash(a) MUST equal hash(b)                 │
# │                                                              │
# │  But: hash(a) == hash(b) does NOT mean a == b               │
# │  (this is called a "hash collision" — different objects      │
# │   can share the same hash, Python handles it internally)     │
# └──────────────────────────────────────────────────────────────┘
#
# WHY THIS MATTERS:
# When Python looks up dict[key], it first checks hash(key) to
# find the slot, then uses == to confirm it's the right object.
# If you break the contract (equal objects with different hashes),
# dict lookups silently fail.
#
# PYTHON'S DEFAULT BEHAVIOR FOR CLASSES:
#   - __hash__ = based on id() (memory address)
#   - __eq__   = identity comparison (a is b)
#   - If you define __eq__ without __hash__, Python sets
#     __hash__ = None (making the class unhashable!)
#
# =============================================================================


def section_4_hash_eq_contract() -> None:
    """
    Show the relationship between __hash__ and __eq__, and what
    happens when you define one without the other.
    """
    print("\n" + "=" * 70)
    print("SECTION 4: THE __hash__ AND __eq__ CONTRACT")
    print("=" * 70)

    # ── Equal objects must have equal hashes ────────────────────
    print(f"\n── The contract: a == b → hash(a) == hash(b) ──")
    a = "blur"
    b = "blur"
    print(f"  a = 'blur', b = 'blur'")
    print(f"  a == b:          {a == b}")
    print(f"  hash(a) == hash(b): {hash(a) == hash(b)}")  # Must be True

    # ── Hash collisions are allowed ─────────────────────────────
    # Different objects CAN have the same hash (collision)
    # Python handles this internally with "open addressing"
    print(f"\n── Collisions: same hash ≠ same object ──")
    print(f"  hash(0)   = {hash(0)}")
    print(f"  hash(0.0) = {hash(0.0)}")
    print(f"  0 == 0.0:    {0 == 0.0}")      # True (int and float compare equal)
    zero_int, zero_float = 0, 0.0
    print(f"  0 is 0.0:    {zero_int is zero_float}")  # False (different objects)

    # ── Class with __eq__ only → becomes unhashable ─────────────
    print(f"\n── Defining __eq__ without __hash__ ──")

    class PixelBroken:
        """Defining __eq__ makes Python set __hash__ = None."""
        def __init__(self, r: int, g: int, b: int) -> None:
            self.r = r
            self.g = g
            self.b = b

        def __eq__(self, other: object) -> bool:
            if not isinstance(other, PixelBroken):
                return NotImplemented
            return (self.r, self.g, self.b) == (other.r, other.g, other.b)
        # No __hash__ defined!

    px = PixelBroken(100, 150, 200)
    print(f"  PixelBroken.__hash__ is None: {PixelBroken.__hash__ is None}")
    try:
        hash(px)
    except TypeError as e:
        print(f"  hash(PixelBroken) → TypeError: {e}")
    # Python does this ON PURPOSE to protect you. If two objects
    # compare equal but have different hashes, dicts break silently.
    # By removing __hash__, Python forces you to think about it.

    # ── Class with BOTH __eq__ and __hash__ → hashable ──────────
    print(f"\n── Defining both __eq__ and __hash__ ──")

    class PixelFixed:
        """Both methods defined — hashable and correct."""
        def __init__(self, r: int, g: int, b: int) -> None:
            self.r = r
            self.g = g
            self.b = b

        def __eq__(self, other: object) -> bool:
            if not isinstance(other, PixelFixed):
                return NotImplemented
            return (self.r, self.g, self.b) == (other.r, other.g, other.b)

        def __hash__(self) -> int:
            # Hash the same tuple used in __eq__ to satisfy the contract
            return hash((self.r, self.g, self.b))

    px1 = PixelFixed(100, 150, 200)
    px2 = PixelFixed(100, 150, 200)
    print(f"  px1 == px2:            {px1 == px2}")
    print(f"  hash(px1) == hash(px2): {hash(px1) == hash(px2)}")
    print(f"  Can use as dict key:   {{{px1}: 'red-ish'}}  ✅")
    print(f"  Can put in set:        {{{px1, px2}}}  (deduped: {len({px1, px2})} item)")


# =============================================================================
# SECTION 5: HASHING IN YOUR DATA STRUCTURES
# =============================================================================
#
# How each structure in your bmp_config.py handles hashing:
#
# ┌─────────────────────────────────────────────────────────────┐
# │  Structure           │ Hashable? │ Why?                     │
# │──────────────────────│───────────│──────────────────────────│
# │  Pixel (NamedTuple)  │ ✅ Yes    │ Immutable by design      │
# │  ImageSize (Named..) │ ✅ Yes    │ Immutable by design      │
# │  BmpData (Named..)   │ ❌ No*    │ Contains list (pixels)   │
# │  BmpDirectories      │ ✅ Yes    │ frozen=True dataclass    │
# │  BmpConstants        │ ✅ Yes    │ frozen=True dataclass    │
# │  FilterInfo          │ ❌ No     │ Regular (mutable) DC     │
# │  ExitCode (IntEnum)  │ ✅ Yes    │ Enums are immutable      │
# │  BrightDarkFilter    │ ✅ Yes    │ IntEnum, immutable       │
# └─────────────────────────────────────────────────────────────┘
#
# *BmpData is a NamedTuple but one of its fields (pixels) is a
#  list of lists — so hash(BmpData) would raise TypeError.
#  Same edge case as tuple-containing-a-list from Section 3.
#
# =============================================================================


def section_5_your_data_structures() -> None:
    """
    Demonstrate hashability of structures matching your BMP project.

    Uses simplified versions of your actual config types to show
    why NamedTuple, frozen dataclass, and regular dataclass behave
    differently.
    """
    print("\n" + "=" * 70)
    print("SECTION 5: HASHING IN YOUR DATA STRUCTURES")
    print("=" * 70)

    # ── NamedTuple: hashable by default ─────────────────────────
    class Pixel(NamedTuple):
        b: int
        g: int
        r: int

    class ImageSize(NamedTuple):
        height: int
        width: int

    px = Pixel(100, 150, 200)
    size = ImageSize(480, 640)

    print(f"\n── NamedTuple (always hashable) ──")
    print(f"  hash(Pixel(100, 150, 200))   = {hash(px)}  ✅")
    print(f"  hash(ImageSize(480, 640))    = {hash(size)}  ✅")

    # You can use Pixels as dict keys or in sets
    color_names = {Pixel(0, 0, 0): "black", Pixel(255, 255, 255): "white"}
    print(f"  Pixel as dict key: {color_names}")

    # Deduplication with sets
    pixels = [Pixel(0, 0, 0), Pixel(255, 0, 0), Pixel(0, 0, 0)]
    unique = set(pixels)
    print(f"  3 pixels, 2 unique: {unique}")

    # ── NamedTuple with mutable field: BREAKS ───────────────────
    class BmpData(NamedTuple):
        size: ImageSize
        pixels: list  # list is mutable!

    bmp = BmpData(size=ImageSize(2, 2), pixels=[[1, 2], [3, 4]])
    print(f"\n── NamedTuple with mutable field ──")
    try:
        hash(bmp)
    except TypeError as e:
        print(f"  hash(BmpData) → TypeError: {e}  ❌")
    print(f"  BmpData contains a list → entire NamedTuple unhashable")

    # ── frozen dataclass: hashable ──────────────────────────────
    @dataclass(frozen=True, slots=True)
    class BmpConstants:
        HEADER_SIZE: int = 14
        SIGNATURE: bytes = b"BM"
        PIXEL_SIZE: int = 3

    consts = BmpConstants()
    print(f"\n── frozen dataclass ──")
    print(f"  hash(BmpConstants()) = {hash(consts)}  ✅")
    # frozen=True makes all attributes read-only AND auto-generates
    # __hash__ based on all fields. This is why your BmpDirectories
    # and BmpConstants are both hashable.

    # ── Regular dataclass: NOT hashable ─────────────────────────
    @dataclass
    class FilterInfo:
        func: object
        name: str
        description: str

    info = FilterInfo(func=lambda x: x, name="blur", description="Apply blur")
    print(f"\n── Regular dataclass ──")
    try:
        hash(info)
    except TypeError as e:
        print(f"  hash(FilterInfo) → TypeError: {e}  ❌")
    print(f"  Regular dataclass has __eq__ but __hash__ = None")
    print(f"  This is fine — FilterInfo is a dict VALUE, not a KEY")

    # ── Enum: always hashable ───────────────────────────────────
    from enum import IntEnum

    class ExitCode(IntEnum):
        SUCCESS = 0
        FAILURE = 1

    print(f"\n── IntEnum ──")
    print(f"  hash(ExitCode.SUCCESS) = {hash(ExitCode.SUCCESS)}  ✅")
    print(f"  hash(ExitCode.FAILURE) = {hash(ExitCode.FAILURE)}  ✅")
    # Enums are singletons — each value exists exactly once.
    # They're immutable and always hashable.


# =============================================================================
# SECTION 6: CUSTOM __hash__ — WHEN AND HOW
# =============================================================================
#
# WHEN to implement __hash__:
#   - You need instances as dict keys or in sets
#   - You need @lru_cache on a method (requires hashable self)
#   - You're building a custom immutable data structure
#
# WHEN NOT to:
#   - NamedTuple / frozen dataclass already handle it for you
#   - The object is mutable (don't force it — redesign instead)
#   - You only need equality, not dict/set membership
#
# THE RECIPE:
#   1. Make __hash__ return hash() of a tuple of the SAME fields
#      used in __eq__
#   2. Only include fields that define the object's identity
#   3. Exclude mutable fields or fields not used in __eq__
#
# =============================================================================


def section_6_custom_hash() -> None:
    """
    Show when and how to implement __hash__ correctly.

    Includes the lru_cache use case relevant to Stage 3+ caching.
    """
    print("\n" + "=" * 70)
    print("SECTION 6: CUSTOM __hash__ — WHEN AND HOW")
    print("=" * 70)

    # ── The recipe: hash the same fields as __eq__ ──────────────
    class Color:
        """Immutable color with custom hash for set/dict usage."""
        def __init__(self, r: int, g: int, b: int) -> None:
            self.r = r
            self.g = g
            self.b = b

        def __eq__(self, other: object) -> bool:
            if not isinstance(other, Color):
                return NotImplemented
            return (self.r, self.g, self.b) == (other.r, other.g, other.b)

        def __hash__(self) -> int:
            # SAME fields as __eq__ — this satisfies the contract
            return hash((self.r, self.g, self.b))

        def __repr__(self) -> str:
            return f"Color({self.r}, {self.g}, {self.b})"

    red1 = Color(255, 0, 0)
    red2 = Color(255, 0, 0)
    blue = Color(0, 0, 255)

    print(f"\n── Custom hashable class ──")
    print(f"  red1 == red2:  {red1 == red2}")
    print(f"  As set:        {{{red1, red2, blue}}}  (2 unique)")
    print(f"  As dict key:   {{{red1}: 'warm', {blue}: 'cool'}}")

    # ── dataclass with unsafe_hash ──────────────────────────────
    # If you MUST have a hashable mutable dataclass (rare, be careful)
    # you can use unsafe_hash=True. Python generates __hash__ but
    # warns you: if you mutate fields after using it as a key, BAD THINGS.
    @dataclass(unsafe_hash=True)
    class UnsafeConfig:
        name: str
        value: int

    cfg = UnsafeConfig("threshold", 50)
    print(f"\n── unsafe_hash=True (use with caution) ──")
    print(f"  hash(UnsafeConfig) = {hash(cfg)}  ⚠️")
    print(f"  Works as key: {{{cfg}: 'data'}}  ⚠️")
    print(f"  BUT: if you mutate cfg.value, dict lookups BREAK silently!")

    # ── @lru_cache requires hashable arguments ──────────────────
    # This is why hashability matters for Stage 3 ML caching
    print(f"\n── @lru_cache and hashability ──")

    @lru_cache(maxsize=128)
    def expensive_lookup(color: Color) -> str:
        """Cached function — requires hashable arg."""
        return f"Processed {color}"

    result = expensive_lookup(Color(255, 0, 0))
    print(f"  expensive_lookup(Color(255,0,0)) = {result!r}")
    print(f"  Cache info: {expensive_lookup.cache_info()}")

    # If Color wasn't hashable, this would raise:
    # TypeError: unhashable type: 'Color'


# =============================================================================
# SECTION 7: COMMON PITFALLS AND GOTCHAS
# =============================================================================


def section_7_pitfalls() -> None:
    """
    Show the most common hash-related bugs and how to avoid them.
    """
    print("\n" + "=" * 70)
    print("SECTION 7: COMMON PITFALLS AND GOTCHAS")
    print("=" * 70)

    # ── Pitfall 1: Mutable default in set/dict ──────────────────
    print(f"\n── Pitfall 1: Trying to use a list as a dict key ──")
    print(f"  Fix: Convert to tuple first")
    filters_applied = ["blur", "edges"]
    # bad:  cache = {filters_applied: result}     → TypeError
    # good: cache = {tuple(filters_applied): "result"}
    cache = {tuple(filters_applied): "result"}
    print(f"  tuple(list) as key: {cache}  ✅")

    # ── Pitfall 2: Hash changes across sessions ─────────────────
    # Since Python 3.3, string hashes are randomized per session
    # (PYTHONHASHSEED environment variable). Never persist hash
    # values to disk or send them across processes.
    print(f"\n── Pitfall 2: Hash randomization ──")
    print(f"  hash('blur') this session = {hash('blur')}")
    print(f"  This number WILL CHANGE next time you run Python!")
    print(f"  NEVER store hash() values in files or databases.")
    print(f"  Use hashlib for persistent hashing instead.")

    # ── Pitfall 3: Mutating after insertion ─────────────────────
    print(f"\n── Pitfall 3: Mutating an object after using it as key ──")

    class MutablePoint:
        def __init__(self, x: int, y: int) -> None:
            self.x = x
            self.y = y

        def __hash__(self) -> int:
            return hash((self.x, self.y))

        def __eq__(self, other: object) -> bool:
            if not isinstance(other, MutablePoint):
                return NotImplemented
            return (self.x, self.y) == (other.x, other.y)

    p = MutablePoint(1, 2)
    data = {p: "original"}
    print(f"  Before mutation: data[p] = {data[p]!r}")

    p.x = 99  # Mutate AFTER inserting as key!
    try:
        _ = data[p]
        print(f"  After mutation:  data[p] found")
    except KeyError:
        print(f"  After mutation:  KeyError! Object is 'lost' in dict ❌")
        print(f"  Hash changed from hash((1,2)) to hash((99,2))")
        print(f"  Python looks in the wrong slot and can't find it.")

    # The fix: use frozen/immutable objects as keys (NamedTuple,
    # frozen dataclass). They CAN'T be mutated, preventing this bug.

    # ── Pitfall 4: int/float/bool equality surprises ────────────
    print(f"\n── Pitfall 4: 0, 0.0, False are all 'equal' ──")
    d: dict[int | float | bool, str] = {}
    d[0] = "zero"
    d[0.0] = "float zero"   # Overwrites! Because 0 == 0.0
    d[False] = "false"       # Overwrites again! Because False == 0
    print(f"  d[0], d[0.0], d[False] all point to: {d[0]!r}")
    print(f"  Dict has {len(d)} entry, not 3")


# =============================================================================
# SECTION 8: QUICK REFERENCE CHEAT SHEET
# =============================================================================
#
# ┌─────────────────────────────────────────────────────────────────┐
# │  TYPE               │ HASHABLE? │ CAN BE DICT KEY? │ IN SET?   │
# │─────────────────────│───────────│──────────────────│───────────│
# │  int, float, bool   │ ✅        │ ✅               │ ✅        │
# │  str                │ ✅        │ ✅               │ ✅        │
# │  bytes              │ ✅        │ ✅               │ ✅        │
# │  tuple (all hashable│ ✅        │ ✅               │ ✅        │
# │    contents)        │           │                  │           │
# │  tuple (with list)  │ ❌        │ ❌               │ ❌        │
# │  frozenset          │ ✅        │ ✅               │ ✅        │
# │  None               │ ✅        │ ✅               │ ✅        │
# │  NamedTuple         │ ✅*       │ ✅*              │ ✅*       │
# │  frozen dataclass   │ ✅        │ ✅               │ ✅        │
# │  regular dataclass  │ ❌        │ ❌               │ ❌        │
# │  Enum / IntEnum     │ ✅        │ ✅               │ ✅        │
# │  list               │ ❌        │ ❌               │ ❌        │
# │  dict               │ ❌        │ ❌               │ ❌        │
# │  set                │ ❌        │ ❌               │ ❌        │
# │  bytearray          │ ❌        │ ❌               │ ❌        │
# └─────────────────────────────────────────────────────────────────┘
# * NamedTuple is hashable only if ALL its fields are hashable.
#
# DECISION GUIDE:
# ┌──────────────────────────────────────────────────────────────┐
# │ Need to...                     │ Use                         │
# │────────────────────────────────│─────────────────────────────│
# │ Use as dict key or in set      │ NamedTuple or frozen DC     │
# │ Store as dict value only       │ Regular dataclass is fine   │
# │ Make a set of sets             │ frozenset                   │
# │ Cache function results         │ @lru_cache (hashable args)  │
# │ Deduplicate a list             │ set() (if items hashable)   │
# │ Convert list → hashable        │ tuple(my_list)              │
# │ Convert set → hashable         │ frozenset(my_set)           │
# │ Convert dict → hashable        │ tuple(d.items()) (approx.)  │
# └──────────────────────────────────────────────────────────────┘
#
# =============================================================================


# =============================================================================
# MAIN EXECUTION
# =============================================================================

if __name__ == "__main__":
    section_1_what_is_hash()
    section_2_why_hashing_matters()
    section_3_hashable_vs_unhashable()
    section_4_hash_eq_contract()
    section_5_your_data_structures()
    section_6_custom_hash()
    section_7_pitfalls()

    print("\n" + "=" * 70)
    print("REFERENCE COMPLETE — See Section 8 (cheat sheet) in source code")
    print("=" * 70)
