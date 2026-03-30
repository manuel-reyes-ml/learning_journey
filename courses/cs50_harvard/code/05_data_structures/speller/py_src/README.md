# CS50 Speller — Production-Grade Python Spell Checker

A Python reimplementation of [CS50's Speller](https://cs50.harvard.edu/x/psets/5/speller/) problem set, built as an installable package with professional software engineering practices. Translates C's manual hash table, linked lists, and memory management into idiomatic Python — demonstrating that fundamentals transfer across languages when you understand the *why*, not just the *how*.

> **Part of:** [Learning Journey](https://github.com/manuel-reyes-ml/learning_journey) — Stage 1 of a 37-month career transformation from financial services to Senior LLM Engineer.

---

## What It Does

Spell-checks a text file against a dictionary and reports statistics with performance benchmarks. Run multiple backends in a single invocation to compare data structures side by side:

```
$ speller -o hash sorted texts/austen.txt

MISSPELLED WORDS -- HashTableDictionary --

Use Set as hash table - O(1) average lookup.

WORDS MISSPELLED:     1614
WORDS IN DICTIONARY:  143091
WORDS IN TEXT:        125203
CHECKED FILE:         austen.txt
FILE PATH:            texts/austen.txt
TIME IN load:         0.08
TIME IN check:        0.15
TIME IN size:         0.00
TIME IN TOTAL:        0.23

MISSPELLED WORDS -- SortedListDictionary --

Use sorted list - O(log n) binary search lookup.

WORDS MISSPELLED:     1614
WORDS IN DICTIONARY:  143091
WORDS IN TEXT:        125203
CHECKED FILE:         austen.txt
FILE PATH:            texts/austen.txt
TIME IN load:         1.82
TIME IN check:        2.31
TIME IN size:         0.00
TIME IN TOTAL:        4.13
```

Misspelled words are saved to `misspelled/<filename>` when `--show-misspelled` is passed.

---

## Why This Project Exists

CS50's Speller is a C exercise about hash tables and memory management. This project asks: *what happens when you reimplement it in Python with production standards?*

The answer: every pattern here — Protocol interfaces, ABC Template Method, plugin registry, `Generic[T]` class hierarchies, frozen dataclasses, generator streaming, context manager timing, `pyproject.toml` packaging — transfers directly to the [7 portfolio projects](https://manuel-reyes-ml.github.io/learning_journey/roadmap.html) in my roadmap. It's not a toy spell checker; it's a training ground for GenAI application architecture.

| Pattern Learned Here | Used Next In |
| --- | --- |
| `Protocol` interfaces | DataVault (swappable LLM providers) |
| ABC Template Method | PolicyPulse (swappable retrieval strategies) |
| Plugin registry (`@register_class`) | All 7 projects (swappable backend systems) |
| `Generic[T]` class hierarchies | DataVault (`LLMProvider[ResponseT]`), AFC (`DataSource[RecordT]`) |
| `@dataclass(frozen=True)` vs Pydantic | DataVault (structured outputs) |
| Generator streaming (`yield`) | PolicyPulse (RAG chunk retrieval) |
| `@contextmanager` timing | All 7 projects (benchmark pipelines) |
| `pyproject.toml` packaging | All 7 projects |
| Dependency injection | FormSense (swappable extraction backends) |
| `pytest` fixtures | All 7 projects (CI/CD via GitHub Actions) |

---

## Architecture

```
speller/
├── __init__.py           NullHandler logging + version + side-effect backend registration
├── __main__.py           CLI entry point (composition root)
├── config.py             Constants, enums, path resolution
├── protocols.py          DictionaryProtocol (structural typing)
├── benchmarks.py         timer() context manager + timed() decorator
├── register.py           Plugin registry: DictInfo, dicts{}, register_class()
├── logger.py             ColoredFormatter + configure_logging()
├── dictionaries.py       _BaseDictionary[WordContainer] ABC + four concrete backends
├── text_processor.py     Character-level state machine (generator)
└── speller.py            Orchestrator + SpellerResult (dependency injection)
```

### Dependency Chain

```
config.py ──────────┐
                    ├── No internal imports (bottom of chain)
protocols.py ───────┘
                         ↓
               register.py ←── imports protocols + speller
                    ↓
         dictionaries.py ←──── imports config + register
                    ↓
          (backends registered via @register_class at import time)

benchmarks.py ──────────── standalone (stdlib only)
logger.py ──────────────── imports config
text_processor.py ──────── imports config

speller.py ─────────────── imports protocols, benchmarks, text_processor
__main__.py ────────────── imports EVERYTHING (composition root)
                           reads dicts{} from register
```

`__init__.py` imports `dictionaries` as a side effect (`# noqa: F401`) so all `@register_class` decorators execute and `dicts{}` is fully populated before `__main__.py` reads it.

### Key Design Decisions

**Protocol over ABC for external interfaces** — `speller.py` depends on `DictionaryProtocol`, not `HashTableDictionary`. Swapping to a database-backed or ML-powered dictionary requires zero changes to the orchestrator. The concrete class is injected by `__main__.py`.

**ABC Template Method for internal hierarchy** — `_BaseDictionary` defines the complete algorithm in `load()` and `check()`. Subclasses provide only the two variable steps: `_create_container()` and `_add_word()`. Everything else — file reading, case normalisation, `_ensure_loaded()` guard, dunders, logging — is inherited unchanged.

**`Generic[WordContainer]` over Union or Protocol on mutable attributes** — `_words` is a mutable instance attribute. Declaring it as `set[str] | list[str]` causes pyright to reject `.add()` and `.append()` calls (union can't be narrowed inside methods). A Protocol on a mutable attribute triggers an invariance error. `Generic[WordContainer]` with a constrained `TypeVar` resolves the concrete type per subclass at specialisation time — no invariance violation.

```python
WordContainer = TypeVar("WordContainer", set[str], list[str], dict[str, None])

class _BaseDictionary(ABC, Generic[WordContainer]):
    self._words: WordContainer = self._create_container()  # unresolved

class HashTableDictionary(_BaseDictionary[set[str]]):      # W = set[str]
    def _add_word(self, word: str) -> None:
        self._words.add(word)       # pyright knows _words IS set[str] ✓

class ListDictionary(_BaseDictionary[list[str]]):          # W = list[str]
    def _add_word(self, word: str) -> None:
        self._words.append(word)    # pyright knows _words IS list[str] ✓

class DictDictionary(_BaseDictionary[dict[str, None]]):    # W = dict[str, None]
    def _add_word(self, word: str) -> None:
        self._words[word] = None    # pyright knows _words IS dict[str, None] ✓
```

**Plugin registry** — each backend self-registers at import time via `@register_class`. `__main__.py` selects backends by key from `dicts{}` — it never imports or names a concrete class. Adding a new backend requires zero changes to `__main__.py`, `speller.py`, or `protocols.py`.

```python
@register_class("dict", "Use Dictionary as hash table - O(1) average lookup.")
class DictDictionary(_BaseDictionary[dict[str, None]]): ...
```

**Dataclass over Pydantic** — `BenchmarkResult` and `SpellerResult` are frozen dataclasses (6.5x faster creation, 2.5x less memory than Pydantic). Pydantic is reserved for service boundaries in future projects.

**Generator streaming** — `extract_words()` yields words one at a time via a character-level state machine. No intermediate list, constant memory regardless of file size.

**Context manager timing** — `timer()` wraps code blocks; `timed()` decorator wraps functions. Both produce `BenchmarkResult` dataclasses. `ParamSpec` + `TypeVar` preserve decorated function type signatures — pyright sees real types, not `Any`.

---

## Dictionary Backends

Four backends demonstrate the same algorithm with different data structures. All satisfy `DictionaryProtocol` through structural typing and self-register via `@register_class`.

| Backend | Key | Container | Load | Check | 376K checks |
|---|---|---|---|---|---|
| `HashTableDictionary` | `hash` | `set[str]` | O(n) | **O(1)** avg | ~376K ops |
| `DictDictionary` | `dict` | `dict[str, None]` | O(n) | **O(1)** avg | ~376K ops |
| `SortedListDictionary` | `sorted` | sorted `list[str]` | O(n log n) | **O(log n)** | ~6.4M ops |
| `ListDictionary` | `list` | unsorted `list[str]` | O(n) | **O(n)** | ~53B ops |

`DictDictionary` uses `None` as a singleton sentinel — all 143,091 value slots point to the same `None` object, avoiding per-entry allocation. Algorithmically equivalent to `HashTableDictionary` but uses ~2× the memory (dict has key + hash + value pointer; set has key + hash only). `SortedListDictionary` uses `bisect.insort` on load and `bisect.bisect_left` on check. `ListDictionary` exists as a performance baseline only — never use in production.

---

## C → Python Concept Map

| C (dictionary.c / speller.c) | Python (this project) |
| --- | --- |
| Hash table with linked-list buckets | `set[str]` (built-in hash table) |
| `#define LENGTH 45` | `MAX_WORD_LENGTH: Final[int] = 45` |
| `malloc` / `free` / `valgrind` | Garbage collection (automatic) |
| `struct node` | `@dataclass(frozen=True, slots=True)` |
| Header file (`.h`) | `Protocol` class (structural typing) |
| `getrusage` benchmarking | `time.perf_counter()` + `@contextmanager` |
| `Makefile` | `pyproject.toml` + `pip install -e .` |
| `argc` / `argv` | `argparse` with `nargs='?'` |
| `fprintf(stderr, ...)` | `logging` module + `RotatingFileHandler` |
| `fread` char by char | `content[pos]` indexing + state machine |
| `strcasecmp` (case-insensitive) | `word.lower() in self._words` |

---

## Installation

```bash
# Clone the repository
git clone https://github.com/manuel-reyes-ml/learning_journey.git
cd learning_journey/speller

# Create virtual environment
python -m venv .venv
source .venv/bin/activate        # Linux/Mac
# .venv\Scripts\activate         # Windows

# Install in editable mode with dev tools
pip install -e ".[dev,test]"
```

## Usage

```bash
# Default dictionary (dictionaries/large — 143,091 words), default backend (hash)
speller texts/cat.txt

# Custom dictionary
speller dictionaries/small texts/cat.txt

# python -m alternative
python -m speller texts/austen.txt

# Select a specific backend
speller -o sorted texts/austen.txt

# Run the dict backend
speller -o dict texts/austen.txt

# Run multiple backends and compare
speller -o hash dict sorted texts/austen.txt

# Run all four backends
speller -o all texts/austen.txt

# Verbose mode (DEBUG-level console output)
speller --verbose texts/constitution.txt

# Save misspelled words to misspelled/<filename>
speller --show-misspelled texts/austen.txt

# Console only (no log file)
speller --no-log-file texts/cat.txt
```

## Testing

```bash
# Run all tests
pytest

# Verbose output
pytest -v

# Specific test file
pytest tests/test_dictionary.py

# Run only fast unit tests (exclude integration)
pytest -m "not integration"

# With coverage
pytest --cov=speller

# Show print() output
pytest -s
```

96 tests across 7 files:

| Test File | Patterns |
| --- | --- |
| `conftest.py` | Path fixtures, factory fixtures, mock classes, fixture chaining |
| `test_config.py` | Basic assertions, `pytest.raises`, class-level tests |
| `test_benchmarks.py` | Context manager testing, `pytest.approx` |
| `test_dictionary.py` | `parametrize`, Protocol `isinstance`, integration markers |
| `test_text_processor.py` | Factory fixture, `parametrize` with IDs, generator materialization |
| `test_speller.py` | `MockDictionary` injection, `SystemExit` testing |
| `test_main.py` | `argv` injection, `capsys`, argparse testing |

The dependency injection payoff — `MockDictionary` satisfies `DictionaryProtocol` structurally, no files or disk needed:

```python
class MockDictionary:
    def load(self, filepath: str) -> bool: return True
    def check(self, word: str) -> bool: return word in {"cat", "dog"}
    def size(self) -> int: return 2
    def __len__(self) -> int: return 2
    def __contains__(self, word: str) -> bool: return self.check(word)

def test_run_speller_counts(tmp_text_file):
    result = run_speller(
        dictionary=MockDictionary(),
        text_path=tmp_text_file,
        dict_path="fake/path",
    )
    assert result.words_misspelled == 1
```

## Code Quality

```bash
# Lint (find issues)
ruff check src/

# Lint + auto-fix
ruff check src/ --fix

# Format
ruff format src/

# Type check
mypy src/
```

---

## Validation Results

Output matches CS50's C staff solution exactly across all test files:

| Text File | Misspelled | Dictionary | Words in Text | Status |
| --- | --- | --- | --- | --- |
| cat.txt | 0 | 143,091 | 6 | ✅ |
| constitution.txt | 30 | 143,091 | 7,573 | ✅ |
| carroll.txt | 295 | 143,091 | 29,758 | ✅ |
| grimm.txt | 718 | 143,091 | 103,614 | ✅ |
| her.txt | 767 | 143,091 | 18,402 | ✅ |
| federalist.txt | 935 | 143,091 | 196,784 | ✅ |
| burnett.txt | 1,000 | 143,091 | 58,171 | ✅ |
| birdman.txt | 1,179 | 143,091 | 21,798 | ✅ |
| austen.txt | 1,614 | 143,091 | 125,203 | ✅ |
| frankenstein.txt | 2,451 | 143,091 | 80,527 | ✅ |
| aca.txt | 17,062 | 143,091 | 376,904 | ✅ |

---

## Project Structure

```
speller/
├── src/
│   └── speller/
│       ├── __init__.py
│       ├── __main__.py
│       ├── config.py
│       ├── protocols.py
│       ├── benchmarks.py
│       ├── register.py
│       ├── logger.py
│       ├── dictionaries.py
│       ├── text_processor.py
│       └── speller.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_config.py
│   ├── test_benchmarks.py
│   ├── test_dictionary.py
│   ├── test_text_processor.py
│   ├── test_speller.py
│   └── test_main.py
├── dictionaries/
│   ├── large                  # 143,091 words
│   └── small                  # 2 words (cat, caterpillar)
├── texts/                     # Text files to spell-check
├── keys/                      # CS50 answer keys for validation
├── logs/                      # Rotating log files (auto-created)
├── misspelled/                # Misspelled word output (auto-created)
├── pyproject.toml
├── README.md
└── LICENSE
```

---

## Technical Highlights

### Production Python Practices

- `pyproject.toml` — Unified config for build, dependencies, pytest, mypy, ruff
- `src/` **layout** — Prevents accidental imports during testing
- **Type hints** — Full type annotations, `mypy --strict` compliant
- `from __future__ import annotations` — Deferred evaluation in every module
- `TypeVar` **with constraints** — `WordContainer = TypeVar("WordContainer", set[str], list[str], dict[str, None])` solves mypy invariance in Generic class hierarchies
- `ParamSpec` **+** `TypeVar` — Type-safe decorators preserving function signatures
- **NumPy-style docstrings** — Consistent documentation across all public APIs
- `__all__` **exports** — Explicit public API per module
- `logging` **over** `print` — `NullHandler` library pattern + `RotatingFileHandler`

### CS50 Fidelity

The text processor replicates `speller.c`'s character-by-character state machine exactly, including edge cases:

- Digit mid-word discards the entire token AND consumes remaining alphanumeric characters
- Words exceeding 45 characters are skipped with remaining alpha characters consumed
- Apostrophes are valid only mid-word (not at position 0)
- The C `fread` terminator-consumption behavior is replicated for answer key accuracy

---

## Tech Stack

| Tool | Purpose |
| --- | --- |
| Python 3.12+ | Language (`type X = ...` syntax, PEP 695) |
| `set` / `list` / `dict` / `bisect` (built-in) | Four dictionary backends |
| `argparse` | CLI argument parsing |
| `logging` + `RotatingFileHandler` | Structured logging |
| `dataclasses` | Immutable result containers |
| `typing.Protocol` | Structural typing interfaces |
| `typing.Generic` + `TypeVar` | Parameterised class hierarchies |
| `contextlib.contextmanager` | Benchmark timing |
| `pathlib.Path` | File system operations |
| `pyproject.toml` + `setuptools` | Package management |
| `pytest` | Testing framework |
| `mypy` | Static type checking |
| `ruff` | Linting + formatting |

---

## What I Learned

Building this project taught me production Python patterns that directly apply to GenAI engineering:

1. **Protocol > ABC for external interfaces** — `DictionaryProtocol` lets `speller.py` accept any backend without importing concrete classes. The same pattern powers swappable LLM backends in DataVault.
2. **ABC Template Method for internal hierarchies** — `_BaseDictionary` defines the algorithm once; subclasses fill in two lines. Four backends, zero duplicated logic.
3. **`Generic[T]` solves the invariance problem** — mutable instance attributes in class hierarchies must use `Generic[WordContainer]`, not Union or Protocol. This distinction matters the moment you build `LLMProvider[ResponseT]` or `DataSource[RecordT]`.
4. **Plugin registry separates registration from use** — `@register_class` means `__main__.py` never names a concrete class. Add a new backend: three lines in `dictionaries.py`, zero changes anywhere else.
5. **Singletons matter for memory** — `dict[str, None]` avoids 143,091 empty string allocations vs `dict[str, ""]`. `None` is a singleton; `""` is not guaranteed to be.
6. **Dataclass vs Pydantic boundary** — internal logic uses frozen dataclasses for speed; Pydantic is reserved for API/validation boundaries.
7. **Generator streaming** is the foundation for LLM token streaming, RAG chunk retrieval, and ETL pipeline processing.
8. `pyproject.toml` replaces 5+ config files and is non-negotiable for modern Python.
9. **Dependency injection via Protocol** makes every component independently testable — `MockDictionary` is five lines and no files required.

---

## Related Projects

| Project | Description | Status |
| --- | --- | --- |
| [1099 Reconciliation Pipeline](https://github.com/manuel-reyes-ml/1099_reconciliation_pipeline) | Production ETL pipeline — $15K/yr savings | ✅ Deployed |
| [DataVault Analyst](https://github.com/manuel-reyes-ml/datavault-analyst) | LLM-powered data analytics with Pydantic | Next |
| [PolicyPulse](https://github.com/manuel-reyes-ml/policypulse) | RAG chatbot with ChromaDB | Planned |
| [Learning Journey](https://github.com/manuel-reyes-ml/learning_journey) | Full career transformation documentation | Active |

---

## Author

**Manuel Reyes** — Financial services professional transitioning to Senior LLM Engineer.

- [LinkedIn](https://www.linkedin.com/in/mr410/)
- [GitHub](https://github.com/manuel-reyes-ml)
- [Portfolio](https://manuel-reyes-ml.github.io/learning_journey/)

---

## License

MIT License — see [LICENSE](./LICENSE) for details.