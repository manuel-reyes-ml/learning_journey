"""CLI entry point for the speller package.

Runs when the user executes::

    $ python -m speller [dictionary] text
    $ speller [dictionary] text          (via pyproject.toml scripts)

This module is the COMPOSITION ROOT — the single place that:
1. Parses CLI arguments
2. Configures logging (before any speller logic runs)
3. Creates concrete implementations (HashTableDictionary)
4. Injects them into the orchestrator (run_speller)
5. Handles display and exit codes

No other module imports from __main__.py. This module imports
from everything else. It's the top of the dependency chain.

Dependency Chain (complete picture)
------------------------------------
    config.py            ← constants, enums (bottom — no internal imports)
    protocols.py         ← DictionaryProtocol (bottom — no internal imports)
    benchmarks.py        ← timer, timed, BenchmarkResult (imports nothing internal)
    logger.py            ← config_logging, ColoredFormatter (imports config)
    dictionary.py        ← HashTableDictionary (imports config)
    text_processor.py    ← extract_words (imports config)
    speller.py           ← run_speller, SpellerResult (imports protocols, benchmarks, text_processor)
    __main__.py          ← THIS FILE (imports everything — composition root)

CS50 CLI Behavior
------------------
Matches speller.c usage::

    Usage: ./speller [DICTIONARY] text

    argc == 2:  dictionary defaults to dictionaries/large, argv[1] is text
    argc == 3:  argv[1] is dictionary, argv[2] is text
    otherwise:  print usage and exit with code 1
"""

# =============================================================================
# IMPORTS
# =============================================================================

from __future__ import annotations

import sys


# =====================================================
# Import Guard
# =====================================================

# __main__.py is the FRONT DOOR — if imports fail, give a friendly
# error message and exit. This is the ONE place where sys.exit()
# on ImportError is correct, because the user explicitly ran the
# program and expects it to either work or explain why it can't.
#
# Every other module lets ImportError propagate upward to here.
try:
    from collections import defaultdict
    from dataclasses import replace, dataclass, KW_ONLY
    from importlib.resources.abc import Traversable
    from pathlib import Path
    import argparse
    import logging
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table
    import string
    from typing import Final, TypedDict, Required, NotRequired
    
    from speller.benchmarks import BenchmarkResult
    from speller.config import ExitCode, file_dirs, default_fnames
    from speller.load_dictionary import load_dictionary
    from speller.logger import configure_logging
    from speller.register import dicts
    from speller.speller import run_speller, Report, SpellerResult, get_console
    
except ImportError as e:
    sys.exit(f"Error missing speller module.\nDetails: {e}")
    

# =============================================================================
# LOGGER SETUP
# =============================================================================

# Logger is created here but NOT configured yet.
# config_logging() is called INSIDE main() after argparse determines
# the verbosity level. This ensures --verbose flag controls log output
logger = logging.getLogger(__name__)

console: Console = get_console()


# =============================================================================
# MODULE CONFIGURATION
# =============================================================================
# =====================================================
# Constants
# =====================================================

ops_list: Final[str] = ", ".join(dicts.keys())

# Sentinel for `--dir` flag passed without a value. A unique singleton
# object — comparison with `is` is unambiguous (PEP 661 pattern).
# Cannot be confused with any user-supplied Path or with None.
_USE_BUNDLED_DIR: Final = object()


# =====================================================
# Class Constants Configuration
# =====================================================

class FileErrorData(TypedDict, total=False):
    """Typed mapping for per-batch file error tracking.

    Uses ``TypedDict`` with ``Required`` / ``NotRequired`` to enforce
    that both error lists must always be present while ``error_other``
    is optional.  Populated via a ``defaultdict(list)`` in ``main()``
    and read when constructing :class:`GeneralReport`.

    Fields
    ------
    error_decode : list of str
        Filenames that raised :exc:`UnicodeDecodeError` during text
        extraction.  Required — always present, may be empty.
    error_empty : list of str
        Filenames that contained no extractable words (empty files or
        files with only digits/punctuation).  Required — always present,
        may be empty.
    error_other : list of str, optional
        Filenames that raised an unexpected :exc:`Exception`.  Not
        required — omitted when no unexpected errors occurred.
    """
    
    error_decode: Required[list[str]]
    error_empty: Required[list[str]]
    error_other: NotRequired[list[str]]
    

# =====================================================
# Frozen Dataclass
# ===================================================== 

# SpellerArgs is a CLI-layer concern-it represents parsed
# command-line arguments and belongs here.
#
# frozen=True makes instances immutable.
@dataclass(frozen=True)
class SpellerArgs:
    """Typed container for parsed CLI arguments.

    Converts ``argparse.Namespace`` — whose attributes are typed as
    ``Any`` — into a fully typed, immutable dataclass.  This gives
    Pyright complete static coverage for all ``args.*`` accesses in
    ``main()`` and helper functions, catching typos and type mismatches
    at analysis time rather than runtime.

    ``frozen=True`` prevents accidental mutation after construction.
    Constructed once in ``main()`` immediately after ``parse_args()``;
    passed by value to helper functions.

    Attributes
    ----------
    text : str or None
        Path to a single text file.  ``None`` when only ``--dir``
        is provided.
    dictionary : str
        Path to the dictionary file.  Defaults to
        ``dictionaries/large`` when omitted from the CLI.
    operations : list of str
        Validated backend operation names (e.g. ``["hash", "sorted"]``).
        Defaults to ``["hash"]``.
    directory : Path or None
        Directory to glob for ``.txt`` files.  ``None`` when
        ``--dir`` is not provided.
    verbose : bool
        ``True`` enables ``DEBUG``-level console logging.
    no_log_file : bool
        ``True`` disables the rotating file handler.
    show_misspelled : bool
        ``True`` writes misspelled words to ``misspelled/`` directory.

    Notes
    -----
    This is the typed-dataclass CLI args pattern described in the
    ``argparse.Namespace`` reference at the bottom of this module.
    The same pattern applies to every future project's CLI layer:
    ``DataVaultArgs``, ``PolicyPulseArgs``, ``FormSenseArgs``.
    """
    
    text: str | None
    dictionary: str
    operations: list[str]
    directory: Path | Traversable | None
    demo: bool
    verbose: bool
    no_log_file: bool
    show_misspelled: bool
    no_custom_console: bool
    template_logging: bool
    structured_logging: bool
    table_report: bool


