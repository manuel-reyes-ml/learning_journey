"""
pytest_fixtures_reference.py
==============================

Personal reference: pytest Fixtures, conftest.py, and Testing Patterns —
how fixtures work, when to use each pattern, and the dependency injection
system that makes tests clean, isolated, and maintainable.

Topics covered
--------------
1.  What Is a Fixture — setup functions that pytest injects automatically
2.  How Injection Works — parameter name matching and the discovery chain
3.  conftest.py — auto-discovered shared fixtures (no imports needed)
4.  Fixture Scopes — function, class, module, session lifecycle
5.  Fixture Chaining — fixtures that depend on other fixtures
6.  Built-in Fixtures — tmp_path, capsys, monkeypatch, request
7.  Factory Fixtures — returning functions instead of values
8.  Parametrize — one test function, many data inputs
9.  Markers — categorizing and filtering tests
10. Mock Classes — test doubles for dependency injection
11. Assertions and pytest.raises — verifying behavior and exceptions
12. Common Pitfalls and Gotchas
13. Decision Guide and Cheat Sheet

Why this matters for your roadmap (v8.1 GenAI-First)
------------------------------------------------------
- Stage 1 (Speller):     conftest fixtures for dictionary, text files, mocks
                          MockDictionary via Protocol (dependency injection payoff)
                          parametrize for word/expected pairs
- Stage 1 (DataVault):   MockLLMProvider fixture (avoid API costs in tests)
                          tmp_path for test data files
                          capsys for verifying Streamlit output
- Stage 1 (PolicyPulse): MockVectorStore fixture (no ChromaDB server needed)
                          Factory fixtures for creating test embeddings
                          Integration markers for slow RAG pipeline tests
- Stage 1 (FormSense):   MockExtractor fixture (no Gemini Vision API calls)
                          Image file fixtures (sample form images)
                          parametrize for multiple form types
- Stage 2 (Data Eng):    PostgreSQL testcontainer fixtures (session scope)
                          S3 mock fixtures (moto library)
                          Airflow DAG test patterns
- Stage 3 (ML):          Model cache fixtures (session scope — load once)
                          Synthetic data fixtures (factory pattern)
                          pytest-benchmark for performance regression
- Stage 4 (LLM):         LangChain mock fixtures (chain, agent, tool)
                          Vector store fixtures with test embeddings
                          Async fixtures for streaming tests
- Stage 5 (Senior):      Full integration test suites with CI/CD
                          Fixture libraries shared across microservices

How to use this file
---------------------
Run it directly to see all output::

    $ python pytest_fixtures_reference.py

Or import individual sections to experiment in a REPL::

    >>> from pytest_fixtures_reference import section_1_what_is_a_fixture

Author: Manuel Reyes — CS50 Speller / Stage 1 Learning Reference
Version: 1.0.0 — March 2026

References
----------
.. [1] pytest Docs — Fixtures
   https://docs.pytest.org/en/stable/how-to/fixtures.html
.. [2] pytest Docs — conftest.py
   https://docs.pytest.org/en/stable/how-to/fixtures.html#conftest-py
.. [3] pytest Docs — Parametrize
   https://docs.pytest.org/en/stable/how-to/parametrize.html
.. [4] pytest Docs — Markers
   https://docs.pytest.org/en/stable/how-to/mark.html
.. [5] pytest Docs — tmp_path
   https://docs.pytest.org/en/stable/how-to/tmp_path.html
"""

from __future__ import annotations

import sys
import time
import tempfile
from dataclasses import dataclass
from pathlib import Path


# =============================================================================
# SECTION 1: WHAT IS A FIXTURE — Setup Functions pytest Injects Automatically
# =============================================================================
# ┌─────────────────────────────────────────────────────────────────┐
# │              FIXTURE = SETUP FUNCTION                           │
# │─────────────────────────────────────────────────────────────────│
# │                                                                 │
# │  WITHOUT fixtures:                                              │
# │    def test_check_cat():                                        │
# │        dictionary = HashTableDictionary()   ← repeated          │
# │        dictionary.load("dict/large")        ← repeated          │
# │        assert dictionary.check("cat")                           │
# │                                                                 │
# │    def test_check_dog():                                        │
# │        dictionary = HashTableDictionary()   ← SAME setup!       │
# │        dictionary.load("dict/large")        ← SAME setup!       │
# │        assert dictionary.check("dog")                           │
# │                                                                 │
# │  WITH fixtures:                                                 │
# │    @pytest.fixture                                              │
# │    def loaded_dictionary():                                     │
# │        dictionary = HashTableDictionary()   ← setup ONCE        │
# │        dictionary.load("dict/large")                            │
# │        return dictionary                                        │
# │                                                                 │
# │    def test_check_cat(loaded_dictionary):   ← injected!         │
# │        assert loaded_dictionary.check("cat")                    │
# │                                                                 │
# │    def test_check_dog(loaded_dictionary):   ← injected!         │
# │        assert loaded_dictionary.check("dog")                    │
# │                                                                 │
# │  KEY INSIGHT: You never CALL fixtures yourself.                 │
# │  pytest sees the parameter NAME and injects the VALUE.          │
# └─────────────────────────────────────────────────────────────────┘

def section_1_what_is_a_fixture() -> None:
    """Demonstrate what a fixture is and why it exists."""
    print("=" * 70)
    print("SECTION 1: WHAT IS A FIXTURE")
    print("=" * 70)

    # --- 1a: Without fixtures — repeated setup ---
    print("\n--- 1a: Without fixtures (repeated setup) ---")
    print("  Every test creates its own data from scratch:")
    print()
    print("  def test_check_cat():")
    print("      dictionary = HashTableDictionary()   # repeated")
    print("      dictionary.load('dict/large')        # repeated")
    print("      assert dictionary.check('cat')")
    print()
    print("  def test_check_dog():")
    print("      dictionary = HashTableDictionary()   # SAME setup!")
    print("      dictionary.load('dict/large')        # SAME setup!")
    print("      assert dictionary.check('dog')")
    print()
    print("  Problem: 10 tests = 10 copies of the same setup code.")

    # --- 1b: With fixtures — setup once, inject everywhere ---
    print("\n--- 1b: With fixtures (DRY setup) ---")
    print("  The fixture does the setup ONCE. pytest injects it:")
    print()
    print("  @pytest.fixture")
    print("  def loaded_dictionary():")
    print("      dictionary = HashTableDictionary()")
    print("      dictionary.load('dict/large')")
    print("      return dictionary")
    print()
    print("  def test_check_cat(loaded_dictionary):   # injected!")
    print("      assert loaded_dictionary.check('cat')")
    print()
    print("  def test_check_dog(loaded_dictionary):   # injected!")
    print("      assert loaded_dictionary.check('dog')")

    # --- 1c: What fixtures RETURN ---
    print("\n--- 1c: What fixtures can return ---")
    print("  Fixtures can return ANY Python object:")
    print()
    print("  • A value:      return 42")
    print("  • A string:     return 'hello'")
    print("  • An object:    return HashTableDictionary()")
    print("  • A Path:       return tmp_path / 'test.txt'")
    print("  • A list:       return ['cat', 'dog', 'fish']")
    print("  • A function:   return lambda x: x * 2   (factory pattern)")
    print("  • A dict:       return {'key': 'value'}")
    print("  • None:         (for setup-only fixtures with side effects)")

    # --- 1d: Simulating a fixture ---
    print("\n--- 1d: Simulating how fixtures work ---")

    # This is what a fixture looks like (without @pytest.fixture):
    def sample_data():
        """A function that prepares test data."""
        return {"name": "Manuel", "role": "engineer"}

    # This is what pytest does behind the scenes:
    data = sample_data()      # 1. Call the fixture function
    # 2. Pass the result to the test as an argument
    print(f"  Fixture returned: {data}")
    print(f"  Test would receive: data['name'] = '{data['name']}'")
    print()
    print("  In real pytest, you NEVER call sample_data() yourself.")
    print("  pytest does it for you based on the parameter name.")

    print()


