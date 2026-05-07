"""
python_search_algorithms_reference.py
=======================================

Personal reference: Python Search Algorithms and Sorting Utilities —
bisect, heapq, sorted, Counter, difflib, and the stdlib tools for
finding, ranking, and organizing data efficiently.

Topics covered
--------------
1.  Linear vs Binary Search — O(n) vs O(log n) fundamentals
2.  bisect — Binary search in sorted lists
3.  heapq — Priority queues and top-N problems
4.  sorted() and key functions — Custom sorting
5.  collections.Counter — Frequency counting and ranking
6.  difflib — Fuzzy matching and similarity search
7.  functools.lru_cache — Memoized search (caching results)
8.  Algorithm Complexity Cheat Sheet — Big-O reference
9.  Decision Guide — Which tool for which problem

Why this matters for your roadmap (v8.1 GenAI-First)
------------------------------------------------------
- Stage 1 (Speller):     bisect for SortedListDictionary benchmark
                          Counter for misspelled word frequency analysis
                          sorted() for report ordering
- Stage 1 (DataVault):   heapq for top-N query results
                          Counter for token usage tracking
                          difflib for fuzzy column name matching
- Stage 1 (PolicyPulse): difflib for fuzzy question matching
                          heapq for top-K chunk retrieval ranking
                          sorted() with key= for relevance ordering
- Stage 1 (FormSense):   difflib for fuzzy field name matching
                          Counter for field type frequency
- Stage 1 (AFC):         bisect for time-series price lookups
                          heapq for top-N/bottom-N stock screening
                          sorted() for portfolio ranking
- Stage 2 (Data Eng):    heapq.merge for sorted stream merging
                          bisect for partition boundary lookups
- Stage 3 (ML):          heapq for K-nearest neighbors (concept)
                          sorted() for feature importance ranking
                          Counter for class distribution analysis
- Stage 4 (LLM):         Counter for token frequency / vocabulary
                          difflib for RAG deduplication
                          lru_cache for embedding cache
- Stage 5 (Senior):      All patterns in production LLMOps systems

How to use this file
---------------------
Run it directly to see all output::

    $ python python_search_algorithms_reference.py

Or import individual sections to experiment in a REPL::

    >>> from python_search_algorithms_reference import (
    ...     section_2_bisect
    ... )

Author: Manuel Reyes — CS50 Speller / Stage 1 Learning Reference
Version: 1.0.0 — March 2026

References
----------
.. [1] Python Docs — bisect
   https://docs.python.org/3/library/bisect.html
.. [2] Python Docs — heapq
   https://docs.python.org/3/library/heapq.html
.. [3] Python Docs — difflib
   https://docs.python.org/3/library/difflib.html
.. [4] Python Docs — collections.Counter
   https://docs.python.org/3/library/collections.html#collections.Counter
.. [5] Python Docs — functools.lru_cache
   https://docs.python.org/3/library/functools.html#functools.lru_cache
"""

from __future__ import annotations

import bisect
import difflib
import heapq
import time
from collections import Counter
from dataclasses import dataclass
from functools import lru_cache


# =============================================================================
# SECTION 1: LINEAR vs BINARY SEARCH — The Fundamental Tradeoff
# =============================================================================
# ┌─────────────────────────────────────────────────────────────────┐
# │         WHY SEARCH ALGORITHM CHOICE MATTERS                     │
# │─────────────────────────────────────────────────────────────────│
# │                                                                 │
# │  Data size      │ Linear O(n)    │ Binary O(log n) │ Hash O(1) │
# │─────────────────│────────────────│─────────────────│───────────│
# │  100 items      │ 100 checks     │ 7 checks        │ 1 check  │
# │  1,000 items    │ 1,000 checks   │ 10 checks       │ 1 check  │
# │  143,091 items  │ 143,091 checks │ 17 checks       │ 1 check  │
# │  1,000,000      │ 1,000,000      │ 20 checks       │ 1 check  │
# │                 │                │                 │          │
# │  REQUIREMENT:   │ None           │ SORTED data     │ Hashable │
# │                 │ Works on any   │ Must be sorted  │ keys     │
# │                 │ list/sequence  │ BEFORE searching│ (set/dict)│
# │                 │                │                 │          │
# │  YOUR SPELLER:  │ ListDictionary │ SortedListDict  │ HashTable│
# │                 │ O(n) per check │ O(log n)        │ O(1)     │
# └─────────────────────────────────────────────────────────────────┘

