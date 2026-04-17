"""Template-string logging formatters for the speller package.

Extends the two-handler strategy from ``logger.py`` with t-string
(PEP 750) awareness.  When a ``Template`` object is passed to a
logger call, these formatters can render it in two ways:

Human-readable (console)
    :class:`TemplateMessageFormatter` renders the ``Template`` exactly
    like an f-string would — colored, timestamped, readable.

Structured JSON (file / observability)
    :class:`JsonTemplateFormatter` extracts every interpolated variable
    into a JSON object alongside the rendered message.  This is the
    pattern used by production observability stacks (Datadog, ELK,
    CloudWatch) where you need both a human summary AND machine-
    parseable fields.

How t-strings work (quick reference)
-------------------------------------
An f-string evaluates immediately to ``str``::

    f"Loaded {count} words"  → "Loaded 143091 words"

A t-string evaluates to a ``Template`` object::

    t"Loaded {count} words"  → Template('Loaded ', Interpolation(value=143091), ' words')

The ``Template`` is iterable.  Each element is either a ``str``
(static text) or an ``Interpolation`` (a variable with its value,
expression text, and format spec — all preserved separately).

This separation is what lets different formatters render the SAME
log call in completely different ways.

Roadmap relevance
-----------------
- DataVault:   structured logging for LLM API calls (tokens, cost, latency as JSON fields)
- PolicyPulse: dual output — console for developer, JSON for observability pipeline
- AFC:         trade execution logs with structured fields for backtesting analysis

References
----------
.. [1] PEP 750 — Template Strings
   https://peps.python.org/pep-0750/
.. [2] PEP 750 Examples — Logging
   https://github.com/t-strings/pep750-examples
"""

# =============================================================================
# IMPORTS
# =============================================================================

from __future__ import annotations

import json
import logging
from logging.handlers import RotatingFileHandler
from typing import Any, Final, override
from string.templatelib import Template, Interpolation

from speller.config import file_dirs, fhandler_config, FileDirectories, FileHandlerConfig


# =============================================================================
# EXPORTS
# =============================================================================

__all__ = [
    "render_message",
    "extract_values",
    "TemplateMessageFormatter",
    "JsonTemplateFormatter",
    "configure_template_logging",
]


# =============================================================================
# INTERNAL HELPER FUNCTIONS
# =============================================================================

def _setup_chandler(
    *,
    level: int,
    formatter: type[logging.Formatter],
) -> logging.StreamHandler:
    """Create and configure a console (stream) logging handler.
 
    Writes to ``sys.stderr`` so log output and program output
    (``stdout``) remain on separate streams and can be redirected
    independently.
 
    Parameters
    ----------
    level : int
        Minimum log level for this handler (e.g. ``logging.INFO``).
        Derived from the ``--verbose`` flag in ``__main__.py``.
    formatter : type[logging.Formatter]
        Formatter class to instantiate.  Pass plain
        ``logging.Formatter`` in tests to suppress ANSI color codes
        from captured output.
 
    Returns
    -------
    logging.StreamHandler
        Fully configured handler ready to add to a logger.
    """ 
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter(
        fmt='%(asctime)s : %(levelname)s : %(message)s',
        datefmt='%H:%M:%S',
    ))
    return console_handler


def _setup_fhandler(
    file_dirs: FileDirectories = file_dirs,
    fhandler_config: FileHandlerConfig = fhandler_config,
) -> RotatingFileHandler:
    """Create and configure a rotating file logging handler.
 
    Always captures ``DEBUG`` level regardless of console verbosity so
    full diagnostic information is available on disk even when the
    console shows only ``INFO``.  Rotates at
    :attr:`~speller.config.FileHandlerConfig.max_log_bytes` and keeps
    :attr:`~speller.config.FileHandlerConfig.BACKUP_COUNT` backups.
 
    Parameters
    ----------
    file_dirs : FileDirectories, optional
        Provides the log file path.  Defaults to the module-level
        singleton from ``config.py``.
    fhandler_config : FileHandlerConfig, optional
        Provides size and rotation settings.  Defaults to the
        module-level singleton from ``config.py``.
 
    Returns
    -------
    RotatingFileHandler
        Fully configured handler ready to add to a logger.
 
    Notes
    -----
    The log directory is created by :func:`configure_logging` before
    this function is called.  Directory creation is a side effect and
    belongs at the call site, not inside a handler factory.
    """
    file_handler = RotatingFileHandler(
        filename=file_dirs.log_file.tlog_path,
        maxBytes=fhandler_config.max_log_bytes,
        backupCount=fhandler_config.BACKUP_COUNT,
        encoding=fhandler_config.ENCODING,
    )
    file_handler.setLevel(logging.DEBUG)
    
    # %(name)s shows module name (speller.main)
    file_handler.setFormatter(JsonTemplateFormatter(
        fmt='%(asctime)s : %(name)s : %(levelname)s : %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
    ))
    return file_handler