# =============================================================================
# SECTION 2: HOW INJECTION WORKS — Parameter Name Matching
# =============================================================================
# ┌─────────────────────────────────────────────────────────────────┐
# │        FIXTURE INJECTION — NAME-BASED MATCHING                  │
# │─────────────────────────────────────────────────────────────────│
# │                                                                 │
# │  @pytest.fixture                                                │
# │  def loaded_dictionary():    ← fixture NAME = "loaded_dictionary"│
# │      ...                                                        │
# │      return dictionary                                          │
# │                                                                 │
# │  def test_check(loaded_dictionary):                             │
# │                  ↑                                              │
# │                  pytest sees this PARAMETER NAME                │
# │                  searches for a fixture with the SAME name      │
# │                  calls the fixture function                     │
# │                  passes the return value as the argument         │
# │                                                                 │
# │  SEARCH ORDER:                                                  │
# │    1. Same test file (local fixtures)                           │
# │    2. conftest.py in same directory                             │
# │    3. conftest.py in parent directories                         │
# │    4. Installed plugins (pytest-cov, etc.)                      │
# │    5. Built-in fixtures (tmp_path, capsys, monkeypatch)         │
# └─────────────────────────────────────────────────────────────────┘

def section_2_how_injection_works() -> None:
    """Demonstrate how pytest matches parameter names to fixtures."""
    print("=" * 70)
    print("SECTION 2: HOW INJECTION WORKS")
    print("=" * 70)

    # --- 2a: The matching mechanism ---
    print("\n--- 2a: Name-based matching ---")
    print("  The fixture NAME must match the parameter NAME exactly:")
    print()
    print("  @pytest.fixture")
    print("  def loaded_dictionary():    # name = 'loaded_dictionary'")
    print("      ...")
    print()
    print("  def test_a(loaded_dictionary):   # ✓ MATCH → injected")
    print("  def test_b(loaded_dict):         # ✗ NO MATCH → error!")
    print("  def test_c(dictionary):          # ✗ NO MATCH → error!")
    print()
    print("  The name must be EXACT. No partial matching, no aliases.")

    # --- 2b: Multiple fixtures in one test ---
    print("\n--- 2b: Multiple fixtures in one test ---")
    print("  A test can request ANY number of fixtures:")
    print()
    print("  def test_speller(mock_dictionary, sample_text_file, capsys):")
    print("                    ↑                ↑                ↑")
    print("              from conftest    from conftest     built-in")
    print()
    print("  pytest resolves ALL of them independently,")
    print("  then passes all values as arguments.")

    # --- 2c: Where pytest searches ---
    print("\n--- 2c: Fixture search order ---")
    print("  When pytest sees 'loaded_dictionary' as a parameter:")
    print()
    print("  1. Same .py file     → @pytest.fixture in this test file?")
    print("  2. conftest.py       → @pytest.fixture in conftest.py?")
    print("  3. Parent conftest   → @pytest.fixture in parent dir?")
    print("  4. Plugins           → installed plugin fixtures?")
    print("  5. Built-in          → tmp_path, capsys, monkeypatch?")
    print()
    print("  First match wins. Local fixtures shadow global ones.")

    # --- 2d: What happens when no fixture is found ---
    print("\n--- 2d: When no fixture matches ---")
    print("  def test_check(nonexistent_fixture):")
    print("  → ERRORS: fixture 'nonexistent_fixture' not found")
    print()
    print("  This is a COMPILE-TIME error (before the test runs).")
    print("  pytest tells you exactly which fixture is missing.")

    print()


# =============================================================================
# SECTION 3: conftest.py — Auto-Discovered Shared Fixtures
# =============================================================================
# ┌─────────────────────────────────────────────────────────────────┐
# │              conftest.py — THE FIXTURE HUB                      │
# │─────────────────────────────────────────────────────────────────│
# │                                                                 │
# │  conftest.py is a SPECIAL filename in pytest:                   │
# │  • Auto-discovered — no import needed in test files             │
# │  • Shared — all test files in same dir can use its fixtures     │
# │  • Hierarchical — can exist at multiple directory levels        │
# │                                                                 │
# │  tests/                                                         │
# │  ├── conftest.py         ← fixtures available to ALL below     │
# │  ├── test_dictionary.py  ← uses fixtures from conftest.py     │
# │  ├── test_speller.py     ← uses fixtures from conftest.py     │
# │  └── test_config.py      ← uses fixtures from conftest.py     │
# │                                                                 │
# │  RULE: "How many test files use this fixture?"                  │
# │    ONE file only    → define it IN that test file               │
# │    MULTIPLE files   → define it in conftest.py                  │
# └─────────────────────────────────────────────────────────────────┘