def section_1_linear_vs_binary() -> None:
    """Compare linear and binary search performance."""
    print("=" * 70)
    print("SECTION 1: LINEAR vs BINARY SEARCH")
    print("=" * 70)

    # --- 1a: Linear search — check every item ---
    print("\n--- 1a: Linear search — O(n) ---")

    data = list(range(100_000))  # sorted list of 100K numbers
    target = 99_999             # worst case: last element

    start = time.perf_counter()
    found = target in data      # Python's 'in' on list = linear scan
    linear_time = time.perf_counter() - start

    print(f"  Linear search for {target:,} in {len(data):,} items")
    print(f"  Found: {found}")
    print(f"  Time:  {linear_time:.6f}s")
    print(f"  Checks: up to {len(data):,} (every element)")

    # --- 1b: Binary search — divide and conquer ---
    print("\n--- 1b: Binary search — O(log n) ---")

    start = time.perf_counter()
    i = bisect.bisect_left(data, target)
    found = i < len(data) and data[i] == target
    binary_time = time.perf_counter() - start

    print(f"  Binary search for {target:,} in {len(data):,} items")
    print(f"  Found: {found}")
    print(f"  Time:  {binary_time:.6f}s")
    print(f"  Checks: ~{len(data).bit_length()} (log₂ {len(data):,})")

    # --- 1c: Hash lookup — O(1) ---
    print("\n--- 1c: Hash lookup — O(1) ---")

    data_set = set(data)
    start = time.perf_counter()
    found = target in data_set  # 'in' on set = hash lookup
    hash_time = time.perf_counter() - start

    print(f"  Hash lookup for {target:,} in {len(data_set):,} items")
    print(f"  Found: {found}")
    print(f"  Time:  {hash_time:.6f}s")
    print(f"  Checks: 1 (hash → bucket → match)")

    # --- 1d: Speedup comparison ---
    print("\n--- 1d: Speedup comparison ---")
    if linear_time > 0 and binary_time > 0:
        print(f"  Binary is ~{linear_time / max(binary_time, 1e-9):.0f}x "
              f"faster than linear")
    if linear_time > 0 and hash_time > 0:
        print(f"  Hash is   ~{linear_time / max(hash_time, 1e-9):.0f}x "
              f"faster than linear")

    print()


# =============================================================================
# SECTION 2: bisect — Binary Search in Sorted Lists
# =============================================================================
# ┌─────────────────────────────────────────────────────────────────┐
# │              bisect MODULE — 6 FUNCTIONS                        │
# │─────────────────────────────────────────────────────────────────│
# │                                                                 │
# │  SEARCH (find where a value belongs):                           │
# │    bisect_left(a, x)   → index BEFORE existing x               │
# │    bisect_right(a, x)  → index AFTER existing x                │
# │    bisect(a, x)        → alias for bisect_right                │
# │                                                                 │
# │  INSERT (add and keep sorted):                                  │
# │    insort_left(a, x)   → insert at bisect_left position        │
# │    insort_right(a, x)  → insert at bisect_right position       │
# │    insort(a, x)        → alias for insort_right                │
# │                                                                 │
# │  REQUIREMENT: the list MUST already be sorted.                  │
# │  bisect does NOT check if the list is sorted.                   │
# │  Unsorted input = wrong results (silent bug!).                  │
# └─────────────────────────────────────────────────────────────────┘