# =============================================================================
# CORE FUNCTIONS — Template Processing
# =============================================================================

def render_message(template: Template) -> str:
    """Render a Template as a human-readable string (f-string equivalent).

    Iterates over the Template's parts and reconstructs the final
    string, applying any format specs to interpolated values.

    This replicates what an f-string does automatically — but here
    YOU control the rendering.  The same Template can be rendered
    differently by different functions (this one for humans,
    :func:`extract_values` for machines).

    Parameters
    ----------
    template : Template
        A t-string ``Template`` object from ``string.templatelib``.

    Returns
    -------
    str
        The fully rendered string, identical to what an f-string
        would have produced.

    Examples
    --------
    >>> count = 143091
    >>> render_message(t"Loaded {count} words")
    'Loaded 143091 words'
    >>> render_message(t"Time: {0.1423:.2f}s")
    'Time: 0.14s'
    """
    parts: list[str] = []
    
    for item in template:
        # ─── Structural pattern matching (Python 3.10+) ───
        # match/case is the idiomatic way to process Template parts.
        # Each element is either a str (static text) or an
        # Interpolation (a variable with metadata).
        match item:
            case str() as text:
                # Static text - pass through unchanged
                parts.append(text)
            case Interpolation() as interp:
                # Dynamic value - apply format spec if present
                # interp.value = the actual Python object (int, str, etc.)
                # interp.format_spec = the format string after ':' (e.g. ".2f")
                # interp.expression = the source code text (e.g. "count")
                if interp.format_spec:
                    parts.append(format(interp.value, interp.format_spec))
                else:
                    parts.append(str(interp.value))
    
    return "".join(parts)

# Here's the problem: when someone writes t"Time: {elapsed:.2f}s", the Template stores:
#   interp.value → the raw float, e.g. 0.1423
#   interp.format_spec → the string ".2f"
# These are separate — the Template preserves them independently so you can process each
# before combining.
#
# But you can't write f"{interp.value:interp.format_spec}" (f-strings don't allow dynamic format
# specs like that). You need a function that takes a value and a format spec as separate arguments
# and returns the formatted string.
# That function is format(). It's the runtime equivalent of f-string formatting.
#
# format() is the visible piece of a trio most Python developers don't realize are connected:
#   f"{value:.2f}"           ←  syntax sugar
#   format(value, ".2f")     ←  the function
#   value.__format__(".2f")  ←  the dunder method underneath
# All three produce the exact same result. The first calls the second, which calls the third.


def extract_values(template: Template) -> dict[str, Any]:
    """Extract interpolated values from a Template as a dictionary.

    Pulls out every ``Interpolation`` and maps its source expression
    to its runtime value.  This is the machine-readable counterpart
    to :func:`render_message`.

    Parameters
    ----------
    template : Template
        A t-string ``Template`` object.

    Returns
    -------
    dict of {str : Any}
        Mapping of expression text to runtime value.
        Example: ``{"count": 143091, "path": "dictionaries/large"}``

    Examples
    --------
    >>> count = 143091
    >>> extract_values(t"Loaded {count} words")
    {'count': 143091}
    """
    values: dict[str, Any] = {}
    
    for item in template:
        match item:
            case Interpolation() as interp:
                #interp.expression is the source text: "count", "path.name", etc.
                values[interp.expression] = interp.value
                
    return values


# =============================================================================
# CUSTOM FORMATTER CLASSES
# =============================================================================