def section_3_conftest() -> None:
    """Explain conftest.py purpose and placement rules."""
    print("=" * 70)
    print("SECTION 3: conftest.py — AUTO-DISCOVERED SHARED FIXTURES")
    print("=" * 70)

    # --- 3a: What makes conftest.py special ---
    print("\n--- 3a: What makes conftest.py special ---")
    print("  1. NAME MATTERS — must be exactly 'conftest.py'")
    print("     (not 'conf_test.py', not 'test_conf.py')")
    print()
    print("  2. AUTO-DISCOVERED — pytest finds it by name")
    print("     You NEVER write: from conftest import my_fixture")
    print("     pytest registers all @pytest.fixture functions")
    print("     automatically before running any tests")
    print()
    print("  3. SCOPED TO DIRECTORY — fixtures are available to")
    print("     all test files in the SAME directory and below")

    # --- 3b: Where to put fixtures ---
    print("\n--- 3b: Where to put fixtures (decision rule) ---")
    print()
    print("  ┌──────────────────────────────────────────────────┐")
    print("  │ Question                    │ Put fixture in...  │")
    print("  │─────────────────────────────│────────────────────│")
    print("  │ Used by 1 test file?        │ That test file     │")
    print("  │ Used by 2+ test files?      │ conftest.py        │")
    print("  │ Used by 1 test class only?  │ Inside that class  │")
    print("  │ Expensive setup?            │ conftest.py +      │")
    print("  │                             │ wider scope        │")
    print("  └──────────────────────────────────────────────────┘")

    # --- 3c: conftest.py example ---
    print("\n--- 3c: Example conftest.py ---")
    print()
    print("  # conftest.py (no test_ prefix — it's NOT a test file)")
    print("  import pytest")
    print("  from speller.dictionaries import HashTableDictionary")
    print()
    print("  @pytest.fixture")
    print("  def empty_dictionary():")
    print("      return HashTableDictionary()")
    print()
    print("  @pytest.fixture")
    print("  def loaded_dictionary(sample_dict_file):")
    print("      d = HashTableDictionary()")
    print("      d.load(str(sample_dict_file))")
    print("      return d")
    print()
    print("  # test_dictionary.py (NO import of fixtures)")
    print("  def test_check(loaded_dictionary):     # ← just use the name")
    print("      assert loaded_dictionary.check('cat')")

    # --- 3d: Hierarchical conftest ---
    print("\n--- 3d: Hierarchical conftest.py files ---")
    print("  You can have conftest.py at multiple levels:")
    print()
    print("  project/")
    print("  ├── conftest.py              ← project-wide fixtures")
    print("  └── tests/")
    print("      ├── conftest.py          ← test-specific fixtures")
    print("      ├── test_unit/")
    print("      │   ├── conftest.py      ← unit test fixtures")
    print("      │   └── test_dict.py     ← uses ALL conftest.py above")
    print("      └── test_integration/")
    print("          ├── conftest.py      ← integration test fixtures")
    print("          └── test_full.py     ← uses project + tests conftest")
    print()
    print("  Deeper conftest.py files can OVERRIDE parent fixtures")
    print("  with the same name. For Speller, one conftest.py is enough.")

    print()


# =============================================================================
# SECTION 4: FIXTURE SCOPES — How Often Fixtures Run
# =============================================================================
# ┌─────────────────────────────────────────────────────────────────┐
# │              FIXTURE SCOPES                                     │
# │─────────────────────────────────────────────────────────────────│
# │                                                                 │
# │  SCOPE        │ CREATED          │ DESTROYED                    │
# │───────────────│──────────────────│──────────────────────────────│
# │  "function"   │ Before EACH test │ After EACH test              │
# │  (DEFAULT)    │                  │ (fresh instance every time)  │
# │               │                  │                              │
# │  "class"      │ Before first     │ After last test in class     │
# │               │ test in class    │                              │
# │               │                  │                              │
# │  "module"     │ Before first     │ After last test in .py file  │
# │               │ test in file     │ (shared within one file)     │
# │               │                  │                              │
# │  "session"    │ Before first     │ After last test in run       │
# │               │ test ANYWHERE    │ (shared across ALL files)    │
# │───────────────│──────────────────│──────────────────────────────│
# │                                                                 │
# │  DEFAULT IS "function" — USE IT UNLESS YOU HAVE A REASON NOT TO│
# │                                                                 │
# │  Why? Each test gets a FRESH fixture. If test A mutates the     │
# │  data, test B is NOT affected. This is TEST ISOLATION.          │
# │                                                                 │
# │  Wider scopes share data — if one test mutates the fixture,     │
# │  all subsequent tests see the mutation. Use wider scopes ONLY   │
# │  for expensive, READ-ONLY setup (DB connections, model loading).│
# └─────────────────────────────────────────────────────────────────┘

def section_4_fixture_scopes() -> None:
    """Demonstrate fixture scope options and their lifecycles."""
    print("=" * 70)
    print("SECTION 4: FIXTURE SCOPES")
    print("=" * 70)

    # --- 4a: Default scope (function) ---
    print("\n--- 4a: Default scope = 'function' ---")
    print("  @pytest.fixture                   # scope='function' (implicit)")
    print("  def dictionary():")
    print("      return HashTableDictionary()  # NEW instance per test")
    print()
    print("  def test_a(dictionary):  # gets instance #1")
    print("  def test_b(dictionary):  # gets instance #2 (fresh!)")
    print("  def test_c(dictionary):  # gets instance #3 (fresh!)")
    print()
    print("  3 tests = 3 separate dictionary objects")
    print("  If test_a mutates its dictionary, test_b is NOT affected")

    # --- 4b: Session scope ---
    print("\n--- 4b: Session scope (shared across ALL tests) ---")
    print("  @pytest.fixture(scope='session')")
    print("  def large_dictionary():")
    print("      d = HashTableDictionary()")
    print("      d.load('dictionaries/large')  # loads 143K words ONCE")
    print("      return d")
    print()
    print("  def test_a(large_dictionary):  # same instance")
    print("  def test_b(large_dictionary):  # same instance")
    print("  def test_c(large_dictionary):  # same instance")
    print()
    print("  3 tests = 1 dictionary load (fast!)")
    print("  BUT: if test_a calls unload(), test_b breaks!")

    # --- 4c: When to use each scope ---
    print("\n--- 4c: Scope decision guide ---")
    print()
    print("  'function' (default):")
    print("    → Unit tests, mutable objects, fast setup")
    print("    → Your Speller: empty_dictionary, loaded_dictionary")
    print()
    print("  'class':")
    print("    → Share fixture within one test class")
    print("    → Rarely used — 'function' is usually better")
    print()
    print("  'module':")
    print("    → Share fixture within one .py file")
    print("    → Good for read-only data loaded from disk")
    print()
    print("  'session':")
    print("    → Share fixture across ALL test files")
    print("    → Stage 2: PostgreSQL connection (expensive to create)")
    print("    → Stage 3: Pre-trained ML model (slow to load)")
    print("    → Stage 4: LLM client initialization")

    # --- 4d: Scope restriction rule ---
    print("\n--- 4d: Scope restriction rule ---")
    print("  A fixture can ONLY depend on fixtures with EQUAL or WIDER scope:")
    print()
    print("  @pytest.fixture(scope='session')")
    print("  def db_connection(): ...")
    print()
    print("  @pytest.fixture(scope='function')   # ← narrower")
    print("  def user(db_connection):             # ← depends on wider → OK!")
    print("      ...")
    print()
    print("  @pytest.fixture(scope='session')")
    print("  def config(tmp_path):                # ← ERROR!")
    print("      # tmp_path is function-scoped (narrower)")
    print("      # session-scoped fixture can't use function-scoped fixture")

    print()


