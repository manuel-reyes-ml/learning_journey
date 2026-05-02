"""
python_protocols_abc_reference.py
==================================

Personal reference: Python Protocol (structural typing) and ABC
(Abstract Base Classes / nominal typing) — how they define contracts,
when to use each, and production patterns for swappable backends.

Topics covered
--------------
1.  The Problem — Why interfaces matter (swappable backends)
2.  ABC — Abstract Base Classes (nominal typing / inheritance)
3.  Protocol — Structural subtyping (duck typing with type safety)
4.  ABC vs Protocol — Side-by-side comparison
5.  @runtime_checkable — Adding isinstance() support to Protocol
6.  Protocol with Properties and Attributes
7.  Protocol with @dataclass and Pydantic
8.  Dependency Injection — Wiring protocols to concrete classes
9.  collections.abc — Built-in protocols you already use
10. Common Pitfalls and Gotchas
11. Decision Guide and Cheat Sheet

Why this matters for your roadmap (v8.1 GenAI-First)
------------------------------------------------------
- Stage 1 (Speller):     DictionaryProtocol for swappable dictionary backends
                          Dependency injection in __main__.py
- Stage 1 (DataVault):   LLMProvider protocol (swap Gemini/OpenAI/Claude/Ollama)
                          OutputFormatter protocol (swap JSON/table/chart outputs)
- Stage 1 (PolicyPulse): VectorStore protocol (swap ChromaDB → Pinecone in Stage 4)
                          EmbeddingProvider protocol (swap embedding models)
                          Retriever protocol (swap retrieval strategies)
- Stage 1 (FormSense):   ExtractionBackend protocol (swap Gemini Vision → custom)
                          Validator protocol (swap ERISA rule engines)
- Stage 1 (StreamSmart): ContentAPI protocol (swap Watchmode → TMDB → scraper)
- Stage 1 (AFC):         DataSource protocol (swap SEC/Wikipedia/news providers)
- Stage 2 (Data Eng):    StorageBackend protocol (swap S3 → GCS → local)
                          QueueProvider protocol (swap SQS → RabbitMQ)
- Stage 3 (ML):          ModelBackend protocol (swap scikit-learn → PyTorch → TF)
                          Trainer protocol for MLOps pipeline abstraction
- Stage 4 (LLM):         AgentTool protocol (MCP tool integration)
                          Memory protocol (swap conversation memory backends)
- Stage 5 (Senior):      All protocols combined in production multi-provider systems

How to use this file
---------------------
Run it directly to see all output::

    $ python python_protocols_abc_reference.py

Or import individual sections to experiment in a REPL::

    >>> from python_protocols_abc_reference import section_3_protocol

Author: Manuel Reyes — CS50 Speller / Stage 1 Learning Reference
Version: 1.0.0 — March 2026

References
----------
.. [1] PEP 544 — Protocols: Structural subtyping (static duck typing)
   https://peps.python.org/pep-0544/
.. [2] PEP 3119 — Introducing Abstract Base Classes
   https://peps.python.org/pep-3119/
.. [3] Python Docs — typing.Protocol
   https://docs.python.org/3/library/typing.html#typing.Protocol
.. [4] Python Docs — abc module
   https://docs.python.org/3/library/abc.html
.. [5] Python Docs — collections.abc
   https://docs.python.org/3/library/collections.abc.html
.. [6] mypy — Protocols and structural subtyping
   https://mypy.readthedocs.io/en/stable/protocols.html
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Iterator
from dataclasses import dataclass
from typing import Any, Protocol, runtime_checkable


# =============================================================================
# SECTION 1: THE PROBLEM — Why Interfaces Matter
# =============================================================================
# ┌─────────────────────────────────────────────────────────────────┐
# │                WHY INTERFACES MATTER                            │
# │─────────────────────────────────────────────────────────────────│
# │                                                                 │
# │  WITHOUT an interface (hardcoded dependency):                   │
# │                                                                 │
# │    class DataVault:                                             │
# │        def __init__(self):                                      │
# │            self.llm = GeminiClient()  ← stuck with Gemini      │
# │                                                                 │
# │  Problem: To use OpenAI, you rewrite DataVault.                 │
# │  Problem: To test, you need a real Gemini API key.              │
# │  Problem: Every change to GeminiClient might break DataVault.   │
# │                                                                 │
# │  WITH an interface (dependency on abstraction):                 │
# │                                                                 │
# │    class DataVault:                                             │
# │        def __init__(self, llm: LLMProvider):                    │
# │            self.llm = llm  ← accepts ANY provider              │
# │                                                                 │
# │  Solution: DataVault works with Gemini, OpenAI, Claude, Ollama  │
# │  Solution: Tests pass in a MockLLM (no API key needed)          │
# │  Solution: Providers change independently of DataVault          │
# │                                                                 │
# │  This is the Dependency Inversion Principle (the "D" in SOLID): │
# │  "Depend on abstractions, not concretions."                     │
# └─────────────────────────────────────────────────────────────────┘

def section_1_the_problem() -> None:
    """Demonstrate why interfaces and swappable backends matter."""
    print("=" * 70)
    print("SECTION 1: THE PROBLEM — Why Interfaces Matter")
    print("=" * 70)

    # --- 1a: Without an interface — hardcoded dependency ---
    print("\n--- 1a: WITHOUT interface (hardcoded — fragile) ---")

    class FakeGeminiClient:
        """Simulated Gemini client."""
        def complete(self, prompt: str) -> str:
            return f"[Gemini] Response to: {prompt}"

    class DataVaultHardcoded:
        """DataVault hardcoded to Gemini — CAN'T swap providers."""
        def __init__(self) -> None:
            self.llm = FakeGeminiClient()       # ← hardcoded!

        def analyze(self, query: str) -> str:
            return self.llm.complete(query)

    vault = DataVaultHardcoded()
    print(f"  {vault.analyze('show revenue')}")
    print("  Problem: Can't use OpenAI without rewriting DataVault")

    # --- 1b: With an interface — swappable backends ---
    print("\n--- 1b: WITH interface (flexible — swappable) ---")

    class FakeOpenAIClient:
        """Simulated OpenAI client."""
        def complete(self, prompt: str) -> str:
            return f"[OpenAI] Response to: {prompt}"

    class FakeMockLLM:
        """Test double — no API calls, deterministic output."""
        def complete(self, prompt: str) -> str:
            return f"[Mock] Deterministic response"

    class DataVaultFlexible:
        """DataVault that accepts ANY provider with .complete()."""
        def __init__(self, llm: Any) -> None:
            self.llm = llm                      # ← accepts anything

        def analyze(self, query: str) -> str:
            return self.llm.complete(query)

    # Same DataVault code, three different providers:
    print(f"  {DataVaultFlexible(FakeGeminiClient()).analyze('show revenue')}")
    print(f"  {DataVaultFlexible(FakeOpenAIClient()).analyze('show revenue')}")
    print(f"  {DataVaultFlexible(FakeMockLLM()).analyze('show revenue')}")
    print("  Solution: One DataVault, infinite providers")

    # --- 1c: The problem with 'Any' ---
    print("\n--- 1c: The problem with using 'Any' ---")
    print("  Using 'Any' works at runtime but loses type safety:")
    print("  • mypy can't check if the provider HAS .complete()")
    print("  • Typos like .complet() won't be caught until runtime")
    print("  • No autocomplete in VS Code / Cursor AI")
    print("  • No documentation of what methods are required")
    print()
    print("  Solution: Define a contract (ABC or Protocol) that specifies")
    print("  exactly what methods are required. Then mypy catches errors")
    print("  BEFORE your code runs.")

    print()