def section_2_bisect() -> None:
    """Demonstrate bisect module for binary search."""
    print("=" * 70)
    print("SECTION 2: bisect — BINARY SEARCH IN SORTED LISTS")
    print("=" * 70)

    # --- 2a: bisect_left — "where would this go?" ---
    print("\n--- 2a: bisect_left — find insertion point (left side) ---")

    scores = [10, 20, 30, 40, 50]

    # Value EXISTS in list:
    i = bisect.bisect_left(scores, 30)
    print(f"  scores = {scores}")
    print(f"  bisect_left(scores, 30) = {i}")
    print(f"  → 30 is at index {i} (position BEFORE the existing 30)")

    # Value DOESN'T exist:
    i = bisect.bisect_left(scores, 25)
    print(f"\n  bisect_left(scores, 25) = {i}")
    print(f"  → 25 would be inserted at index {i} (between 20 and 30)")

    # Value smaller than all:
    i = bisect.bisect_left(scores, 5)
    print(f"\n  bisect_left(scores, 5) = {i}")
    print(f"  → 5 would go at index {i} (before everything)")

    # Value larger than all:
    i = bisect.bisect_left(scores, 99)
    print(f"\n  bisect_left(scores, 99) = {i}")
    print(f"  → 99 would go at index {i} (after everything)")

    # --- 2b: bisect_left vs bisect_right ---
    print("\n--- 2b: bisect_left vs bisect_right (duplicates) ---")

    grades = [70, 80, 80, 80, 90]
    #          0   1   2   3   4

    left = bisect.bisect_left(grades, 80)
    right = bisect.bisect_right(grades, 80)
    print(f"  grades = {grades}")
    print(f"  bisect_left(grades, 80)  = {left}")
    print(f"  bisect_right(grades, 80) = {right}")
    print(f"  → Left puts new 80 BEFORE existing 80s (index {left})")
    print(f"  → Right puts new 80 AFTER existing 80s (index {right})")
    print(f"  → Existing 80s are at indices [{left}:{right}]")

    # --- 2c: Using bisect_left for exact match search ---
    print("\n--- 2c: Exact match search pattern ---")

    words = ["ant", "bat", "cat", "dog", "elk"]

    def binary_search(sorted_list: list[str], target: str) -> bool:
        """Check if target exists in sorted list using bisect.

        Two checks needed:
        1. BOUNDS: is the index within the list?
        2. VALUE:  does the element at that index match?

        bisect_left returns where target WOULD go. If the target
        exists, it returns the index OF the target. If it doesn't
        exist, it returns where it would be inserted — which points
        to a different value (or past the end).
        """
        i = bisect.bisect_left(sorted_list, target)
        return i < len(sorted_list) and sorted_list[i] == target

    print(f"  words = {words}")
    print(f"  binary_search(words, 'cat') = {binary_search(words, 'cat')}")
    print(f"  binary_search(words, 'cow') = {binary_search(words, 'cow')}")
    print(f"  binary_search(words, 'zebra') = {binary_search(words, 'zebra')}")

    # --- 2d: insort — insert and keep sorted ---
    print("\n--- 2d: insort — insert in sorted order ---")

    names: list[str] = []
    for name in ["dog", "ant", "cat", "bat"]:
        bisect.insort(names, name)
        print(f"  insort('{name}') → {names}")

    print("  List stays sorted after every insertion!")

    # --- 2e: Practical pattern — grade classification ---
    print("\n--- 2e: Grade classification (range lookup) ---")

    # bisect can classify values into ranges:
    breakpoints = [60, 70, 80, 90]       # grade boundaries
    letter_grades = ["F", "D", "C", "B", "A"]

    def grade(score: int) -> str:
        """Convert numeric score to letter grade.

        bisect_right finds which bucket the score falls into:
          score < 60  → index 0 → "F"
          60 ≤ score < 70 → index 1 → "D"
          70 ≤ score < 80 → index 2 → "C"
          80 ≤ score < 90 → index 3 → "B"
          score ≥ 90 → index 4 → "A"
        """
        i = bisect.bisect_right(breakpoints, score)
        return letter_grades[i]

    test_scores = [55, 65, 72, 85, 95]
    for s in test_scores:
        print(f"  Score {s:3d} → Grade {grade(s)}")

    # --- 2f: AFC pattern — time-series price lookup ---
    print("\n--- 2f: Time-series lookup (AFC pattern) ---")
    print("  Your AFC project will look up prices at specific timestamps:")
    print()
    print("  timestamps = [100, 200, 300, 400, 500]  # sorted")
    print("  prices     = [10.5, 11.2, 10.8, 12.1, 11.9]")
    print()
    print("  # Find price at or before timestamp 350:")
    print("  i = bisect_right(timestamps, 350) - 1  # → 2")
    print("  price = prices[2]  # → 10.8")
    print()
    print("  This is O(log n) — critical for backtesting thousands")
    print("  of trades against millions of price points.")

    print()


# =============================================================================
# SECTION 3: heapq — Priority Queues and Top-N Problems
# =============================================================================
# ┌─────────────────────────────────────────────────────────────────┐
# │              heapq — MIN-HEAP OPERATIONS                        │
# │─────────────────────────────────────────────────────────────────│
# │                                                                 │
# │  A heap is a binary tree where PARENT ≤ CHILDREN (min-heap).    │
# │  Python implements it as a regular list with heap ordering.     │
# │                                                                 │
# │  KEY OPERATIONS:                                                │
# │    heappush(heap, item)     → add item, maintain heap  O(log n)│
# │    heappop(heap)            → remove smallest item     O(log n)│
# │    heapify(list)            → convert list to heap     O(n)    │
# │    nlargest(n, iterable)    → top N largest items      O(n log k)│
# │    nsmallest(n, iterable)   → top N smallest items     O(n log k)│
# │    merge(*iterables)        → merge sorted streams     O(n)    │
# │                                                                 │
# │  WHEN TO USE:                                                   │
# │    "Give me the top 10"     → heapq.nlargest                   │
# │    "Give me the bottom 5"   → heapq.nsmallest                  │
# │    "Process in priority"    → heappush/heappop loop             │
# │    "Merge sorted files"     → heapq.merge (Stage 2 pipelines)  │
# └─────────────────────────────────────────────────────────────────┘

