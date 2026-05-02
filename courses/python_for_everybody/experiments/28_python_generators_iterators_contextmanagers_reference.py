"""
python_generators_iterators_contextmanagers_reference.py
=========================================================

Personal reference: Python Generators, Iterators, and Context Managers —
how they work, when to use each, and the three communication channels
(yield, send, return) that power advanced patterns.

Topics covered
--------------
1.  Iterator Protocol — what makes an object iterable
2.  Generator Functions — yield, lazy evaluation, memory efficiency
3.  Generator Three Channels — yield (OUT), send (IN), return (FINAL)
4.  Iterator vs Generator Type Hints — when to use which
5.  Context Managers — with statement, __enter__/__exit__, cleanup
6.  @contextmanager Decorator — generators as context managers
7.  Context Manager + Generator Combined — how @contextmanager uses Generator protocol
8.  Practical Patterns — timer, resource management, streaming
9.  Common Pitfalls and Gotchas
10. ParamSpec + TypeVar — Type-safe decorators that preserve function signatures
11. typing vs collections.abc — Where to import what (Python 3.9+ rules)
12. Decision Guide and Cheat Sheet

Why this matters for your roadmap (v8.1 GenAI-First)
------------------------------------------------------
- Stage 1 (Speller):     Generator for text_processor.py (streaming word extraction)
                          Context manager for timer() benchmark utility
                          Context manager for all file I/O (dictionary loading)
- Stage 1 (DataVault):   Generator for streaming LLM responses token by token
                          Context manager for LLM API client connections
- Stage 1 (PolicyPulse): Generator for streaming RAG chunk retrieval
                          Context manager for ChromaDB vector store sessions
- Stage 1 (FormSense):   Generator for batch document processing (scan inbox)
                          Context manager for email/ticket system connections
- Stage 2 (Data Eng):    Generator for PySpark partition streaming
                          Context manager for PostgreSQL connections (psycopg2)
                          Context manager for AWS S3 sessions (boto3)
- Stage 3 (ML):          Generator for DataLoader batches (PyTorch training loops)
                          Context manager for MLflow experiment tracking runs
- Stage 4 (LLM):         Generator for LangChain streaming (token-by-token output)
                          Context manager for LangGraph agent state management
                          send() used internally by LangGraph for agent transitions
- Stage 5 (Senior):      All patterns combined in production LLMOps systems

How to use this file
---------------------
Run it directly to see all output::

    $ python python_generators_iterators_contextmanagers_reference.py

Or import individual sections to experiment in a REPL::

    >>> from python_generators_iterators_contextmanagers_reference import (
    ...     section_3_three_channels
    ... )

Author: Manuel Reyes — CS50 Speller / Stage 1 Learning Reference
Version: 1.1.0 — March 2026

References
----------
.. [1] Python Docs — Generator Types
   https://docs.python.org/3/library/stdtypes.html#generator-types
.. [2] Python Docs — The with statement
   https://docs.python.org/3/reference/compound_stmts.html#the-with-statement
.. [3] PEP 255 — Simple Generators
   https://peps.python.org/pep-0255/
.. [4] PEP 342 — Coroutines via Enhanced Generators (send/throw)
   https://peps.python.org/pep-0342/
.. [5] PEP 343 — The "with" Statement
   https://peps.python.org/pep-0343/
.. [6] contextlib — Utilities for with-statement contexts
   https://docs.python.org/3/library/contextlib.html
.. [7] PEP 612 — ParamSpec (Parameter Specification Variables)
   https://peps.python.org/pep-0612/
.. [8] PEP 484 — TypeVar (Type Hints)
   https://peps.python.org/pep-0484/
.. [9] PEP 585 — Type Hinting Generics In Standard Collections
   https://peps.python.org/pep-0585/
"""

from __future__ import annotations

import sys
import time
from collections.abc import Callable, Generator, Iterator
from contextlib import contextmanager
from dataclasses import dataclass, field
from functools import wraps
from typing import Any, ParamSpec, TypeVar


# =============================================================================
# SECTION 1: THE ITERATOR PROTOCOL — What Makes an Object Iterable
# =============================================================================
# ┌─────────────────────────────────────────────────────────────────┐
# │                    ITERATOR PROTOCOL                            │
# │─────────────────────────────────────────────────────────────────│
# │                                                                 │
# │  Any object that implements these two methods is an iterator:   │
# │                                                                 │
# │    __iter__()  → returns self (the iterator object)             │
# │    __next__()  → returns the next value OR raises StopIteration │
# │                                                                 │
# │  Any object that implements __iter__() is ITERABLE:             │
# │    - lists, tuples, sets, dicts, strings → all iterable         │
# │    - __iter__() returns an iterator object                      │
# │    - the iterator has __next__()                                │
# │                                                                 │
# │  for x in something:                                            │
# │      ↓                                                          │
# │  iter_obj = something.__iter__()    # get the iterator          │
# │  while True:                                                    │
# │      try:                                                       │
# │          x = iter_obj.__next__()    # get next value            │
# │      except StopIteration:                                      │
# │          break                      # done                      │
# └─────────────────────────────────────────────────────────────────┘

def section_1_iterator_protocol() -> None:
    """Demonstrate the iterator protocol that underlies all for loops.

    The ``for`` loop is syntactic sugar — under the hood, Python calls
    ``__iter__()`` to get an iterator, then ``__next__()`` repeatedly
    until ``StopIteration`` is raised.
    """
    print("=" * 70)
    print("SECTION 1: THE ITERATOR PROTOCOL")
    print("=" * 70)

    # --- 1a: Manual iteration (what for-loop does under the hood) ---
    print("\n--- 1a: Manual iteration (what 'for' does internally) ---")
    numbers = [10, 20, 30]

    # Step 1: Get the iterator object
    iter_obj = iter(numbers)           # calls numbers.__iter__()
    print(f"Iterator object: {iter_obj}")
    print(f"Type: {type(iter_obj)}")

    # Step 2: Call __next__() repeatedly
    print(f"next() call 1: {next(iter_obj)}")   # 10
    print(f"next() call 2: {next(iter_obj)}")   # 20
    print(f"next() call 3: {next(iter_obj)}")   # 30

    # Step 3: StopIteration when exhausted
    try:
        next(iter_obj)
    except StopIteration:
        print("StopIteration raised — iterator is exhausted")

    # --- 1b: Custom iterator class ---
    print("\n--- 1b: Custom iterator class (Countdown) ---")

    class Countdown:
        """Iterator that counts down from a starting number.

        Implements the full iterator protocol:
        - __iter__() returns self
        - __next__() returns next value or raises StopIteration
        """

        def __init__(self, start: int) -> None:
            self._current = start

        def __iter__(self) -> Countdown:
            return self

        def __next__(self) -> int:
            if self._current <= 0:
                raise StopIteration
            value = self._current
            self._current -= 1
            return value

    for num in Countdown(5):
        print(f"  Countdown: {num}")

    # --- 1c: Iterable vs Iterator distinction ---
    print("\n--- 1c: Iterable vs Iterator ---")
    my_list = [1, 2, 3]
    print(f"list has __iter__: {hasattr(my_list, '__iter__')}")     # True
    print(f"list has __next__: {hasattr(my_list, '__next__')}")     # False
    # A list is ITERABLE (has __iter__) but NOT an iterator (no __next__)
    # iter(my_list) CREATES an iterator from the iterable

    my_iter = iter(my_list)
    print(f"iter has __iter__: {hasattr(my_iter, '__iter__')}")     # True
    print(f"iter has __next__: {hasattr(my_iter, '__next__')}")     # True
    # An iterator is BOTH iterable AND has __next__

    print()