# =============================================================================
# SECTION 2: ABC — Abstract Base Classes (Nominal Typing)
# =============================================================================
# ┌─────────────────────────────────────────────────────────────────┐
# │              ABSTRACT BASE CLASSES (ABC)                        │
# │─────────────────────────────────────────────────────────────────│
# │                                                                 │
# │  ABC = "You MUST explicitly inherit from me"                    │
# │  This is NOMINAL typing — the class NAME matters                │
# │  Like a membership card: you have to sign up                    │
# │                                                                 │
# │  class Animal(ABC):               ← defines the contract       │
# │      @abstractmethod                                            │
# │      def speak(self) -> str: ...                                │
# │                                                                 │
# │  class Dog(Animal):               ← MUST inherit from Animal   │
# │      def speak(self) -> str:                                    │
# │          return "Woof"                                          │
# │                                                                 │
# │  class Robot:                     ← has speak() but didn't      │
# │      def speak(self) -> str:        inherit from Animal         │
# │          return "Beep"                                          │
# │                                                                 │
# │  isinstance(Dog(), Animal)    → True  (inherited)               │
# │  isinstance(Robot(), Animal)  → False (didn't inherit)          │
# │                                                                 │
# │  KEY: The class must DECLARE allegiance by inheriting.          │
# │  Having matching methods is NOT enough.                         │
# └─────────────────────────────────────────────────────────────────┘

def section_2_abc() -> None:
    """Demonstrate Abstract Base Classes (ABC) — nominal typing."""
    print("=" * 70)
    print("SECTION 2: ABC — Abstract Base Classes (Nominal Typing)")
    print("=" * 70)

    # --- 2a: Basic ABC definition ---
    print("\n--- 2a: Defining an ABC ---")

    class LLMProvider(ABC):
        """Abstract contract — all LLM providers must implement these.

        To satisfy this contract, a class MUST:
        1. Inherit from LLMProvider
        2. Implement all @abstractmethod methods
        If either is missing, Python raises TypeError on instantiation.
        """

        @abstractmethod
        def complete(self, prompt: str) -> str:
            """Generate a completion from a prompt."""
            ...

        @abstractmethod
        def model_name(self) -> str:
            """Return the model identifier."""
            ...

    # --- 2b: Implementing an ABC (correct way) ---
    print("\n--- 2b: Correct implementation (inherits + implements) ---")

    class GeminiProvider(LLMProvider):
        """Concrete implementation — inherits from LLMProvider."""

        def complete(self, prompt: str) -> str:
            return f"[Gemini] {prompt}"

        def model_name(self) -> str:
            return "gemini-pro"

    gemini = GeminiProvider()
    print(f"  isinstance(gemini, LLMProvider): {isinstance(gemini, LLMProvider)}")
    print(f"  gemini.complete('hello'): {gemini.complete('hello')}")
    print(f"  gemini.model_name(): {gemini.model_name()}")

    # --- 2c: Can't instantiate ABC directly ---
    print("\n--- 2c: Can't instantiate ABC directly ---")
    try:
        provider = LLMProvider()         # type: ignore[abstract]
    except TypeError as e:
        print(f"  TypeError: {e}")
        print("  ABC enforces: you MUST implement all abstract methods")

    # --- 2d: Missing an abstract method ---
    print("\n--- 2d: Missing an abstract method ---")

    class IncompleteProvider(LLMProvider):
        """Missing model_name() — will fail on instantiation."""
        def complete(self, prompt: str) -> str:
            return "response"
        # model_name() NOT implemented!

    try:
        bad = IncompleteProvider()       # type: ignore[abstract]
    except TypeError as e:
        print(f"  TypeError: {e}")
        print("  ABC catches missing methods at instantiation time")

    # --- 2e: ABC with concrete (shared) methods ---
    print("\n--- 2e: ABC with shared concrete methods ---")

    class DataSource(ABC):
        """ABC with both abstract AND concrete methods.

        Abstract methods: subclasses MUST implement
        Concrete methods: subclasses INHERIT for free

        This is where ABC has an advantage over Protocol —
        Protocol can't provide shared implementations.
        """

        @abstractmethod
        def fetch(self, query: str) -> list[str]:
            """Subclasses must implement this."""
            ...

        def fetch_with_retry(self, query: str, retries: int = 3) -> list[str]:
            """Shared logic — all subclasses get this for free.

            This concrete method calls the abstract fetch() method.
            Subclasses inherit retry logic without reimplementing it.
            """
            for attempt in range(retries):
                try:
                    return self.fetch(query)
                except ConnectionError:
                    if attempt == retries - 1:
                        raise
                    print(f"    Retry {attempt + 1}/{retries}...")
            return []

    class SECDataSource(DataSource):
        """Concrete implementation — only implements fetch()."""
        def fetch(self, query: str) -> list[str]:
            return [f"SEC filing: {query}"]

    sec = SECDataSource()
    # Gets fetch_with_retry() for FREE from the ABC
    result = sec.fetch_with_retry("AAPL 10-K")
    print(f"  sec.fetch_with_retry('AAPL 10-K'): {result}")
    print("  SECDataSource only wrote fetch() but gets retry logic for free")

    # --- 2f: Limitation — can't use with third-party classes ---
    print("\n--- 2f: ABC limitation — third-party classes ---")

    class ThirdPartyLLM:
        """Imagine this is from an external library (LangChain, OpenAI SDK).
        You CANNOT make it inherit from your LLMProvider ABC."""
        def complete(self, prompt: str) -> str:
            return f"[ThirdParty] {prompt}"

        def model_name(self) -> str:
            return "third-party-model"

    third_party = ThirdPartyLLM()
    print(f"  Has complete(): {hasattr(third_party, 'complete')}")
    print(f"  Has model_name(): {hasattr(third_party, 'model_name')}")
    print(f"  isinstance(third_party, LLMProvider): "
          f"{isinstance(third_party, LLMProvider)}")
    print("  ↑ False! Even though it has ALL required methods")
    print("  This is ABC's biggest limitation — Protocol solves this")

    print()