def section_3_heapq() -> None:
    """Demonstrate heapq for priority queues and top-N problems."""
    print("=" * 70)
    print("SECTION 3: heapq — PRIORITY QUEUES AND TOP-N")
    print("=" * 70)

    # --- 3a: nlargest / nsmallest ---
    print("\n--- 3a: nlargest / nsmallest — top-N problems ---")

    scores = [85, 92, 78, 95, 88, 73, 91, 82, 97, 69]
    print(f"  scores = {scores}")

    top_3 = heapq.nlargest(3, scores)
    bottom_3 = heapq.nsmallest(3, scores)
    print(f"  Top 3:    {top_3}")       # [97, 95, 92]
    print(f"  Bottom 3: {bottom_3}")    # [69, 73, 78]

    # --- 3b: nlargest with key function ---
    print("\n--- 3b: nlargest with key= (objects) ---")

    @dataclass
    class Stock:
        ticker: str
        price: float
        volume: int

    stocks = [
        Stock("AAPL", 175.50, 50_000_000),
        Stock("MSFT", 380.20, 25_000_000),
        Stock("GOOGL", 140.30, 30_000_000),
        Stock("AMZN", 178.90, 45_000_000),
        Stock("NVDA", 875.40, 60_000_000),
    ]

    # Top 3 by price:
    top_by_price = heapq.nlargest(3, stocks, key=lambda s: s.price)
    print("  Top 3 stocks by price:")
    for s in top_by_price:
        print(f"    {s.ticker}: ${s.price:.2f}")

    # Top 3 by volume:
    top_by_volume = heapq.nlargest(3, stocks, key=lambda s: s.volume)
    print("  Top 3 stocks by volume:")
    for s in top_by_volume:
        print(f"    {s.ticker}: {s.volume:,}")

    # --- 3c: heappush / heappop — priority queue ---
    print("\n--- 3c: Priority queue pattern ---")

    # Tasks with priority (lower number = higher priority)
    task_queue: list[tuple[int, str]] = []

    heapq.heappush(task_queue, (3, "check spelling"))
    heapq.heappush(task_queue, (1, "load dictionary"))    # highest priority
    heapq.heappush(task_queue, (2, "extract words"))

    print("  Processing tasks by priority:")
    while task_queue:
        priority, task = heapq.heappop(task_queue)  # always pops smallest
        print(f"    Priority {priority}: {task}")

    # --- 3d: heapq.merge — merge sorted streams ---
    print("\n--- 3d: merge — combine sorted streams ---")

    # Stage 2 pattern: merge sorted log files or partitions
    stream_a = [1, 4, 7, 10]    # sorted
    stream_b = [2, 5, 8, 11]    # sorted
    stream_c = [3, 6, 9, 12]    # sorted

    merged = list(heapq.merge(stream_a, stream_b, stream_c))
    print(f"  stream_a = {stream_a}")
    print(f"  stream_b = {stream_b}")
    print(f"  stream_c = {stream_c}")
    print(f"  merged   = {merged}")
    print("  Merges in O(n) total — no re-sorting needed!")

    # --- 3e: When to use heapq vs sorted ---
    print("\n--- 3e: heapq vs sorted() decision ---")
    print()
    print("  Need ALL items sorted?     → sorted()     O(n log n)")
    print("  Need top K items only?     → nlargest()   O(n log k)")
    print("  Need continuous priority?  → heappush/pop O(log n) each")
    print("  Need to merge sorted data? → merge()      O(n)")
    print()
    print("  Rule of thumb:")
    print("  K < n/4  → heapq.nlargest is faster")
    print("  K ≈ n    → sorted() is faster")
    print("  K = 1    → just use min() or max()")

    print()


# =============================================================================
# SECTION 4: sorted() and key Functions — Custom Sorting
# =============================================================================