# frozen=True makes instances immutable.
# slots=True prevents dynamic attribute creation and
# reduces memory fooprint.
# Together they create a truly locked-down data container.
@dataclass(frozen=True, slots=True)
class GeneralReport:
    """Immutable summary of a complete batch spell-check run.

    Aggregates file-level statistics across all text files processed
    in a single ``main()`` invocation.  ``frozen=True`` prevents
    accidental mutation after construction; ``slots=True`` reduces
    memory footprint.

    Constructed once at the end of ``main()`` after all text files
    have been processed.  The same result-container pattern used by
    :class:`~speller.speller.SpellerResult` — compute all data first,
    then display via :meth:`format_general_report`.

    Attributes
    ----------
    files_not_found : int
        Count of text paths that did not exist on disk.
    files_in_dir : int
        Total number of ``.txt`` files resolved for the batch
        (single file + directory glob, deduplicated).
    files_with_error : FileErrorData
        Categorised error lists keyed by error type.  See
        :class:`FileErrorData` for field details.

    Notes
    -----
    The same frozen-result-dataclass pattern applies to every future
    project:

    - DataVault:   ``AnalysisReport`` (token usage, latency, error counts)
    - PolicyPulse: ``RAGBatchReport`` (retrieval counts, RAGAS scores)
    - AFC:         ``BacktestReport`` (trade counts, drawdown, Sharpe)
    """
    
    # Required fields (no default) must come first
    # Optional fields with defaults afterwards
    _: KW_ONLY  # Everything after is keyword-only
    files_not_found: int
    files_in_dir: int
    files_with_error: FileErrorData
    
    def format_general_report(self) -> str:
        """Format the batch summary into a human-readable report string.

        Builds a fixed-width text report aligned to match the
        :meth:`~speller.speller.SpellerResult.format_report` style.
        Returns a string rather than printing directly so the caller
        decides the output destination (stdout, log file, test assertion).

        Returns
        -------
        str
            Multi-line report including a ``GENERAL REPORT`` header,
            file counts, and the full :class:`FileErrorData` breakdown.

        Notes
        -----
        Command-query separation: this method *queries* the data and
        returns a string.  :func:`_print_reports` is the *command* that
        decides to print it.  The same separation applies to
        :meth:`~speller.speller.SpellerResult.format_report`.
        """
        lines: list[str] = []
        
        # Header
        lines.append("\n")
        lines.append("[bold blue]" + "=" * 80 + "[/bold blue]")
        lines.append("[bold blue]GENERAL REPORT[bold blue]")
        lines.append("[bold blue]" + "=" * 80 + "[/bold blue]")
        
        # Color choice - red if error, green if clean run
        has_errors = (
            self.files_not_found > 0
            or any(self.files_with_error.values())
        )
        summary_color = "red" if has_errors else "green"
        
        # Statistics
        lines.append("\n")
        lines.append(
            f"[blue]{'FILES NOT FOUND':<22}[/blue]"
            f"[bold {summary_color}]{self.files_not_found}[/bold {summary_color}]"
        )
        lines.append(f"[blue]{'FILES IN DIRECTORY:':<22}[/blue][bold]{self.files_in_dir}[/bold]")
        lines.append(
            f"[blue]{'FILES WITH ERROR:':<22}[/blue]"
            f"[bold {summary_color}]{self.files_with_error}[/bold {summary_color}]"
        )
        lines.append("\n")
        
        return "\n".join(lines)
    
    
    # Note the return type changed from str to Table. console.print(table) knows how to
    # render it automatically. This is the beauty of rich's architecture — any object that
    # follows the Console Protocol (tables, panels, trees, markdown, syntax-highlighted code)
    # can be passed to console.print().
    def format_table(self) -> Table:
        """
        """
        table = Table(
            show_header=True,
            box=None,  # no borders for a clean look
            padding=(0, 2),
        )
        table.add_column(style="blue")
        table.add_column(style="bold")
        
        table.add_row("FILES NOT FOUND:", str(self.files_not_found))
        table.add_row("FILES IN DIRECTORY:", str(self.files_in_dir))
        
        # Error categories - one row per non-empty category, colored red
        for category, filenames in self.files_with_error.items():
            if filenames and isinstance(filenames, list):
                table.add_row(
                    f"[red]{category.upper()}:[/red]",
                    f"[red]{', '.join(filenames)}[/red]",
                )
        
        table.add_row()
            
        return table
    
    
    def __rich__(self) -> Table:
        """Rich Console Protocol hook — called by console.print(report)."""
        return self.format_table()
    
    # Why this design respects your existing architecture
    # Your current code uses command-query separation — format_report() queries the data and
    # returns a string; the caller (_print_reports()) commands what to do with it. This is the
    # right pattern, and rich fits into it cleanly:
    #   - Data layer (SpellerResult) — unchanged, still frozen dataclass
    #   - Formatting layer (format_report()) — now emits markup instead of plain text
    #   - Rendering layer (_print_reports() + console.print()) — interprets markup and outputs colored text
    # A test could still assert on the REPORT.main string, because markup tags are just regular string
    #
    # characters until rendered. That preserves your test suite's independence from ANSI codes. 