# =============================================================================
# SECTION 5: FIXTURE CHAINING — Fixtures That Depend on Other Fixtures
# =============================================================================
# ┌─────────────────────────────────────────────────────────────────┐
# │              FIXTURE CHAINING                                   │
# │─────────────────────────────────────────────────────────────────│
# │                                                                 │
# │  Fixtures can depend on OTHER fixtures. pytest resolves the     │
# │  entire chain automatically:                                    │
# │                                                                 │
# │  test_check(loaded_dictionary)                                  │
# │       ↓ needs                                                   │
# │  loaded_dictionary(sample_dict_file)                            │
# │       ↓ needs                                                   │
# │  sample_dict_file(tmp_path)                                     │
# │       ↓ needs                                                   │
# │  tmp_path  ← built-in (root of chain)                           │
# │                                                                 │
# │  RESOLUTION ORDER:                                              │
# │  Step 1: Resolve dependencies BOTTOM-UP (find the chain)       │
# │  Step 2: Execute fixtures TOP-DOWN (create values)              │
# │  Step 3: Pass final value to the test                           │
# │                                                                 │
# │  You never manage this chain — pytest does it ALL.              │
# └─────────────────────────────────────────────────────────────────┘

def section_5_fixture_chaining() -> None:
    """Demonstrate how fixtures depend on and chain through other fixtures."""
    print("=" * 70)
    print("SECTION 5: FIXTURE CHAINING")
    print("=" * 70)

    # --- 5a: Chain example ---
    print("\n--- 5a: Chain from your Speller project ---")
    print()
    print("  # FIXTURE 1: Built-in (tmp_path)")
    print("  # pytest creates: /tmp/pytest-abc/test_check0/")
    print()
    print("  # FIXTURE 2: Uses tmp_path")
    print("  @pytest.fixture")
    print("  def sample_dict_file(tmp_path):        # ← needs tmp_path")
    print("      path = tmp_path / 'dict.txt'")
    print("      path.write_text('cat\\ndog\\n')")
    print("      return path")
    print()
    print("  # FIXTURE 3: Uses sample_dict_file")
    print("  @pytest.fixture")
    print("  def loaded_dictionary(sample_dict_file):  # ← needs fixture 2")
    print("      d = HashTableDictionary()")
    print("      d.load(str(sample_dict_file))")
    print("      return d")
    print()
    print("  # TEST: Uses fixture 3 (which triggers 2 → 1)")
    print("  def test_check(loaded_dictionary):        # ← needs fixture 3")
    print("      assert loaded_dictionary.check('cat')")

    # --- 5b: Execution trace ---
    print("\n--- 5b: Execution trace ---")
    print("  When pytest runs test_check(loaded_dictionary):")
    print()
    print("  ① tmp_path()          → creates /tmp/pytest-xyz/")
    print("  ② sample_dict_file()  → writes 'cat\\ndog\\n' to tmp dir")
    print("  ③ loaded_dictionary() → loads dict file into set")
    print("  ④ test_check()        → assert loaded.check('cat')")
    print("  ⑤ cleanup             → tmp dir deleted automatically")

    # --- 5c: Simulating the chain ---
    print("\n--- 5c: Simulating a fixture chain in plain Python ---")

    # Simulate tmp_path
    tmp_dir = Path(tempfile.mkdtemp())

    # Fixture 2: depends on tmp_path
    def sample_dict_file(tmp_path: Path) -> Path:
        path = tmp_path / "dict.txt"
        path.write_text("cat\ndog\nfish\n", encoding="utf-8")
        return path

    # Fixture 3: depends on fixture 2
    def loaded_words(dict_file: Path) -> set[str]:
        return set(dict_file.read_text().strip().split("\n"))

    # pytest would chain these automatically:
    dict_file = sample_dict_file(tmp_dir)        # step 1
    words = loaded_words(dict_file)              # step 2
    print(f"  tmp_path:    {tmp_dir}")
    print(f"  dict_file:   {dict_file}")
    print(f"  words:       {words}")
    print(f"  'cat' in words: {'cat' in words}")

    # Cleanup
    dict_file.unlink()
    tmp_dir.rmdir()

    print()


# =============================================================================
# SECTION 6: BUILT-IN FIXTURES — Free from pytest
# =============================================================================
# ┌─────────────────────────────────────────────────────────────────┐
# │              BUILT-IN FIXTURES (no setup needed)                │
# │─────────────────────────────────────────────────────────────────│
# │                                                                 │
# │  tmp_path       → temporary directory, auto-cleaned             │
# │  tmp_path_factory → factory version of tmp_path                │
# │  capsys         → capture stdout/stderr                         │
# │  capfd          → capture file descriptors (lower level)        │
# │  monkeypatch    → temporarily modify objects, env vars          │
# │  request        → info about the requesting test                │
# │  pytestconfig   → access to pytest configuration                │
# │                                                                 │
# │  Just use the NAME as a parameter — pytest provides the value  │
# └─────────────────────────────────────────────────────────────────┘

def section_6_builtin_fixtures() -> None:
    """Explain the most important built-in pytest fixtures."""
    print("=" * 70)
    print("SECTION 6: BUILT-IN FIXTURES")
    print("=" * 70)

    # --- 6a: tmp_path ---
    print("\n--- 6a: tmp_path — temporary directory ---")
    print("  def test_file_creation(tmp_path):    # ← built-in, no setup")
    print("      my_file = tmp_path / 'test.txt'")
    print("      my_file.write_text('hello', encoding='utf-8')")
    print("      assert my_file.read_text() == 'hello'")
    print("      # tmp_path is DELETED after the test session")
    print()
    print("  WHY USE IT:")
    print("    - No manual cleanup needed")
    print("    - Each test gets a unique directory (isolation)")
    print("    - Tests can't corrupt real project files")
    print("    - Fast (no disk seek for distant paths)")

    # --- 6b: capsys ---
    print("\n--- 6b: capsys — capture stdout/stderr ---")
    print("  def test_output(capsys):             # ← built-in")
    print("      print('hello world')")
    print("      captured = capsys.readouterr()   # returns named tuple")
    print("      assert captured.out == 'hello world\\n'   # .out = stdout")
    print("      assert captured.err == ''                 # .err = stderr")
    print()
    print("  YOUR SPELLER USAGE:")
    print("    def test_main_output(capsys):")
    print("        main(['--no-log-file', 'texts/cat.txt'])")
    print("        captured = capsys.readouterr()")
    print("        assert 'WORDS MISSPELLED:' in captured.out")

    # --- 6c: monkeypatch ---
    print("\n--- 6c: monkeypatch — temporarily modify objects ---")
    print("  def test_env_var(monkeypatch):        # ← built-in")
    print("      monkeypatch.setenv('API_KEY', 'test-key-123')")
    print("      import os")
    print("      assert os.environ['API_KEY'] == 'test-key-123'")
    print("      # After test: API_KEY is RESTORED automatically")
    print()
    print("  METHODS:")
    print("    monkeypatch.setattr(obj, 'attr', value)  # replace attribute")
    print("    monkeypatch.setenv('VAR', 'value')       # set env variable")
    print("    monkeypatch.delenv('VAR')                 # delete env variable")
    print("    monkeypatch.chdir(path)                   # change cwd")
    print()
    print("  FUTURE USE:")
    print("    DataVault:   monkeypatch API keys for testing")
    print("    PolicyPulse: monkeypatch ChromaDB connection string")
    print("    AFC:         monkeypatch SEC API rate limits")

    # --- 6d: request ---
    print("\n--- 6d: request — test metadata ---")
    print("  @pytest.fixture")
    print("  def debug_fixture(request):           # ← built-in")
    print("      print(f'Running: {request.node.name}')")
    print("      print(f'Module:  {request.module.__name__}')")
    print("      yield")
    print("      print(f'Finished: {request.node.name}')")
    print()
    print("  Mostly used in advanced fixtures that need to know")
    print("  WHICH test is requesting them (for conditional setup).")

    print()