# =============================================================================
# SECTION 3: PROTOCOL — Structural Subtyping (Duck Typing with Type Safety)
# =============================================================================
# ┌─────────────────────────────────────────────────────────────────┐
# │                    PROTOCOL                                     │
# │─────────────────────────────────────────────────────────────────│
# │                                                                 │
# │  Protocol = "I don't care WHO you are, I care WHAT you can do"  │
# │  This is STRUCTURAL typing — the SHAPE matters, not the NAME    │
# │  Like a door that checks "do you have a key?" — doesn't care    │
# │  where you got it                                               │
# │                                                                 │
# │  class Speakable(Protocol):        ← defines the contract       │
# │      def speak(self) -> str: ...                                │
# │                                                                 │
# │  class Dog:                        ← NO inheritance needed!     │
# │      def speak(self) -> str:                                    │
# │          return "Woof"                                          │
# │                                                                 │
# │  class Robot:                      ← also satisfies contract    │
# │      def speak(self) -> str:                                    │
# │          return "Beep"                                          │
# │                                                                 │
# │  Both Dog and Robot satisfy Speakable because they HAVE         │
# │  a speak() method — no inheritance declaration needed.          │
# │                                                                 │
# │  mypy checks this at COMPILE TIME (static analysis)             │
# │  @runtime_checkable adds isinstance() for RUNTIME checks        │
# └─────────────────────────────────────────────────────────────────┘

def section_3_protocol() -> None:
    """Demonstrate Protocol — structural subtyping (duck typing + type safety)."""
    print("=" * 70)
    print("SECTION 3: PROTOCOL — Structural Subtyping")
    print("=" * 70)

    # --- 3a: Basic Protocol definition ---
    print("\n--- 3a: Defining a Protocol ---")

    @runtime_checkable
    class Completable(Protocol):
        """Any class with a complete() method satisfies this.

        No inheritance needed. mypy checks at compile time.
        @runtime_checkable adds isinstance() support.
        """
        def complete(self, prompt: str) -> str:
            """The ONLY requirement: have this method signature."""
            ...

    # --- 3b: Classes that satisfy the Protocol (no inheritance!) ---
    print("\n--- 3b: Classes satisfying Protocol (no inheritance) ---")

    class GeminiClient:
        """Has complete() → satisfies Completable. No inheritance."""
        def complete(self, prompt: str) -> str:
            return f"[Gemini] {prompt}"

    class OpenAIClient:
        """Has complete() → satisfies Completable. No inheritance."""
        def complete(self, prompt: str) -> str:
            return f"[OpenAI] {prompt}"

    class MockLLM:
        """Test double — also satisfies Completable."""
        def complete(self, prompt: str) -> str:
            return "[Mock] Deterministic output"

    # All three satisfy Completable — zero inheritance
    for client in [GeminiClient(), OpenAIClient(), MockLLM()]:
        print(f"  isinstance({type(client).__name__}, Completable): "
              f"{isinstance(client, Completable)}")
        print(f"    → {client.complete('test prompt')}")

    # --- 3c: Class that does NOT satisfy the Protocol ---
    print("\n--- 3c: Class that does NOT satisfy Protocol ---")

    class BrokenClient:
        """Has 'generate' instead of 'complete' — does NOT satisfy."""
        def generate(self, prompt: str) -> str:
            return "response"

    print(f"  isinstance(BrokenClient(), Completable): "
          f"{isinstance(BrokenClient(), Completable)}")
    print("  ↑ False! Method name doesn't match")

    # --- 3d: Protocol with multiple methods ---
    print("\n--- 3d: Protocol with multiple methods ---")

    @runtime_checkable
    class DictionaryProtocol(Protocol):
        """Your Speller protocol — requires three methods.

        ALL three must be present for a class to satisfy it.
        """
        def load(self, filepath: str) -> bool: ...
        def check(self, word: str) -> bool: ...
        def size(self) -> int: ...

    class HashTableDictionary:
        """Satisfies DictionaryProtocol — has all three methods."""
        def __init__(self) -> None:
            self._words: set[str] = set()

        def load(self, filepath: str) -> bool:
            self._words = {"cat", "dog", "fish"}
            return True

        def check(self, word: str) -> bool:
            return word.lower() in self._words

        def size(self) -> int:
            return len(self._words)

    class PartialDictionary:
        """Missing size() — does NOT satisfy DictionaryProtocol."""
        def load(self, filepath: str) -> bool:
            return True
        def check(self, word: str) -> bool:
            return True
        # NO size() method!

    htd = HashTableDictionary()
    pd = PartialDictionary()
    print(f"  HashTableDictionary satisfies: {isinstance(htd, DictionaryProtocol)}")
    print(f"  PartialDictionary satisfies:   {isinstance(pd, DictionaryProtocol)}")

    # --- 3e: Using Protocol as type hint in functions ---
    print("\n--- 3e: Protocol as function parameter type ---")

    def run_spell_check(dictionary: DictionaryProtocol, words: list[str]) -> None:
        """Accepts ANY object satisfying DictionaryProtocol.

        This function never imports HashTableDictionary.
        It only knows about the Protocol (the contract).
        mypy verifies the caller passes a valid implementation.
        """
        dictionary.load("dictionaries/large")
        for word in words:
            status = "✓" if dictionary.check(word) else "✗"
            print(f"    {status} {word}")
        print(f"    Dictionary size: {dictionary.size()}")

    run_spell_check(HashTableDictionary(), ["cat", "xyz", "dog"])

    print()