# =============================================================================
# INTERNAL HELPER FUNCTIONS
# =============================================================================

# Extracting parser construction into its own function means tests can parse
# arguments without running the full program.
def _build_parser() -> argparse.ArgumentParser:
    """Build and return the argument parser.

    Separated from main() for two reasons:
    1. Single responsibility: parsing logic is isolated and testable
    2. Testability: tests can call _build_parser().parse_args([...])
       without running main()

    CS50 CLI behavior to match::

        Usage: ./speller [DICTIONARY] text

        - 1 argument:  text file only (dictionary defaults to large)
        - 2 arguments: dictionary file + text file
        - 0 or 3+ arguments: usage error

    Returns
    -------
    argparse.ArgumentParser
        Configured parser ready to parse sys.argv.

    Notes
    -----
    Why ``nargs='?'`` for dictionary?
        The ``?`` means "zero or one argument." If provided, it's used.
        If omitted, the ``default`` value is used. This replicates C's
        ``(argc == 3) ? argv[1] : DICTIONARY`` ternary pattern.

    Why ``type=str`` (not ``type=Path``)?
        argparse returns strings by default. We convert to Path inside
        main() where we also validate existence. Keeping argparse simple
        and doing validation separately follows single responsibility.
    """
    # Without RawDescriptionHelpFormatter, argparse reformats your epilog text
    # — collapsing newlines and wrapping. It preserves your formatting so the
    # examples display cleanly.
    parser = argparse.ArgumentParser(
        prog="speller",
        description="Spell-check a text file against a dictionary",
        epilog=(
            "Examples:\n"
            "   %(prog)s texts/cat.txt\n"
            "   %(prog)s dictionaries/small texts/cat.txt\n"
            "   %(prog)s --verbose texts/austen.txt"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        "text",  # positional argument required
        nargs="?",  # was required - now optional (zero or one)
        default=None,
        help="Path to text file to spell-check. Omit when using --dir.",
    )
    
    # -- Positional arguments --
    # nargs='?' makes dictionary optional, returns a single str.
    # nargs='*', nargs='+', nargs='N' return lists.
    # When user provides 1 positional arg -> it goes to 'text' (not dictionary)
    # When user provides 2 positional args -> first is dictionary, second is text
    parser.add_argument(
        "dictionary",
        nargs="?",  # zero or one
        default=str(
            file_dirs.DICT_DIR / default_fnames["dictionaries"].large  # "large"
        ),
        help=(
            "Path to dictionary file. One word per line. "
            "Default: dictionaries/large"
        ),
    )
    
    # -- Keyword arguments --
    parser.add_argument(
        "--ops",
        nargs="+",  # one or more
        default=["hash"],
        metavar="OPERATIONS",
        help=f"Data structure(s) to use. Default: hash. Available: {ops_list}",
    )
    
    parser.add_argument(
        "--dir",
        nargs="?",                  # zero or one value
        type=Path,
        default=None,               # flag absent
        const=_USE_BUNDLED_DIR,     # flag present, no value -> bundled
        metavar="DIRECTORY",
        help=(
            "Process all .txt files in this directory. "
            "When provided, 'text' argument is optional. "
            " Example: --dir texts/ "
            " Pair with --demo and omit the value to use bundled samples: "
            "`speller --demo --dir`."
        ),
    )
    
    # -- Optional flags --
    parser.add_argument(
        "--demo",
        action="store_true",
        default=False,
        help="Use a bundled sample text instead of a user file",
    )
    
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        default=False,
        help="Enable verbose output (DEBUG-level logging).",
    )
    
    parser.add_argument(
        "--no-custom-console",
        action="store_true",
        default=False,
        help="Disable use of Colored Formatter and use regular logging.Formatter",
    )
    
    # Enforce mutual exclusion between --structured-logging and --template-logging.
    # The cleanest way is to wrap both flags in an add_mutually_exclusive_group.
    #
    # When you wrap two or more flags in a mutually exclusive group, argparse enforces
    # at the command-line parsing layer that at most one of them can be set in any given
    # invocation. If the user passes two, argparse itself raises an error and exits
    # before your main() function ever runs.
    #
    # By default, passing neither flag is still valid. That's what you want here — passing
    # neither drops through to your default configure_logging() path. If you wanted to require
    # exactly one of them, you'd pass required=True:
    #   pythonlogging_group = parser.add_mutually_exclusive_group(required=True)
    # Now the user MUST pass either -t or -s
    logging_group = parser.add_mutually_exclusive_group()
    logging_group.add_argument(
        "-t", "--template-logging",
        action="store_true",
        default=False,
        help="Use t-string (PEP 750) logging with JSON file output. "
             "Requires Python 3.14+.",
    )
    logging_group.add_argument(
        "-s", "--structured-logging",
        action="store_true",
        default=False,
        help="Use structlog with NDJSON file output and ConsoleRenderer. "
             "Enable contextvars binding for richer observability.",
    )
    
    parser.add_argument(
        "--no-log-file",
        action="store_true",
        default=False,
        help="Disable file logging (console only).",
    )
    
    parser.add_argument(
        "--show-misspelled",
        action="store_true",
        default=False,
        help="Show all misspelled words from input txt file.",
    )
    
    parser.add_argument(
        "--table-report",
        action="store_true",
        default=False,
        help="Enable General report as an enriched table",
    )
    
    return parser