# =============================================================================
# SECTION 2: GENERATOR FUNCTIONS — yield, Lazy Evaluation, Memory Efficiency
# =============================================================================
# ┌─────────────────────────────────────────────────────────────────┐
# │                  GENERATOR FUNCTIONS                            │
# │─────────────────────────────────────────────────────────────────│
# │                                                                 │
# │  A generator function uses `yield` instead of `return`.         │
# │  When called, it doesn't execute — it returns a generator       │
# │  object. Each call to next() runs code until the next yield.    │
# │                                                                 │
# │  def my_gen():          gen = my_gen()                          │
# │      yield 1            next(gen)  → runs to yield 1 → pauses  │
# │      yield 2            next(gen)  → runs to yield 2 → pauses  │
# │      yield 3            next(gen)  → runs to yield 3 → pauses  │
# │                         next(gen)  → StopIteration              │
# │                                                                 │
# │  KEY INSIGHT: Code between yields is FROZEN in place.           │
# │  Local variables, execution position — all preserved.           │
# │  This is how generators use constant memory for huge datasets.  │
# └─────────────────────────────────────────────────────────────────┘

def section_2_generator_functions() -> None:
    """Demonstrate generator functions and lazy evaluation.

    Generators produce values one at a time instead of building
    an entire list in memory. This is the streaming pattern you'll
    use in text_processor.py (Speller) and LLM token streaming
    (DataVault, PolicyPulse).
    """
    print("=" * 70)
    print("SECTION 2: GENERATOR FUNCTIONS")
    print("=" * 70)

    # --- 2a: Basic generator vs regular function ---
    print("\n--- 2a: Generator vs regular function ---")

    def get_squares_list(n: int) -> list[int]:
        """Regular function — builds ENTIRE list in memory."""
        result = []
        for i in range(n):
            result.append(i * i)
        return result                          # returns list all at once

    def get_squares_gen(n: int) -> Generator[int, None, None]:
        """Generator function — yields one value at a time."""
        for i in range(n):
            yield i * i                        # pauses here, resumes on next()

    # Compare behavior
    list_result = get_squares_list(5)
    gen_result = get_squares_gen(5)

    print(f"List result type: {type(list_result)}")    # <class 'list'>
    print(f"Gen result type:  {type(gen_result)}")     # <class 'generator'>
    print(f"List result:      {list_result}")          # [0, 1, 4, 9, 16]
    print(f"Gen result:       {gen_result}")           # <generator object ...>

    # Generator only produces values when asked
    print(f"next(gen): {next(gen_result)}")  # 0
    print(f"next(gen): {next(gen_result)}")  # 1
    print(f"next(gen): {next(gen_result)}")  # 4

    # --- 2b: Memory comparison ---
    print("\n--- 2b: Memory efficiency ---")
    print("List of 1M items: stores ALL 1,000,000 values in memory")
    print("Generator of 1M items: stores only 1 value at a time")

    # This would use ~8MB of memory:
    # big_list = [x * x for x in range(1_000_000)]

    # This uses constant memory (~100 bytes) regardless of size:
    # big_gen = (x * x for x in range(1_000_000))

    # --- 2c: Generator expression (comprehension syntax) ---
    print("\n--- 2c: Generator expression vs list comprehension ---")

    # List comprehension — builds entire list in memory
    squares_list = [x * x for x in range(5)]
    print(f"List comprehension: {squares_list}")

    # Generator expression — lazy evaluation (note: parentheses not brackets)
    squares_gen = (x * x for x in range(5))
    print(f"Generator expression: {squares_gen}")
    print(f"Consuming generator:  {list(squares_gen)}")

    # --- 2d: Execution flow visualization ---
    print("\n--- 2d: Execution flow (watch the pauses) ---")

    def traced_generator() -> Generator[str, None, None]:
        """Generator with print statements to show execution flow."""
        print("  [gen] Starting... running to first yield")
        yield "first"

        print("  [gen] Resumed... running to second yield")
        yield "second"

        print("  [gen] Resumed... running to third yield")
        yield "third"

        print("  [gen] Resumed... no more yields, finishing")
        # StopIteration raised automatically here

    gen = traced_generator()
    print("Created generator (nothing executed yet)")
    print(f"Call next(): got '{next(gen)}'")
    print("--- back in caller ---")
    print(f"Call next(): got '{next(gen)}'")
    print("--- back in caller ---")
    print(f"Call next(): got '{next(gen)}'")
    print("--- back in caller ---")
    try:
        next(gen)
    except StopIteration:
        print("StopIteration — generator finished")

    # --- 2e: Speller-relevant example — streaming word extraction ---
    print("\n--- 2e: Streaming word extraction (Speller pattern) ---")

    def extract_words_from_text(text: str) -> Iterator[str]:
        """Yield words one at a time from a text string.

        This is the simplified version of what text_processor.py does.
        It yields words instead of building a list — constant memory
        regardless of how large the text is.

        Parameters
        ----------
        text : str
            The input text to extract words from.

        Yields
        ------
        str
            Each word found in the text.
        """
        word_buffer: list[str] = []
        for char in text:
            if char.isalpha() or (char == "'" and word_buffer):
                word_buffer.append(char)
            elif word_buffer:
                yield "".join(word_buffer)
                word_buffer.clear()

        # Don't forget the last word if text doesn't end with a delimiter
        if word_buffer:
            yield "".join(word_buffer)

    sample = "The cat's hat sat on the mat"
    print(f"Text: '{sample}'")
    print("Words extracted (streaming):")
    for word in extract_words_from_text(sample):
        print(f"  → '{word}'")

    print()


# =============================================================================
# SECTION 3: THE THREE CHANNELS — yield (OUT), send (IN), return (FINAL)
# =============================================================================
# ┌─────────────────────────────────────────────────────────────────┐
# │            GENERATOR THREE COMMUNICATION CHANNELS               │
# │─────────────────────────────────────────────────────────────────│
# │                                                                 │
# │  ┌──────────┐    yield (OUT)    ┌──────────┐                    │
# │  │          │ ────────────────→ │          │                    │
# │  │ GENERATOR│                   │  CALLER  │                    │
# │  │          │ ←──────────────── │          │                    │
# │  └──────────┘    send (IN)      └──────────┘                    │
# │       │                                                         │
# │       │ return (FINAL)                                          │
# │       ↓                                                         │
# │  StopIteration.value                                            │
# │                                                                 │
# │  Generator[YieldType, SendType, ReturnType]                     │
# │              ↑           ↑          ↑                           │
# │          what goes    what goes   what goes                     │
# │          OUT via      IN via      into                          │
# │          yield        send()      StopIteration.value           │
# └─────────────────────────────────────────────────────────────────┘

