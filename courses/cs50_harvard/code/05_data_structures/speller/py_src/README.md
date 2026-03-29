# CS50 Speller — Production-Grade Python Spell Checker

A Python reimplementation of [CS50's Speller](https://cs50.harvard.edu/x/psets/5/speller/) problem set, built as an installable package with professional software engineering practices. Translates C's manual hash table, linked lists, and memory management into idiomatic Python — demonstrating that fundamentals transfer across languages when you understand the *why*, not just the *how*.

> **Part of:** [Learning Journey](https://github.com/manuel-reyes-ml/learning_journey) — Stage 1 of a 37-month career transformation from financial services to Senior LLM Engineer.

---

## What It Does

Spell-checks a text file against a dictionary and reports misspelled words with performance benchmarks:

```
$ speller texts/austen.txt

MISSPELLED WORDS

Netherfield
Bingley
Longbourn
Meryton
...

WORDS MISSPELLED:     1614
WORDS IN DICTIONARY:  143091
WORDS IN TEXT:        125203
CHECKED FILE:         austen.txt
FILE PATH:            texts/austen.txt
TIME IN load:         0.08
TIME IN check:        0.15
TIME IN size:         0.00
TIME IN TOTAL:        0.23

```

---

## Why This Project Exists

CS50's Speller is a C exercise about hash tables and memory management. This project asks: *what happens when you reimplement it in Python with production standards?*

The answer: every pattern here — Protocol interfaces, frozen dataclasses, generator streaming, context manager timing, `pyproject.toml` packaging — transfers directly to the [7 portfolio projects](https://manuel-reyes-ml.github.io/learning_journey/roadmap.html) in my roadmap. It's not a toy spell checker; it's a training ground for GenAI application architecture.


| Pattern Learned Here                  | Used Next In                              |
| ------------------------------------- | ----------------------------------------- |
| `Protocol` interfaces                 | DataVault (swappable LLM providers)       |
| `@dataclass(frozen=True)` vs Pydantic | DataVault (structured outputs)            |
| Generator streaming (`yield`)         | PolicyPulse (RAG chunk retrieval)         |
| `@contextmanager` timing              | All 7 projects (benchmark pipelines)      |
| `pyproject.toml` packaging            | All 7 projects                            |
| Dependency injection                  | FormSense (swappable extraction backends) |
| `pytest` fixtures                     | All 7 projects (CI/CD via GitHub Actions) |


---

## Architecture

```
src/speller/
├── __init__.py           NullHandler logging + version
├── __main__.py           CLI entry point (composition root)
├── config.py             Constants, enums, path resolution
├── protocols.py          DictionaryProtocol (structural typing)
├── benchmarks.py         timer() context manager + timed() decorator
├── logger.py             ColoredFormatter + configure_logging()
├── dictionaries.py       HashTableDictionary (set-backed, O(1) lookup)
├── text_processor.py     Character-level state machine (generator)
└── speller.py            Orchestrator (dependency injection)

```

### Dependency Chain

```
config.py ──────┐
                ├── No internal imports (bottom of chain)
protocols.py ───┘

benchmarks.py ──── standalone (stdlib only)
logger.py ──────── imports config

dictionaries.py ── imports config
text_processor.py ─ imports config

speller.py ──────── imports protocols, benchmarks, text_processor
__main__.py ─────── imports EVERYTHING (composition root)

```

### Key Design Decisions

**Protocol over ABC** — `speller.py` depends on `DictionaryProtocol`, not `HashTableDictionary`. Swapping to a database-backed or ML-powered dictionary requires zero changes to the orchestrator. The concrete class is injected by `__main__.py`.

**Dataclass over Pydantic** — `BenchmarkResult` and `SpellerResult` are frozen dataclasses (6.5x faster creation, 2.5x less memory than Pydantic). Pydantic is reserved for service boundaries in future projects.

**Generator streaming** — `extract_words()` yields words one at a time via a character-level state machine. No intermediate list, constant memory regardless of file size.

**Context manager timing** — `timer()` wraps code blocks; `timed()` decorator wraps functions. Both produce `BenchmarkResult` dataclasses. `ParamSpec` + `TypeVar` preserve decorated function type signatures.

---

## C → Python Concept Map


| C (dictionary.c / speller.c)        | Python (this project)                     |
| ----------------------------------- | ----------------------------------------- |
| Hash table with linked-list buckets | `set[str]` (built-in hash table)          |
| `#define LENGTH 45`                 | `MAX_WORD_LENGTH: Final[int] = 45`        |
| `malloc` / `free` / `valgrind`      | Garbage collection (automatic)            |
| `struct node`                       | `@dataclass(frozen=True, slots=True)`     |
| Header file (`.h`)                  | `Protocol` class (structural typing)      |
| `getrusage` benchmarking            | `time.perf_counter()` + `@contextmanager` |
| `Makefile`                          | `pyproject.toml` + `pip install -e .`     |
| `argc` / `argv`                     | `argparse` with `nargs='?'`               |
| `fprintf(stderr, ...)`              | `logging` module + `RotatingFileHandler`  |
| `fread` char by char                | `content[pos]` indexing + state machine   |
| `strcasecmp` (case-insensitive)     | `word.lower() in self._words`             |


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
# Default dictionary (dictionaries/large — 143,091 words)
speller texts/cat.txt

# Custom dictionary
speller dictionaries/small texts/cat.txt

# python -m alternative
python -m speller texts/austen.txt

# Verbose mode (DEBUG-level console output)
speller --verbose texts/constitution.txt

# Show misspelled words and save to file
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

# With coverage
pytest --cov=speller

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


| Text File        | Misspelled | Dictionary | Words in Text | Status |
| ---------------- | ---------- | ---------- | ------------- | ------ |
| cat.txt          | 0          | 143,091    | 6             | ✅      |
| constitution.txt | 30         | 143,091    | 7,573         | ✅      |
| carroll.txt      | 295        | 143,091    | 29,758        | ✅      |
| grimm.txt        | 718        | 143,091    | 103,614       | ✅      |
| her.txt          | 767        | 143,091    | 18,402        | ✅      |
| federalist.txt   | 935        | 143,091    | 196,784       | ✅      |
| burnett.txt      | 1,000      | 143,091    | 58,171        | ✅      |
| birdman.txt      | 1,179      | 143,091    | 21,798        | ✅      |
| austen.txt       | 1,614      | 143,091    | 125,203       | ✅      |
| frankenstein.txt | 2,451      | 143,091    | 80,527        | ✅      |
| aca.txt          | 17,062     | 143,091    | 376,904       | ✅      |


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
│       ├── logger.py
│       ├── dictionaries.py
│       ├── text_processor.py
│       └── speller.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_dictionary.py
│   ├── test_text_processor.py
│   └── test_benchmarks.py
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


| Tool                              | Purpose                             |
| --------------------------------- | ----------------------------------- |
| Python 3.11+                      | Language                            |
| `set` (built-in)                  | Hash table dictionary (O(1) lookup) |
| `argparse`                        | CLI argument parsing                |
| `logging` + `RotatingFileHandler` | Structured logging                  |
| `dataclasses`                     | Immutable result containers         |
| `typing.Protocol`                 | Structural typing interfaces        |
| `contextlib.contextmanager`       | Benchmark timing                    |
| `pathlib.Path`                    | File system operations              |
| `pyproject.toml` + `setuptools`   | Package management                  |
| `pytest`                          | Testing framework                   |
| `mypy`                            | Static type checking                |
| `ruff`                            | Linting + formatting                |


---

## What I Learned

Building this project taught me production Python patterns that directly apply to GenAI engineering:

1. **Protocol > ABC** for multi-provider architectures — the same pattern powers swappable LLM backends in my next project (DataVault)
2. **Dataclass vs Pydantic boundary** — internal logic uses frozen dataclasses for speed; Pydantic is reserved for API/validation boundaries
3. **Generator streaming** is the foundation for LLM token streaming, RAG chunk retrieval, and ETL pipeline processing
4. `pyproject.toml` replaces 5+ config files and is non-negotiable for modern Python
5. **Dependency injection via Protocol** makes every component independently testable

---

## Related Projects


| Project                                                                                         | Description                               | Status     |
| ----------------------------------------------------------------------------------------------- | ----------------------------------------- | ---------- |
| [1099 Reconciliation Pipeline](https://github.com/manuel-reyes-ml/1099_reconciliation_pipeline) | Production ETL pipeline — $15K/yr savings | ✅ Deployed |
| [DataVault Analyst](https://github.com/manuel-reyes-ml/datavault-analyst)                       | LLM-powered data analytics with Pydantic  | Next       |
| [PolicyPulse](https://github.com/manuel-reyes-ml/policypulse)                                   | RAG chatbot with ChromaDB                 | Planned    |
| [Learning Journey](https://github.com/manuel-reyes-ml/learning_journey)                         | Full career transformation documentation  | Active     |


---

## Author

**Manuel Reyes** — Financial services professional transitioning to Senior LLM Engineer.

- [LinkedIn](https://www.linkedin.com/in/mr410/)
- [GitHub](https://github.com/manuel-reyes-ml)
- [Portfolio](https://manuel-reyes-ml.github.io/learning_journey/)

---

## License

MIT License — see [LICENSE](https://claude.ai/chat/LICENSE) for details.