# Returns ExitCode correctly since its only consumer is main().
# It exists specifically to serve exit code logic. 
def _validate_paths(
    raw_path: Path | Traversable,
    *,
    path_name: str = "path",
) -> ExitCode | None:
    """Validate that required files exist before processing.

    Separated from main() because validation is a distinct concern
    from argument parsing and program execution. This function is
    also independently testable.

    Parameters
    ----------
    raw_path : Path
        The filesystem path to validate.  Can be a dictionary file,
        a text file, or any path that must exist before processing.
    path_name : str, optional
        Human-readable label used in the error log message
        (e.g. ``"dictionary"``, ``"text"``).  Title-cased automatically.
        Defaults to ``"path"``.

    Returns
    -------
    ExitCode or None
        ExitCode if validation fails, None if all paths are valid.

    Notes
    -----
    Why return ExitCode instead of raising?
        main() handles the exit logic. This function just reports
        what it found. Separation of detection (here) from action
        (main) keeps both functions simple.

    Why check BEFORE calling run_speller()?
        run_speller() has its own error handling, but catching missing
        files here gives cleaner error messages. Fail fast — don't
        load a 143K-word dictionary only to discover the text file
        is missing.
    """
    if not raw_path.is_file():
        logger.error("%s file not found: %s", path_name.title(), raw_path)
        return ExitCode.FILE_NOT_FOUND
    
    return None  # None means "all good"


# The production pattern to know to get full type safety on CLI args, you define a typed
# dataclass so you can access each arg directly as an attribute at static level.
def _resolve_text_paths(args: SpellerArgs) -> list[Path | Traversable]:
    """Resolve the ordered, deduplicated list of text files to process.

    Supports three calling modes:

    - **Single file only** — ``args.text`` is set, ``args.directory``
      is ``None``.  Returns a one-element list.
    - **Directory only** — ``args.directory`` is set, ``args.text``
      is ``None``.  Returns all ``*.txt`` files in sorted order.
    - **Both** — single file first, then directory files.
      Deduplicates so the single file is not processed twice if it
      lives inside the directory.

    Parameters
    ----------
    args : SpellerArgs
        Parsed and typed CLI arguments.  Uses ``args.text`` and
        ``args.directory``.

    Returns
    -------
    list of Path
        Ordered, deduplicated list of ``.txt`` files ready for
        iteration.  Empty list signals that no valid input was found;
        the caller (``main()``) maps this to
        :attr:`~speller.config.ExitCode.FILE_NOT_FOUND`.

    Notes
    -----
    Why ``sorted()`` for the directory glob?
        ``Path.glob()`` returns results in filesystem order, which
        varies by OS and filesystem.  ``sorted()`` makes the batch
        order deterministic — same output every run, same log entries
        in the same order.  Essential for reproducible benchmarks and
        test assertions.

    Why a ``seen`` set for deduplication?
        If the user passes ``texts/cat.txt`` as a positional arg AND
        ``--dir texts/``, ``cat.txt`` would appear twice without the
        set.  Processing the same file twice wastes time and produces
        duplicate report entries.

    Why return an empty list instead of raising?
        Returning an empty list separates detection (here) from action
        (``main()``).  ``main()`` decides the exit code and log message;
        this function just reports what it found.  The same pattern as
        :func:`_validate_paths`.
    """
    paths: list[Path | Traversable] = []
    seen: set[Path | Traversable] = set()
    
    # iterdir() is a directory listing — it returns every immediate child,
    # no filtering, no recursion.
    bundled = sorted(p.name for p in file_dirs.TXT_DIR.iterdir())
    
    if args.demo:
        if args.text:
            # User wants to bundle samples - look inside the installed package
            text_path = file_dirs.TXT_DIR / args.text
            if not text_path.is_file():
                raise SystemExit(
                    f"Bundled sample '{args.text}' not found. "
                    f"Available: {", ".join(bundled)}"
                )
            if text_path not in seen:
                paths.append(text_path)
                seen.add(text_path)
        
        if args.directory:
            for txt_file in args.directory.iterdir():
                if txt_file not in seen:
                    paths.append(txt_file)
                    seen.add(txt_file)
    
    else:
        # Single file from positional arg (existing behavior, unchanged)
        if args.text:  # SpellerArgs gives Pyright full static coverage here
            p = Path(args.text)
            if p.exists() and p not in seen:
                paths.append(p)
                seen.add(p)
            elif p.name in bundled:
                logger.warning(
                    "Did you mean to use a bundled sample? Try: "
                        f"speller --demo {p.name}"
                )
                console.print(f"[bold yellow]Bundle samples available: [/bold yellow]"
                              f"[yellow]{", ".join(bundled)}[yellow]")
                
        # Directory glob - same pattern as black/ruff/mypy
        if args.directory and isinstance(args.directory, Path):
            dir_path = args.directory  # <- args.directory is already Path | None
            if not dir_path.is_dir():
                logger.error("--dir path is not a directory: %s", dir_path)
                return []
            
            # glob(pattern) is a search — it returns only entries matching a shell-style
            # wildcard pattern, and with ** can recurse arbitrarily deep.
            for txt_file in sorted(dir_path.glob("*.txt")):  # sorted = deterministic order
                if txt_file not in seen:
                    paths.append(txt_file)
                    seen.add(txt_file)
                
    return paths       