def section_3_three_channels() -> None:
    """Demonstrate all three generator communication channels.

    Most generators only use yield (channel 1). The send() and return
    channels exist for advanced patterns like coroutines and the
    @contextmanager decorator.
    """
    print("=" * 70)
    print("SECTION 3: THE THREE CHANNELS — yield, send, return")
    print("=" * 70)

    # --- 3a: Channel 1 — yield (OUT) — values go from generator to caller ---
    print("\n--- 3a: Channel 1 — yield (OUT) ---")
    print("This is the channel you already know and use most often.\n")

    def fibonacci(limit: int) -> Generator[int, None, None]:
        """Yield Fibonacci numbers up to a limit."""
        a, b = 0, 1
        while a < limit:
            yield a          # send value OUT to caller
            a, b = b, a + b

    print("Fibonacci numbers < 100:")
    for num in fibonacci(100):
        print(f"  {num}", end="")
    print()

    # --- 3b: Channel 2 — send (IN) — values go from caller into generator ---
    print("\n--- 3b: Channel 2 — send (IN) ---")
    print("The caller can push values INTO the generator via .send()")
    print("The sent value becomes the return value of the yield expression.\n")

    def running_average() -> Generator[float, float, None]:
        """Maintain a running average — receive values via send().

        Each .send(value) pushes a number IN, and the generator
        yields the updated average OUT.

        The flow for each send():
            value = yield current_avg    ← receive IN, send OUT
            update total and count
            loop back to yield           ← send new average OUT
        """
        total = 0.0
        count = 0
        average = 0.0

        while True:
            value = yield average     # send average OUT, receive value IN
            # ↑ This line does TWO things:
            # 1. yield average  → sends current average to the caller
            # 2. value =        → receives the sent value from the caller
            total += value
            count += 1
            average = total / count

    avg = running_average()
    next(avg)                         # "prime" the generator — run to first yield
    # ↑ IMPORTANT: must call next() first before send()
    #   This runs the generator to the first yield, which establishes
    #   the "receiving" point. Without this, there's no yield waiting
    #   to receive the sent value.

    print(f"send(10.0) → average = {avg.send(10.0)}")   # 10.0
    print(f"send(20.0) → average = {avg.send(20.0)}")   # 15.0
    print(f"send(30.0) → average = {avg.send(30.0)}")   # 20.0
    print(f"send(40.0) → average = {avg.send(40.0)}")   # 25.0

    # --- 3c: Detailed send() flow trace ---
    print("\n--- 3c: send() flow trace ---")

    def traced_send() -> Generator[str, str, None]:
        """Generator with traces showing send() data flow."""
        print("  [gen] Running to first yield...")
        received = yield "ready"
        print(f"  [gen] Received '{received}' from send()")

        print("  [gen] Running to second yield...")
        received = yield f"got: {received}"
        print(f"  [gen] Received '{received}' from send()")

        print("  [gen] Running to third yield...")
        yield f"got: {received}"
        print("  [gen] Finished")

    gen = traced_send()
    result = next(gen)                           # prime — runs to first yield
    print(f"[caller] next() returned: '{result}'")

    result = gen.send("hello")                   # sends "hello" IN
    print(f"[caller] send('hello') returned: '{result}'")

    result = gen.send("world")                   # sends "world" IN
    print(f"[caller] send('world') returned: '{result}'")

    # --- 3d: Channel 3 — return (FINAL) — StopIteration.value ---
    print("\n--- 3d: Channel 3 — return (FINAL value) ---")
    print("When a generator returns, the value is in StopIteration.value\n")

    def process_items() -> Generator[str, None, int]:
        """Process items, yield status updates, return final count.

        Generator[str, None, int]
                  ↑     ↑     ↑
                  yield  send  return
                  (OUT)  (IN)  (FINAL)
        """
        count = 0
        for item in ["apple", "banana", "cherry"]:
            yield f"processing: {item}"      # yield status OUT
            count += 1
        return count                          # final value → StopIteration.value

    gen = process_items()
    print(f"  {next(gen)}")    # "processing: apple"
    print(f"  {next(gen)}")    # "processing: banana"
    print(f"  {next(gen)}")    # "processing: cherry"

    try:
        next(gen)              # generator is done → raises StopIteration
    except StopIteration as e:
        print(f"  Generator finished! Return value: {e.value}")   # 3

    # --- 3e: All three channels in one generator ---
    print("\n--- 3e: All three channels together ---")

    def accumulator() -> Generator[float, float, str]:
        """Demonstrates all three channels in one generator.

        Yields running total (OUT),
        receives numbers via send (IN),
        returns summary string (FINAL).

        Generator[float, float, str]
                  ↑      ↑      ↑
                  yield   send   return
        """
        total = 0.0
        count = 0

        while True:
            value = yield total               # OUT: total, IN: number
            if value is None:                 # next() sends None implicitly
                break
            total += value
            count += 1

        return f"Sum={total}, Count={count}"  # FINAL: summary

    acc = accumulator()
    next(acc)                                  # prime → yields 0.0
    print(f"  send(5.0) → total = {acc.send(5.0)}")     # 5.0
    print(f"  send(3.0) → total = {acc.send(3.0)}")     # 8.0
    print(f"  send(2.0) → total = {acc.send(2.0)}")     # 10.0

    try:
        next(acc)                              # sends None → breaks → returns
    except StopIteration as e:
        print(f"  Final: {e.value}")           # "Sum=10.0, Count=3"

    print()


# =============================================================================
# SECTION 4: ITERATOR vs GENERATOR TYPE HINTS — When to Use Which
# =============================================================================
# ┌─────────────────────────────────────────────────────────────────┐
# │             TYPE HINT DECISION GUIDE                            │
# │─────────────────────────────────────────────────────────────────│
# │                                                                 │
# │  "Does my generator ONLY yield values outward?"                 │
# │                                                                 │
# │  YES → Iterator[YieldType]                                      │
# │         Simpler, cleaner, sufficient 90% of the time            │
# │         Example: text_processor.py extract_words()              │
# │                                                                 │
# │  NO  → Generator[YieldType, SendType, ReturnType]               │
# │         Need send() and/or return value                         │
# │         Example: @contextmanager timer()                        │
# │                                                                 │
# │  Iterator is a SUPERTYPE of Generator:                          │
# │    Every Generator IS an Iterator (has __next__)                │
# │    Not every Iterator is a Generator (might be a class)         │
# │                                                                 │
# │  collections.abc.Iterator[Y]  =  Generator[Y, None, None]      │
# │                                                                 │
# │  ┌───────────────────────────────────────┐                      │
# │  │           Iterable                    │                      │
# │  │  ┌────────────────────────────┐       │                      │
# │  │  │        Iterator            │       │                      │
# │  │  │  ┌─────────────────────┐   │       │                      │
# │  │  │  │     Generator       │   │       │                      │
# │  │  │  │  (yield + send +    │   │       │                      │
# │  │  │  │   return)           │   │       │                      │
# │  │  │  └─────────────────────┘   │       │                      │
# │  │  └────────────────────────────┘       │                      │
# │  └───────────────────────────────────────┘                      │
# └─────────────────────────────────────────────────────────────────┘

def section_4_type_hints() -> None:
    """Demonstrate when to use Iterator vs Generator type hints."""
    print("=" * 70)
    print("SECTION 4: ITERATOR vs GENERATOR TYPE HINTS")
    print("=" * 70)

    # --- 4a: Iterator — simple one-way streaming ---
    print("\n--- 4a: Iterator[str] — one-way streaming (90% of cases) ---")

    def greetings(names: list[str]) -> Iterator[str]:
        """Yield greetings — only sends data OUT, never receives IN.

        Use Iterator[YieldType] because:
        - No send() needed
        - No return value needed
        - Simpler type annotation
        """
        for name in names:
            yield f"Hello, {name}!"

    for greeting in greetings(["Alice", "Bob"]):
        print(f"  {greeting}")

    # --- 4b: Generator — full protocol needed ---
    print("\n--- 4b: Generator[str, str, int] — bidirectional ---")

    def echo_counter() -> Generator[str, str, int]:
        """Echo what's sent in, count total sends.

        Use Generator[Y, S, R] because:
        - send() pushes data IN (channel 2)
        - return gives final count (channel 3)
        """
        count = 0
        response = "ready"
        while True:
            received = yield response
            if received is None:
                break
            response = f"echo: {received}"
            count += 1
        return count

    gen = echo_counter()
    next(gen)                                      # prime
    print(f"  {gen.send('ping')}")                 # "echo: ping"
    print(f"  {gen.send('pong')}")                 # "echo: pong"
    try:
        next(gen)
    except StopIteration as e:
        print(f"  Total sends: {e.value}")         # 2

    # --- 4c: Import location ---
    print("\n--- 4c: Where to import from ---")
    print("  from collections.abc import Iterator    # for simple generators")
    print("  from collections.abc import Generator   # for full protocol")
    print("  # NOTE: collections.abc (not typing) is preferred since Python 3.9+")
    print("  # typing.Iterator and typing.Generator still work but are older style")

    print()