class TemplateMessageFormatter(logging.Formatter):
    """Formatter that renders Template objects as colored human text.

    Extends the same pattern as :class:`~speller.logger.ColoredFormatter`
    but adds Template awareness.  When ``record.msg`` is a ``Template``,
    it renders it via :func:`render_message` before the parent formats
    the timestamp and level.

    When ``record.msg`` is a plain ``str`` (normal log call), it falls
    through to standard ``Formatter`` behavior — fully backward compatible.

    Attributes
    ----------
    COLORS : dict of {int : str}
        ANSI color codes per log level (same as ColoredFormatter).
    RESET : str
        ANSI reset code.
    """
    
    COLORS: Final[dict[int, str]] = {
        logging.DEBUG:    "\033[90m",    # Gray
        logging.INFO:     "\033[92m",    # Green
        logging.WARNING:  "\033[93m",    # Yellow
        logging.ERROR:    "\033[91m",    # Red
        logging.CRITICAL: "\033[1;91m",  # Bold Red
    }
    RESET: Final[str] = "\033[0m"
    
    # Override the parent's format method
    # Apply override decorator to a subclass method that overrides a base class method.
    # Static type checkers will warn if the base class is modified such that the overridden method
    # no longer exists — avoiding accidentally turning a method override into dead code.
    @override
    def format(self, record: logging.LogRecord) -> str:
        """Format a log record, rendering any Template to human text.

        The key insight: ``record.msg`` holds whatever was passed to
        ``logger.info()``.  If it's a Template, we render it BEFORE
        the parent class calls ``getMessage()`` (which would just
        call ``str()`` on it and lose the structured data).

        Parameters
        ----------
        record : logging.LogRecord
            The log record to format.

        Returns
        -------
        str
            Colored, human-readable log line.
        """
        # ─── Template-aware rendering ───
        # Check if the message is a Template BEFORE the parent processes it.
        # This is the interception point that t-strings enable.
        # If msg is a Template, render it into a local variable instead of
        # overwriting record.msg. Mutating the record breaks downstream
        # handlers — they all receive the SAME LogRecord instance.
        if isinstance(record.msg, Template):
            rendered = render_message(record.msg)
            
            # Build a shallow copy of the record with the rendered message,
            # leaving the original intact for other handlers
            #
            # --- Why logging.makeLogRecord(record.__dict__) works ---
            # This is a Python logging idiom worth adding to your toolkit. makeLogRecord() is a stdlib
            # helper that creates a fresh LogRecord from a dictionary of attributes. Passing
            # record.__dict__ gives you a shallow copy with all the same metadata (level, timestamp,
            # logger name, etc.) but as a separate object — so mutating it doesn't leak to other handlers.
            # Think of it the same way you already think about dataclasses.replace() in your __main__.py
            record = logging.makeLogRecord(record.__dict__)
            record.msg = rendered
            record.args = None # Clear args - already rendered
            
        color = self.COLORS.get(record.levelno, self.RESET)
        message = super().format(record)
        return f"{color}{message}{self.RESET}"
    
    
class JsonTemplateFormatter(logging.Formatter):
    """Formatter that renders Template objects as structured JSON.

    When ``record.msg`` is a ``Template``, produces a single JSON line
    containing:

    - ``timestamp`` — ISO-format time
    - ``level`` — log level name
    - ``module`` — logger name (e.g. ``speller.load_dictionary``)
    - ``message`` — human-readable rendered text
    - ``values`` — dict of every interpolated variable and its value

    This is the format consumed by log aggregation tools (ELK, Datadog,
    CloudWatch Logs Insights).  Each interpolated variable becomes a
    searchable, filterable field.

    When ``record.msg`` is a plain ``str``, falls back to a simple
    JSON structure with just ``message`` (no ``values``).

    Examples
    --------
    Given::

        count = 143091
        logger.info(t"Dictionary loaded: {count} words")

    Console handler (TemplateMessageFormatter) outputs::

        14:30:45 : INFO : Dictionary loaded: 143091 words

    File handler (JsonTemplateFormatter) outputs::

        {"timestamp": "2026-04-15 14:30:45", "level": "INFO",
         "module": "speller.load_dictionary",
         "message": "Dictionary loaded: 143091 words",
         "values": {"count": 143091}}
    """
    
    # Override the parent's format method
    # Apply override decorator to a subclass method that overrides a base class method.
    # Static type checkers will warn if the base class is modified such that the overridden method
    # no longer exists — avoiding accidentally turning a method override into dead code.
    @override
    def format(self, record: logging.LogRecord) -> str:
        """Format a log record as a JSON line.

        Parameters
        ----------
        record : logging.LogRecord
            The log record to format.

        Returns
        -------
        str
            Single-line JSON string.
        """
        log_entry: dict[str, Any] = {
            "timestamp": self.formatTime(record, datefmt="%Y-%m-%d %H:%M:%S"),
            "level": record.levelname,
            "module": record.name,
        }
        
        if isinstance(record.msg, Template):
            log_entry["message"] = render_message(record.msg)
            log_entry["values"] = extract_values(record.msg)
            # No mutation — we just READ from record.msg
            # record.args = None
        else:
            # Fallback for plain string log calls - backward compatible
            log_entry["message"] = record.getMessage()
            
        return json.dumps(log_entry)