def section_4_sorted() -> None:
    """Demonstrate sorted() with key functions for custom ordering."""
    print("=" * 70)
    print("SECTION 4: sorted() AND KEY FUNCTIONS")
    print("=" * 70)

    # --- 4a: Basic sorted ---
    print("\n--- 4a: sorted() returns a NEW sorted list ---")

    words = ["banana", "apple", "cherry", "date"]
    result = sorted(words)
    print(f"  original: {words}")       # unchanged
    print(f"  sorted:   {result}")      # new sorted list
    print(f"  reversed: {sorted(words, reverse=True)}")

    # --- 4b: key= function ---
    print("\n--- 4b: key= for custom sort criteria ---")

    # Sort by word length:
    by_length = sorted(words, key=len)
    print(f"  By length: {by_length}")

    # Sort by last character:
    by_last = sorted(words, key=lambda w: w[-1])
    print(f"  By last char: {by_last}")

    # Sort case-insensitive:
    mixed = ["Banana", "apple", "Cherry"]
    by_lower = sorted(mixed, key=str.lower)
    print(f"  Case-insensitive: {by_lower}")

    # --- 4c: Sorting objects ---
    print("\n--- 4c: Sorting dataclass objects ---")

    @dataclass
    class MisspelledWord:
        word: str
        count: int
        line_number: int

    misspelled = [
        MisspelledWord("Bingley", 5, 10),
        MisspelledWord("Netherfield", 12, 3),
        MisspelledWord("Longbourn", 8, 7),
    ]

    # Sort by count (descending — most frequent first):
    by_count = sorted(misspelled, key=lambda m: m.count, reverse=True)
    print("  Sorted by frequency (descending):")
    for m in by_count:
        print(f"    {m.word}: {m.count} occurrences")

    # Sort by multiple criteria (count desc, then word asc):
    by_multi = sorted(misspelled, key=lambda m: (-m.count, m.word))
    print("  Sorted by count desc, then word asc:")
    for m in by_multi:
        print(f"    {m.word}: {m.count} occurrences")

    # --- 4d: operator.attrgetter (cleaner than lambda) ---
    print("\n--- 4d: attrgetter — cleaner than lambda for attributes ---")
    print("  from operator import attrgetter")
    print()
    print("  # These are equivalent:")
    print("  sorted(stocks, key=lambda s: s.price)")
    print("  sorted(stocks, key=attrgetter('price'))  # ← no lambda")
    print()
    print("  # Multi-key sort:")
    print("  sorted(data, key=attrgetter('department', 'name'))")

    # --- 4e: sort() vs sorted() ---
    print("\n--- 4e: sort() vs sorted() ---")
    print()
    print("  sorted(my_list)    → returns NEW list   (original unchanged)")
    print("  my_list.sort()     → modifies IN PLACE  (returns None)")
    print()
    print("  Use sorted() when you need the original preserved.")
    print("  Use .sort() when you're done with the original order.")

    print()


# =============================================================================
# SECTION 5: collections.Counter — Frequency Counting
# =============================================================================

def section_5_counter() -> None:
    """Demonstrate Counter for frequency analysis and ranking."""
    print("=" * 70)
    print("SECTION 5: collections.Counter — FREQUENCY COUNTING")
    print("=" * 70)

    # --- 5a: Basic counting ---
    print("\n--- 5a: Basic counting ---")

    words = ["cat", "dog", "cat", "bird", "dog", "cat", "fish"]
    counts = Counter(words)
    print(f"  words = {words}")
    print(f"  Counter = {counts}")
    print(f"  counts['cat'] = {counts['cat']}")
    print(f"  counts['xyz'] = {counts['xyz']}")  # 0 (not KeyError!)

    # --- 5b: most_common ---
    print("\n--- 5b: most_common(n) — top N by frequency ---")

    text = "the cat sat on the mat the cat the the"
    word_counts = Counter(text.split())
    print(f"  text: '{text}'")
    print(f"  Counter: {word_counts}")
    print(f"  most_common(2): {word_counts.most_common(2)}")
    print(f"  most_common(): {word_counts.most_common()}")  # all, sorted

    # --- 5c: Counter arithmetic ---
    print("\n--- 5c: Counter arithmetic ---")

    a = Counter(["cat", "dog", "cat"])
    b = Counter(["cat", "bird"])

    print(f"  a = {a}")
    print(f"  b = {b}")
    print(f"  a + b = {a + b}")    # combine counts
    print(f"  a - b = {a - b}")    # subtract (drops zero/negative)
    print(f"  a & b = {a & b}")    # intersection (min of each)
    print(f"  a | b = {a | b}")    # union (max of each)

    # --- 5d: Speller pattern — analyze misspelled words ---
    print("\n--- 5d: Your Speller — misspelled word analysis ---")

    misspelled = [
        "Bingley", "Netherfield", "Bingley", "Longbourn",
        "Bingley", "Netherfield", "Meryton", "Bingley",
    ]
    freq = Counter(misspelled)
    print("  Most frequently misspelled words:")
    for word, count in freq.most_common(3):
        print(f"    {word}: {count} times")

    # --- 5e: Counting characters (useful for NLP/tokenization) ---
    print("\n--- 5e: Character frequency (NLP pattern) ---")

    text = "hello world"
    char_freq = Counter(text)
    print(f"  Character frequencies in '{text}':")
    for char, count in char_freq.most_common(5):
        display = repr(char) if char == " " else char
        print(f"    {display}: {count}")

    print()


# =============================================================================
# SECTION 6: difflib — Fuzzy Matching and Similarity Search
# =============================================================================
# ┌─────────────────────────────────────────────────────────────────┐
# │              difflib — APPROXIMATE STRING MATCHING              │
# │─────────────────────────────────────────────────────────────────│
# │                                                                 │
# │  "Did you mean...?" — when exact match fails, find CLOSE matches│
# │                                                                 │
# │  KEY FUNCTIONS:                                                 │
# │    get_close_matches(word, possibilities)  → fuzzy search       │
# │    SequenceMatcher(a, b).ratio()           → similarity score   │
# │    unified_diff(a, b)                      → line-by-line diff  │
# │                                                                 │
# │  USES IN YOUR ROADMAP:                                          │
# │    PolicyPulse:  "Did you mean: vacation policy?"               │
# │    FormSense:    Match form field names to expected fields       │
# │    DataVault:    Fuzzy column name matching                      │
# │    AFC:          Match company names across data sources         │
# └─────────────────────────────────────────────────────────────────┘