# =============================================================================
# SECTION 5: CONTEXT MANAGERS — with statement, __enter__/__exit__
# =============================================================================
# ┌─────────────────────────────────────────────────────────────────┐
# │                   CONTEXT MANAGER PROTOCOL                      │
# │─────────────────────────────────────────────────────────────────│
# │                                                                 │
# │  with EXPRESSION as VARIABLE:                                   │
# │      BODY                                                       │
# │                                                                 │
# │  Translates to:                                                 │
# │                                                                 │
# │  manager = EXPRESSION                                           │
# │  VARIABLE = manager.__enter__()      # setup                    │
# │  try:                                                           │
# │      BODY                            # your code runs here      │
# │  finally:                                                       │
# │      manager.__exit__(exc_info)      # cleanup ALWAYS runs      │
# │                                                                 │
# │  KEY GUARANTEE: __exit__() runs even if BODY raises exception   │
# │  This is why context managers are essential for:                 │
# │    - File handles (close the file)                              │
# │    - DB connections (close the connection)                       │
# │    - Locks (release the lock)                                   │
# │    - Timers (record end time)                                   │
# │    - API clients (close the session)                            │
# └─────────────────────────────────────────────────────────────────┘

def section_5_context_managers() -> None:
    """Demonstrate context managers and the with statement protocol."""
    print("=" * 70)
    print("SECTION 5: CONTEXT MANAGERS")
    print("=" * 70)

    # --- 5a: Built-in context manager (file) ---
    print("\n--- 5a: Built-in context manager (file handling) ---")
    print("  with open('file.txt') as f:")
    print("      data = f.read()")
    print("  # f.close() called automatically — even if exception in body")
    print("  # This is the pattern you use in dictionary.py load()")

    # --- 5b: Custom context manager class ---
    print("\n--- 5b: Custom context manager class ---")

    class DatabaseConnection:
        """Simulated DB connection showing context manager protocol.

        This is the pattern you'll use in Stage 2 (PostgreSQL)
        and in PolicyPulse (ChromaDB).

        Methods
        -------
        __enter__
            Called when 'with' block starts — setup/connect.
        __exit__
            Called when 'with' block ends — cleanup/disconnect.
            Receives exception info if an error occurred.
        """

        def __init__(self, db_name: str) -> None:
            self.db_name = db_name
            self.connected = False

        def __enter__(self) -> DatabaseConnection:
            print(f"  [DB] Connecting to '{self.db_name}'...")
            self.connected = True
            return self    # this becomes the 'as' variable

        def __exit__(
            self,
            exc_type: type[BaseException] | None,
            exc_val: BaseException | None,
            exc_tb: Any,
        ) -> bool:
            print(f"  [DB] Disconnecting from '{self.db_name}'...")
            self.connected = False

            if exc_type is not None:
                print(f"  [DB] Exception occurred: {exc_val}")
                # Return False = let the exception propagate
                # Return True = suppress the exception (rarely wanted)
            return False

    # Normal usage — __exit__ called after block
    with DatabaseConnection("speller_db") as db:
        print(f"  [app] Connected: {db.connected}")
        print("  [app] Doing work...")

    print(f"  [app] After with: connected = {db.connected}")

    # With exception — __exit__ STILL called
    print("\n  With exception:")
    try:
        with DatabaseConnection("speller_db") as db:
            print("  [app] Doing work...")
            raise ValueError("something broke")
    except ValueError:
        print("  [app] Exception caught by caller")
    print(f"  [app] Connection cleaned up: {db.connected}")

    print()


# =============================================================================
# SECTION 6: @contextmanager DECORATOR — Generators as Context Managers
# =============================================================================
# ┌─────────────────────────────────────────────────────────────────┐
# │              @contextmanager FLOW                               │
# │─────────────────────────────────────────────────────────────────│
# │                                                                 │
# │  @contextmanager                                                │
# │  def my_context():                                              │
# │      # SETUP (before yield)  →  runs during __enter__()        │
# │      resource = acquire()                                       │
# │      yield resource           →  value goes to 'as' variable   │
# │      # CLEANUP (after yield) →  runs during __exit__()         │
# │      release(resource)                                          │
# │                                                                 │
# │                                                                 │
# │  EXECUTION FLOW:                                                │
# │                                                                 │
# │  with my_context() as resource:                                 │
# │      │                                                          │
# │      ├─ 1. Generator starts running                             │
# │      ├─ 2. Code BEFORE yield executes (setup)                   │
# │      ├─ 3. yield sends resource to 'as' variable                │
# │      ├─ 4. Generator PAUSES                                     │
# │      ├─ 5. Your 'with' block body runs                          │
# │      ├─ 6. Generator RESUMES after yield                        │
# │      └─ 7. Code AFTER yield executes (cleanup)                  │
# │                                                                 │
# │  If exception in step 5:                                        │
# │      @contextmanager calls .throw() on the generator            │
# │      Exception is re-raised at the yield point                  │
# │      You can catch it with try/except around yield              │
# └─────────────────────────────────────────────────────────────────┘

def section_6_contextmanager_decorator() -> None:
    """Demonstrate @contextmanager — the shortcut for context managers.

    Writing a class with __enter__/__exit__ is verbose. The
    @contextmanager decorator lets you write the same thing as a
    generator function with yield. This is what you use in
    benchmarks.py timer().
    """
    print("=" * 70)
    print("SECTION 6: @contextmanager DECORATOR")
    print("=" * 70)

    # --- 6a: Basic @contextmanager ---
    print("\n--- 6a: Basic @contextmanager ---")

    @contextmanager
    def managed_resource(name: str) -> Generator[str, None, None]:
        """Simple context manager using @contextmanager.

        Everything before yield = setup (__enter__)
        The yield value = 'as' variable
        Everything after yield = cleanup (__exit__)
        """
        print(f"  [setup] Acquiring '{name}'")
        yield name                                    # this value goes to 'as'
        print(f"  [cleanup] Releasing '{name}'")

    with managed_resource("database") as resource:
        print(f"  [body] Using: {resource}")

    # --- 6b: Timer context manager (your Speller pattern) ---
    print("\n--- 6b: Timer context manager (Speller benchmarks.py pattern) ---")

    @dataclass(frozen=True, slots=True)
    class BenchmarkResult:
        """Immutable benchmark result."""
        operation: str
        elapsed_seconds: float
        metadata: dict[str, Any] = field(default_factory=dict)

    @contextmanager
    def timer(operation_name: str) -> Generator[dict[str, Any], None, None]:
        """Time a block of code, store result in mutable container.

        Parameters
        ----------
        operation_name : str
            Label for the benchmark.

        Yields
        ------
        dict[str, Any]
            Mutable container — access result via container['result']
            after the 'with' block completes.

        Why yield a dict (mutable) not a BenchmarkResult (frozen)?
        ----------------------------------------------------------
        The container is yielded BEFORE timing is complete. We need
        to fill it in AFTER the 'with' block runs. A frozen dataclass
        can't be mutated, so we use a dict as the container and put
        the BenchmarkResult inside it after measuring.
        """
        container: dict[str, Any] = {}
        start = time.perf_counter()

        yield container              # caller's 'with' block runs here

        elapsed = time.perf_counter() - start
        container["result"] = BenchmarkResult(
            operation=operation_name,
            elapsed_seconds=elapsed,
        )

    # Usage
    with timer("example_operation") as t:
        # simulate some work
        total = sum(range(1_000_000))

    result = t["result"]
    print(f"  Operation: {result.operation}")
    print(f"  Elapsed:   {result.elapsed_seconds:.6f}s")

    # --- 6c: Exception handling in @contextmanager ---
    print("\n--- 6c: Exception handling in @contextmanager ---")

    @contextmanager
    def safe_resource(name: str) -> Generator[str, None, None]:
        """Context manager with exception handling.

        Use try/finally around yield to guarantee cleanup
        even if the 'with' block raises an exception.
        """
        print(f"  [setup] Acquiring '{name}'")
        try:
            yield name
        except Exception as e:
            print(f"  [error] Exception in 'with' block: {e}")
            raise               # re-raise so caller can handle it
        finally:
            print(f"  [cleanup] Releasing '{name}' (always runs)")

    try:
        with safe_resource("connection") as r:
            print(f"  [body] Using {r}")
            raise RuntimeError("simulated error")
    except RuntimeError:
        print("  [caller] Caught the error")

    print()