# =============================================================================
# SECTION 7: FACTORY FIXTURES — Returning Functions Instead of Values
# =============================================================================
# ┌─────────────────────────────────────────────────────────────────┐
# │              FACTORY FIXTURES                                   │
# │─────────────────────────────────────────────────────────────────│
# │                                                                 │
# │  REGULAR FIXTURE:   returns a VALUE                             │
# │    @pytest.fixture                                              │
# │    def data():                                                  │
# │        return {"key": "value"}   ← test gets the dict           │
# │                                                                 │
# │  FACTORY FIXTURE:   returns a FUNCTION                          │
# │    @pytest.fixture                                              │
# │    def make_data():                                             │
# │        def _create(key, value):                                 │
# │            return {key: value}                                  │
# │        return _create            ← test gets the FUNCTION       │
# │                                                                 │
# │  The test then CALLS the function:                              │
# │    def test_something(make_data):                               │
# │        data = make_data("name", "Manuel")  ← creates on demand │
# │                                                                 │
# │  WHY: When tests need DIFFERENT variations of the same          │
# │  type of data. Instead of 10 separate fixtures, one factory.    │
# └─────────────────────────────────────────────────────────────────┘

def section_7_factory_fixtures() -> None:
    """Demonstrate factory fixtures that return functions."""
    print("=" * 70)
    print("SECTION 7: FACTORY FIXTURES")
    print("=" * 70)

    # --- 7a: The problem ---
    print("\n--- 7a: Why factory fixtures exist ---")
    print("  Without factories, you'd need separate fixtures for each variation:")
    print()
    print("  @pytest.fixture")
    print("  def hello_text_file(tmp_path):              # fixture 1")
    print("      path = tmp_path / 'hello.txt'")
    print("      path.write_text('hello world')")
    print("      return path")
    print()
    print("  @pytest.fixture")
    print("  def digit_text_file(tmp_path):              # fixture 2")
    print("      path = tmp_path / 'digit.txt'")
    print("      path.write_text('abc123 next')")
    print("      return path")
    print()
    print("  @pytest.fixture")
    print("  def apostrophe_text_file(tmp_path):         # fixture 3")
    print("      path = tmp_path / 'apos.txt'")
    print("      path.write_text(\"it's don't\")")
    print("      return path")
    print()
    print("  That's 3 fixtures doing the same thing with different content!")

    # --- 7b: The factory solution ---
    print("\n--- 7b: One factory fixture replaces all three ---")
    print()
    print("  @pytest.fixture")
    print("  def make_text_file(tmp_path):     # ← regular fixture parameter")
    print("      def _create(content, filename='test.txt'):   # ← inner function")
    print("          path = tmp_path / filename")
    print("          path.write_text(content, encoding='utf-8')")
    print("          return path")
    print("      return _create                # ← return the FUNCTION, not a file")
    print()
    print("  # Tests call the factory with different content:")
    print("  def test_hello(make_text_file):")
    print("      path = make_text_file('hello world')        # call factory")
    print("      words = list(extract_words(path))")
    print()
    print("  def test_digits(make_text_file):")
    print("      path = make_text_file('abc123 next')        # different content!")
    print("      words = list(extract_words(path))")
    print()
    print("  def test_apostrophe(make_text_file):")
    print("      path = make_text_file(\"it's don't\")         # another variation!")
    print("      words = list(extract_words(path))")

    # --- 7c: Simulating a factory fixture ---
    print("\n--- 7c: Simulating a factory fixture ---")

    tmp_dir = Path(tempfile.mkdtemp())

    # The factory fixture:
    def make_text_file(content: str, filename: str = "test.txt") -> Path:
        path = tmp_dir / filename
        path.write_text(content, encoding="utf-8")
        return path

    # Tests call it with different content:
    file1 = make_text_file("hello world")
    file2 = make_text_file("abc123 next", "digits.txt")
    file3 = make_text_file("it's don't", "apostrophe.txt")

    print(f"  file1: {file1.read_text()!r}")
    print(f"  file2: {file2.read_text()!r}")
    print(f"  file3: {file3.read_text()!r}")
    print()
    print("  One factory → infinite variations. DRY principle.")

    # Cleanup
    for f in tmp_dir.iterdir():
        f.unlink()
    tmp_dir.rmdir()

    # --- 7d: Where you'll use factory fixtures ---
    print("\n--- 7d: Future factory fixture usage ---")
    print("  DataVault:   make_query(question, context)")
    print("  PolicyPulse: make_embedding(text, model_name)")
    print("  FormSense:   make_form_image(form_type, fields)")
    print("  AFC:         make_market_data(ticker, date_range)")
    print("  Stage 2:     make_csv_file(rows, columns)")
    print("  Stage 3:     make_training_batch(features, labels)")

    print()


# =============================================================================
# SECTION 8: PARAMETRIZE — One Test Function, Many Data Inputs
# =============================================================================
# ┌─────────────────────────────────────────────────────────────────┐
# │              @pytest.mark.parametrize                           │
# │─────────────────────────────────────────────────────────────────│
# │                                                                 │
# │  Instead of writing 5 separate test functions:                  │
# │    def test_check_the():   assert dictionary.check("the")       │
# │    def test_check_cat():   assert dictionary.check("cat")       │
# │    def test_check_xyz():   assert not dictionary.check("xyz")   │
# │    def test_check_THE():   assert dictionary.check("THE")       │
# │    def test_check_empty(): assert not dictionary.check("")       │
# │                                                                 │
# │  Write ONE function with @pytest.mark.parametrize:              │
# │    @pytest.mark.parametrize("word, expected", [                 │
# │        ("the", True),                                           │
# │        ("cat", True),                                           │
# │        ("xyz", False),                                          │
# │        ("THE", True),                                           │
# │        ("", False),                                             │
# │    ])                                                           │
# │    def test_check(loaded_dictionary, word, expected):           │
# │        assert loaded_dictionary.check(word) is expected         │
# │                                                                 │
# │  pytest runs the test 5 times with different arguments.         │
# │  Output shows each case separately:                             │
# │    test_check[the-True]    PASSED                               │
# │    test_check[cat-True]    PASSED                               │
# │    test_check[xyz-False]   PASSED                               │
# └─────────────────────────────────────────────────────────────────┘

