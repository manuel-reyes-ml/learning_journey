"""
33_pytest_builtin_fixtures_reference.py
=========================================

Personal reference: pytest Built-in Fixtures — the fixtures pytest
provides automatically without any imports or conftest.py definitions.
Every fixture here is available to any test just by using its name as
a parameter. No @pytest.fixture decoration needed by you.

Topics covered
--------------
1.  tmp_path          — unique temporary directory per test (Path object)
2.  tmp_path_factory  — temporary directories with session scope
3.  capsys            — capture stdout and stderr output
4.  capfd             — capture file descriptors (C-level stdout/stderr)
5.  caplog            — capture logging output
6.  monkeypatch       — safely patch attributes, env vars, sys.path
7.  request           — fixture metadata and parametrize access
8.  pytestconfig      — access to pytest configuration and CLI options
9.  recwarn           — capture warnings
10. cache             — persist values across test sessions
11. doctest_namespace  — inject names into doctests
12. Decision Guide and Cheat Sheet

Why this matters for your roadmap (v8.2 GenAI-First)
------------------------------------------------------
- Stage 1 (Speller):     tmp_path for test dict/text files
                          capsys for verifying print() report output
                          caplog for verifying logger calls
                          monkeypatch for env var and sys.argv control
                          request for parametrized fixture backends
- Stage 1 (DataVault):   monkeypatch for Gemini API key injection
                          capsys for Streamlit output verification
                          tmp_path for test CSV/JSON data files
- Stage 1 (PolicyPulse): caplog for RAG pipeline logging verification
                          monkeypatch for ChromaDB path override
                          tmp_path for test embedding files
- Stage 1 (FormSense):   tmp_path for sample form image files
                          monkeypatch for Gemini Vision API keys
                          caplog for extraction pipeline log checks
- Stage 2 (Data Eng):    monkeypatch for AWS credential injection
                          tmp_path for test Parquet/CSV files
                          cache for expensive fixture data across runs
- Stage 3 (ML):          tmp_path for model checkpoint files
                          monkeypatch for CUDA device override
                          caplog for training loop log verification
- Stage 4 (LLM):         monkeypatch for LangSmith API keys
                          caplog for agent step logging verification
                          monkeypatch for LangGraph state injection
- Stage 5 (Senior):      All fixtures combined in CI/CD test suites
                          cache for cross-session benchmark baselines

How to use this file
---------------------
Run it directly to see all output::

    $ python 33_pytest_builtin_fixtures_reference.py

Or import individual sections to experiment in a REPL::

    >>> from 33_pytest_builtin_fixtures_reference import section_1_tmp_path

Author: Manuel Reyes — CS50 Speller / Stage 1 Learning Reference
Version: 1.0.0 — April 2026

References
----------
.. [1] pytest Docs — Built-in fixtures reference
   https://docs.pytest.org/en/stable/reference/fixtures.html
.. [2] pytest Docs — tmp_path
   https://docs.pytest.org/en/stable/how-to/tmp_path.html
.. [3] pytest Docs — monkeypatch
   https://docs.pytest.org/en/stable/how-to/monkeypatch.html
.. [4] pytest Docs — capsys / capfd
   https://docs.pytest.org/en/stable/how-to/capture.html
.. [5] pytest Docs — caplog
   https://docs.pytest.org/en/stable/how-to/logging.html
"""

from __future__ import annotations

import logging
import os
import sys
import warnings
from pathlib import Path


# =============================================================================
# SECTION 1: tmp_path — Unique Temporary Directory Per Test
# =============================================================================
# ┌─────────────────────────────────────────────────────────────────┐
# │                        tmp_path                                 │
# │─────────────────────────────────────────────────────────────────│
# │                                                                 │
# │  Type:    pathlib.Path                                          │
# │  Scope:   function (unique per test — never shared)             │
# │  Purpose: create files and directories tests need               │
# │                                                                 │
# │  WHAT YOU GET                                                   │
# │  Each test gets a UNIQUE directory, e.g.:                       │
# │    /tmp/pytest-of-manuel/pytest-42/test_load_words0/            │
# │    /tmp/pytest-of-manuel/pytest-42/test_check_cat1/             │
# │                                                                 │
# │  pytest creates it before the test, deletes it after the        │
# │  session (keeps last 3 by default). You never clean up.         │
# │                                                                 │
# │  WHAT IT REPLACES                                               │
# │  Without tmp_path:                                              │
# │    import tempfile, os                                          │
# │    tmpdir = tempfile.mkdtemp()       ← you manage creation      │
# │    try:                                                         │
# │        ...test code...                                          │
# │    finally:                                                      │
# │        shutil.rmtree(tmpdir)         ← you manage cleanup       │
# │                                                                 │
# │  With tmp_path:                                                 │
# │    def test_something(tmp_path):     ← pytest handles both      │
# │        file = tmp_path / "test.txt"                             │
# │        file.write_text("hello")                                 │
# └─────────────────────────────────────────────────────────────────┘