# =============================================================================
# SECTION 7: HOW @contextmanager USES THE GENERATOR PROTOCOL INTERNALLY
# =============================================================================
# ┌─────────────────────────────────────────────────────────────────┐
# │     @contextmanager INTERNAL MECHANICS                          │
# │─────────────────────────────────────────────────────────────────│
# │                                                                 │
# │  When you write:                                                │
# │    with timer("load") as t:                                     │
# │        dictionary.load(path)                                    │
# │                                                                 │
# │  @contextmanager does this internally:                          │
# │                                                                 │
# │  __enter__():                                                   │
# │      gen = timer("load")          # create generator            │
# │      value = next(gen)            # run to yield → get value    │
# │      return value                 # value becomes 't'           │
# │                                                                 │
# │  __exit__(no exception):                                        │
# │      next(gen)                    # resume after yield          │
# │      # expects StopIteration      # generator finishes          │
# │                                                                 │
# │  __exit__(with exception):                                      │
# │      gen.throw(exc_type, exc_val) # send exception INTO gen     │
# │      # generator can catch or let it propagate                  │
# │                                                                 │
# │  This is why @contextmanager needs Generator[Y, None, None]:    │
# │    - Uses next() for yield channel                              │
# │    - Uses .throw() for error channel (part of Generator proto)  │
# │    - send() is available but not used by @contextmanager        │
# └─────────────────────────────────────────────────────────────────┘

def section_7_internal_mechanics() -> None:
    """Show what @contextmanager does under the hood."""
    print("=" * 70)
    print("SECTION 7: @contextmanager INTERNAL MECHANICS")
    print("=" * 70)

    # --- 7a: Manual simulation of what @contextmanager does ---
    print("\n--- 7a: Simulating @contextmanager manually ---")

    def my_timer_generator(name: str) -> Generator[dict[str, Any], None, None]:
        """Raw generator (without @contextmanager)."""
        container: dict[str, Any] = {}
        start = time.perf_counter()
        yield container
        elapsed = time.perf_counter() - start
        container["result"] = f"{name}: {elapsed:.6f}s"

    # This is what @contextmanager does internally:
    gen = my_timer_generator("manual_test")

    # __enter__: run generator to first yield
    container = next(gen)
    print(f"  __enter__ returned: {container}")      # empty dict

    # Body of 'with' block would run here
    total = sum(range(500_000))

    # __exit__: resume generator after yield
    try:
        next(gen)                                    # generator finishes
    except StopIteration:
        pass                                         # expected

    print(f"  After __exit__: {container}")           # now has result

    # --- 7b: .throw() demonstration ---
    print("\n--- 7b: .throw() — how exceptions enter generators ---")

    def demo_throw() -> Generator[str, None, None]:
        """Generator that receives exceptions via .throw()."""
        try:
            yield "waiting"
        except ValueError as e:
            print(f"  [gen] Caught inside generator: {e}")
            yield "recovered"

    gen = demo_throw()
    print(f"  next(): {next(gen)}")
    # .throw() sends an exception INTO the generator at the yield point
    print(f"  throw(): {gen.throw(ValueError('test error'))}")

    print()


# =============================================================================
# SECTION 8: PRACTICAL PATTERNS — Timer, Streaming, Resource Management
# =============================================================================

def section_8_practical_patterns() -> None:
    """Production patterns using generators and context managers.

    These patterns directly map to your v8.1 roadmap projects.
    """
    print("=" * 70)
    print("SECTION 8: PRACTICAL PATTERNS")
    print("=" * 70)

    # --- 8a: timed() decorator that wraps timer() context manager ---
    print("\n--- 8a: timed() decorator wrapping timer() (type-safe) ---")
    print("  Uses ParamSpec + TypeVar to preserve function signatures")
    print("  See Section 10 for full ParamSpec/TypeVar explanation\n")

    # Type variables for preserving decorated function signatures
    P = ParamSpec("P")     # captures the function's parameter types
    T = TypeVar("T")       # captures the function's return type

    @dataclass(frozen=True, slots=True)
    class BResult:
        operation: str
        elapsed_seconds: float

    @contextmanager
    def timer_cm(name: str) -> Generator[dict[str, Any], None, None]:
        container: dict[str, Any] = {}
        start = time.perf_counter()
        yield container
        elapsed = time.perf_counter() - start
        container["result"] = BResult(operation=name, elapsed_seconds=elapsed)

    def timed(operation_name: str) -> Callable[[Callable[P, T]], Callable[P, T]]:
        """Type-safe decorator that wraps timer() context manager.

        Three-layer structure:
            timed("load")              → returns decorator  (receives NAME)
            decorator(my_func)         → returns wrapper    (receives FUNCTION)
            wrapper(*args, **kwargs)   → calls func + times (receives ARGUMENTS)

        ParamSpec(P) + TypeVar(T) ensure mypy knows the decorated function
        keeps its original parameter types and return type.
        """
        def decorator(func: Callable[P, T]) -> Callable[P, T]:
            @wraps(func)
            def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
                with timer_cm(operation_name) as t:
                    result = func(*args, **kwargs)
                wrapper.benchmark = t["result"]       # type: ignore[attr-defined]
                return result
            wrapper.benchmark = None                  # type: ignore[attr-defined]
            return wrapper
        return decorator

    @timed("computation")
    def heavy_work(n: int) -> int:
        """Sum numbers from 0 to n."""
        return sum(range(n))

    answer = heavy_work(1_000_000)
    print(f"  Result: {answer}")
    print(f"  Benchmark: {heavy_work.benchmark}")

    # After decoration, mypy still knows:
    #   heavy_work: (n: int) -> int    ← types preserved!
    # Without ParamSpec/TypeVar, mypy would see:
    #   heavy_work: (*Any, **Any) -> Any  ← types erased!

    # --- 8b: Generator pipeline (chaining generators) ---
    print("\n--- 8b: Generator pipeline (composable data streaming) ---")
    print("  Chain generators like Unix pipes: data | filter | transform\n")

    def read_lines(text: str) -> Iterator[str]:
        """Stage 1: Yield lines from text."""
        for line in text.strip().split("\n"):
            yield line

    def filter_nonempty(lines: Iterator[str]) -> Iterator[str]:
        """Stage 2: Skip empty lines."""
        for line in lines:
            if line.strip():
                yield line

    def to_uppercase(lines: Iterator[str]) -> Iterator[str]:
        """Stage 3: Transform to uppercase."""
        for line in lines:
            yield line.upper()

    sample_text = """
    hello world

    python generators

    are powerful
    """

    # Chain them together — no intermediate lists, constant memory
    pipeline = to_uppercase(filter_nonempty(read_lines(sample_text)))

    for line in pipeline:
        print(f"  → {line}")

    # --- 8c: Generator with cleanup (close) ---
    print("\n--- 8c: Generator cleanup with .close() ---")

    def limited_reader() -> Iterator[int]:
        """Generator that cleans up when closed early."""
        try:
            for i in range(1_000_000):
                yield i
        except GeneratorExit:
            # Called when .close() is invoked or generator is garbage collected
            print("  [gen] Cleanup: generator closed early")

    gen = limited_reader()
    for i, val in enumerate(gen):
        if i >= 3:
            gen.close()          # explicitly stop — triggers GeneratorExit
            break
        print(f"  Got: {val}")

    print()