def section_6_difflib() -> None:
    """Demonstrate difflib for fuzzy matching and similarity."""
    print("=" * 70)
    print("SECTION 6: difflib — FUZZY MATCHING")
    print("=" * 70)

    # --- 6a: get_close_matches ---
    print("\n--- 6a: get_close_matches — 'Did you mean...?' ---")

    dictionary_words = [
        "python", "pydantic", "pytest", "pytorch",
        "pandas", "pathlib", "pattern", "parse",
    ]

    # Typo: "pythn" → suggests "python"
    matches = difflib.get_close_matches("pythn", dictionary_words)
    print(f"  Searching for 'pythn' in {dictionary_words}")
    print(f"  Did you mean: {matches}")

    # Multiple close matches:
    matches = difflib.get_close_matches("pyt", dictionary_words, n=3)
    print(f"\n  Searching for 'pyt' (top 3):")
    print(f"  Suggestions: {matches}")

    # Cutoff controls minimum similarity (0.0 to 1.0):
    matches = difflib.get_close_matches(
        "xyz", dictionary_words, cutoff=0.3
    )
    print(f"\n  Searching for 'xyz' (low cutoff=0.3):")
    print(f"  Suggestions: {matches}")  # probably empty

    # --- 6b: SequenceMatcher — similarity ratio ---
    print("\n--- 6b: SequenceMatcher — similarity score ---")

    pairs = [
        ("python", "python"),     # exact match
        ("python", "pyhton"),     # typo
        ("python", "javascript"), # completely different
        ("cat", "cats"),          # plural
        ("hello", "hallo"),       # one char different
    ]

    for a, b in pairs:
        ratio = difflib.SequenceMatcher(None, a, b).ratio()
        print(f"  '{a}' vs '{b}': {ratio:.2%} similar")

    # --- 6c: Speller enhancement — suggest corrections ---
    print("\n--- 6c: Your Speller — 'Did you mean?' enhancement ---")
    print("  When a word is misspelled, suggest the closest match:")
    print()

    known_words = ["definitely", "separate", "occurrence", "necessary"]

    typos = ["definately", "seperate", "occurence", "neccessary"]
    for typo in typos:
        suggestions = difflib.get_close_matches(
            typo, known_words, n=1, cutoff=0.6
        )
        if suggestions:
            print(f"  '{typo}' → Did you mean '{suggestions[0]}'?")
        else:
            print(f"  '{typo}' → No suggestion found")

    # --- 6d: PolicyPulse pattern — fuzzy question matching ---
    print("\n--- 6d: PolicyPulse — fuzzy question matching ---")
    print("  When a user asks a question, find the closest FAQ:")
    print()

    faqs = [
        "How many vacation days do I get?",
        "What is the remote work policy?",
        "How do I submit an expense report?",
        "What are the health insurance options?",
    ]

    query = "how much vacation time"
    matches = difflib.get_close_matches(query, faqs, n=1, cutoff=0.4)
    print(f"  Query: '{query}'")
    print(f"  Best FAQ match: '{matches[0] if matches else 'None'}'")

    print()


# =============================================================================
# SECTION 7: functools.lru_cache — Memoized Search
# =============================================================================