def section_1_tmp_path() -> None:
    """Demonstrate tmp_path usage patterns."""
    print("=" * 70)
    print("SECTION 1: tmp_path — Unique Temporary Directory Per Test")
    print("=" * 70)

    # --- 1a: Basic file creation ---
    print("\n--- 1a: Basic file creation ---")
    print("  def test_load_words(tmp_path: Path) -> None:")
    print("      dict_file = tmp_path / 'words.txt'")
    print("      dict_file.write_text('cat\\ndog\\n', encoding='utf-8')")
    print("      assert dict_file.exists()")
    print("      content = dict_file.read_text(encoding='utf-8')")
    print("      assert 'cat' in content")
    print()
    print("  # tmp_path IS a Path object — all Path methods available:")
    print("  # tmp_path / 'subdir' / 'file.txt'  → nested paths")
    print("  # tmp_path.mkdir(parents=True)       → create subdirectories")
    print("  # tmp_path.glob('*.txt')             → glob for files")

    # --- 1b: Creating subdirectories ---
    print("\n--- 1b: Creating subdirectories ---")
    print("  def test_batch(tmp_path: Path) -> None:")
    print("      texts = tmp_path / 'texts'")
    print("      texts.mkdir()                    # create subdir")
    print("      (texts / 'cat.txt').write_text('A cat is not a caterpillar')")
    print("      (texts / 'dog.txt').write_text('A dog is not a dinosaur')")
    print("      files = list(texts.glob('*.txt'))")
    print("      assert len(files) == 2")

    # --- 1c: Why function scope matters ---
    print("\n--- 1c: Why function scope matters (isolation) ---")
    print("  test_a gets:  /tmp/pytest-.../test_a0/  (unique)")
    print("  test_b gets:  /tmp/pytest-.../test_b0/  (unique)")
    print()
    print("  Files written by test_a are INVISIBLE to test_b.")
    print("  This is the isolation guarantee — tests cannot interfere.")
    print("  If test_a creates 'large' dict and test_b also creates it,")
    print("  they get DIFFERENT files in DIFFERENT directories.")

    # --- 1d: Factory fixture pattern using tmp_path ---
    print("\n--- 1d: Factory fixture built on tmp_path (your make_text_file) ---")
    print("  @pytest.fixture")
    print("  def make_text_file(tmp_path: Path):")
    print("      def _create(content: str, filename: str = 'test.txt') -> Path:")
    print("          file_path = tmp_path / filename")
    print("          file_path.write_text(content, encoding='utf-8')")
    print("          return file_path")
    print("      return _create")
    print()
    print("  def test_extract(make_text_file):")
    print("      path = make_text_file('hello world')")
    print("      content = path.read_text(encoding='utf-8')")
    print("      words = list(extract_words(content, path.name))")
    print("      assert words == ['hello', 'world']")

    # --- 1e: Path methods quick reference ---
    print("\n--- 1e: Most-used Path methods with tmp_path ---")
    print("  tmp_path / 'file.txt'              → PosixPath (join)")
    print("  (tmp_path / 'f').write_text('hi')  → write string to file")
    print("  (tmp_path / 'f').read_text()       → read file as string")
    print("  (tmp_path / 'f').write_bytes(b'')  → write raw bytes")
    print("  (tmp_path / 'f').read_bytes()      → read raw bytes")
    print("  (tmp_path / 'd').mkdir()            → create directory")
    print("  tmp_path.exists()                   → True (always exists)")
    print("  tmp_path.is_dir()                   → True")

    print()


# =============================================================================
# SECTION 2: tmp_path_factory — Session-Scoped Temporary Directories
# =============================================================================
# ┌─────────────────────────────────────────────────────────────────┐
# │                   tmp_path_factory                              │
# │─────────────────────────────────────────────────────────────────│
# │                                                                 │
# │  Type:    TempPathFactory object                                │
# │  Scope:   session (shared across ALL tests if you want)         │
# │  Purpose: create directories that survive the whole session     │
# │                                                                 │
# │  WHY IT EXISTS                                                  │
# │  tmp_path has function scope — a new dir per test.              │
# │  tmp_path_factory lets you create a directory at session scope  │
# │  so a session-scoped fixture can create files once for all.     │
# │                                                                 │
# │  RULE OF THUMB                                                  │
# │  tmp_path         → inside function-scoped fixtures/tests       │
# │  tmp_path_factory → inside session/module-scoped fixtures only  │
# └─────────────────────────────────────────────────────────────────┘

def section_2_tmp_path_factory() -> None:
    """Demonstrate tmp_path_factory for session-scoped fixtures."""
    print("=" * 70)
    print("SECTION 2: tmp_path_factory — Session-Scoped Temp Directories")
    print("=" * 70)

    # --- 2a: Why you need tmp_path_factory ---
    print("\n--- 2a: Why you can't use tmp_path in session fixtures ---")
    print("  # WRONG — tmp_path is function-scoped, can't use in session:")
    print("  @pytest.fixture(scope='session')")
    print("  def large_dict_data(tmp_path):       # pytest raises an error!")
    print("      ...")
    print()
    print("  # RIGHT — tmp_path_factory works at any scope:")
    print("  @pytest.fixture(scope='session')")
    print("  def large_dict_data(tmp_path_factory):")
    print("      base = tmp_path_factory.mktemp('data')")
    print("      dict_file = base / 'large.txt'")
    print("      dict_file.write_text('cat\\ndog\\n...')")
    print("      return dict_file")

    # --- 2b: mktemp vs getbasetemp ---
    print("\n--- 2b: Two methods on tmp_path_factory ---")
    print("  tmp_path_factory.mktemp('name')")
    print("    → Creates a NEW unique subdirectory each call:")
    print("      /tmp/pytest-.../name0/")
    print("      /tmp/pytest-.../name1/  (next call)")
    print()
    print("  tmp_path_factory.getbasetemp()")
    print("    → Returns the shared session base directory:")
    print("      /tmp/pytest-of-manuel/pytest-42/")
    print("    → Use when you need a stable root for multiple fixtures.")

    # --- 2c: Practical pattern for expensive data ---
    print("\n--- 2c: Expensive setup created once for the session ---")
    print("  @pytest.fixture(scope='session')")
    print("  def prebuilt_index(tmp_path_factory):")
    print("      # PolicyPulse: build ChromaDB index ONCE for all tests")
    print("      path = tmp_path_factory.mktemp('chroma')")
    print("      # ... build expensive index ...")
    print("      return path")
    print()
    print("  def test_retrieval_a(prebuilt_index): ...")
    print("  def test_retrieval_b(prebuilt_index): ...")
    print("  # Both tests share the SAME index — built only once.")

    print()