def _validate_ops(ops_names: list[str]) -> list[str]:
    """Validate and normalise requested backend operation names.
 
    Strips whitespace and punctuation from each name, lower-cases it,
    and checks it against the live :data:`~speller.register.dicts`
    registry.  Expands the special value ``"all"`` into every
    registered key.
 
    Parameters
    ----------
    ops_names : list of str
        Raw operation names from the ``-o`` / ``--operations`` argument.
 
    Returns
    -------
    list of str
        Cleaned, validated operation names ready for iteration.
        Order matches the input (or the registry insertion order for
        ``"all"``).
 
    Raises
    ------
    KeyError
        If any name (after cleaning) is not in :data:`dicts` and is
        not the literal string ``"all"``.  The error message lists all
        available operations.
 
    Examples
    --------
    >>> _validate_ops(["hash"])
    [\'hash\']
    >>> _validate_ops(["all"])
    [\'hash\', \'list\', \'sorted\']   # depends on registered backends
    >>> _validate_ops(["unknown"])
    KeyError: "Unknown operation \'unknown\'. Available: hash, list, sorted"
    """
    clean_names = [
        name.strip().strip(string.punctuation).lower()
        for name in ops_names
    ]
    
    if "all" in clean_names:
        return list(dicts.keys())  # <- clear intent, no mutation during iteration
    
    for name in clean_names:
        # This validates against the actual registry,
        # which is the single source of truth.
        if name not in dicts:
            raise KeyError(
                f"Unknown operation '{name}'. Available: {ops_list}"
            )
    
    return clean_names


def _print_reports(
    reports: Report | GeneralReport,
    infile_name: str = "file",
    *,
    table_report: bool = False,
    console: Console,
) -> None:
    """Write the misspelled-words file (if requested) and print the report.
 
    If ``reports.misspelled`` is not ``None``, creates the misspelled
    words output directory and writes the word list to a file named
    ``misspelled_<infile_name>``.  Always prints ``reports.main`` to
    ``stdout``.
 
    Parameters
    ----------
    reports : REPORT
        Named tuple from :meth:`~speller.speller.SpellerResult.format_report`.
        ``reports.main`` is the CS50-format summary string.
        ``reports.misspelled`` is a newline-joined word list, or
        ``None`` if ``--show-misspelled`` was not requested.
    infile_name : str
        Base name of the checked text file (e.g. ``"austen.txt"``).
        Used to construct the output filename.
 
    Notes
    -----
    Directory creation uses ``mkdir(parents=True, exist_ok=True)`` so
    the call is idempotent — no error if the directory already exists.
    """
    if isinstance(reports, Report):
        console.print(reports.main)
        
        if reports.misspelled is not None:
            file_dirs.MISS_DIR.mkdir(parents=True, exist_ok=True)
            out_file = file_dirs.MISS_DIR / f"misspelled_{infile_name}"
            out_file.write_text(reports.misspelled, encoding="utf-8")
            logger.info("Misspelled words saved to '%s'", out_file)
    
    else:
        if table_report:
            print()  # Print a new line ('\n') by default
            # rich.panel.Panel wraps any content in a decorated box with a title.
            console.print(
                Panel(
                    "[bold blue]GENERAL REPORT[/bold blue]",
                    expand=False,
                    border_style="blue",
                )
            )
            # Using __rich__ dunder method to be called by console.print() automatically
            # __rich__ returns a Table object that Console parses it.
            console.print(reports)
        else:
            # Print out regular string with color mark ups
            console.print(reports.format_general_report())
    

# =============================================================================
# MAIN FUNCTION
# =============================================================================