def section_7_lru_cache() -> None:
    """Demonstrate lru_cache for caching expensive computations."""
    print("=" * 70)
    print("SECTION 7: functools.lru_cache — CACHING RESULTS")
    print("=" * 70)

    # --- 7a: The problem — repeated expensive calls ---
    print("\n--- 7a: The problem — repeated computation ---")

    call_count = 0

    def slow_lookup(word: str) -> bool:
        """Simulate an expensive lookup (API call, DB query)."""
        nonlocal call_count
        call_count += 1
        time.sleep(0.01)  # simulate latency
        return word.lower() in {"cat", "dog", "fish"}

    start = time.perf_counter()
    # Same word checked multiple times:
    for _ in range(5):
        slow_lookup("cat")
    uncached_time = time.perf_counter() - start
    print(f"  Without cache: {call_count} calls, {uncached_time:.3f}s")

    # --- 7b: lru_cache solution ---
    print("\n--- 7b: lru_cache — compute once, reuse forever ---")

    cached_call_count = 0

    @lru_cache(maxsize=128)
    def cached_lookup(word: str) -> bool:
        """Same lookup but with caching.

        lru_cache stores results in a dict:
          {"cat": True, "xyz": False, ...}

        On repeat calls with the same argument,
        returns the cached result WITHOUT calling the function.

        maxsize=128 means cache the last 128 unique inputs.
        maxsize=None means unlimited cache (careful with memory!).

        LRU = Least Recently Used — when cache is full, the
        least recently accessed entry is evicted.
        """
        nonlocal cached_call_count
        cached_call_count += 1
        time.sleep(0.01)  # simulate latency
        return word.lower() in {"cat", "dog", "fish"}

    start = time.perf_counter()
    for _ in range(5):
        cached_lookup("cat")  # computed once, cached 4 times
    cached_time = time.perf_counter() - start
    print(f"  With cache: {cached_call_count} actual calls, {cached_time:.3f}s")

    # --- 7c: Cache statistics ---
    print("\n--- 7c: Cache stats ---")
    info = cached_lookup.cache_info()
    print(f"  hits:     {info.hits} (returned cached result)")
    print(f"  misses:   {info.misses} (had to compute)")
    print(f"  maxsize:  {info.maxsize}")
    print(f"  currsize: {info.currsize}")

    # --- 7d: Clear cache ---
    print("\n--- 7d: Cache management ---")
    print("  cached_lookup.cache_clear()    → empty the cache")
    print("  cached_lookup.cache_info()     → hits, misses, size")
    print()
    print("  Use lru_cache for:")
    print("    - API calls with same parameters (LLM embeddings)")
    print("    - Database queries with same filters")
    print("    - Expensive computations with repeating inputs")
    print("    - Recursive algorithms (fibonacci, dynamic programming)")
    print()
    print("  DON'T use lru_cache for:")
    print("    - Functions with mutable arguments (lists, dicts)")
    print("    - Functions with side effects (writing files)")
    print("    - Functions where results change over time (live data)")

    print()


# =============================================================================
# SECTION 8: ALGORITHM COMPLEXITY CHEAT SHEET
# =============================================================================
#
# ┌──────────────────────────────────────────────────────────────────┐
# │                  BIG-O COMPLEXITY REFERENCE                      │
# │──────────────────────────────────────────────────────────────────│
# │                                                                  │
# │  O(1)       │ Constant  │ set lookup, dict access, array index  │
# │  O(log n)   │ Logarithm │ bisect, binary search, balanced tree  │
# │  O(n)       │ Linear    │ list scan, 'in' on list, single loop  │
# │  O(n log n) │ Linearithmic │ sorted(), .sort(), heapify+extract│
# │  O(n²)      │ Quadratic │ nested loops, bubble sort, 'in' list  │
# │             │           │ called n times                        │
# │  O(2ⁿ)     │ Exponential │ brute-force subsets, bad recursion  │
# │──────────────────────────────────────────────────────────────────│
# │                                                                  │
# │  For n = 143,091 (your dictionary):                              │
# │    O(1)       → 1 operation                                      │
# │    O(log n)   → 17 operations                                    │
# │    O(n)       → 143,091 operations                               │
# │    O(n log n) → 2,432,547 operations                             │
# │    O(n²)      → 20,475,034,281 operations (20 billion!)          │
# │──────────────────────────────────────────────────────────────────│
# │                                                                  │
# │  PYTHON DATA STRUCTURE COMPLEXITY:                               │
# │                                                                  │
# │  list:                                                           │
# │    x in list    → O(n)      linear scan                         │
# │    list[i]      → O(1)      direct index                        │
# │    list.append  → O(1)*     amortized (occasional resize O(n))  │
# │    list.insert  → O(n)      shifts elements right               │
# │    sorted(list) → O(n log n)                                    │
# │                                                                  │
# │  set:                                                            │
# │    x in set     → O(1)*     hash lookup (amortized)             │
# │    set.add      → O(1)*     hash + insert                       │
# │    set.remove   → O(1)*     hash + delete                       │
# │                                                                  │
# │  dict:                                                           │
# │    d[key]       → O(1)*     hash lookup                         │
# │    d[key] = val → O(1)*     hash + insert                       │
# │    key in d     → O(1)*     hash lookup                         │
# │                                                                  │
# │  heapq:                                                          │
# │    heappush     → O(log n)  bubble up                           │
# │    heappop      → O(log n)  bubble down                         │
# │    nlargest(k)  → O(n log k)                                    │
# │    heapify      → O(n)      clever — not O(n log n)!            │
# │                                                                  │
# │  bisect:                                                         │
# │    bisect_left  → O(log n)  binary search                       │
# │    insort       → O(n)      O(log n) search + O(n) insert       │
# └──────────────────────────────────────────────────────────────────┘