# =============================================================================
# SECTION 3: capsys — Capture stdout and stderr
# =============================================================================
# ┌─────────────────────────────────────────────────────────────────┐
# │                         capsys                                  │
# │─────────────────────────────────────────────────────────────────│
# │                                                                 │
# │  Type:    CaptureFixture[str]                                   │
# │  Scope:   function                                              │
# │  Purpose: capture text written to sys.stdout and sys.stderr     │
# │                                                                 │
# │  KEY METHOD                                                     │
# │  captured = capsys.readouterr()                                 │
# │    .out  → everything written to stdout (print(), sys.stdout)   │
# │    .err  → everything written to stderr (logging, sys.stderr)   │
# │                                                                 │
# │  readouterr() CLEARS the capture buffer each call.             │
# │  Call it multiple times to check output at different stages.    │
# │                                                                 │
# │  In your codebase:                                              │
# │    print() in __main__.py   → captured.out                     │
# │    logging handlers         → captured.err (StreamHandler)      │
# └─────────────────────────────────────────────────────────────────┘

def section_3_capsys() -> None:
    """Demonstrate capsys for capturing stdout and stderr."""
    print("=" * 70)
    print("SECTION 3: capsys — Capture stdout and stderr")
    print("=" * 70)

    # --- 3a: Basic usage ---
    print("\n--- 3a: Basic stdout capture ---")
    print("  def test_report_output(")
    print("      mock_dictionary, sample_text_file, capsys")
    print("  ) -> None:")
    print("      main(['--no-log-file', str(sample_text_file)])")
    print()
    print("      captured = capsys.readouterr()")
    print("      assert 'WORDS MISSPELLED:' in captured.out")
    print("      assert 'WORDS IN DICTIONARY:' in captured.out")

    # --- 3b: Checking stderr (logging) ---
    print("\n--- 3b: Checking stderr (your logging goes here) ---")
    print("  def test_verbose_output(large_dict_path, texts_dir, capsys):")
    print("      main(['--verbose', '--no-log-file', str(text_path)])")
    print()
    print("      captured = capsys.readouterr()")
    print("      # print() report → stdout")
    print("      assert 'WORDS MISSPELLED:' in captured.out")
    print("      # logging (StreamHandler → sys.stderr) → err")
    print("      assert len(captured.err) > 0")

    # --- 3c: readouterr clears the buffer ---
    print("\n--- 3c: readouterr() clears the buffer each call ---")
    print("  def test_staged_output(capsys):")
    print("      print('first')")
    print("      captured = capsys.readouterr()")
    print("      assert captured.out == 'first\\n'    # only 'first'")
    print()
    print("      print('second')")
    print("      captured = capsys.readouterr()")
    print("      assert captured.out == 'second\\n'   # only 'second'")
    print("      # 'first' is gone — buffer was cleared on first call")

    # --- 3d: Temporarily disabling capture ---
    print("\n--- 3d: Temporarily disabling capture (show output in terminal) ---")
    print("  def test_debug(capsys):")
    print("      with capsys.disabled():")
    print("          print('this goes straight to terminal')")
    print("          # Useful during development to see real output")
    print("          # NOT for production tests — remove before committing")

    # --- 3e: capsys vs capfd ---
    print("\n--- 3e: capsys vs capfd — when to use which ---")
    print("  capsys  → captures sys.stdout / sys.stderr (Python level)")
    print("            Use for: print(), logging.StreamHandler, sys.stdout.write()")
    print()
    print("  capfd   → captures file descriptors 1 and 2 (OS level)")
    print("            Use for: C extensions, subprocesses, os.write(1, ...)")
    print()
    print("  Rule: use capsys unless you're testing C-level output.")
    print("  Your entire codebase uses Python-level I/O → always capsys.")

    print()


# =============================================================================
# SECTION 4: capfd — Capture File Descriptors
# =============================================================================

def section_4_capfd() -> None:
    """Demonstrate capfd for OS-level file descriptor capture."""
    print("=" * 70)
    print("SECTION 4: capfd — Capture File Descriptors (OS Level)")
    print("=" * 70)

    # --- 4a: What capfd captures that capsys misses ---
    print("\n--- 4a: What capfd captures that capsys misses ---")
    print("  capsys patches sys.stdout/sys.stderr in Python.")
    print("  capfd patches file descriptors 1 and 2 at the OS level.")
    print()
    print("  # capsys MISSES this:")
    print("  import os")
    print("  os.write(1, b'hello')          # fd 1 = stdout, bypasses sys.stdout")
    print()
    print("  # capfd CATCHES this:")
    print("  def test_fd_output(capfd):")
    print("      os.write(1, b'hello')")
    print("      captured = capfd.readouterr()")
    print("      assert captured.out == 'hello'")

    # --- 4b: Same API as capsys ---
    print("\n--- 4b: Identical API to capsys ---")
    print("  capfd.readouterr()   → (out, err) named tuple")
    print("  capfd.disabled()     → context manager to disable capture")
    print()
    print("  Both have identical method signatures.")
    print("  The only difference is WHERE they intercept output.")

    # --- 4c: When you'd use this in your roadmap ---
    print("\n--- 4c: When this appears in your roadmap ---")
    print("  Stage 2 (Data Eng): testing tools that call C libraries")
    print("  Stage 3 (ML):       testing PyTorch/NumPy C extensions")
    print("  Stage 4 (LLM):      testing tools that spawn subprocesses")
    print()
    print("  For Stage 1 (Speller, DataVault, PolicyPulse): use capsys.")

    print()