# =============================================================================
# SECTION 4: ABC vs PROTOCOL — Side-by-Side Comparison
# =============================================================================
# ┌──────────────────────────────────────────────────────────────────┐
# │                 ABC vs PROTOCOL COMPARISON                       │
# │──────────────────────────────────────────────────────────────────│
# │                                                                  │
# │  Feature              │ ABC               │ Protocol             │
# │───────────────────────│───────────────────│──────────────────────│
# │  Typing style         │ Nominal           │ Structural           │
# │  Inheritance needed   │ YES               │ NO                   │
# │  Third-party classes  │ Can't use them    │ Works if methods     │
# │                       │                   │ match                │
# │  Shared methods       │ YES (concrete     │ NO (interface only)  │
# │                       │ methods in ABC)   │                      │
# │  Instantiation guard  │ YES (can't create │ NO (Protocol itself  │
# │                       │ ABC instance)     │ is not enforced)     │
# │  mypy checking        │ YES               │ YES                  │
# │  isinstance()         │ YES (always)      │ YES (if              │
# │                       │                   │ @runtime_checkable)  │
# │  When to use          │ You OWN all       │ You DON'T own all    │
# │                       │ classes AND need   │ classes OR want      │
# │                       │ shared logic       │ loose coupling       │
# │  Python analogy       │ Membership card    │ Door checks for key  │
# │  Real-world analogy   │ "Are you a member │ "Can you do the      │
# │                       │  of this club?"   │  job?"               │
# └──────────────────────────────────────────────────────────────────┘

def section_4_abc_vs_protocol() -> None:
    """Side-by-side comparison of ABC and Protocol with the same contract."""
    print("=" * 70)
    print("SECTION 4: ABC vs PROTOCOL — Side-by-Side")
    print("=" * 70)

    # --- 4a: Same contract, two approaches ---
    print("\n--- 4a: Same contract defined both ways ---")

    # ABC approach
    class StorageABC(ABC):
        """ABC: classes MUST inherit to satisfy."""
        @abstractmethod
        def save(self, key: str, data: str) -> bool: ...

        @abstractmethod
        def load(self, key: str) -> str | None: ...

    # Protocol approach
    @runtime_checkable
    class StorageProtocol(Protocol):
        """Protocol: classes just need matching methods."""
        def save(self, key: str, data: str) -> bool: ...
        def load(self, key: str) -> str | None: ...

    # --- 4b: Class that inherits from ABC ---
    class LocalFileABC(StorageABC):
        """Satisfies ABC by inheriting."""
        def save(self, key: str, data: str) -> bool:
            return True
        def load(self, key: str) -> str | None:
            return f"data for {key}"

    # --- 4c: Class that matches Protocol (no inheritance) ---
    class LocalFileProtocol:
        """Satisfies Protocol by having matching methods."""
        def save(self, key: str, data: str) -> bool:
            return True
        def load(self, key: str) -> str | None:
            return f"data for {key}"

    # --- 4d: Third-party class (can't modify) ---
    class ThirdPartyS3:
        """Imagine this is from boto3 — you can't add inheritance."""
        def save(self, key: str, data: str) -> bool:
            return True
        def load(self, key: str) -> str | None:
            return f"s3://{key}"

    abc_impl = LocalFileABC()
    proto_impl = LocalFileProtocol()
    third_party = ThirdPartyS3()

    print("  ABC isinstance checks:")
    print(f"    LocalFileABC:    {isinstance(abc_impl, StorageABC)}")
    print(f"    LocalFileProto:  {isinstance(proto_impl, StorageABC)}")
    print(f"    ThirdPartyS3:    {isinstance(third_party, StorageABC)}")

    print("\n  Protocol isinstance checks:")
    print(f"    LocalFileABC:    {isinstance(abc_impl, StorageProtocol)}")
    print(f"    LocalFileProto:  {isinstance(proto_impl, StorageProtocol)}")
    print(f"    ThirdPartyS3:    {isinstance(third_party, StorageProtocol)}")
    print("\n  ↑ Protocol accepts ThirdPartyS3 — ABC rejects it!")
    print("  This is why Protocol wins for your multi-provider projects")

    # --- 4e: ABC advantage — shared concrete methods ---
    print("\n--- 4e: ABC advantage — shared methods ---")

    class RetryableStorageABC(ABC):
        """ABC can include shared logic that ALL subclasses inherit."""

        @abstractmethod
        def save(self, key: str, data: str) -> bool: ...

        def save_with_retry(self, key: str, data: str, retries: int = 3) -> bool:
            """Shared retry logic — subclasses get this for free."""
            for attempt in range(retries):
                if self.save(key, data):
                    return True
                print(f"    Retry {attempt + 1}...")
            return False

    print("  ABC can provide shared concrete methods (like retry logic)")
    print("  Protocol CANNOT — it's interface-only")
    print("  If you need shared logic: use ABC or a mixin class")

    print()