# =============================================================================
# SECTION 9: COMMON PITFALLS AND GOTCHAS
# =============================================================================

def section_9_pitfalls() -> None:
    """Common mistakes with generators, iterators, and context managers."""
    print("=" * 70)
    print("SECTION 9: COMMON PITFALLS AND GOTCHAS")
    print("=" * 70)

    # --- 9a: Generator exhaustion ---
    print("\n--- 9a: Generators exhaust — can only iterate ONCE ---")

    def numbers() -> Iterator[int]:
        yield 1
        yield 2
        yield 3

    gen = numbers()
    first_pass = list(gen)          # consumes all values
    second_pass = list(gen)         # empty — already exhausted!

    print(f"  First pass:  {first_pass}")     # [1, 2, 3]
    print(f"  Second pass: {second_pass}")    # [] ← empty!
    print("  Fix: create a new generator, or use list() if you need multiple passes")

    # --- 9b: Forgetting to prime send() generators ---
    print("\n--- 9b: Must call next() before send() ---")

    def receiver() -> Generator[str, int, None]:
        while True:
            value = yield "ready"
            print(f"  Got: {value}")

    gen = receiver()
    # gen.send(42)  ← TypeError! Can't send to a just-started generator
    next(gen)         # ← must prime first
    gen.send(42)      # now it works
    print("  Fix: always call next(gen) before gen.send()")

    # --- 9c: Context manager without with ---
    print("\n--- 9c: Context managers MUST be used with 'with' ---")
    print("  # WRONG — cleanup never runs:")
    print("  f = open('file.txt')")
    print("  data = f.read()")
    print("  # forgot f.close() → file handle leaked!")
    print()
    print("  # CORRECT — cleanup guaranteed:")
    print("  with open('file.txt') as f:")
    print("      data = f.read()")
    print("  # f.close() called automatically")

    # --- 9d: Returning inside a generator ---
    print("\n--- 9d: return in a generator ends it (doesn't yield) ---")

    def tricky() -> Iterator[int]:
        yield 1
        yield 2
        return          # ← stops the generator, StopIteration raised
        yield 3         # ← NEVER reached

    result = list(tricky())
    print(f"  Result: {result}")     # [1, 2] — no 3!

    # --- 9e: yield from --- delegation to sub-generator ---
    print("\n--- 9e: yield from — delegate to another generator ---")

    def inner() -> Iterator[int]:
        yield 1
        yield 2

    def outer_manual() -> Iterator[int]:
        """Manual delegation — verbose."""
        for val in inner():
            yield val
        yield 3

    def outer_yield_from() -> Iterator[int]:
        """yield from — clean delegation."""
        yield from inner()     # yields all values from inner()
        yield 3

    print(f"  Manual:     {list(outer_manual())}")
    print(f"  yield from: {list(outer_yield_from())}")

    print()


# =============================================================================
# SECTION 10: ParamSpec + TypeVar — Type-Safe Decorators
# =============================================================================
# ┌─────────────────────────────────────────────────────────────────┐
# │         THE PROBLEM: DECORATORS ERASE TYPE INFO                 │
# │─────────────────────────────────────────────────────────────────│
# │                                                                 │
# │  WITHOUT ParamSpec/TypeVar:                                     │
# │                                                                 │
# │    def timed(name):                                             │
# │        def decorator(func):         ← func: Callable (no info) │
# │            def wrapper(*args, **kwargs):  ← Any, Any            │
# │                return func(...)     ← returns Any               │
# │            return wrapper                                       │
# │        return decorator                                         │
# │                                                                 │
# │    @timed("load")                                               │
# │    def load_dict(path: str) -> bool: ...                        │
# │                                                                 │
# │    # mypy thinks: load_dict(*Any, **Any) -> Any  ← ERASED!     │
# │    result: str = load_dict(42)  ← mypy says "fine" (it's NOT)  │
# │                                                                 │
# │  WITH ParamSpec/TypeVar:                                        │
# │                                                                 │
# │    P = ParamSpec("P")                                           │
# │    T = TypeVar("T")                                             │
# │                                                                 │
# │    def timed(name) -> Callable[[Callable[P, T]], Callable[P,T]]:│
# │        def decorator(func: Callable[P, T]) -> Callable[P, T]:  │
# │            def wrapper(*args: P.args, **kwargs: P.kwargs) -> T: │
# │                return func(...)     ← returns T (preserved!)    │
# │            return wrapper                                       │
# │        return decorator                                         │
# │                                                                 │
# │    @timed("load")                                               │
# │    def load_dict(path: str) -> bool: ...                        │
# │                                                                 │
# │    # mypy knows: load_dict(path: str) -> bool  ← PRESERVED!    │
# │    result: str = load_dict(42)  ← mypy ERROR: int!=str, str!=  │
# └─────────────────────────────────────────────────────────────────┘