# =============================================================================
# CONFIGURATION FUNCTION
# =============================================================================

def configure_template_logging(
    *,
    console_verbose: bool = False,
    log_to_file: bool = True,
    custom_console: bool = True,
) -> None:
    """Configure logging with template-aware formatters.

    Drop-in replacement for :func:`~speller.logger.configure_logging`
    that uses :class:`TemplateMessageFormatter` for console and
    :class:`JsonTemplateFormatter` for file output.

    Both formatters are backward compatible — plain ``str`` log
    messages work exactly as before.  Only ``Template`` messages
    get the enhanced dual rendering.

    Parameters
    ----------
    console_verbose : bool, optional
        ``True`` sets console to DEBUG.  ``False`` (default) shows INFO+.
    log_to_file : bool, optional
        ``True`` (default) writes structured JSON to disk.
    """
    # 1. Grab the top-level logger for the package
    # CUR_DIR.name gives the current directory in string "speller"
    package_logger = logging.getLogger(file_dirs.CUR_DIR.name)
    package_logger.setLevel(logging.DEBUG)  # Let handlers decide their own level
    
    # 2. Prevent duplicate handlers if this function is called multiple times
    if package_logger.hasHandlers():
        package_logger.handlers.clear()
        
    # 3. Console handler: colored human-readable output, respected the 'level' parameter
    level = logging.DEBUG if console_verbose else fhandler_config.LEVEL_DEFAULT
    formatter = TemplateMessageFormatter if custom_console else logging.Formatter
    
    console_handler = _setup_chandler(level=level, formatter=formatter)
    package_logger.addHandler(console_handler)
    
    # 4. File handler - structured JSON output -  always captures DEBUG
    if log_to_file:
        # parents=True: create any missing parent directories
        # exist_ok=True: no error if directory already exists
        file_dirs.LOG_DIR.mkdir(parents=True, exist_ok=True)
        
        file_handler = _setup_fhandler()
        package_logger.addHandler(file_handler)
        
    # 5. When 'False' - prevents logs from bubbling up to Python's default root logger
    # (prevents duplicate printing in some environments).    
    package_logger.propagate = True
    
    
# =============================================================================
# REFERENCE GUIDES
# =============================================================================
# =====================================================
# Python format() Spec Mini-Language
# =====================================================

# The format_spec string passed to format(value, spec) — or written after
# the colon in f-strings and t-strings — follows this grammar:
#
#   [[fill]align][sign][#][0][width][,][.precision][type]
#
# Every field is optional. Build from right to left: start with the type,
# then add precision, width, alignment, padding as needed.


# =====================================================
# FLOATS — precision and fixed-point
# =====================================================

# format(0.1423, ".2f")           → "0.14"           fixed-point, 2 decimals
# format(0.1, ".4f")              → "0.1000"         trailing zeros preserved
# format(3.14159, ".0f")          → "3"              no decimals (rounded)
# format(143091.5, ",.2f")        → "143,091.50"     thousands separator + decimals
# format(0.000001234, ".3e")      → "1.234e-06"      scientific notation
# format(0.85, ".1%")             → "85.0%"          percentage (×100 + %)

# Your existing usage:
#   f"{self.elapsed_seconds:.2f}s"           → "0.14s"
#   f"{result.time_total:.4f}"               → "0.2010"