# The if __name__ block and pyproject.toml script call main() with no arguments,which
# defaults to None, which triggers sys.argv reading. Your tests pass explicit lists.
def main(argv: list[str] | None = None) -> ExitCode:
    """Entry point for the speller CLI.

    Parameters
    ----------
    argv : list[str] or None
        Command-line arguments. If None, reads from sys.argv.
        Pass explicitly for testing:
            main(["texts/cat.txt"])
            main(["--verbose", "dictionaries/small", "texts/cat.txt"])
    
    Orchestrates the full program lifecycle:
    1. Parse arguments
    2. Configure logging (respects --verbose and --no-log-file)
    3. Validate file paths
    4. Create dictionary (concrete implementation chosen HERE)
    5. Run spell checker (dependency injection via Protocol)
    6. Display results
    7. Return exit code

    Returns
    -------
    int
        Exit code (0 for success, non-zero for errors).
        Used by sys.exit() and by shell scripts checking $?.

    Notes
    -----
    Why return int instead of calling sys.exit() directly?
        Returning an int makes main() testable:
            assert main() == ExitCode.SUCCESS
        If main() called sys.exit() internally, tests would need
        to catch SystemExit exceptions — messy and fragile.

        sys.exit() is called ONE place: the if __name__ block at
        the bottom. main() just returns the code.
    """
    # -- Step 1: Parse arguments --
    # _build_parser() returns an ArgumentParser object
    parser = _build_parser()
    raw: argparse.Namespace = parser.parse_args(argv)
    
    # Resolve --dir sentinel into a real Path (or None for "no batch mode"),
    # before constructing SpellerArgs. That keeps the dataclass clean.
    if raw.dir is _USE_BUNDLED_DIR:
        if not raw.demo:
            # parser.error() is the idiomatic argparse exit-with-message function — it
            # integrates cleanly with your existing ExitCode flow because it never returns.
            # exits with code 2.
            parser.error(
                "--dir without a path is only valid with --demo. "
                        "Either pass `--demo --dir`or `--dir <path>`."
            )
        resolved_dir: Path | Traversable | None = file_dirs.TXT_DIR
    elif raw.dir is None:
        resolved_dir = None
    else:
        resolved_dir = Path(raw.dir)
    
    # Convert from Namespace to SpellerArgs attributes
    # That gives you full Pyright coverage for the rest of main()
    args = SpellerArgs(
        text=raw.text,
        dictionary=raw.dictionary,
        operations=raw.ops, 
        directory=resolved_dir,
        demo=raw.demo,
        verbose=raw.verbose,
        no_log_file=raw.no_log_file,
        show_misspelled=raw.show_misspelled,
        no_custom_console=raw.no_custom_console,
        template_logging=raw.template_logging,
        structured_logging=raw.structured_logging,
        table_report=raw.table_report,
    )
    
    # -- Step 2: Configure logging FIRST --
    # Must happen before any logger.info/debug calls.
    # --verbose flag controls console log level.
    # --no-log-file disable the rotating file handler.
    #
    # ─── Select logging backend based on CLI flag ───
    #   Both functions have the same parameter signature — they're interchangeable
    #   at the composition root. This is the Strategy pattern applied to logging:
    #   the flag selects WHICH configuration runs, but the rest of main() doesn't
    #   know or care which one was picked.
    #
    #   Why import configure_template_logging locally inside the if block? Because
    #   t-strings require Python 3.14. If a user on Python 3.12 runs without the flag,
    #   the import never executes and the program works fine. If they use the flag
    #   on 3.12, they get a clear ImportError instead of a mysterious crash elsewhere.
    #   This is lazy import as a feature-gate pattern.
    if args.template_logging:
        try:
            from speller.template_logger import configure_template_logging
        except ImportError as e:
            sys.exit(f"Error: Template lib available in Python 3.14+. Details: {e}")
        
        configure_template_logging(
            console_verbose=args.verbose,
            log_to_file=not args.no_log_file,
            custom_console=not args.no_custom_console,
        )
        logger.info("Template (t-string) logging mode enabled")
    
    elif args.structured_logging:
        # Lazy import: structlog is only required when this flag is set.
        # Keeps the package importable even if the dependency is missing.
        try:
            from speller.structured_logger import configure_structured_logging
        except ImportError as e:
            sys.exit(f"Error: structlog not installed. Details: {e}")
        
        configure_structured_logging(
            console_verbose=args.verbose,
            log_to_file=not args.no_log_file,
            custom_console=not args.no_custom_console,
        )
        logger.info("Structured logging mode enabled") 
            
    else:
        configure_logging(
            console_verbose=args.verbose,
            log_to_file=not args.no_log_file,
            custom_console=not args.no_custom_console,
        )
        logger.info("Regular logging mode enabled")
        
    if args.verbose:
        logger.debug("Verbose mode enabled (console debug output)")
    
    logger.debug("Arguments parsed: %s", args)
    
    # -- Step 3: Convert and validate paths --
    dict_path = Path(args.dictionary)
    path_validation = _validate_paths(dict_path, path_name="dictionary")
    if path_validation is not None:
        return path_validation
    
    text_paths: list[Path | Traversable] = _resolve_text_paths(args)
    # If no files in directory provided
    if not text_paths:
        logger.error("No text files found. Provide a file or --dir path.")
        return ExitCode.FILE_NOT_FOUND
    
    # Variables to  build General Report
    files_in_dir = 0
    files_not_found = 0
    # defaultdict() to initialize values as empty lists
    # list[str] is a type annotation, not a factory function. 'defaultdict[list[str]]' works
    # by accident because list[str]() produces an empty list, but it's semantically wrong. 
    # Use defaultdict(list) (untyped factory) and annotate the variable.
    files_with_error: defaultdict[str, list[str]] = defaultdict(list)
   
    success = False
    try:
        # _validate_ops() returns a list of valid ops
        validated_ops: list[str] = _validate_ops(args.operations)
        first_op = validated_ops[0]
        
        for operation in validated_ops:
            data = dicts[operation]
            
            # -- Step 4: Create concrete dictionary -- 
            # THIS IS THE COMPOSITION ROOT — the one place that picks
            # the concrete implementation. Everything downstream depends
            # on DictionaryProtocol (the abstraction), not this class.
            #
            # To swap implementations:
            #   dictionary = DatabaseDictionary(conn_string)  # Stage 2
            #   dictionary = MockDictionary()                 # testing
            
            # Load dictionary ONCE for this backend
            loaded_dict, load_result = load_dictionary(dictionary=data.dict_class(), dict_path=dict_path)
            
            # rich.panel.Panel wraps any content in a decorated box with a title:
            console.print(Panel("Dictionary loaded successfully", title="[green]SUCCESS[/green]"))
            
            # -- Step 5: Run spell checker --
            # run_speller() accepts DictionaryProtocol - it doesn´t know
            # or care that we passed a HashTableDictionary.
            logger.debug("Running Speller with '%s'", data.name)

            files_in_dir = len(text_paths)
            
            # Now iterate over all text files - no dictionary reload
            for text_path in text_paths:
                path_validation: ExitCode | None = _validate_paths(text_path, path_name="text")
                if path_validation is not None:
                    logger.warning("Skipping '%s': not found", text_path)
                    files_not_found += 1
                    continue    # skip missing files, don't abort the batch
                
                # ─── Structlog contextvars binding (per-file scope) ───
                # Every log call downstream in run_speller() and its
                # callees automatically includes these fields in the
                # NDJSON output - without the emitting code knowing.
                # This is the Stage 2+ request-scoped logging pattern.
                if args.structured_logging:
                    import structlog
                    structlog.contextvars.clear_contextvars()  # clears vars before assignment for each run
                    structlog.contextvars.bind_contextvars(
                        file=text_path.name,
                        backend=type(loaded_dict).__name__,
                        operation=operation,
                    )
                
                # Use t-strings or f-strings (regular string) for logger.info()
                if args.template_logging:
                    text_name = text_path.name
                    dict_name = dict_path.name
                    backend = type(loaded_dict).__name__  # getting class name
                    # The extra dict is the pre-t-string way to attach structured data.
                    # Access as 'record.author'
                    logger.info(
                        t"Spell checking '{text_name}' with dictionary '{dict_name}', in {backend}",
                        extra={"author": "manuel_reyes"},
                    )
                else:
                    logger.info(
                        "Spell checking '%s' with dictionary '%s', in %s",
                        text_path.name,
                        dict_path.name,
                        type(loaded_dict).__name__,
                    )
                
                benchmarks: dict[str, BenchmarkResult] = {}
                benchmarks["load"] = load_result
                
                try:
                    # Initial results[] (ops_name, description empty)
                    # data.results[str]: Type hints = ... fail, because in Python we cannot annotate
                    # a subscript assignment. PEP 526 only allows annotations on: 
                    #   - Simple names: x: int = 5
                    #   - Attribute access: self.x: int = 5
                    data.results[text_path.name] = run_speller(
                        dictionary=loaded_dict, 
                        text_path=text_path,
                        benchmarks=benchmarks,
                    )
                except UnicodeDecodeError as e:
                    logger.warning("Skipping file: %s", e)
                    files_with_error["error_decode"].append(text_path.name)
                    continue    # skip bad files, don't abort the batch
                except ValueError as e:
                    logger.warning("Skipping file: %s", e)
                    files_with_error["error_empty"].append(text_path.name)
                    continue    # skip bad files, don't abort the batch
                except Exception as e:
                    logger.warning("Exception: Skipping file: %s", e)
                    files_with_error["error_other"].append(text_path.name)
                    continue    # skip bad files, don't abort the batch
                
                result: SpellerResult = data.results[text_path.name]
                
                # "Update" by creating a NEW frozen instance (original unchanged)
                # replace() doesn't mutate — it copies all fields into a new frozen instance with the
                # specified fields overridden. The original object is untouched. This is the idiomatic
                # pattern for "updating" immutable data in Python.
                result = replace(
                    result,
                    ops_name=data.name,
                    description=data.description,
                )
            
                # Show for the FIRST operation only (avoid duplicate files)
                show_misspelled = (args.show_misspelled and (operation == first_op))
        
                # -- Step 6: Display SpellerResult reports --
                # format_report() returns a string — main() decides to print it.
                # In a web app (Stage 1 Streamlit), you'd display it differently.
                # In tests, you'd just check result.words_misspelled.
                reports: Report = result.format_report(log_misspelled=show_misspelled)
                _print_reports(reports, text_path.name, console=console)
        
        # -- Step 7: Builds and display GeneralReport report --
        general_report = GeneralReport(
            files_not_found=files_not_found,
            files_in_dir=files_in_dir,
            files_with_error=FileErrorData(  
                error_decode=files_with_error["error_decode"],
                error_empty=files_with_error["error_empty"],
                error_other=files_with_error["error_other"],
            ),  # Construct FileErrorData with defaultdict values
        )
        
        _print_reports(general_report, table_report=args.table_report, console=console)
        
        # -- Step 8: Return exit code --
        success = True
        return ExitCode.SUCCESS

    except KeyboardInterrupt:
        logger.warning("Interrupted by user. Exiting.")
        return ExitCode.KEYBOARD_INTERRUPT
    
    except SystemExit as e:
        # run_speller raises SystemExit if dictionary fails to load
        logger.error("Speller failed: %s", e)
        return ExitCode.LOAD_FAILED
    
    except (KeyError, TypeError) as e:
        logger.error("Operation argument failed: %s", e)
        return ExitCode.USAGE_ERROR
    
    except Exception as e:  # Catches every other exception in program
        # Appears as logging.error, provides Python's traceback info
        logger.exception("Unexpected Error: %s", e)
        return ExitCode.FAILURE
    
    # Why %s over f-string in logging? The f-string is evaluated immediately even if the log level
    # is disabled. The %s format is only evaluated if the message actually gets logged. This is a
    # performance pattern that matters in hot loops (Stage 2 ETL, Stage 3 training).
    
    finally:   # Always runs (error or no erros)
        if args.structured_logging:
            import structlog
            structlog.contextvars.clear_contextvars()  # Clear variables for final log mssgs
            
        if success:
            logger.info("Program completed.\n")
            logger.debug("Spell check completed successfully\n")
        else:
            logger.warning("Program terminated with errors.\n")
            
        for log_file in file_dirs.log_file:
            if log_file.exists():
                logger.info(
                    "%s saved in %s",
                    log_file.name,
                    log_file,
                )
    
   