def section_10_paramspec_typevar() -> None:
    """Demonstrate ParamSpec and TypeVar for type-safe decorators.

    ParamSpec captures a function's PARAMETER types as a group.
    TypeVar captures a function's RETURN type.
    Together they let decorators say: "the output function has the
    SAME signature as the input function."
    """
    print("=" * 70)
    print("SECTION 10: ParamSpec + TypeVar — Type-Safe Decorators")
    print("=" * 70)

    # --- 10a: TypeVar basics — captures ONE type ---
    print("\n--- 10a: TypeVar — captures and reuses a single type ---")

    T_demo = TypeVar("T_demo")

    def identity(x: T_demo) -> T_demo:
        """Returns exactly what it receives — type preserved.

        T_demo 'binds' to whatever type flows in:
          identity(42)    → T_demo = int  → returns int
          identity("hi")  → T_demo = str  → returns str

        mypy tracks this binding through the function.
        """
        return x

    int_result = identity(42)        # mypy knows: int
    str_result = identity("hello")   # mypy knows: str
    print(f"  identity(42) = {int_result} (mypy knows it's int)")
    print(f"  identity('hello') = {str_result} (mypy knows it's str)")

    # --- 10b: ParamSpec basics — captures ALL parameters as a group ---
    print("\n--- 10b: ParamSpec — captures parameter types as a group ---")
    print("  ParamSpec('P') captures the entire parameter list:")
    print("    def load(path: str, verbose: bool) -> bool:")
    print("    P binds to → (path: str, verbose: bool)")
    print("    P.args  = positional args types")
    print("    P.kwargs = keyword args types")
    print()
    print("  Unlike TypeVar which captures ONE type,")
    print("  ParamSpec captures the WHOLE signature at once.")

    # --- 10c: The type flow through a decorated function ---
    print("\n--- 10c: How types flow through a parameterized decorator ---")

    P10 = ParamSpec("P10")
    T10 = TypeVar("T10")

    def logged(label: str) -> Callable[[Callable[P10, T10]], Callable[P10, T10]]:
        """Type-safe decorator — preserves the decorated function's types.

        The return type reads as:
          "Returns a function that:
             takes a Callable[P, T]  (original function)
             returns a Callable[P, T]  (same signature!)"

        Breaking down Callable[[Callable[P, T]], Callable[P, T]]:
          Callable[                      outer: the decorator itself
              [Callable[P, T]],          input: original function
              Callable[P, T]             output: wrapped function (SAME types)
          ]
        """
        def decorator(func: Callable[P10, T10]) -> Callable[P10, T10]:
            @wraps(func)
            def wrapper(*args: P10.args, **kwargs: P10.kwargs) -> T10:
                print(f"    [{label}] Calling {func.__name__}")
                result = func(*args, **kwargs)
                print(f"    [{label}] {func.__name__} returned: {result}")
                return result    # returns T10 — type preserved
            return wrapper
        return decorator

    @logged("demo")
    def add(a: int, b: int) -> int:
        """Add two numbers."""
        return a + b

    @logged("demo")
    def greet(name: str) -> str:
        """Greet someone."""
        return f"Hello, {name}!"

    # Types are fully preserved after decoration:
    sum_result = add(3, 4)          # mypy knows: int
    greet_result = greet("Manuel")  # mypy knows: str
    print(f"  add(3, 4) = {sum_result}")
    print(f"  greet('Manuel') = {greet_result}")
    print(f"  add.__name__ = '{add.__name__}' (preserved by @wraps)")

    # --- 10d: P.args and P.kwargs explained ---
    print("\n--- 10d: P.args and P.kwargs syntax ---")
    print("  Inside the wrapper, you can't write *args: P")
    print("  ParamSpec has TWO special attributes:\n")
    print("    def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:")
    print("                       ↑                  ↑")
    print("                 positional args     keyword args")
    print("                 types from P        types from P")
    print()
    print("  If the original function is:")
    print("    def load(path: str, verbose: bool = False) -> bool")
    print()
    print("  Then P.args captures:   (str,)")
    print("  And P.kwargs captures:  {verbose: bool}")
    print("  And T captures:         bool")

    # --- 10e: Three-layer decorator with ParamSpec ---
    print("\n--- 10e: Why three layers? ---")
    print("  A decorator WITH parameters needs three nested functions:")
    print()
    print("    timed('load')              → returns decorator  (LAYER 1: name)")
    print("    decorator(load_dict)       → returns wrapper    (LAYER 2: function)")
    print("    wrapper(*args, **kwargs)   → calls + times      (LAYER 3: arguments)")
    print()
    print("  Python evaluates @timed('load') in two steps:")
    print("    Step 1: Python calls timed('load') → gets decorator")
    print("    Step 2: Python calls decorator(load_dict) → gets wrapper")
    print()
    print("  A decorator WITHOUT parameters only needs two layers:")
    print("    @simple_log       → decorator(func) → wrapper(*args)")

    # --- 10f: What mypy catches with ParamSpec/TypeVar ---
    print("\n--- 10f: What mypy catches (type safety in action) ---")
    print("  @timed('load')")
    print("  def load_dict(path: str) -> bool: ...")
    print()
    print("  # WITH ParamSpec/TypeVar — mypy catches ALL of these:")
    print("  result: str = load_dict('large')  # ERROR: bool != str")
    print("  load_dict(42)                     # ERROR: int != str")
    print("  load_dict()                       # ERROR: missing 'path'")
    print("  load_dict('a', 'b')               # ERROR: too many args")
    print()
    print("  # WITHOUT ParamSpec/TypeVar — mypy catches NONE:")
    print("  result: str = load_dict('large')  # 'fine' (it's not)")
    print("  load_dict(42)                     # 'fine' (it's not)")

    # --- 10g: Common mistake — mixing type and ParamSpec ---
    print("\n--- 10g: Pitfall — type statement vs ParamSpec/TypeVar ---")
    print("  # WRONG — 'type' statement has its own scope")
    print("  P = ParamSpec('P')")
    print("  T = TypeVar('T')")
    print("  type Wrapped = Callable[P, T]   # ERROR: P, T not in scope!")
    print()
    print("  # CORRECT — use P and T directly in function signatures")
    print("  def timed(name: str) -> Callable[[Callable[P, T]], Callable[P, T]]:")
    print("      ...")
    print()
    print("  # WHY: P and T need to 'flow' through all three decorator")
    print("  # layers. The 'type' statement creates isolated scope.")
    print("  # Type aliases break the flow. Write types inline instead.")

    # --- 10h: Where you'll use this pattern ---
    print("\n--- 10h: Your v8.1 roadmap usage ---")
    print("  Every parameterized decorator you write should use P + T:")
    print("  • Speller:     @timed('load') — benchmarks.py")
    print("  • DataVault:   @retry(max_attempts=3) — LLM API calls")
    print("  • PolicyPulse: @cached_embedding — vector store queries")
    print("  • FormSense:   @validate_input — form field validation")
    print("  • AFC:         @rate_limited(calls_per_min=60) — SEC API")
    print("  • Stage 2:     @log_pipeline_step — Airflow task decoration")
    print("  • Stage 3:     @track_experiment — MLflow metric logging")

    print()


# =============================================================================
# SECTION 11: typing vs collections.abc — Where to Import What
# =============================================================================
# ┌─────────────────────────────────────────────────────────────────┐
# │       typing vs collections.abc IMPORT RULES                    │
# │─────────────────────────────────────────────────────────────────│
# │                                                                 │
# │  HISTORY:                                                       │
# │    Python 3.5 (2015):  typing module created                    │
# │                        Generator, Iterator live in typing       │
# │    Python 3.9 (2020):  collections.abc becomes subscriptable    │
# │                        Can write collections.abc.Iterator[str]  │
# │    Python 3.12 (2023): typing versions marked as legacy aliases │
# │                                                                 │
# │  RULE: Import based on what the thing IS                        │
# │                                                                 │
# │  "Is it a CONTAINER or CALLABLE type?"                          │
# │    YES → from collections.abc                                   │
# │          (Generator, Iterator, Iterable, Callable, Sequence,    │
# │           Mapping, MutableMapping, Set, MutableSet)             │
# │                                                                 │
# │  "Is it a TYPE SYSTEM concept?"                                 │
# │    YES → from typing                                            │
# │          (Protocol, runtime_checkable, TypeVar, ParamSpec,      │
# │           Any, Final, TypeAlias, TypedDict, Literal)            │
# │                                                                 │
# │  WHY: collections.abc is the SOURCE OF TRUTH for runtime types. │
# │  typing re-exports them for backwards compatibility only.       │
# │  Modern tools (mypy, ruff, pyright) prefer collections.abc.    │
# └─────────────────────────────────────────────────────────────────┘