# =====================================================
# INTEGERS — padding, bases, separators
# =====================================================

# format(42, "d")                 → "42"             decimal (default for int)
# format(42, "05d")               → "00042"          zero-pad to width 5
# format(143091, ",")             → "143,091"        thousands separator
# format(255, "x")                → "ff"             hexadecimal (lowercase)
# format(255, "X")                → "FF"             hexadecimal (uppercase)
# format(255, "#x")               → "0xff"           hex with prefix
# format(8, "b")                  → "1000"           binary
# format(8, "08b")                → "00001000"       binary, zero-padded to 8
# format(64, "o")                 → "100"            octal


# =====================================================
# STRINGS — alignment and width
# =====================================================

# format("hi", "<10")             → "hi        "     left-align, width 10
# format("hi", ">10")             → "        hi"    right-align, width 10
# format("hi", "^10")             → "    hi    "    center, width 10
# format("hi", "*^10")            → "****hi****"    center with fill char '*'
# format("hi", ".3")              → "hi"             max width 3 (truncation)
# format("hello world", ".5")     → "hello"          truncate to 5 chars

# Your existing usage:
#   f"{'WORDS MISSPELLED':<22}"              → "WORDS MISSPELLED      "
#   f"{'TIME IN load':<22}{elapsed:.2f}"     → "TIME IN load          0.14"


# =====================================================
# SIGN CONTROL
# =====================================================

# format(42, "+d")                → "+42"            always show sign
# format(-42, "+d")               → "-42"            negative sign shown
# format(42, " d")                → " 42"            space for positive, "-" for negative
# format(-42, " d")               → "-42"


# =====================================================
# ALIGNMENT CHARACTERS
# =====================================================

# <   left-align       (default for strings)
# >   right-align      (default for numbers)
# ^   center
# =   pad AFTER the sign, before the digits — useful for "+0000042"


# =====================================================
# COMMON PATTERNS IN PRODUCTION LOGGING
# =====================================================

# Timing:             f"{elapsed:.2f}s"               → "0.14s"
# Byte counts:        f"{n_bytes:,} bytes"            → "143,091 bytes"
# Percentages:        f"{accuracy:.1%}"               → "94.3%"
# Table columns:      f"{label:<20}{value:>10}"       → "WORDS MISSPELLED              30"
# Progress:           f"{done:>3}/{total}"            → " 42/100"
# IDs (zero-padded):  f"{user_id:08d}"                → "00001234"
# Memory in MB:       f"{bytes / 1024**2:.2f} MB"     → "5.25 MB"


# =====================================================
# NESTED FIELDS — width/precision from variables
# =====================================================

# Width and precision can come from nested expressions:
#
#   width = 10
#   value = 3.14159
#   f"{value:>{width}.2f}"          → "      3.14"
#   format(value, f">{width}.2f")   → "      3.14"
#
# This is exactly what render_message() does internally — at runtime it
# assembles the spec string from Interpolation.format_spec and applies it
# via format(). The mechanism is the same; only the call site differs.


# =====================================================
# CUSTOM __format__ — YOUR OWN FORMAT SPECS
# =====================================================

# Any class can implement __format__(self, spec) to respond to custom specs:
#
#   @dataclass(frozen=True, slots=True)
#   class BenchmarkResult:
#       operation: str
#       elapsed_seconds: float
#
#       def __format__(self, spec: str) -> str:
#           if spec == "json":
#               return f'{{"op": "{self.operation}", "s": {self.elapsed_seconds}}}'
#           if spec == "short":
#               return f"{self.operation[:4]}:{self.elapsed_seconds:.1f}s"
#           return str(self)      # default → delegates to __str__
#
#   format(result, "json")          → '{"op": "load", "s": 0.14}'
#   format(result, "short")         → "load:0.1s"
#   f"{result}"                     → "load: 0.14s"        (empty spec → __str__)
#
# This is the same pattern datetime uses: f"{now:%Y-%m-%d}" works because
# datetime.__format__ parses the strftime codes. Worth knowing for Stage 2+
# when you build LLMResponse, RetrievalResult, and TradeSignal dataclasses.


# =====================================================
# DECISION TABLE — WHEN TO USE WHICH
# =====================================================