# =============================================================================
# EXECUTION GUARD
# =============================================================================

# This block runs ONLY when the module is executed directly:
#   $ python -m speller texts/cat.txt    → runs this block
#   from speller.__main__ import main    → does NOT run this block
#
# sys.exit() lives HERE and ONLY here — never inside main().
# main() returns an int, this block converts it to a process exit code.
#
# The shell can check the exit code:
#   $ python -m speller texts/cat.txt && echo "success" || echo "failed"
if __name__ == "__main__":
    sys.exit(main())
    
# Execution: __name__ == "__main__" → runs sys.exit(main())
#   $ python -m speller texts/cat.txt

# Import: __name__ == "speller.__main__" → guard block skipped
#   >>> from speller.__main__ import main
#   >>> code = main()  # returns int, no sys.exit


# =============================================================================
# SHORT REFERENCE GUIDES
# =============================================================================
# =====================================================
# CLI Arguments And sys.argv
# =====================================================

# When you call parse_args() with NO arguments:
#   args = parser.parse_args()
# It implicitly reads from sys.argv[1:]
# Same as: args = parser.parse_args(sys.argv[1:])

# When you call parse_args() WITH arguments:
#   args = parser.parse_args(["texts/cat.txt"])
# It uses YOUR list instead of sys.argv