def section_11_import_rules() -> None:
    """Demonstrate the import rules for typing vs collections.abc."""
    print("=" * 70)
    print("SECTION 11: typing vs collections.abc — Import Rules")
    print("=" * 70)

    # --- 11a: Both work, but one is preferred ---
    print("\n--- 11a: Both work — one is preferred ---")
    print("  # OLD WAY (typing) — still works, but legacy")
    print("  from typing import Generator, Iterator, Callable")
    print()
    print("  # NEW WAY (collections.abc) — preferred since Python 3.9+")
    print("  from collections.abc import Generator, Iterator, Callable")
    print()
    print("  Both produce identical behavior. The difference is")
    print("  collections.abc is the source, typing is the re-export.")

    # --- 11b: What lives WHERE ---
    print("\n--- 11b: What lives where ---")
    print()
    print("  ┌──────────────────────────────────────────────────────┐")
    print("  │  from collections.abc        │  from typing          │")
    print("  │  (container/callable types)   │  (type system tools)  │")
    print("  │──────────────────────────────│───────────────────────│")
    print("  │  Generator                   │  Protocol             │")
    print("  │  Iterator                    │  runtime_checkable    │")
    print("  │  Iterable                    │  TypeVar              │")
    print("  │  Callable                    │  ParamSpec            │")
    print("  │  Sequence                    │  Any                  │")
    print("  │  Mapping                     │  Final                │")
    print("  │  MutableMapping              │  TypeAlias            │")
    print("  │  Set                         │  TypedDict            │")
    print("  │  MutableSet                  │  Literal              │")
    print("  │  Sized                       │  Annotated            │")
    print("  │  Container                   │  overload             │")
    print("  │──────────────────────────────│───────────────────────│")
    print("  │  ✓ Source of truth           │  ✓ No equivalent in   │")
    print("  │  ✓ What mypy/ruff recommend  │    collections.abc    │")
    print("  │  ✓ Modern codebases use this │  ✓ Type system only   │")
    print("  └──────────────────────────────────────────────────────┘")

    # --- 11c: Your Speller imports as a model ---
    print("\n--- 11c: Model imports for your Speller modules ---")
    print()
    print("  # benchmarks.py")
    print("  from collections.abc import Callable, Generator  # container types")
    print("  from typing import Any, ParamSpec, TypeVar        # type system")
    print()
    print("  # protocols.py")
    print("  from typing import Protocol, runtime_checkable    # type system only")
    print()
    print("  # text_processor.py")
    print("  from collections.abc import Iterator              # container type")
    print()
    print("  # dictionary.py")
    print("  # (no generic type imports needed — just uses set[str])")

    # --- 11d: The built-in types that also became subscriptable ---
    print("\n--- 11d: Built-in types (no import needed since 3.9) ---")
    print("  These built-in types are directly subscriptable since 3.9:")
    print()
    print("  list[str]          # was typing.List[str]")
    print("  dict[str, int]     # was typing.Dict[str, int]")
    print("  set[str]           # was typing.Set[str]")
    print("  tuple[int, str]    # was typing.Tuple[int, str]")
    print("  type[MyClass]      # was typing.Type[MyClass]")
    print()
    print("  NEVER import List, Dict, Set, Tuple, Type from typing.")
    print("  Just use the lowercase built-in names directly.")

    # --- 11e: Quick decision flowchart ---
    print("\n--- 11e: Quick decision ---")
    print("  1. Is it list, dict, set, tuple?  → use the built-in (no import)")
    print("  2. Is it Iterator, Generator,")
    print("     Callable, Sequence, Mapping?   → from collections.abc")
    print("  3. Is it Protocol, TypeVar,")
    print("     ParamSpec, Any, Final?         → from typing")
    print("  4. Not sure?                      → check if it represents a")
    print("                                       runtime object (→ collections)")
    print("                                       or a type concept (→ typing)")

    print()


# =============================================================================
# SECTION 12: DECISION GUIDE AND CHEAT SHEET
# =============================================================================
#
# ┌──────────────────────────────────────────────────────────────────┐
# │                    DECISION GUIDE                                │
# │──────────────────────────────────────────────────────────────────│
# │  Need to...                          │ Use                      │
# │──────────────────────────────────────│──────────────────────────│
# │  Stream data (one-way out)           │ Generator + Iterator     │
# │  Two-way communication               │ Generator + send()      │
# │  Ensure cleanup (files, DB, locks)   │ Context manager (with)   │
# │  Time a code block                   │ @contextmanager + yield  │
# │  Time a function                     │ Decorator wrapping CM    │
# │  Chain data transformations          │ Generator pipeline       │
# │  Process huge files without RAM      │ Generator (constant mem) │
# │  Stream LLM tokens                   │ async Generator          │
# └──────────────────────────────────────────────────────────────────┘
#
# ┌──────────────────────────────────────────────────────────────────┐
# │                    TYPE HINT CHEAT SHEET                         │
# │──────────────────────────────────────────────────────────────────│
# │  Pattern                    │ Type Hint                         │
# │─────────────────────────────│───────────────────────────────────│
# │  Simple streaming           │ Iterator[YieldType]               │
# │  with send()/return         │ Generator[Yield, Send, Return]    │
# │  @contextmanager            │ Generator[YieldType, None, None]  │
# │  Generator expression       │ Generator[YieldType, None, None]  │
# │  Class-based iterator       │ Iterator[YieldType]               │
# │  Accepts any iterable       │ Iterable[ItemType]                │
# └──────────────────────────────────────────────────────────────────┘
#
# ┌──────────────────────────────────────────────────────────────────┐
# │                 IMPORT CHEAT SHEET                               │
# │──────────────────────────────────────────────────────────────────│
# │  CONTAINER / CALLABLE TYPES → from collections.abc              │
# │    from collections.abc import Iterator         # simple yield  │
# │    from collections.abc import Generator        # yield+send+ret│
# │    from collections.abc import Iterable         # accepts any   │
# │    from collections.abc import Callable         # function types│
# │                                                                  │
# │  TYPE SYSTEM CONCEPTS → from typing                              │
# │    from typing import ParamSpec                 # param types   │
# │    from typing import TypeVar                   # return type   │
# │    from typing import Any                       # escape hatch  │
# │    from typing import Protocol, runtime_checkable  # interfaces │
# │    from typing import Final                     # immutability  │
# │                                                                  │
# │  STANDARD LIBRARY → direct import                                │
# │    from contextlib import contextmanager        # generator → CM│
# │    from functools import wraps                  # decorator help│
# │    import time  → time.perf_counter()           # high-res timer│
# │                                                                  │
# │  BUILT-IN TYPES → no import needed (Python 3.9+)                │
# │    list[str], dict[str, int], set[str], tuple[int, str]         │
# └──────────────────────────────────────────────────────────────────┘
#
# ┌──────────────────────────────────────────────────────────────────┐
# │              ParamSpec + TypeVar CHEAT SHEET                     │
# │──────────────────────────────────────────────────────────────────│
# │                                                                  │
# │  P = ParamSpec("P")   → captures ALL parameter types as a group │
# │  T = TypeVar("T")     → captures the return type                │
# │                                                                  │
# │  Simple decorator (no params):                                   │
# │    def deco(func: Callable[P, T]) -> Callable[P, T]:            │
# │        @wraps(func)                                              │
# │        def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:     │
# │            return func(*args, **kwargs)                          │
# │        return wrapper                                            │
# │                                                                  │
# │  Parameterized decorator (with params):                          │
# │    def deco(name: str) -> Callable[[Callable[P,T]], Callable[P,T]]:│
# │        def decorator(func: Callable[P, T]) -> Callable[P, T]:  │
# │            @wraps(func)                                          │
# │            def wrapper(*args: P.args, **kw: P.kwargs) -> T:    │
# │                return func(*args, **kw)                          │
# │            return wrapper                                        │
# │        return decorator                                          │
# │                                                                  │
# │  NEVER use 'type' statement with ParamSpec/TypeVar:              │
# │    type Wrapped = Callable[P, T]    # BROKEN — P, T not in scope│
# │  Instead write types INLINE on function signatures.              │
# └──────────────────────────────────────────────────────────────────┘
#
# ┌──────────────────────────────────────────────────────────────────┐
# │              YOUR SPELLER MODULE MAP                             │
# │──────────────────────────────────────────────────────────────────│
# │  Module              │ Pattern Used                             │
# │──────────────────────│─────────────────────────────────────────│
# │  text_processor.py   │ Generator → Iterator[str]               │
# │  benchmarks.py       │ @contextmanager → timer()               │
# │  benchmarks.py       │ Decorator → timed() wraps timer()       │
# │  benchmarks.py       │ ParamSpec + TypeVar for type-safe timed()│
# │  dictionary.py       │ Context manager → with open() in load() │
# │  __main__.py         │ Context manager → configure logging     │
# └──────────────────────────────────────────────────────────────────┘
#
# =============================================================================


# =============================================================================
# MAIN EXECUTION
# =============================================================================

if __name__ == "__main__":
    section_1_iterator_protocol()
    section_2_generator_functions()
    section_3_three_channels()
    section_4_type_hints()
    section_5_context_managers()
    section_6_contextmanager_decorator()
    section_7_internal_mechanics()
    section_8_practical_patterns()
    section_9_pitfalls()
    section_10_paramspec_typevar()
    section_11_import_rules()

    print("=" * 70)
    print("REFERENCE COMPLETE — See Section 12 (cheat sheets) in source code")
    print("=" * 70)