# =============================================================================
# SECTION 5: caplog — Capture Logging Output
# =============================================================================
# ┌─────────────────────────────────────────────────────────────────┐
# │                         caplog                                  │
# │─────────────────────────────────────────────────────────────────│
# │                                                                 │
# │  Type:    LogCaptureFixture                                     │
# │  Scope:   function                                              │
# │  Purpose: capture logging records directly — without needing   │
# │           to parse stderr text                                  │
# │                                                                 │
# │  WHY caplog OVER capsys FOR LOGGING                             │
# │  capsys captures the formatted string:                          │
# │    "14:30:45 : INFO : Dictionary loaded: 143091 words"          │
# │  caplog captures the structured LogRecord object:              │
# │    record.levelname == "INFO"                                   │
# │    record.message == "Dictionary loaded: 143091 words"          │
# │    record.name == "speller.load_dictionary"                     │
# │                                                                 │
# │  caplog lets you assert on level and message separately,        │
# │  without depending on the exact log format string.              │
# └─────────────────────────────────────────────────────────────────┘

def section_5_caplog() -> None:
    """Demonstrate caplog for capturing logging records."""
    print("=" * 70)
    print("SECTION 5: caplog — Capture Logging Output")
    print("=" * 70)

    # --- 5a: Basic usage ---
    print("\n--- 5a: Basic caplog usage ---")
    print("  def test_load_logs_word_count(caplog) -> None:")
    print("      with caplog.at_level(logging.INFO, logger='speller'):")
    print("          dictionary = HashTableDictionary()")
    print("          dictionary.load('dictionaries/large')")
    print()
    print("      assert 'Loaded' in caplog.text")
    print("      assert '143091' in caplog.text")

    # --- 5b: Checking structured records ---
    print("\n--- 5b: Checking structured LogRecord objects ---")
    print("  def test_error_on_missing_file(caplog) -> None:")
    print("      with caplog.at_level(logging.ERROR, logger='speller'):")
    print("          dictionary = HashTableDictionary()")
    print("          dictionary.load('nonexistent.txt')")
    print()
    print("      # caplog.records — list of LogRecord objects")
    print("      assert len(caplog.records) > 0")
    print("      record = caplog.records[0]")
    print("      assert record.levelname == 'ERROR'")
    print("      assert 'not found' in record.message")

    # --- 5c: Attributes available ---
    print("\n--- 5c: caplog attributes ---")
    print("  caplog.records      → list[LogRecord] — all captured records")
    print("  caplog.text         → str — formatted log output (all records)")
    print("  caplog.messages     → list[str] — just the message strings")
    print("  caplog.record_tuples → list[(logger_name, level, message)]")
    print()
    print("  Per LogRecord:")
    print("  record.levelname    → 'DEBUG', 'INFO', 'WARNING', 'ERROR'")
    print("  record.message      → the formatted message string")
    print("  record.name         → logger name ('speller.dictionaries')")
    print("  record.levelno      → numeric level (10, 20, 30, 40)")

    # --- 5d: Setting log level ---
    print("\n--- 5d: Controlling log level in tests ---")
    print("  # Method 1: context manager (recommended)")
    print("  with caplog.at_level(logging.DEBUG, logger='speller'):")
    print("      run_some_code()")
    print()
    print("  # Method 2: set_level on the fixture")
    print("  caplog.set_level(logging.DEBUG, logger='speller')")
    print("  run_some_code()")
    print()
    print("  # logger= argument scopes it to one package — best practice.")
    print("  # Without logger=, ALL loggers in the process are captured.")

    # --- 5e: caplog vs capsys for logging ---
    print("\n--- 5e: caplog vs capsys — when to use which ---")
    print("  capsys  → parse the full formatted log string from stderr")
    print("            Use when you need to check format or color codes")
    print()
    print("  caplog  → inspect structured LogRecord objects")
    print("            Use when you need to check level, logger name,")
    print("            or message content WITHOUT depending on format")
    print()
    print("  Rule: caplog is cleaner for log behavior. capsys is cleaner")
    print("  for verifying the final formatted output the user sees.")

    print()


# =============================================================================
# SECTION 6: monkeypatch — Safely Patch Attributes, Env Vars, sys.path
# =============================================================================
# ┌─────────────────────────────────────────────────────────────────┐
# │                       monkeypatch                               │
# │─────────────────────────────────────────────────────────────────│
# │                                                                 │
# │  Type:    MonkeyPatch                                           │
# │  Scope:   function (all patches reversed after the test)        │
# │  Purpose: temporarily change attributes, env vars, or imports  │
# │           for the duration of a single test                     │
# │                                                                 │
# │  THE GOLDEN RULE                                                │
# │  monkeypatch automatically UNDOES every change after the test  │
# │  ends — even if the test fails or raises an exception.         │
# │  You never need to manually restore anything.                   │
# │                                                                 │
# │  MAIN METHODS                                                   │
# │  monkeypatch.setenv(name, value)     → set env var             │
# │  monkeypatch.delenv(name)            → delete env var          │
# │  monkeypatch.setattr(obj, name, val) → replace attribute       │
# │  monkeypatch.delattr(obj, name)      → delete attribute        │
# │  monkeypatch.syspath_prepend(path)   → prepend to sys.path     │
# │  monkeypatch.chdir(path)             → change working directory │
# └─────────────────────────────────────────────────────────────────┘