def section_8_complexity() -> None:
    """Display algorithm complexity cheat sheet."""
    print("=" * 70)
    print("SECTION 8: ALGORITHM COMPLEXITY CHEAT SHEET")
    print("=" * 70)

    print("\n  For n = 143,091 (your Speller dictionary):")
    n = 143_091
    import math
    print(f"    O(1)       → {1:>15,} operations")
    print(f"    O(log n)   → {int(math.log2(n)):>15,} operations")
    print(f"    O(n)       → {n:>15,} operations")
    print(f"    O(n log n) → {int(n * math.log2(n)):>15,} operations")
    print(f"    O(n²)      → {n * n:>15,} operations")

    print(f"\n  Your Speller with 376,904 check() calls on aca.txt:")
    checks = 376_904
    print(f"    HashTable  O(1):     {checks:>15,} total operations")
    print(f"    SortedList O(log n): {int(checks * math.log2(n)):>15,} total operations")
    print(f"    PlainList  O(n):     {checks * n:>15,} total operations")

    print()


# =============================================================================
# SECTION 9: DECISION GUIDE — Which Tool for Which Problem
# =============================================================================
#
# ┌──────────────────────────────────────────────────────────────────┐
# │                    DECISION GUIDE                                │
# │──────────────────────────────────────────────────────────────────│
# │  Problem                           │ Tool                       │
# │────────────────────────────────────│────────────────────────────│
# │  "Is X in this collection?"        │ set (O(1)) or dict         │
# │  "Is X in this SORTED list?"       │ bisect.bisect_left (log n) │
# │  "Give me the top 10 results"      │ heapq.nlargest             │
# │  "Sort by custom criteria"         │ sorted(key=...)            │
# │  "How many of each?"               │ Counter                    │
# │  "Did you mean...?"                │ difflib.get_close_matches  │
# │  "How similar are these strings?"  │ SequenceMatcher.ratio()    │
# │  "Cache expensive lookups"         │ @lru_cache                 │
# │  "Insert into sorted list"         │ bisect.insort              │
# │  "Merge sorted streams"            │ heapq.merge                │
# │  "Classify into ranges"            │ bisect.bisect_right        │
# │  "Process by priority"             │ heapq push/pop             │
# │  "Find differences between lists"  │ difflib.unified_diff       │
# │  "Count most common items"         │ Counter.most_common(n)     │
# └──────────────────────────────────────────────────────────────────┘
#
# ┌──────────────────────────────────────────────────────────────────┐
# │              YOUR PROJECT USAGE MAP                              │
# │──────────────────────────────────────────────────────────────────│
# │  Project          │ Module     │ Use Case                       │
# │───────────────────│────────────│────────────────────────────────│
# │  Speller          │ bisect     │ SortedListDictionary check()   │
# │                   │ Counter    │ Misspelled word frequency       │
# │  DataVault        │ heapq      │ Top-N query results             │
# │                   │ Counter    │ Token usage tracking             │
# │                   │ difflib    │ Fuzzy column name matching       │
# │  PolicyPulse      │ difflib    │ FAQ fuzzy matching               │
# │                   │ heapq      │ Top-K relevant chunks            │
# │                   │ lru_cache  │ Embedding cache                  │
# │  FormSense        │ difflib    │ Field name fuzzy matching        │
# │  AFC              │ bisect     │ Time-series price lookup         │
# │                   │ heapq      │ Top-N stock screening            │
# │                   │ Counter    │ Sector/industry frequency        │
# │  Stage 2          │ heapq      │ merge sorted partitions          │
# │                   │ bisect     │ Partition boundary lookup        │
# │  Stage 3          │ heapq      │ K-nearest neighbors concept      │
# │                   │ Counter    │ Class distribution analysis       │
# │  Stage 4          │ Counter    │ Token frequency / vocabulary     │
# │                   │ lru_cache  │ LLM response cache               │
# │                   │ difflib    │ RAG chunk deduplication           │
# └──────────────────────────────────────────────────────────────────┘
#
# ┌──────────────────────────────────────────────────────────────────┐
# │                  IMPORT CHEAT SHEET                              │
# │──────────────────────────────────────────────────────────────────│
# │  import bisect                      # binary search              │
# │  import heapq                       # priority queues, top-N     │
# │  import difflib                     # fuzzy matching             │
# │  from collections import Counter    # frequency counting         │
# │  from functools import lru_cache    # result caching             │
# │  from operator import attrgetter    # clean key functions        │
# └──────────────────────────────────────────────────────────────────┘
#
# =============================================================================


# =============================================================================
# MAIN EXECUTION
# =============================================================================

if __name__ == "__main__":
    section_1_linear_vs_binary()
    section_2_bisect()
    section_3_heapq()
    section_4_sorted()
    section_5_counter()
    section_6_difflib()
    section_7_lru_cache()
    section_8_complexity()

    print("=" * 70)
    print("REFERENCE COMPLETE — See Section 9 (cheat sheets) in source code")
    print("=" * 70)