# The flow:

#   $ python -m speller --verbose texts/cat.txt

#   sys.argv = ["speller/__main__.py", "--verbose", "texts/cat.txt"]
#   sys.argv[1:] = ["--verbose", "texts/cat.txt"]    ← [1:] skips the script name

#   parser.parse_args()       → reads sys.argv[1:] automatically
#   parser.parse_args(None)   → same thing (None = use sys.argv[1:])
#   parser.parse_args([...])  → uses YOUR list instead

# def main(argv: list[str] | None = None) -> ExitCode:
#     args = parser.parse_args(argv)

# ┌─────────────────────────────────────────────────────────────────┐
# │  Caller                        │ argv value   │ parse_args uses │
# │────────────────────────────────│──────────────│─────────────────│
# │  if __name__ == "__main__":    │              │                 │
# │      sys.exit(main())          │ None         │ sys.argv[1:]    │
# │                                │              │ (real CLI args) │
# │────────────────────────────────│──────────────│─────────────────│
# │  pyproject.toml script:        │              │                 │
# │      speller texts/cat.txt     │ None         │ sys.argv[1:]    │
# │                                │              │ (real CLI args) │
# │────────────────────────────────│──────────────│─────────────────│
# │  Test:                         │              │                 │
# │      main(["texts/cat.txt"])   │ ["texts/..."]│ your list       │
# │                                │              │ (controlled)    │
# │────────────────────────────────│──────────────│─────────────────│
# │  Another module:               │              │                 │
# │      main(["--verbose", path]) │ [...]        │ your list       │
# │                                │              │ (programmatic)  │
# └─────────────────────────────────────────────────────────────────┘

# =====================================================
# [project.scripts]: How pyproject.toml connects
# =====================================================

# [project.scripts]
# speller = "speller.__main__:main"

# When the user types `speller texts/cat.txt`, pip's generated script calls `main()`
# directly and handles the exit code — it doesn't go through the `if __name__` block.

## Complete Module Flow
# $ python -m speller --verbose dictionaries/small texts/cat.txt

# 1. Python finds speller/__main__.py
# 2. __init__.py runs → NullHandler set
# 3. ImportError guard → all modules import successfully
# 4. if __name__ == "__main__" → sys.exit(main())
# 5. main() starts:
#      a. _build_parser() → ArgumentParser created
#      b. parse_args() → dictionary="dictionaries/small", text="texts/cat.txt", verbose=True
#      c. config_logging(verbose=True) → DEBUG console + file handlers
#      d. _validate_paths() → both files exist → None (success)
#      e. HashTableDictionary() → concrete instance created
#      f. run_speller(dictionary, text, dict) → SpellerResult returned
#         ├── timer("load") → dictionary.load("dictionaries/small")
#         ├── timer("check") → for word in extract_words("texts/cat.txt"):
#         │                        dictionary.check(word)
#         └── timer("size") → dictionary.size()
#      g. print(result.format_report()) → CS50-format output
#      h. return ExitCode.SUCCESS → 0
# 6. sys.exit(0) → process exits cleanly


# =====================================================
# argparse.Namespace Object
# =====================================================

# argparse.Namespace is the object that parser.parse_args() returns. It's
# essentially a simple container that holds your parsed CLI arguments as
# dot-access attributes.
#
# The tradeoff is that argparse.Namespace attribute access is typed as Any — Pyright can't verify
# that args.text actually exists, because argparse builds the namespace dynamically at runtime.
# That's just an argparse limitation, not something you did wrong.
#
#   def _resolve_text_paths(args: argparse.Namespace) -> list[Path]:


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