# ┌─────────────────────────────┬────────────────────────────────────────┐
# │ Situation                    │ Use                                    │
# │──────────────────────────────┼────────────────────────────────────────│
# │ Spec is known at write time  │ f-string:    f"{x:.2f}"                │
# │ Spec comes from a variable   │ format():    format(x, spec)           │
# │ Spec stored in a data struct │ format():    format(x, config.fmt)     │
# │ Need to delegate to a method │ format():    format(x, custom_spec)    │
# │ Processing Template objects  │ format():    interp.value + .format_spec│
# │ No custom formatting needed  │ str():       str(x)                    │
# └─────────────────────────────┴────────────────────────────────────────┘


# =====================================================
# REFERENCES
# =====================================================
# Python Docs — Format Specification Mini-Language:
#   https://docs.python.org/3/library/string.html#format-specification-mini-language
# Python Docs — format() built-in:
#   https://docs.python.org/3/library/functions.html#format
# PyFormat — visual cheatsheet:
#   https://pyformat.info/


# =============================================================================
# REFERENCE GUIDE — LogRecord ATTRIBUTES
# =============================================================================
#
# A LogRecord holds ALL context about a single log event. Python creates one
# automatically every time you call logger.info(), logger.debug(), etc., and
# passes it to every handler attached to the logger.
#
# Formatters read these attributes via %(name)s placeholders in their format
# string, OR via record.name attribute access in custom formatters like yours.
#
# The list below is exhaustive — most code uses only 5-6 of these.


# =====================================================
# CORE MESSAGE ATTRIBUTES (what you log)
# =====================================================

# record.msg           → The raw message object passed to logger.info/debug/etc.
#                        Normally a str, but can be ANY object (Template, dict,
#                        custom class). This is what your formatter inspects
#                        with isinstance(record.msg, Template).
#                        Format spec: %(msg)s  (rare — usually use %(message)s)

# record.args          → Arguments passed AFTER the message for %-style
#                        formatting. For logger.info("x=%s", 42), args is (42,).
#                        For logger.info("plain msg"), args is None.
#                        Format spec: not directly accessible — merged into message.

# record.message       → The FINAL rendered message (msg % args).
#                        Computed lazily — only exists after record.getMessage()
#                        or formatter.format() is called. This is what you
#                        USUALLY want in format strings.
#                        Format spec: %(message)s


# =====================================================
# LEVEL / SEVERITY ATTRIBUTES
# =====================================================

# record.levelname     → Human-readable level name: "DEBUG", "INFO", "WARNING",
#                        "ERROR", "CRITICAL".
#                        Format spec: %(levelname)s
#                        Your code: record.levelname (in JsonTemplateFormatter)

# record.levelno       → Integer level value: 10, 20, 30, 40, 50.
#                        Used for comparisons (record.levelno >= logging.WARNING).
#                        Format spec: %(levelno)d
#                        Your code: record.levelno (in ColoredFormatter.COLORS.get)


# =====================================================
# LOGGER IDENTITY ATTRIBUTES
# =====================================================

# record.name          → Logger name (usually __name__ of the module that logged).
#                        Example: "speller.load_dictionary"
#                        Format spec: %(name)s
#                        Your code: record.name (in JsonTemplateFormatter)


# =====================================================
# SOURCE LOCATION ATTRIBUTES (where the log came from)
# =====================================================

# record.pathname      → Full file path where the log call occurred.
#                        Example: "/home/manuel/speller/load_dictionary.py"
#                        Format spec: %(pathname)s

# record.filename      → Basename of pathname (just the filename).
#                        Example: "load_dictionary.py"
#                        Format spec: %(filename)s

# record.module        → Module name without extension.
#                        Example: "load_dictionary"
#                        Format spec: %(module)s

# record.funcName      → Name of the function that issued the log call.
#                        Example: "load_dictionary"
#                        Format spec: %(funcName)s

# record.lineno        → Line number in the source file.
#                        Example: 142
#                        Format spec: %(lineno)d


# =====================================================
# TIMING ATTRIBUTES
# =====================================================

# record.created       → Unix timestamp when LogRecord was created.
#                        float, e.g. 1713369045.123 — seconds since epoch.
#                        Format spec: %(created)f