# =============================================================================
# SECTION 5: @runtime_checkable — Deep Dive
# =============================================================================
# ┌─────────────────────────────────────────────────────────────────┐
# │              @runtime_checkable DETAILS                         │
# │─────────────────────────────────────────────────────────────────│
# │                                                                 │
# │  Without @runtime_checkable:                                    │
# │    - mypy checks Protocol at COMPILE time (static analysis)     │
# │    - isinstance() raises TypeError at runtime                   │
# │                                                                 │
# │  With @runtime_checkable:                                       │
# │    - mypy still checks at compile time                          │
# │    - isinstance() ALSO works at runtime                         │
# │                                                                 │
# │  IMPORTANT LIMITATION:                                          │
# │    @runtime_checkable only checks method EXISTENCE              │
# │    It does NOT check:                                           │
# │      - Method signatures (parameter types, return types)        │
# │      - Number of parameters                                     │
# │      - Method behavior                                          │
# │    Full signature checking only happens with mypy               │
# └─────────────────────────────────────────────────────────────────┘

def section_5_runtime_checkable() -> None:
    """Deep dive into @runtime_checkable behavior and limitations."""
    print("=" * 70)
    print("SECTION 5: @runtime_checkable — Deep Dive")
    print("=" * 70)

    # --- 5a: Without @runtime_checkable ---
    print("\n--- 5a: Protocol WITHOUT @runtime_checkable ---")

    class NotCheckable(Protocol):
        """Protocol without @runtime_checkable — mypy only."""
        def process(self) -> str: ...

    class Worker:
        def process(self) -> str:
            return "done"

    try:
        result = isinstance(Worker(), NotCheckable)
        print(f"  isinstance check: {result}")
    except TypeError as e:
        print(f"  TypeError: {e}")
        print("  ↑ Can't use isinstance() without @runtime_checkable")

    # --- 5b: With @runtime_checkable ---
    print("\n--- 5b: Protocol WITH @runtime_checkable ---")

    @runtime_checkable
    class Checkable(Protocol):
        """Protocol with @runtime_checkable — mypy AND isinstance()."""
        def process(self) -> str: ...

    print(f"  isinstance(Worker(), Checkable): {isinstance(Worker(), Checkable)}")
    print("  ↑ Works! @runtime_checkable enables isinstance()")

    # --- 5c: The limitation — only checks method EXISTENCE ---
    print("\n--- 5c: Limitation — only checks existence, not signatures ---")

    @runtime_checkable
    class Adder(Protocol):
        """Contract: add(a: int, b: int) -> int"""
        def add(self, a: int, b: int) -> int: ...

    class CorrectAdder:
        """Correct signature — add(int, int) -> int"""
        def add(self, a: int, b: int) -> int:
            return a + b

    class WrongSignature:
        """WRONG signature — add() takes no args! But isinstance still says True."""
        def add(self) -> str:
            return "wrong"

    correct = CorrectAdder()
    wrong = WrongSignature()
    print(f"  CorrectAdder satisfies Adder: {isinstance(correct, Adder)}")
    print(f"  WrongSignature satisfies Adder: {isinstance(wrong, Adder)}")
    print("  ↑ Both True! @runtime_checkable only checks 'has add attribute'")
    print("  mypy would catch the signature mismatch — isinstance cannot")
    print("  This is why running mypy --strict is essential")

    # --- 5d: Practical guard pattern ---
    print("\n--- 5d: Practical guard pattern for your projects ---")
    print("  Use isinstance() as a runtime safety net in factory functions:\n")
    print("  def create_speller(dictionary: DictionaryProtocol) -> Speller:")
    print("      if not isinstance(dictionary, DictionaryProtocol):")
    print("          raise TypeError(")
    print('          f"Expected DictionaryProtocol, got {type(dictionary)}"')
    print("      )")
    print("      return Speller(dictionary)")

    print()


# =============================================================================
# SECTION 6: PROTOCOL WITH PROPERTIES AND ATTRIBUTES
# =============================================================================

def section_6_properties_and_attributes() -> None:
    """Demonstrate Protocol with @property and class attributes."""
    print("=" * 70)
    print("SECTION 6: PROTOCOL WITH PROPERTIES AND ATTRIBUTES")
    print("=" * 70)

    # --- 6a: Protocol with properties ---
    print("\n--- 6a: Protocol with @property ---")

    @runtime_checkable
    class Named(Protocol):
        """Contract: must have a 'name' property (read-only)."""
        @property
        def name(self) -> str: ...

    class FileStorage:
        """Satisfies Named with a @property."""
        @property
        def name(self) -> str:
            return "local_file"

    class SimpleStorage:
        """Also satisfies Named with a plain attribute.

        IMPORTANT: A plain attribute satisfies a Protocol @property.
        Protocol says 'must have .name that returns str'.
        Whether it's a property or attribute doesn't matter.
        """
        def __init__(self) -> None:
            self.name: str = "simple"

    print(f"  FileStorage (property):    {isinstance(FileStorage(), Named)}")
    print(f"  SimpleStorage (attribute): {isinstance(SimpleStorage(), Named)}")
    print("  Both satisfy Named — Protocol checks shape, not implementation")

    # --- 6b: Protocol with class variables ---
    print("\n--- 6b: Protocol with class-level attributes ---")

    @runtime_checkable
    class Versioned(Protocol):
        """Contract: must have a version class attribute."""
        version: str

    class VersionedPlugin:
        version: str = "1.0.0"

    class UnversionedPlugin:
        pass

    print(f"  VersionedPlugin:   {isinstance(VersionedPlugin(), Versioned)}")
    print(f"  UnversionedPlugin: {isinstance(UnversionedPlugin(), Versioned)}")

    print()