def section_6_monkeypatch() -> None:
    """Demonstrate monkeypatch for safe temporary patching."""
    print("=" * 70)
    print("SECTION 6: monkeypatch — Safe Temporary Patching")
    print("=" * 70)

    # --- 6a: Environment variables ---
    print("\n--- 6a: Environment variables (most common use) ---")
    print("  def test_with_api_key(monkeypatch) -> None:")
    print("      # Set a fake API key for the test")
    print("      monkeypatch.setenv('GEMINI_API_KEY', 'fake-key-for-testing')")
    print("      monkeypatch.setenv('GOOGLE_PROJECT_ID', 'test-project')")
    print()
    print("      result = run_llm_query('Hello')")
    print("      # After test: GEMINI_API_KEY is restored to original value")
    print()
    print("  # Delete an env var for the test duration:")
    print("  monkeypatch.delenv('GEMINI_API_KEY', raising=False)")
    print("  # raising=False: no error if the var didn't exist")

    # --- 6b: Attribute patching ---
    print("\n--- 6b: Attribute patching ---")
    print("  # Replace a function on a module:")
    print("  import speller.dictionaries as dicts_module")
    print()
    print("  def mock_load(self, filepath: str) -> bool:")
    print("      return True   # always succeeds")
    print()
    print("  monkeypatch.setattr(dicts_module.HashTableDictionary, 'load', mock_load)")
    print()
    print("  # Replace a module-level constant:")
    print("  import speller.config as config_module")
    print("  monkeypatch.setattr(config_module, 'MAX_WORD_LENGTH', 10)")
    print("  # Now any code that imports MAX_WORD_LENGTH sees 10, not 45")

    # --- 6c: sys.argv patching ---
    print("\n--- 6c: sys.argv patching (alternative to argv injection) ---")
    print("  # Your main() already accepts argv= parameter — prefer that.")
    print("  # monkeypatch.setattr for sys.argv is the fallback pattern")
    print("  # when the function reads sys.argv directly with no injection.")
    print()
    print("  monkeypatch.setattr(sys, 'argv', ['speller', 'texts/cat.txt'])")
    print("  result = main()   # reads sys.argv internally")
    print("  assert result == ExitCode.SUCCESS")
    print()
    print("  # Your main(argv=...) pattern is cleaner — no monkeypatch needed.")

    # --- 6d: Changing working directory ---
    print("\n--- 6d: Changing working directory ---")
    print("  def test_relative_paths(tmp_path, monkeypatch) -> None:")
    print("      monkeypatch.chdir(tmp_path)    # cwd = tmp_path for this test")
    print("      (tmp_path / 'dict.txt').write_text('cat\\ndog')")
    print()
    print("      # Code that uses relative paths now resolves against tmp_path")
    print("      result = run_speller(dictionary=d, text_path='sample.txt')")
    print("      # After test: cwd is restored to original")

    # --- 6e: syspath_prepend ---
    print("\n--- 6e: sys.path manipulation ---")
    print("  def test_local_plugin(tmp_path, monkeypatch) -> None:")
    print("      plugin_dir = tmp_path / 'plugins'")
    print("      plugin_dir.mkdir()")
    print("      (plugin_dir / 'my_dict.py').write_text('...')")
    print()
    print("      monkeypatch.syspath_prepend(plugin_dir)")
    print("      import my_dict    # now importable for this test only")

    # --- 6f: Why monkeypatch over direct assignment ---
    print("\n--- 6f: Why monkeypatch instead of direct assignment ---")
    print("  # FRAGILE — if test fails, os.environ is permanently polluted:")
    print("  os.environ['API_KEY'] = 'fake'")
    print("  try:")
    print("      run_test()")
    print("  finally:")
    print("      del os.environ['API_KEY']   # easy to forget")
    print()
    print("  # SAFE — monkeypatch always cleans up, even on exception:")
    print("  monkeypatch.setenv('API_KEY', 'fake')")
    print("  run_test()")
    print("  # cleanup is automatic — no try/finally needed")

    print()


# =============================================================================
# SECTION 7: request — Fixture Metadata and Parametrize Access
# =============================================================================
# ┌─────────────────────────────────────────────────────────────────┐
# │                         request                                 │
# │─────────────────────────────────────────────────────────────────│
# │                                                                 │
# │  Type:    pytest.FixtureRequest                                 │
# │  Scope:   matches the fixture it's used in                      │
# │  Purpose: access metadata about the current test execution      │
# │           and retrieve the current parameter in params= fixtures │
# │                                                                 │
# │  MOST COMMON USE                                                │
# │  request.param — the current value when fixture uses params=    │
# │                                                                 │
# │  OTHER ATTRIBUTES                                               │
# │  request.fixturename  → name of the fixture being defined       │
# │  request.node         → the test item (has .name, .nodeid)      │
# │  request.scope        → "function", "class", "module", "session"│
# │  request.config       → pytest config (same as pytestconfig)    │
# │  request.addfinalizer → register a teardown callback            │
# └─────────────────────────────────────────────────────────────────┘