# record.asctime       → Human-readable timestamp string.
#                        Example: "2026-04-17 14:30:45,123"
#                        Only populated AFTER formatter.formatTime() is called.
#                        Format spec: %(asctime)s
#                        Your code: self.formatTime(record, datefmt=...) in JsonTemplateFormatter

# record.msecs         → Millisecond portion of created (0-999).
#                        Format spec: %(msecs)d

# record.relativeCreated → Milliseconds since the logging module was loaded.
#                          Useful for relative timing in a single run.
#                          Format spec: %(relativeCreated)d


# =====================================================
# PROCESS / THREAD ATTRIBUTES (concurrency context)
# =====================================================

# record.process       → Process ID (PID) that created the record.
#                        Format spec: %(process)d

# record.processName   → Process name from multiprocessing module.
#                        Format spec: %(processName)s

# record.thread        → Thread ID (integer).
#                        Format spec: %(thread)d

# record.threadName    → Thread name (e.g. "MainThread").
#                        Format spec: %(threadName)s

# record.taskName      → asyncio task name (Python 3.12+).
#                        Format spec: %(taskName)s


# =====================================================
# EXCEPTION ATTRIBUTES (populated only when logging an exception)
# =====================================================

# record.exc_info      → Tuple of (exc_type, exc_value, traceback) OR None.
#                        Populated by logger.exception() or logger.error(exc_info=True).

# record.exc_text      → Cached formatted traceback string. Starts as None,
#                        filled in by formatter.formatException() on first call.

# record.stack_info    → Stack frame info as a string, for logger.xxx(stack_info=True).


# =====================================================
# EXTRA FIELDS (custom context injection)
# =====================================================

# Any keys you pass via the 'extra' dict become direct attributes of the record:
#
#     logger.info("User action", extra={"user_id": 42, "ip": "10.0.0.1"})
#
# Inside a formatter, you access them like any other attribute:
#     record.user_id   # → 42
#     record.ip        # → "10.0.0.1"
#
# This is the OFFICIAL way to add structured fields to log records WITHOUT
# t-strings. T-strings let you avoid the 'extra' dance by extracting
# interpolated variables automatically.


# =====================================================
# THE ATTRIBUTES YOU'LL ACTUALLY USE
# =====================================================

# In 90% of custom formatters, you read only these SIX:
#
#     record.msg         ← the raw message (Template, str, dict, etc.)
#     record.args        ← args for %-formatting
#     record.levelname   ← "INFO", "ERROR", etc.
#     record.levelno     ← integer level for comparisons
#     record.name        ← "speller.load_dictionary"
#     record.exc_info    ← exception tuple or None
#
# Plus ONE method call:
#     self.formatTime(record, datefmt=...)   ← produces record.asctime


# =====================================================
# HOW YOUR CODE USES THEM
# =====================================================

# TemplateMessageFormatter:
#   record.msg       → checked isinstance(msg, Template)
#   record.levelno   → looked up in COLORS dict
#   super().format() → reads msg, args, levelname, asctime internally
#
# JsonTemplateFormatter:
#   record.msg       → checked isinstance(msg, Template)
#   record.levelname → copied into JSON "level" field
#   record.name      → copied into JSON "module" field
#   self.formatTime  → produces "timestamp" field
#
# ColoredFormatter (logger.py):
#   record.levelno   → looked up in COLORS dict
#   super().format() → reads msg, args, levelname, asctime internally


# =====================================================
# INSPECTING ALL ATTRIBUTES ON A LIVE RECORD
# =====================================================

# For debugging your formatter, dump all attributes with:
#
#     def format(self, record: logging.LogRecord) -> str:
#         import pprint
#         pprint.pprint(record.__dict__)   # Shows EVERY attribute
#         ...
#
# This is the same trick that powers logging.makeLogRecord(record.__dict__) —
# every attribute lives in the record's __dict__, so you can inspect or copy
# the entire state with standard dict operations.


# =====================================================
# REFERENCES
# =====================================================
# Python Docs — LogRecord attributes table:
#   https://docs.python.org/3/library/logging.html#logrecord-attributes
# Python Docs — LogRecord class:
#   https://docs.python.org/3/library/logging.html#logrecord-objects