# =============================================================================
# SECTION 7: PROTOCOL WITH DATACLASS AND PYDANTIC
# =============================================================================

def section_7_with_dataclass_and_pydantic() -> None:
    """Show how Protocol works with dataclasses and Pydantic models."""
    print("=" * 70)
    print("SECTION 7: PROTOCOL WITH DATACLASS AND PYDANTIC")
    print("=" * 70)

    # --- 7a: Dataclass satisfying a Protocol ---
    print("\n--- 7a: @dataclass satisfies Protocol automatically ---")

    @runtime_checkable
    class HasMetadata(Protocol):
        """Contract: must have name and version attributes."""
        name: str
        version: str

    @dataclass
    class PluginInfo:
        """Dataclass — fields automatically satisfy Protocol attributes."""
        name: str
        version: str
        author: str = "unknown"        # extra fields are fine

    plugin = PluginInfo(name="speller", version="1.0.0")
    print(f"  PluginInfo satisfies HasMetadata: {isinstance(plugin, HasMetadata)}")
    print(f"  plugin.name: {plugin.name}")
    print(f"  plugin.version: {plugin.version}")

    # --- 7b: Pydantic preview (conceptual — no import needed) ---
    print("\n--- 7b: Pydantic BaseModel also satisfies Protocol ---")
    print("  # This works in your DataVault project:")
    print("  # from pydantic import BaseModel")
    print("  #")
    print("  # class LLMResponse(BaseModel):    # Pydantic model")
    print("  #     content: str")
    print("  #     model: str")
    print("  #     tokens_used: int")
    print("  #")
    print("  # @runtime_checkable")
    print("  # class HasContent(Protocol):")
    print("  #     content: str")
    print("  #")
    print("  # isinstance(LLMResponse(...), HasContent)  → True!")
    print("  # Pydantic fields satisfy Protocol attributes")

    # --- 7c: The boundary rule in action ---
    print("\n--- 7c: The dataclass/Pydantic boundary with Protocol ---")
    print("  ┌──────────────────────────────────────────────┐")
    print("  │  Protocol defines the CONTRACT               │")
    print("  │  Dataclass implements for INTERNAL use        │")
    print("  │  Pydantic implements for EXTERNAL boundaries  │")
    print("  │  Both satisfy the same Protocol!              │")
    print("  │                                               │")
    print("  │  Protocol:  HasResult                         │")
    print("  │     ↙              ↘                          │")
    print("  │  @dataclass        BaseModel                  │")
    print("  │  InternalResult    APIResponse                │")
    print("  │  (fast, internal)  (validated, external)      │")
    print("  └──────────────────────────────────────────────┘")

    print()


# =============================================================================
# SECTION 8: DEPENDENCY INJECTION — Wiring Protocols to Concrete Classes
# =============================================================================
# ┌─────────────────────────────────────────────────────────────────┐
# │             DEPENDENCY INJECTION PATTERN                        │
# │─────────────────────────────────────────────────────────────────│
# │                                                                 │
# │  protocols.py  →  defines the contract (DictionaryProtocol)     │
# │  dictionary.py →  implements it (HashTableDictionary)           │
# │  speller.py    →  uses the contract (accepts DictionaryProtocol)│
# │  __main__.py   →  WIRES them together (picks the implementation)│
# │                                                                 │
# │  __main__.py is the COMPOSITION ROOT — the one place that       │
# │  knows about both the contract AND the implementation.          │
# │  Everything else depends only on the contract.                  │
# │                                                                 │
# │  ┌──────────┐          ┌──────────────┐                         │
# │  │protocols │◄─────────│ speller.py   │ depends on contract     │
# │  │  .py     │          │              │                         │
# │  └──────────┘          └──────────────┘                         │
# │       ▲                       ▲                                 │
# │       │                       │                                 │
# │  ┌──────────┐          ┌──────────────┐                         │
# │  │dictionary│          │ __main__.py  │ wires them together     │
# │  │  .py     │          │              │                         │
# │  └──────────┘          └──────────────┘                         │
# │   implements              composition root                      │
# └─────────────────────────────────────────────────────────────────┘

def section_8_dependency_injection() -> None:
    """Demonstrate dependency injection with Protocol."""
    print("=" * 70)
    print("SECTION 8: DEPENDENCY INJECTION")
    print("=" * 70)

    # --- 8a: The full pattern ---
    print("\n--- 8a: Full dependency injection pattern ---")

    # Step 1: Protocol (the contract)
    @runtime_checkable
    class Searchable(Protocol):
        def search(self, query: str) -> list[str]: ...

    # Step 2: Concrete implementations
    class InMemorySearch:
        """Fast in-memory search (for dev/testing)."""
        def __init__(self) -> None:
            self._data = ["python", "java", "rust", "go"]

        def search(self, query: str) -> list[str]:
            return [item for item in self._data if query.lower() in item]

    class MockSearch:
        """Test double — returns predictable results."""
        def search(self, query: str) -> list[str]:
            return [f"mock_result_for_{query}"]

    # Step 3: Business logic depends on Protocol
    class SearchApp:
        """Application that depends on the Searchable contract.

        Doesn't import InMemorySearch or MockSearch.
        Doesn't know or care what the implementation is.
        """
        def __init__(self, engine: Searchable) -> None:
            self._engine = engine

        def find(self, query: str) -> None:
            results = self._engine.search(query)
            for result in results:
                print(f"    Found: {result}")

    # Step 4: Composition root wires them together
    print("  Production mode:")
    app = SearchApp(InMemorySearch())          # production engine
    app.find("py")

    print("\n  Test mode:")
    test_app = SearchApp(MockSearch())         # test double
    test_app.find("py")

    # --- 8b: How this maps to your Speller ---
    print("\n--- 8b: Your Speller dependency injection ---")
    print("  # __main__.py (composition root):")
    print("  from speller.dictionary import HashTableDictionary")
    print("  from speller.speller import run_speller")
    print("")
    print("  dictionary = HashTableDictionary()    # pick implementation")
    print("  run_speller(dictionary, args.text)     # inject into speller")
    print("")
    print("  # speller.py (depends on Protocol only):")
    print("  from speller.protocols import DictionaryProtocol")
    print("")
    print("  def run_speller(dictionary: DictionaryProtocol, ...):")
    print("      dictionary.load(...)    # works with ANY implementation")

    # --- 8c: Swapping for tests ---
    print("\n--- 8c: Swapping implementation for tests ---")
    print("  # tests/test_speller.py")
    print("  class MockDictionary:")
    print("      def load(self, filepath: str) -> bool:")
    print("          return True")
    print("      def check(self, word: str) -> bool:")
    print("          return word in {'cat', 'dog'}")
    print("      def size(self) -> int:")
    print("          return 2")
    print("")
    print("  def test_speller():")
    print("      run_speller(MockDictionary(), 'test.txt')  # no file I/O!")
    print("      # Fast, deterministic, no external dependencies")

    print()