def section_7_request() -> None:
    """Demonstrate request fixture for parametrize and metadata access."""
    print("=" * 70)
    print("SECTION 7: request — Fixture Metadata and Parametrize Access")
    print("=" * 70)

    # --- 7a: request.param with params= ---
    print("\n--- 7a: request.param — the core use case ---")
    print("  from speller.register import dicts")
    print()
    print("  @pytest.fixture(params=list(dicts.keys()))")
    print("  def empty_dictionary(request: pytest.FixtureRequest):")
    print("      # request.param holds current key: 'hash', 'list', etc.")
    print("      return dicts[request.param].dict_class()")
    print()
    print("  # Every test using empty_dictionary runs 4 times:")
    print("  # test_load[hash]   test_load[list]")
    print("  # test_load[sorted] test_load[dict]")
    print()
    print("  # The iteration is AUTOMATIC — pytest handles the loop.")
    print("  # You just declare params= and use request.param.")

    # --- 7b: Custom parametrize IDs ---
    print("\n--- 7b: Custom IDs for parametrize ---")
    print("  @pytest.fixture(params=[")
    print("      pytest.param('hash', id='hash_table'),")
    print("      pytest.param('sorted', id='binary_search'),")
    print("  ])")
    print("  def dictionary_backend(request: pytest.FixtureRequest):")
    print("      return dicts[request.param].dict_class()")
    print()
    print("  # Output: test_load[hash_table]  test_load[binary_search]")
    print("  # More readable than test_load[hash0] test_load[sorted1]")

    # --- 7c: request.addfinalizer ---
    print("\n--- 7c: request.addfinalizer — manual teardown ---")
    print("  @pytest.fixture")
    print("  def db_connection(request: pytest.FixtureRequest):")
    print("      conn = connect_to_db()")
    print()
    print("      def teardown():")
    print("          conn.rollback()")
    print("          conn.close()")
    print()
    print("      request.addfinalizer(teardown)")
    print("      return conn")
    print()
    print("  # teardown() always runs after the test — even on failure.")
    print("  # This is the alternative to yield fixtures when you need")
    print("  # to register teardown from inside a conditional branch.")
    print()
    print("  # Prefer yield fixtures for simple cases (cleaner syntax):")
    print("  @pytest.fixture")
    print("  def db_connection():")
    print("      conn = connect_to_db()")
    print("      yield conn          # test runs here")
    print("      conn.rollback()     # teardown — always runs")
    print("      conn.close()")

    # --- 7d: request.node for test name ---
    print("\n--- 7d: request.node — accessing the test name ---")
    print("  @pytest.fixture")
    print("  def named_temp_file(request: pytest.FixtureRequest, tmp_path):")
    print("      # Use the test name as the filename for easier debugging")
    print("      test_name = request.node.name          # 'test_load_words'")
    print("      file = tmp_path / f'{test_name}.txt'")
    print("      file.write_text('content')")
    print("      return file")

    print()


# =============================================================================
# SECTION 8: pytestconfig — Access to pytest Configuration
# =============================================================================

def section_8_pytestconfig() -> None:
    """Demonstrate pytestconfig for accessing CLI options and config."""
    print("=" * 70)
    print("SECTION 8: pytestconfig — pytest Configuration Access")
    print("=" * 70)

    # --- 8a: What it provides ---
    print("\n--- 8a: What pytestconfig gives you ---")
    print("  pytestconfig is the Config object for the current pytest run.")
    print("  It lets fixtures and tests read CLI options and ini settings.")
    print()
    print("  def test_something(pytestconfig) -> None:")
    print("      verbosity = pytestconfig.getoption('verbose')")
    print("      rootdir = pytestconfig.rootdir")

    # --- 8b: Custom CLI options ---
    print("\n--- 8b: Custom CLI options via conftest.py ---")
    print("  # In conftest.py — add a custom CLI flag:")
    print("  def pytest_addoption(parser):")
    print("      parser.addoption(")
    print("          '--run-slow',")
    print("          action='store_true',")
    print("          default=False,")
    print("          help='Run slow tests'")
    print("      )")
    print()
    print("  # In conftest.py — expose it as a fixture:")
    print("  @pytest.fixture")
    print("  def run_slow(pytestconfig):")
    print("      return pytestconfig.getoption('--run-slow')")
    print()
    print("  # In test file — use it to conditionally skip:")
    print("  def test_very_slow(run_slow):")
    print("      if not run_slow:")
    print("          pytest.skip('Pass --run-slow to include this test')")
    print("      ...")
    print()
    print("  # Run: pytest --run-slow")

    # --- 8c: Common config attributes ---
    print("\n--- 8c: Common pytestconfig attributes ---")
    print("  pytestconfig.rootdir          → Path to project root")
    print("  pytestconfig.inipath          → Path to pyproject.toml / pytest.ini")
    print("  pytestconfig.getoption('v')   → verbosity level int")
    print("  pytestconfig.getini('markers')→ registered markers from ini")

    print()


# =============================================================================
# SECTION 9: recwarn — Capture Warnings
# =============================================================================

def section_9_recwarn() -> None:
    """Demonstrate recwarn for capturing warnings."""
    print("=" * 70)
    print("SECTION 9: recwarn — Capture Warnings")
    print("=" * 70)

    # --- 9a: Basic usage ---
    print("\n--- 9a: Basic recwarn usage ---")
    print("  def test_deprecated_api(recwarn) -> None:")
    print("      call_deprecated_function()")
    print()
    print("      assert len(recwarn) == 1")
    print("      warning = recwarn.pop(DeprecationWarning)")
    print("      assert 'deprecated' in str(warning.message).lower()")

    # --- 9b: pytest.warns — the simpler alternative ---
    print("\n--- 9b: pytest.warns — cleaner for most cases ---")
    print("  # Most of the time you want pytest.warns instead of recwarn:")
    print("  def test_deprecated(recwarn) -> None:")
    print("      with pytest.warns(DeprecationWarning, match='use new_api'):")
    print("          call_deprecated_function()")
    print()
    print("  # Same pattern as pytest.raises() but for warnings.")
    print("  # recwarn is for more complex cases where you need")
    print("  # to inspect multiple warnings or check order.")

    # --- 9c: When you'd see this in your roadmap ---
    print("\n--- 9c: When this appears in your roadmap ---")
    print("  Stage 1 (DataVault): PandasAI deprecation warnings")
    print("  Stage 2 (Data Eng):  SQLAlchemy 2.0 migration warnings")
    print("  Stage 3 (ML):        scikit-learn API deprecation warnings")
    print("  Stage 4 (LLM):       LangChain breaking-change warnings")

    print()