def section_8_parametrize() -> None:
    """Demonstrate @pytest.mark.parametrize for data-driven tests."""
    print("=" * 70)
    print("SECTION 8: @pytest.mark.parametrize")
    print("=" * 70)

    # --- 8a: Basic parametrize ---
    print("\n--- 8a: Basic syntax ---")
    print("  @pytest.mark.parametrize('word, expected', [")
    print("      ('the', True),       # test case 1")
    print("      ('cat', True),       # test case 2")
    print("      ('xyz', False),      # test case 3")
    print("  ])")
    print("  def test_check(loaded_dictionary, word, expected):")
    print("      assert loaded_dictionary.check(word) is expected")
    print()
    print("  How it works:")
    print("  1. pytest reads the list of tuples")
    print("  2. For each tuple, runs the test with those values")
    print("  3. Each run is a SEPARATE test (own pass/fail status)")

    # --- 8b: With IDs ---
    print("\n--- 8b: Custom IDs for readable output ---")
    print("  @pytest.mark.parametrize(")
    print("      'text, expected',")
    print("      [")
    print("          ('hello, world', ['hello', 'world']),")
    print("          ('hello. world', ['hello', 'world']),")
    print("      ],")
    print("      ids=['comma', 'period'],    # ← custom labels")
    print("  )")
    print("  def test_punctuation(make_text_file, text, expected): ...")
    print()
    print("  Output:")
    print("    test_punctuation[comma]   PASSED")
    print("    test_punctuation[period]  PASSED")
    print()
    print("  Without ids: test_punctuation[hello, world-...]  (ugly)")

    # --- 8c: Parametrize with fixtures ---
    print("\n--- 8c: Parametrize + fixtures work together ---")
    print("  Parametrized values are passed AS ARGUMENTS alongside fixtures:")
    print()
    print("  @pytest.mark.parametrize('n', [1, 10, 100])")
    print("  def test_load(empty_dictionary, sample_dict_file, n):")
    print("       ↑              ↑                  ↑           ↑")
    print("     param          fixture            fixture     param")
    print("    from parametrize  from conftest   from conftest  from parametrize")
    print()
    print("  pytest resolves fixtures AND parametrize values, then passes all.")

    # --- 8d: When to use parametrize vs separate tests ---
    print("\n--- 8d: When to use parametrize ---")
    print()
    print("  USE parametrize when:")
    print("    - Same assertion logic, different input data")
    print("    - Testing boundary conditions (0, 1, MAX, MAX+1)")
    print("    - Testing multiple valid/invalid inputs")
    print("    - Your Speller: word/expected check pairs")
    print()
    print("  DON'T use parametrize when:")
    print("    - Different assertion logic per case")
    print("    - Tests need different setup")
    print("    - Test cases are complex (use separate test functions)")

    print()


# =============================================================================
# SECTION 9: MARKERS — Categorizing and Filtering Tests
# =============================================================================

def section_9_markers() -> None:
    """Demonstrate pytest markers for test categorization."""
    print("=" * 70)
    print("SECTION 9: MARKERS — CATEGORIZING TESTS")
    print("=" * 70)

    # --- 9a: What markers do ---
    print("\n--- 9a: What markers do ---")
    print("  Markers are LABELS you attach to tests for filtering:")
    print()
    print("  @pytest.mark.integration")
    print("  def test_large_dict():")
    print("      # slow test using real 143K-word dictionary")
    print("      ...")
    print()
    print("  @pytest.mark.slow")
    print("  def test_aca_txt():")
    print("      # processes 376K words")
    print("      ...")

    # --- 9b: Filtering with markers ---
    print("\n--- 9b: Filtering tests by marker ---")
    print("  # Run ONLY integration tests:")
    print("  pytest -m integration")
    print()
    print("  # Run everything EXCEPT integration:")
    print("  pytest -m 'not integration'")
    print()
    print("  # Run slow AND integration:")
    print("  pytest -m 'slow and integration'")
    print()
    print("  # Run slow OR integration:")
    print("  pytest -m 'slow or integration'")

    # --- 9c: Registering markers ---
    print("\n--- 9c: Register markers in pyproject.toml ---")
    print("  # pyproject.toml")
    print("  [tool.pytest.ini_options]")
    print("  markers = [")
    print('      "slow: marks tests as slow",')
    print('      "integration: marks integration tests",')
    print("  ]")
    print()
    print("  WHY REGISTER? Without registration, pytest shows a warning:")
    print("  'PytestUnknownMarkWarning: Unknown pytest.mark.integration'")
    print("  --strict-markers turns this into an ERROR (catches typos).")

    # --- 9d: Built-in markers ---
    print("\n--- 9d: Built-in markers ---")
    print("  @pytest.mark.skip('reason')         # always skip")
    print("  @pytest.mark.skipif(condition, reason='...')  # conditional skip")
    print("  @pytest.mark.xfail(reason='...')    # expected failure")
    print("  @pytest.mark.parametrize(...)       # data-driven tests")

    # --- 9e: pytest.skip() inside a test ---
    print("\n--- 9e: Conditional skipping inside tests ---")
    print("  def test_cs50_validation(texts_dir):")
    print("      path = texts_dir / 'cat.txt'")
    print("      if not path.exists():")
    print("          pytest.skip(f'File not found: {path}')")
    print("      # continue with test...")
    print()
    print("  This skips gracefully when test data files are missing")
    print("  (e.g., CS50 files not downloaded yet).")

    print()


# =============================================================================
# SECTION 10: MOCK CLASSES — Test Doubles for Dependency Injection
# =============================================================================
# ┌─────────────────────────────────────────────────────────────────┐
# │              MOCKS AND TEST DOUBLES                             │
# │─────────────────────────────────────────────────────────────────│
# │                                                                 │
# │  A "mock" is a FAKE implementation used in tests:               │
# │                                                                 │
# │  PRODUCTION:                                                    │
# │    run_speller(HashTableDictionary())  ← real file I/O          │
# │                                                                 │
# │  TESTING:                                                       │
# │    run_speller(MockDictionary())       ← no files, deterministic│
# │                                                                 │
# │  WHY THIS WORKS:                                                │
# │    run_speller accepts DictionaryProtocol (the abstraction)     │
# │    MockDictionary has load/check/size (matches the Protocol)    │
# │    Structural typing = no inheritance needed                    │
# │    The function doesn't know or care which one it gets          │
# │                                                                 │
# │  This is the DEPENDENCY INJECTION PAYOFF.                       │
# │  Without Protocol + DI, you can't mock. With it, mocking is    │
# │  trivial. Every future project benefits from this pattern.      │
# └─────────────────────────────────────────────────────────────────┘