# =============================================================================
# SECTION 9: collections.abc — Built-in Protocols You Already Use
# =============================================================================

def section_9_builtin_protocols() -> None:
    """Show that Python's standard library is full of Protocol-like ABCs."""
    print("=" * 70)
    print("SECTION 9: collections.abc — Built-in Protocols")
    print("=" * 70)

    print("\n--- 9a: Built-in ABCs you use without knowing ---\n")

    # These are ABCs from collections.abc that work like Protocols
    # Any class with __iter__ + __next__ is an Iterator
    # Any class with __iter__ is an Iterable
    # Any class with __len__ is a Sized
    # Any class with __contains__ is a Container

    from collections.abc import Iterable, Sized, Container, Callable

    # Your set satisfies MULTIPLE built-in ABCs:
    my_set: set[str] = {"cat", "dog"}

    print("  set satisfies:")
    print(f"    Iterable:  {isinstance(my_set, Iterable)}")
    print(f"    Sized:     {isinstance(my_set, Sized)}")
    print(f"    Container: {isinstance(my_set, Container)}")

    # Your functions satisfy Callable:
    def greet(name: str) -> str:
        return f"Hello, {name}"

    print(f"\n  function satisfies:")
    print(f"    Callable:  {isinstance(greet, Callable)}")

    # --- 9b: How this relates to your Protocol classes ---
    print("\n--- 9b: Your Protocols extend this philosophy ---")
    print("  collections.abc says: 'has __iter__? → it's Iterable'")
    print("  Your Protocol says:   'has load/check/size? → it's a Dictionary'")
    print("  Same concept, applied to YOUR domain")

    # --- 9c: Common collections.abc cheat sheet ---
    print("\n--- 9c: collections.abc quick reference ---")
    print("  ┌───────────────┬───────────────────────────────────┐")
    print("  │ ABC           │ Required Methods                  │")
    print("  │───────────────│───────────────────────────────────│")
    print("  │ Iterable      │ __iter__()                        │")
    print("  │ Iterator      │ __iter__() + __next__()           │")
    print("  │ Generator     │ __iter__() + __next__() + send()  │")
    print("  │               │ + throw() + close()               │")
    print("  │ Sized         │ __len__()                         │")
    print("  │ Container     │ __contains__()                    │")
    print("  │ Callable      │ __call__()                        │")
    print("  │ Hashable      │ __hash__()                        │")
    print("  │ Mapping       │ __getitem__() + __iter__() +      │")
    print("  │               │ __len__() + keys() + items() ...  │")
    print("  │ Sequence      │ __getitem__() + __len__()         │")
    print("  └───────────────┴───────────────────────────────────┘")

    print()


# =============================================================================
# SECTION 10: COMMON PITFALLS AND GOTCHAS
# =============================================================================

def section_10_pitfalls() -> None:
    """Common mistakes with ABC and Protocol."""
    print("=" * 70)
    print("SECTION 10: COMMON PITFALLS AND GOTCHAS")
    print("=" * 70)

    # --- 10a: Forgetting @abstractmethod in ABC ---
    print("\n--- 10a: Forgetting @abstractmethod (ABC becomes useless) ---")

    class BadABC(ABC):
        """Without @abstractmethod, subclasses don't HAVE to implement."""
        def process(self) -> str:        # NOT abstract!
            return "default"

    class Empty(BadABC):
        pass                             # no error — process() not required

    print(f"  Empty() works: {Empty().process()}")
    print("  ↑ Probably not what you wanted — forgot @abstractmethod")

    # --- 10b: Protocol inheritance trap ---
    print("\n--- 10b: Don't inherit from Protocol to 'implement' it ---")
    print("  # WRONG — unnecessary and misleading:")
    print("  class HashTableDictionary(DictionaryProtocol):  # ✗")
    print("      ...")
    print("")
    print("  # CORRECT — just implement the methods:")
    print("  class HashTableDictionary:  # ✓")
    print("      def load(...): ...")
    print("      def check(...): ...")
    print("      def size(...): ...")
    print("")
    print("  Inheriting from a Protocol class makes YOUR class also a")
    print("  Protocol, which is almost never what you want. Protocol")
    print("  inheritance is for EXTENDING protocols, not implementing them.")

    # --- 10c: @runtime_checkable doesn't check signatures ---
    print("\n--- 10c: @runtime_checkable signature blindness ---")
    print("  isinstance() only checks method EXISTS, not its signature.")
    print("  Always pair @runtime_checkable with mypy --strict for full safety.")
    print("  isinstance() = runtime safety net")
    print("  mypy --strict = compile-time full verification")

    # --- 10d: ABC can't be used with classes you don't own ---
    print("\n--- 10d: ABC limitation with third-party code ---")
    print("  You can't do: class ChromaDB(YourVectorStoreABC)")
    print("  Because you don't control ChromaDB's source code.")
    print("  Protocol solves this — ChromaDB just needs matching methods.")

    # --- 10e: Over-abstracting ---
    print("\n--- 10e: Don't over-abstract ---")
    print("  If you only have ONE implementation and no plans for more,")
    print("  you probably don't need a Protocol or ABC yet.")
    print("  Start with the concrete class. Extract a Protocol later")
    print("  when you actually need to swap implementations.")
    print("")
    print("  For Speller: DictionaryProtocol IS justified because your")
    print("  task brief explicitly plans for future backends. But don't")
    print("  create SpellerProtocol, TextProcessorProtocol, etc. — one")
    print("  Protocol for the main swappable component is enough.")

    print()