# =============================================================================
# SECTION 10: cache — Persist Values Across Test Sessions
# =============================================================================

def section_10_cache() -> None:
    """Demonstrate cache for persisting values across test sessions."""
    print("=" * 70)
    print("SECTION 10: cache — Persist Values Across Test Sessions")
    print("=" * 70)

    # --- 10a: What it does ---
    print("\n--- 10a: What cache does ---")
    print("  cache stores values in .pytest_cache/ between test runs.")
    print("  Unlike session scope (resets each run), cache PERSISTS.")
    print()
    print("  cache.get(key, default)   → read a cached value")
    print("  cache.set(key, value)     → write a value to cache")

    # --- 10b: Practical use — slow fixture baseline ---
    print("\n--- 10b: Practical use — caching expensive computation ---")
    print("  @pytest.fixture(scope='session')")
    print("  def word_frequencies(cache):")
    print("      # Check if we already computed this")
    print("      cached = cache.get('word_frequencies/v1', None)")
    print("      if cached is not None:")
    print("          return cached")
    print()
    print("      # Expensive computation — runs only on first test run")
    print("      frequencies = compute_frequencies('dictionaries/large')")
    print("      cache.set('word_frequencies/v1', frequencies)")
    print("      return frequencies")
    print()
    print("  # First run:  computes and caches (slow)")
    print("  # Later runs: reads from cache (instant)")
    print()
    print("  # Clear cache: pytest --cache-clear")

    # --- 10c: Performance benchmarks ---
    print("\n--- 10c: Benchmark baseline storage (AFC pattern) ---")
    print("  # Stage 3+ pattern: store perf baseline, fail if regression")
    print("  def test_check_performance(cache, large_dict_path):")
    print("      baseline = cache.get('benchmarks/check_ms', None)")
    print()
    print("      elapsed = time_the_check_loop(large_dict_path)")
    print()
    print("      if baseline is None:")
    print("          cache.set('benchmarks/check_ms', elapsed)")
    print("          pytest.skip('Baseline stored — run again to compare')")
    print()
    print("      assert elapsed < baseline * 1.10   # max 10% regression")

    print()


# =============================================================================
# SECTION 11: BUILT-IN FIXTURES QUICK REFERENCE
# =============================================================================
#
# ┌──────────────────────────────────────────────────────────────────┐
# │           ALL PYTEST BUILT-IN FIXTURES AT A GLANCE               │
# │──────────────────────────────────────────────────────────────────│
# │  Fixture              │ Type                   │ Scope           │
# │───────────────────────│────────────────────────│─────────────────│
# │  tmp_path             │ pathlib.Path           │ function        │
# │  tmp_path_factory     │ TempPathFactory        │ session         │
# │  capsys               │ CaptureFixture[str]    │ function        │
# │  capfd                │ CaptureFixture[str]    │ function        │
# │  capfdbinary          │ CaptureFixture[bytes]  │ function        │
# │  caplog               │ LogCaptureFixture      │ function        │
# │  monkeypatch          │ MonkeyPatch            │ function        │
# │  request              │ FixtureRequest         │ matches fixture │
# │  pytestconfig         │ Config                 │ session         │
# │  recwarn              │ WarningsChecker        │ function        │
# │  cache                │ Cache                  │ session         │
# │  doctest_namespace    │ dict                   │ session         │
# │  record_property      │ Callable               │ function        │
# │  record_testsuite_*   │ Callable               │ session         │
# └──────────────────────────────────────────────────────────────────┘

def section_11_quick_reference() -> None:
    """Print quick reference for all built-in fixtures."""
    print("=" * 70)
    print("SECTION 11: BUILT-IN FIXTURES QUICK REFERENCE")
    print("=" * 70)

    print("\n--- Core fixtures you will use in every project ---")
    print()
    print("  tmp_path")
    print("    Use: create test files and directories")
    print("    Type: pathlib.Path  |  Scope: function")
    print("    Example: (tmp_path / 'words.txt').write_text('cat\\ndog')")
    print()
    print("  capsys")
    print("    Use: capture and assert on print() and logging output")
    print("    Type: CaptureFixture[str]  |  Scope: function")
    print("    Example: captured = capsys.readouterr(); captured.out, captured.err")
    print()
    print("  caplog")
    print("    Use: capture logging records structurally (level, name, message)")
    print("    Type: LogCaptureFixture  |  Scope: function")
    print("    Example: with caplog.at_level(logging.INFO, logger='speller'): ...")
    print()
    print("  monkeypatch")
    print("    Use: temporarily patch env vars, attributes, sys.argv, cwd")
    print("    Type: MonkeyPatch  |  Scope: function (auto-reverted)")
    print("    Example: monkeypatch.setenv('GEMINI_API_KEY', 'fake-key')")
    print()
    print("  request")
    print("    Use: access request.param in params= fixtures")
    print("    Type: FixtureRequest  |  Scope: matches fixture")
    print("    Example: return dicts[request.param].dict_class()")
    print()
    print("--- Less common but useful ---")
    print()
    print("  tmp_path_factory")
    print("    Use: session-scoped fixtures that need temp directories")
    print("    Example: base = tmp_path_factory.mktemp('data')")
    print()
    print("  capfd")
    print("    Use: OS-level fd capture (C extensions, subprocesses)")
    print("    Example: same API as capsys")
    print()
    print("  recwarn / pytest.warns()")
    print("    Use: assert that code emits expected warnings")
    print("    Example: with pytest.warns(DeprecationWarning): ...")
    print()
    print("  pytestconfig")
    print("    Use: read CLI options and ini config inside fixtures")
    print("    Example: pytestconfig.getoption('--run-slow')")
    print()
    print("  cache")
    print("    Use: persist expensive values across test sessions")
    print("    Example: cache.get('key', default) / cache.set('key', val)")

    print()