def section_10_mock_classes() -> None:
    """Demonstrate mock classes for testing with dependency injection."""
    print("=" * 70)
    print("SECTION 10: MOCK CLASSES — TEST DOUBLES")
    print("=" * 70)

    # --- 10a: Mock vs Real ---
    print("\n--- 10a: Mock vs Real ---")
    print("  REAL (production):    MockDictionary would be wrong here")
    print("    dictionary = HashTableDictionary()")
    print("    dictionary.load('dictionaries/large')   # reads file")
    print("    dictionary.check('cat')                 # O(1) hash lookup")
    print()
    print("  MOCK (testing):       No file I/O, instant, deterministic")
    print("    dictionary = MockDictionary(words={'cat', 'dog'})")
    print("    dictionary.load('anything')             # always True")
    print("    dictionary.check('cat')                 # word in set")

    # --- 10b: Writing a mock ---
    print("\n--- 10b: Writing a mock class ---")

    class MockDictionary:
        """Satisfies DictionaryProtocol without inheriting from it."""

        def __init__(self, words: set[str] | None = None) -> None:
            self._words = words or {"the", "cat", "sat", "on", "mat"}
            self._loaded = False

        def load(self, filepath: str) -> bool:
            self._loaded = True
            return True      # always succeeds

        def check(self, word: str) -> bool:
            return word.lower() in self._words

        def size(self) -> int:
            return len(self._words)

        def __len__(self) -> int:
            return self.size()

        def __contains__(self, word: str) -> bool:
            return self.check(word)

    mock = MockDictionary(words={"hello", "world"})
    mock.load("ignored.txt")       # doesn't actually read anything
    print(f"  mock.check('hello') = {mock.check('hello')}")
    print(f"  mock.check('xyz')   = {mock.check('xyz')}")
    print(f"  mock.size()         = {mock.size()}")
    print(f"  'hello' in mock     = {'hello' in mock}")
    print(f"  len(mock)           = {len(mock)}")

    # --- 10c: FailingDictionary ---
    print("\n--- 10c: FailingDictionary for error path testing ---")
    print("  class FailingDictionary:")
    print("      def load(self, filepath):  return False  # always fails")
    print("      def check(self, word):     return False")
    print("      def size(self):            return 0")
    print()
    print("  # Test the error path:")
    print("  def test_load_failure(failing_dictionary):")
    print("      with pytest.raises(SystemExit):")
    print("          run_speller(dictionary=failing_dictionary, ...)")
    print()
    print("  NEGATIVE TESTING: verifying error paths is just as")
    print("  important as testing happy paths. If your error handling")
    print("  is broken, you won't know until production crashes.")

    # --- 10d: Mock as fixture ---
    print("\n--- 10d: Wrapping mocks in fixtures ---")
    print("  # In conftest.py:")
    print("  class MockDictionary: ...   # the class (not a fixture)")
    print()
    print("  @pytest.fixture")
    print("  def mock_dictionary():      # the fixture (wraps the class)")
    print("      return MockDictionary()")
    print()
    print("  # In test_speller.py:")
    print("  def test_speller(mock_dictionary):  # ← injected by name")
    print("      result = run_speller(dictionary=mock_dictionary, ...)")
    print()
    print("  WHY WRAP? So test functions can request mocks by name.")
    print("  Without the fixture, each test would create its own mock.")

    print()


# =============================================================================
# SECTION 11: ASSERTIONS AND pytest.raises
# =============================================================================

def section_11_assertions() -> None:
    """Demonstrate assertion patterns and exception testing."""
    print("=" * 70)
    print("SECTION 11: ASSERTIONS AND pytest.raises")
    print("=" * 70)

    # --- 11a: Basic assertions ---
    print("\n--- 11a: Basic assertions (pytest uses plain assert) ---")
    print("  assert result == expected            # equality")
    print("  assert result is True                # identity (for booleans)")
    print("  assert result is not None            # not None")
    print("  assert 'cat' in words                # membership")
    print("  assert len(words) == 6               # length")
    print("  assert result > 0                    # comparison")
    print("  assert isinstance(result, int)       # type check")
    print()
    print("  pytest enhances assert with DETAILED failure messages:")
    print("  > assert [1, 2, 3] == [1, 2, 4]")
    print("  E    At index 2 diff: 3 != 4")
    print()
    print("  No need for assertEqual, assertTrue, etc. — plain assert works.")

    # --- 11b: pytest.approx ---
    print("\n--- 11b: pytest.approx — floating-point comparison ---")
    print("  # WRONG — floating-point math is imprecise:")
    print("  assert 0.1 + 0.2 == 0.3             # FAILS! (0.30000000000000004)")
    print()
    print("  # CORRECT — use pytest.approx:")
    print("  assert 0.1 + 0.2 == pytest.approx(0.3)")
    print("  assert elapsed == pytest.approx(0.05, abs=0.01)  # ±0.01 tolerance")

    # --- 11c: pytest.raises ---
    print("\n--- 11c: pytest.raises — testing expected exceptions ---")
    print("  # Verify exception TYPE:")
    print("  with pytest.raises(RuntimeError):")
    print("      dictionary.check('hello')     # should raise")
    print()
    print("  # Verify TYPE + MESSAGE:")
    print("  with pytest.raises(RuntimeError, match='not loaded'):")
    print("      dictionary.check('hello')     # message must contain 'not loaded'")
    print()
    print("  # Capture the exception for inspection:")
    print("  with pytest.raises(ValueError) as exc_info:")
    print("      FileHandlerConfig(BACKUP_COUNT=-1)")
    print("  assert 'BACKUP_COUNT' in str(exc_info.value)")
    print()
    print("  HOW IT WORKS:")
    print("    with pytest.raises(RuntimeError):   ← expects an exception")
    print("        some_code()                     ← if NO exception → test FAILS")
    print("                                        ← if wrong type → test FAILS")
    print("                                        ← if correct type → test PASSES")

    print()


# =============================================================================
# SECTION 12: COMMON PITFALLS AND GOTCHAS
# =============================================================================

def section_12_pitfalls() -> None:
    """Common mistakes when writing pytest tests."""
    print("=" * 70)
    print("SECTION 12: COMMON PITFALLS AND GOTCHAS")
    print("=" * 70)

    # --- 12a: Calling fixtures ---
    print("\n--- 12a: NEVER call fixtures yourself ---")
    print("  # WRONG:")
    print("  def test_check():")
    print("      d = loaded_dictionary()    # ← NO! Don't call fixtures!")
    print("      assert d.check('cat')")
    print()
    print("  # CORRECT:")
    print("  def test_check(loaded_dictionary):  # ← parameter name = injection")
    print("      assert loaded_dictionary.check('cat')")

    # --- 12b: Name mismatch ---
    print("\n--- 12b: Fixture name must EXACTLY match parameter ---")
    print("  @pytest.fixture")
    print("  def loaded_dictionary(): ...")
    print()
    print("  def test_a(loaded_dictionary):   # ✓ exact match")
    print("  def test_b(loaded_dict):         # ✗ fixture not found!")
    print("  def test_c(dictionary):          # ✗ fixture not found!")

    # --- 12c: Importing conftest ---
    print("\n--- 12c: NEVER import conftest.py ---")
    print("  # WRONG:")
    print("  from tests.conftest import loaded_dictionary  # NO!")
    print()
    print("  # CORRECT:")
    print("  def test_check(loaded_dictionary):  # just use the name")
    print()
    print("  Exception: importing mock CLASSES (not fixtures) from conftest")
    print("  is OK when you need the class outside of fixture context:")
    print("  from tests.conftest import MockDictionary  # OK for class")

    # --- 12d: Mutating shared fixtures ---
    print("\n--- 12d: Don't mutate fixtures with wider scopes ---")
    print("  @pytest.fixture(scope='session')")
    print("  def shared_dict():")
    print("      d = HashTableDictionary()")
    print("      d.load('dictionaries/large')")
    print("      return d")
    print()
    print("  def test_a(shared_dict):")
    print("      shared_dict.unload()        # ← MUTATES shared fixture!")
    print()
    print("  def test_b(shared_dict):        # ← shared_dict is now EMPTY!")
    print("      assert shared_dict.size() == 143091   # FAILS!")
    print()
    print("  FIX: Use function scope (default) for mutable objects.")

    # --- 12e: Test file naming ---
    print("\n--- 12e: Test file and function naming ---")
    print("  Files must be named:   test_*.py  or  *_test.py")
    print("  Functions must be named: test_*")
    print("  Classes must be named:   Test*  (capital T)")
    print()
    print("  WRONG: checks.py, my_tests.py, TestCases.py")
    print("  WRONG: def check_cat(), def verify_load()")
    print("  RIGHT: test_dictionary.py, test_speller.py")
    print("  RIGHT: def test_check_cat(), def test_load()")

    # --- 12f: Generators in assertions ---
    print("\n--- 12f: Materialize generators before asserting ---")
    print("  # WRONG — comparing generator object, not its values:")
    print("  assert extract_words(path) == ['hello', 'world']  # FAILS!")
    print()
    print("  # CORRECT — materialize with list():")
    print("  assert list(extract_words(path)) == ['hello', 'world']")

    print()


