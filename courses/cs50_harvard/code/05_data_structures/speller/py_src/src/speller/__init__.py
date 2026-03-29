"""speller — production-grade Python spell-checker.
 
A re-implementation of CS50\'s ``speller.c`` in idiomatic Python,
applying production engineering patterns from day one: type hints,
frozen dataclasses, structured logging, Protocol-based dependency
injection, ABC Template Method, and a plugin registry for swappable
dictionary backends.
 
Usage
-----
CLI::
 
    python -m speller [dictionary] text
    python -m speller --verbose texts/austen.txt
    python -m speller -o hash sorted texts/austen.txt
 
Programmatic::
 
    from speller.speller import run_speller
    from speller.dictionaries import HashTableDictionary
 
    result = run_speller(
        dictionary=HashTableDictionary(),
        text_path="texts/cat.txt",
        dict_path="dictionaries/large",
    )
    print(result.words_misspelled)
 
Package layout
--------------
::
 
    speller/
    ├── __init__.py        ← you are here; triggers backend registration
    ├── __main__.py        ← CLI entry point (composition root)
    ├── config.py          ← constants, enums (no internal imports)
    ├── protocols.py       ← DictionaryProtocol (no internal imports)
    ├── benchmarks.py      ← timer(), timed(), BenchmarkResult
    ├── register.py        ← DictInfo, dicts registry, register_class()
    ├── dictionaries.py    ← _BaseDictionary ABC + concrete backends
    ├── text_processor.py  ← extract_words() generator
    ├── speller.py         ← run_speller() orchestrator
    └── logger.py          ← configure_logging(), ColoredFormatter
 
Roadmap relevance
-----------------
Stage 1 capstone.  The patterns here — Protocol DI, frozen result
dataclasses, registry decorators, ``@contextmanager`` timer, and
``Generic[T]`` base classes — carry forward unchanged into DataVault,
PolicyPulse, FormSense, and AFC.
"""
# Adding public API exports makes the package more professional

from __future__ import annotations

import logging


# Library logging pattern: stay silent unless the application configures
# logging. The CLI entry point (__main__.py) calls configure_logging() to
# acivate console/file handlers.
logging.getLogger(__name__).addHandler(logging.NullHandler())

# Package metadata
__version__ = "1.0.0"


# Trigger backend registration. Any import of the package guarantees
# all @register_class decorators have run.
#
# The as _dicts_module form is just a way of being explicit about your
# intent. It tellsthe next developer (or future you):
#
# "I imported this for its side effects only. I am not going to call _dicts_module.anything().
# The leading underscore means: don't touch this."
from speller import dictionaries as _dicts_module  # noqa: F401

# The # noqa: F401 comment tells ruff/flake8 "yes, I know I didn't use this
#import — it's intentional." This is a well-known Python pattern for plugin registration.


# __init__.py (runs on import)     → "What does this package OFFER to other code?"
# __main__.py (runs on execution)  → "What happens when someone RUNS this package from the terminal?"

# No ImportError sys.exit() on __init__.py because it kills any progrsam that imports the package


# =============================================================================
# THE UNDERSCORE CONVENTION
# =============================================================================

# _x = "internal variable"       # don't use outside this module
# __x = "name-mangled"           # don't use outside this class
# _MyClass                       # internal class
# _helper_function()             # internal function
# import something as _something # imported for side effects only