# =============================================================================
# SECTION 12: DECISION GUIDE AND CHEAT SHEET
# =============================================================================
#
# ┌──────────────────────────────────────────────────────────────────┐
# │              BUILT-IN FIXTURE DECISION GUIDE                     │
# │──────────────────────────────────────────────────────────────────│
# │  I need to...                        │ Use                       │
# │──────────────────────────────────────│───────────────────────────│
# │  Create a temp file for a test       │ tmp_path                  │
# │  Create temp files in a session      │ tmp_path_factory          │
# │  fixture (session scope)             │                           │
# │  Assert on print() output            │ capsys → .out             │
# │  Assert on logging output            │ capsys → .err  OR caplog  │
# │  Assert on log level/logger name     │ caplog (structured)       │
# │  Assert on format of log string      │ capsys .err (raw text)    │
# │  Set an env var for one test         │ monkeypatch.setenv()      │
# │  Patch a function/attribute          │ monkeypatch.setattr()     │
# │  Change sys.argv for one test        │ monkeypatch (fallback)    │
# │                                      │ OR argv= injection        │
# │  Change cwd for one test             │ monkeypatch.chdir()       │
# │  Get current param in params=fixture │ request.param             │
# │  Register a teardown callback        │ request.addfinalizer()    │
# │  Get the current test's name         │ request.node.name         │
# │  Read a custom CLI option            │ pytestconfig.getoption()  │
# │  Assert a warning was emitted        │ pytest.warns()            │
# │  Persist data between test runs      │ cache.get/set()           │
# └──────────────────────────────────────────────────────────────────┘
#
# ┌──────────────────────────────────────────────────────────────────┐
# │           capsys vs caplog — WHEN TO USE WHICH                   │
# │──────────────────────────────────────────────────────────────────│
# │                                                                  │
# │  capsys                          caplog                          │
# │  ──────                          ──────                          │
# │  assert 'WORDS MISSPELLED:'      assert record.levelname == 'INFO'│
# │      in captured.out             assert 'loaded' in caplog.text  │
# │                                                                  │
# │  Best for:                       Best for:                       │
# │  - print() report output         - log level checks             │
# │  - final formatted text          - logger name checks           │
# │  - integration output checks     - message content without      │
# │  - verifying stdout vs stderr      caring about format          │
# │    separation                    - checking # of log records    │
# └──────────────────────────────────────────────────────────────────┘
#
# ┌──────────────────────────────────────────────────────────────────┐
# │         YOUR SPELLER TEST SUITE — FIXTURE MAPPING                │
# │──────────────────────────────────────────────────────────────────│
# │  Test File            │ Built-in Fixtures Used                   │
# │───────────────────────│──────────────────────────────────────────│
# │  conftest.py          │ tmp_path (sample_text_file,              │
# │                       │   sample_dict_file, mixed_text_file)     │
# │  test_config.py       │ none (pure unit tests)                   │
# │  test_benchmarks.py   │ none (pure unit tests)                   │
# │  test_dictionary.py   │ tmp_path (inline in test methods)        │
# │  test_text_processor  │ tmp_path (via make_text_file factory)    │
# │  test_speller.py      │ tmp_path (inline in test methods)        │
# │  test_main.py         │ capsys (output verification)             │
# │                       │ + tmp_path via conftest fixtures         │
# └──────────────────────────────────────────────────────────────────┘
#
# ┌──────────────────────────────────────────────────────────────────┐
# │         FUTURE PROJECTS — BUILT-IN FIXTURES TO REACH FOR         │
# │──────────────────────────────────────────────────────────────────│
# │  DataVault (Stage 1):                                            │
# │    monkeypatch.setenv('GEMINI_API_KEY', 'fake')                  │
# │    tmp_path for test CSV files                                   │
# │    capsys for Streamlit output                                   │
# │                                                                  │
# │  PolicyPulse (Stage 1):                                          │
# │    monkeypatch for ChromaDB directory                            │
# │    tmp_path for test embedding files                             │
# │    caplog for RAG retrieval log checks                           │
# │                                                                  │
# │  AFC (Stage 1+):                                                 │
# │    tmp_path for synthetic market data files                      │
# │    cache for storing benchmark baselines                         │
# │    monkeypatch for SEC API rate-limit simulation                 │
# │                                                                  │
# │  Stage 2+ (Data Engineering):                                    │
# │    monkeypatch for AWS credential injection (moto library)       │
# │    tmp_path_factory for session-scoped test datasets             │
# │    caplog for ETL pipeline log verification                      │
# └──────────────────────────────────────────────────────────────────┘
#
# =============================================================================


# =============================================================================
# MAIN EXECUTION
# =============================================================================

if __name__ == "__main__":
    section_1_tmp_path()
    section_2_tmp_path_factory()
    section_3_capsys()
    section_4_capfd()
    section_5_caplog()
    section_6_monkeypatch()
    section_7_request()
    section_8_pytestconfig()
    section_9_recwarn()
    section_10_cache()
    section_11_quick_reference()

    print("=" * 70)
    print("REFERENCE COMPLETE — See Section 12 (cheat sheets) in source code")
    print("=" * 70)