# =============================================================================
# SECTION 13: DECISION GUIDE AND CHEAT SHEET
# =============================================================================
#
# ┌──────────────────────────────────────────────────────────────────┐
# │                    FIXTURE DECISION GUIDE                        │
# │──────────────────────────────────────────────────────────────────│
# │  Need to...                          │ Pattern                  │
# │──────────────────────────────────────│──────────────────────────│
# │  Share setup across tests            │ @pytest.fixture          │
# │  Share across files                  │ conftest.py              │
# │  Create temp files                   │ tmp_path (built-in)      │
# │  Capture stdout/stderr               │ capsys (built-in)        │
# │  Modify env vars temporarily         │ monkeypatch (built-in)   │
# │  Create variations of same data      │ Factory fixture          │
# │  Test with multiple inputs           │ @pytest.mark.parametrize │
# │  Skip slow tests                     │ @pytest.mark.slow        │
# │  Test expected exceptions            │ pytest.raises()          │
# │  Test floating-point values          │ pytest.approx()          │
# │  Mock expensive dependencies         │ Mock class + fixture     │
# │  Test error paths                    │ FailingMock + fixture    │
# │  Reduce setup cost                   │ Wider scope (session)    │
# └──────────────────────────────────────────────────────────────────┘
#
# ┌──────────────────────────────────────────────────────────────────┐
# │                FIXTURE TYPE CHEAT SHEET                          │
# │──────────────────────────────────────────────────────────────────│
# │                                                                  │
# │  REGULAR FIXTURE — returns a value                               │
# │    @pytest.fixture                                               │
# │    def data():                                                   │
# │        return {"key": "value"}                                   │
# │                                                                  │
# │  FACTORY FIXTURE — returns a function                            │
# │    @pytest.fixture                                               │
# │    def make_data(tmp_path):                                      │
# │        def _create(content):                                     │
# │            path = tmp_path / "test.txt"                          │
# │            path.write_text(content)                              │
# │            return path                                           │
# │        return _create                                            │
# │                                                                  │
# │  YIELD FIXTURE — setup + teardown                                │
# │    @pytest.fixture                                               │
# │    def db_connection():                                          │
# │        conn = create_connection()                                │
# │        yield conn              # test runs here                  │
# │        conn.close()            # teardown (always runs)          │
# │                                                                  │
# │  MOCK FIXTURE — fake implementation                              │
# │    class MockLLM:                                                │
# │        def generate(self, prompt): return "mocked response"      │
# │    @pytest.fixture                                               │
# │    def mock_llm(): return MockLLM()                              │
# └──────────────────────────────────────────────────────────────────┘
#
# ┌──────────────────────────────────────────────────────────────────┐
# │                  SCOPE CHEAT SHEET                               │
# │──────────────────────────────────────────────────────────────────│
# │  "function" (default) │ Fresh per test. Use for mutable objects. │
# │  "class"              │ Shared in class. Rarely needed.          │
# │  "module"             │ Shared in .py file. Read-only data.      │
# │  "session"            │ Shared everywhere. Expensive setup only. │
# └──────────────────────────────────────────────────────────────────┘
#
# ┌──────────────────────────────────────────────────────────────────┐
# │                  COMMAND CHEAT SHEET                             │
# │──────────────────────────────────────────────────────────────────│
# │  pytest                              # run all tests             │
# │  pytest -v                           # verbose (show test names) │
# │  pytest -x                           # stop on first failure     │
# │  pytest tests/test_dictionary.py     # specific file             │
# │  pytest -k "test_check"             # filter by name pattern    │
# │  pytest -m integration              # only integration tests    │
# │  pytest -m "not integration"        # skip integration tests    │
# │  pytest --cov=speller               # with coverage report      │
# │  pytest -s                          # show print() output       │
# │  pytest --fixtures                  # list all available fixtures│
# └──────────────────────────────────────────────────────────────────┘
#
# ┌──────────────────────────────────────────────────────────────────┐
# │              YOUR SPELLER TEST MAP                               │
# │──────────────────────────────────────────────────────────────────│
# │  Test File            │ Patterns Used                            │
# │───────────────────────│─────────────────────────────────────────│
# │  conftest.py          │ Path fixtures, tmp_path fixtures,        │
# │                       │ object fixtures, factory fixtures,       │
# │                       │ mock classes, fixture chaining           │
# │  test_config.py       │ Basic assert, pytest.raises, class tests │
# │  test_benchmarks.py   │ Context manager testing, pytest.approx   │
# │  test_dictionary.py   │ parametrize, Protocol isinstance,       │
# │                       │ integration markers                      │
# │  test_text_processor  │ Factory fixture, parametrize with IDs,  │
# │                       │ generator materialization, edge cases    │
# │  test_speller.py      │ Mock injection, SystemExit testing,     │
# │                       │ dependency injection payoff              │
# │  test_main.py         │ argv injection, capsys, argparse testing │
# └──────────────────────────────────────────────────────────────────┘
#
# =============================================================================


# =============================================================================
# MAIN EXECUTION
# =============================================================================

if __name__ == "__main__":
    section_1_what_is_a_fixture()
    section_2_how_injection_works()
    section_3_conftest()
    section_4_fixture_scopes()
    section_5_fixture_chaining()
    section_6_builtin_fixtures()
    section_7_factory_fixtures()
    section_8_parametrize()
    section_9_markers()
    section_10_mock_classes()
    section_11_assertions()
    section_12_pitfalls()

    print("=" * 70)
    print("REFERENCE COMPLETE — See Section 13 (cheat sheets) in source code")
    print("=" * 70)