# =============================================================================
# SECTION 11: DECISION GUIDE AND CHEAT SHEET
# =============================================================================
#
# ┌──────────────────────────────────────────────────────────────────┐
# │                    DECISION GUIDE                                │
# │──────────────────────────────────────────────────────────────────│
# │  Situation                         │ Use                        │
# │────────────────────────────────────│────────────────────────────│
# │  Need swappable backends           │ Protocol                   │
# │  Third-party classes involved       │ Protocol                  │
# │  Want loose coupling                │ Protocol                  │
# │  Only need method signatures        │ Protocol                  │
# │  Need shared concrete methods       │ ABC                       │
# │  Need instantiation prevention      │ ABC                       │
# │  Own ALL implementing classes       │ ABC (or Protocol — both)  │
# │  One implementation, no plans more  │ Neither (just use class)  │
# │  Plugin/extension system            │ Protocol                  │
# │  Type checking with mypy            │ Both work equally well    │
# └──────────────────────────────────────────────────────────────────┘
#
# ┌──────────────────────────────────────────────────────────────────┐
# │                    ABC CHEAT SHEET                               │
# │──────────────────────────────────────────────────────────────────│
# │  from abc import ABC, abstractmethod                            │
# │                                                                  │
# │  class MyBase(ABC):                                              │
# │      @abstractmethod                                             │
# │      def required_method(self) -> str: ...    # must implement   │
# │                                                                  │
# │      def shared_method(self) -> str:          # inherited free   │
# │          return "shared logic"                                   │
# │                                                                  │
# │      @property                                                   │
# │      @abstractmethod                                             │
# │      def required_prop(self) -> int: ...      # must implement   │
# │                                                                  │
# │  class Concrete(MyBase):                     # MUST inherit      │
# │      def required_method(self) -> str:                           │
# │          return "implemented"                                    │
# │                                                                  │
# │      @property                                                   │
# │      def required_prop(self) -> int:                             │
# │          return 42                                               │
# └──────────────────────────────────────────────────────────────────┘
#
# ┌──────────────────────────────────────────────────────────────────┐
# │                  PROTOCOL CHEAT SHEET                            │
# │──────────────────────────────────────────────────────────────────│
# │  from typing import Protocol, runtime_checkable                  │
# │                                                                  │
# │  @runtime_checkable                 # enables isinstance()       │
# │  class MyContract(Protocol):                                     │
# │      def required_method(self) -> str: ...   # just signature    │
# │                                                                  │
# │      @property                                                   │
# │      def required_prop(self) -> int: ...     # just signature    │
# │                                                                  │
# │      name: str                      # attribute requirement      │
# │                                                                  │
# │  class Concrete:                    # NO inheritance needed!     │
# │      name: str = "default"                                       │
# │                                                                  │
# │      def required_method(self) -> str:                           │
# │          return "implemented"                                    │
# │                                                                  │
# │      @property                                                   │
# │      def required_prop(self) -> int:                             │
# │          return 42                                               │
# └──────────────────────────────────────────────────────────────────┘
#
# ┌──────────────────────────────────────────────────────────────────┐
# │          YOUR v8.1 PROTOCOL MAP                                  │
# │──────────────────────────────────────────────────────────────────│
# │  Project       │ Protocol              │ Implementations         │
# │────────────────│───────────────────────│─────────────────────────│
# │  Speller       │ DictionaryProtocol    │ HashTableDictionary     │
# │  DataVault     │ LLMProvider           │ Gemini, OpenAI, Claude  │
# │  PolicyPulse   │ VectorStore           │ ChromaDB, Pinecone      │
# │                │ EmbeddingProvider     │ Gemini, OpenAI, HF      │
# │  FormSense     │ ExtractionBackend     │ GeminiVision, Custom    │
# │  StreamSmart   │ ContentAPI            │ Watchmode, TMDB         │
# │  AFC           │ DataSource            │ SEC, Wikipedia, News    │
# └──────────────────────────────────────────────────────────────────┘
#
# ┌──────────────────────────────────────────────────────────────────┐
# │                  IMPORT CHEAT SHEET                              │
# │──────────────────────────────────────────────────────────────────│
# │  from abc import ABC, abstractmethod        # ABC classes        │
# │  from typing import Protocol                # Protocol classes   │
# │  from typing import runtime_checkable       # isinstance support │
# │  from collections.abc import Iterator       # built-in protocol  │
# │  from collections.abc import Iterable       # built-in protocol  │
# │  from collections.abc import Sized          # built-in protocol  │
# │  from collections.abc import Container      # built-in protocol  │
# │  from collections.abc import Callable       # built-in protocol  │
# └──────────────────────────────────────────────────────────────────┘
#
# =============================================================================


# =============================================================================
# MAIN EXECUTION
# =============================================================================

if __name__ == "__main__":
    section_1_the_problem()
    section_2_abc()
    section_3_protocol()
    section_4_abc_vs_protocol()
    section_5_runtime_checkable()
    section_6_properties_and_attributes()
    section_7_with_dataclass_and_pydantic()
    section_8_dependency_injection()
    section_9_builtin_protocols()
    section_10_pitfalls()

    print("=" * 70)
    print("REFERENCE COMPLETE — See Section 11 (cheat sheets) in source code")
    print("=" * 70)
