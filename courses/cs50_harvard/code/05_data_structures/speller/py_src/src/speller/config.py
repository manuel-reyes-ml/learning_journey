"""Package-wide constants and frozen configuration for the speller CLI.
 
All read-only values shared across the package live here.  ``config.py``
is at the **bottom of the dependency chain** — it imports nothing from
within the ``speller`` package, so any module can safely import from it
without risk of circular imports.
 
Structure
---------
``Constants``
    Module-level primitives: ``MAX_WORD_LENGTH``, ``DICT_FNAMES``.
 
``Enumerations``
    :class:`ExitCode`       — POSIX-aligned process exit codes.
    :class:`DefaultDirs`    — subdirectory names as ``StrEnum``.
 
``TypedDict``
    :class:`DefaultFileNames` — typed mapping for default filename config.
 
``Frozen dataclasses``
    :class:`FileDirectories`   — all resolved ``Path`` objects.
    :class:`FileHandlerConfig` — immutable ``RotatingFileHandler`` settings.
 
``Singletons``
    ``file_dirs``        — :class:`FileDirectories` instance.
    ``fhandler_config``  — :class:`FileHandlerConfig` instance.
 
Both singletons are created once at import time so every module that
imports them shares the same resolved paths and validated settings.
 
Roadmap relevance
-----------------
This pattern — a zero-internal-import config module with frozen
dataclass singletons — reappears as ``LLMConfig`` in DataVault,
``RAGConfig`` in PolicyPulse, and ``ExtractionConfig`` in FormSense.
"""

# =============================================================================
# IMPORTS
# =============================================================================

from __future__ import annotations

from enum import IntEnum, StrEnum, unique
from typing import Final, NamedTuple, TypedDict, Required, NotRequired
from dataclasses import dataclass
from importlib.resources import files
from pathlib import Path
from platformdirs import PlatformDirs
import logging
import sys


# =============================================================================
# EXPORTS
# =============================================================================

__all__ = [
    # Constants
    "MAX_WORD_LENGTH",
    "default_fnames",
    # Configuration
    "ExitCode",
    "file_dirs",
    "fhandler_config",
    "default_fnames",
    # Class
    "FileDirectories",
    "FileHandlerConfig",
]


# =============================================================================
# CONSTANTS CONFIGURATION
# =============================================================================
# =====================================================
# Constants
# =====================================================

MAX_WORD_LENGTH: Final[int] = 45

# What platformdirs does?
# Given an app name, it returns the right place to write files on the current OS. 
# The library knows about:
#   - Linux: XDG Base Directory Specification (~/.local/share, ~/.config, ~/.cache, ~/.local/state)
#   - macOS: Apple's guidance (~/Library/Application Support, ~/Library/Caches, ~/Library/Logs)
#   - Windows: AppData\Local and AppData\Roaming via CSIDL APIs
#   - Android: App-private storage conventions
#   - AWS:
#
# Module-level singleton - configured once, used everywhere
_PLATFORM_DIRS: Final[PlatformDirs] = PlatformDirs(
    appname="speller",
    appauthor="manuelreyes",  # Used on Windows only; harmless on Unix
    ensure_exists=True,       # Create dirs on first access
)


# =====================================================
# Class Constants Configuration
# =====================================================

@unique
class ExitCode(IntEnum):
    """POSIX-aligned process exit codes for the speller CLI.
 
    ``IntEnum`` values are passed directly to ``sys.exit()``.
    ``@unique`` prevents accidental duplicate values at definition time.
 
    Attributes
    ----------
    SUCCESS : int
        ``0`` — normal completion.
    USAGE_ERROR : int
        ``1`` — bad arguments or unknown operation name.
    FILE_NOT_FOUND : int
        ``2`` — dictionary or text file does not exist.
    LOAD_FAILED : int
        ``3`` — dictionary file found but ``load()`` returned ``False``.
    FAILURE : int
        ``4`` — unexpected exception caught in ``main()``.
    KEYBOARD_INTERRUPT : int
        ``130`` — standard shell convention for Ctrl-C / SIGINT.
 
    Examples
    --------
    >>> sys.exit(ExitCode.SUCCESS)       # process exits with code 0
    >>> ExitCode.SUCCESS == 0            # True — IntEnum compares to int
    True
    """
    
    SUCCESS = 0
    USAGE_ERROR = 1
    FILE_NOT_FOUND = 2
    LOAD_FAILED = 3
    FAILURE = 4
    KEYBOARD_INTERRUPT = 130
    

@unique
class DefaultDirs(StrEnum):
    """Default subdirectory names relative to the project root.
 
    ``StrEnum`` members compare equal to their string values so they
    can be passed directly to ``Path(...)`` operations without casting.
 
    Attributes
    ----------
    DICT : str
        ``"dictionaries"`` — word-list source files.
    KEYS : str
        ``"keys"`` — reserved for API keys (Stage 2+).
    TXT : str
        ``"texts"`` — sample text files for spell-checking.
    LOG : str
        ``"logs"`` — rotating log output.
    MISS : str
        ``"misspelled"`` — saved misspelled-word reports.
 
    Examples
    --------
    >>> str(DefaultDirs.DICT)
    \'dictionaries\'
    >>> Path("project") / DefaultDirs.DICT
    PosixPath(\'project/dictionaries\')
    """
    
    DICT = "dictionaries"
    KEYS = "keys"
    TXT = "texts"
    LOG = "logs"
    MISS = "misspelled"


# The class-based form gives you typed fields that Pyright can validate at every
# access site, docstring support, default values, and it follows PEP 8 class naming.
# This lets you introduce optional fields without breaking call sites, which is
# useful during staged migrations.
class DictFileNames(NamedTuple):
    """Default dictionary filenames."""
    
    large: str
    small: str
    

class DefaultFileNames(TypedDict, total=False):
    """Typed mapping for default filename configuration.
 
    Uses ``TypedDict`` with ``Required`` / ``NotRequired`` to enforce
    that ``"dictionaries"`` is always present while ``"keys"`` is
    optional.  This is the same pattern used in FastAPI request bodies
    and Pydantic partial schemas.
 
    Fields
    ------
    dictionaries : DICT_FNAMES
        Named tuple with ``large`` and ``small`` dictionary filenames.
        Required — spell-checking cannot proceed without a dictionary.
    keys : tuple of str, optional
        Reserved for future API key filenames.  Not used in Stage 1.
    """
    
    dictionaries: Required[DictFileNames]  # Must be present
    keys: NotRequired[tuple[str, ...]]   # Optional


# Build dictionary using DefaultFileNames structure
default_fnames: DefaultFileNames = {
    "dictionaries": DictFileNames("large", "small"),
}


class LogFilesPath(NamedTuple):
    """Resolved paths for each logging backend's output file.

    Three backends produce three separate files so they can run
    side-by-side and be diffed for comparison.

    Attributes
    ----------
    flog_path : Path
        Plain-text output from :mod:`speller.logger` → ``speller.log``.
    tlog_path : Path
        Custom JSON (PEP 750 t-strings) from
        :mod:`speller.template_logger` → ``speller_json.log``.
    slog_path : Path
        NDJSON output from :mod:`speller.structured_logger`
        → ``speller_structured.log``.
    """
    
    flog_path: Path
    tlog_path: Path
    slog_path: Path
    slog_indent_path: Path


# =====================================================
# Dataclass Frozen Constants
# ===================================================== 

# frozen=True makes instances immutable.
# slots=True prevents dynamic attribute creation and
# reduces memory fooprint.
# Together they create a truly locked-down data container.
@dataclass(frozen=True, slots=True)
class FileDirectories:
    """Resolved filesystem paths for all speller project directories.
 
    All paths are computed from ``__file__`` at instantiation so the
    package works correctly regardless of where it is installed or run
    from.  ``frozen=True`` prevents accidental reassignment;
    ``slots=True`` reduces memory footprint.
 
    Attributes
    ----------
    CUR_DIR : Path
        Absolute path to the ``speller/`` package directory.
    ROOT_DIR : Path
        Two levels above ``CUR_DIR`` — the ``py_src/`` project root.
    DICT_DIR : Path
        ``ROOT_DIR / "dictionaries"`` — dictionary source files.
    KEYS_DIR : Path
        ``ROOT_DIR / "keys"`` — reserved for API keys (Stage 2+).
    TXT_DIR : Path
        ``ROOT_DIR / "texts"`` — sample text files.
    LOG_DIR : Path
        ``ROOT_DIR / "logs"`` — rotating log files.
    MISS_DIR : Path
        ``ROOT_DIR / "misspelled"`` — saved misspelled-word reports.
 
    Examples
    --------
    >>> dirs = FileDirectories()
    >>> dirs.log_file.name
    \'speller.log\'
    """
    
    # Every path in FileDirectories is computed relative to where config.py physically
    # lives on disk. That's what __file__ means — the absolute path to the source file
    # being executed:
    #   CUR_DIR: Final[Path] = Path(__file__).resolve().parent  # speller/
    #   ROOT_DIR: Final[Path] = CUR_DIR.parents[1]              # py_src/
    #
    # Because you ran pip install -e . (editable install), __file__ points into your repo:
    #    __file__  → /Users/manuelreyes/.../speller/py_src/src/speller/config.py
    #    CUR_DIR   → /Users/manuelreyes/.../speller/py_src/src/speller
    #    ROOT_DIR  → /Users/manuelreyes/.../speller/py_src
    #    LOG_DIR   → /Users/manuelreyes/.../speller/py_src/logs   ✓ writable
    # Editable installs create a link back to your source tree rather than copying files into site-packages.
    # So __file__ still resolves to your working directory. Every path works.
    #
    # The moment someone does pip install speller (non-editable, from a wheel), Python copies your code
    # into site-packages:
    #    __file__  → /usr/lib/python3.13/site-packages/speller/config.py
    #    CUR_DIR   → /usr/lib/python3.13/site-packages/speller
    #    ROOT_DIR  → /usr/lib/python3.13                          ✗ SYSTEM dir
    #    LOG_DIR   → /usr/lib/python3.13/logs                     ✗ PermissionError
    #
    # --- Bundled, read-only resources (via importlib.resources) -----
    #
    # `files(anchor)` returns a Traversable. For a normal disk install,
    # this is a pathlib.Path — behaves identically to your current code.
    # For zipped/frozen installs, the Traversable still works via
    # Traversable.read_text() etc.
    #
    # Notice that I did not annotate DICT_DIR and TXT_DIR as Path. That's deliberate — they're Traversables.
    # The runtime type for disk installs is PosixPath (I verified this), but the static type is Traversable.
    DICT_DIR: Final = files("speller.data") / DefaultDirs.DICT
    TXT_DIR: Final = files("speller.data") / DefaultDirs.TXT
    KEYS_DIR: Final = files("speller.data") / DefaultDirs.KEYS
    
    # --- Writable, per-user paths (resolved by platformdirs) --------
    LOG_DIR: Final[Path] = _PLATFORM_DIRS.user_log_path
    MISS_DIR: Final[Path] = _PLATFORM_DIRS.user_data_path / DefaultDirs.MISS
    
    # `CUR_DIR` is no longer needed by path resolution, but keep it
    # for the existing `create_log_fname()` method which uses
    # `self.CUR_DIR.name` for the log filename. It's now purely a
    # naming helper, not a path anchor.
    CUR_DIR: Final[Path] = Path(__file__).resolve().parent  # speller/
    
    def create_log_fname(self) -> tuple[str, ...]:  
        """Build the three log filenames from the package directory name.

        Uses ``CUR_DIR.name`` (``"speller"``) so filenames stay in sync
        with any future package rename without manual updates.

        Returns
        -------
        tuple of (str, str, str)
            ``(plain_log, json_log, structured_log)`` filenames.
        """
        f_string = f"{self.CUR_DIR.name}.log"
        t_string = f"{self.CUR_DIR.name}_json.log"
        s_string = f"{self.CUR_DIR.name}_structured.log"
        s_indent_string = f"{self.CUR_DIR.name}_structured_indent.log"
        
        return f_string, t_string, s_string, s_indent_string
    
    
    @property  # Access function's return as an attribute
    def log_file(self) -> LogFilesPath:
        """Full resolved paths to the three rotating log files.

        Combines :attr:`LOG_DIR` with the result of
        :meth:`create_log_fname` for each backend.

        Returns
        -------
        LogFilesPath
            NamedTuple of absolute paths — one per backend.
        """
        f_string, t_string, s_string, s_indent_string = self.create_log_fname()
        
        flog_path = self.LOG_DIR / f_string
        tlog_path = self.LOG_DIR / t_string
        slog_path = self.LOG_DIR / s_string
        sindentlog_path = self.LOG_DIR / s_indent_string
        
        return LogFilesPath(
            flog_path,
            tlog_path,
            slog_path,
            sindentlog_path
        )


@dataclass(frozen=True, slots=True)
class FileHandlerConfig:
    """
    Immutable configuration for the rotating log file handler.
 
    All fields are frozen (read-only) constants that control log file
    size, rotation, and encoding. Use the ``max_log_bytes`` property
    to get the computed byte limit.
 
    Attributes
    ----------
    LEVEL_DEFAULT : int
        Default logging level for console output (``logging.INFO``).
    ENCODING : str
        Character encoding for log files.
    BACKUP_COUNT : int
        Number of rotated backup log files to retain.
    FILE_MB : int
        Maximum log file size in megabytes.
    MEGABYTE : int
        Bytes per kilobyte (1024).
    KILOBYTE : int
        Bytes per unit (1024).
    """
    
    LEVEL_DEFAULT: Final[int] = logging.INFO
    ENCODING: Final[str] = "utf-8"
    BACKUP_COUNT: Final[int] = 3
    FILE_MB: Final[int] = 5
    MEGABYTE: Final[int] = 1024
    KILOBYTE: Final[int] = 1024
    
    def negative_value(self, var: str) -> Exception:
        """Build a :class:`ValueError` for an invalid configuration field.
 
        Centralises the error message format so all ``__post_init__``
        validation checks produce consistent messages.
 
        Parameters
        ----------
        var : str
            Name of the offending field (e.g. ``"BACKUP_COUNT"``).
 
        Returns
        -------
        ValueError
            Ready-to-raise exception with a descriptive message.
        """
        return ValueError(f"{var} must be positive (> 0)")
    
    
    # The position of __post_init__ in source code doesn't matter-
    # Python's calls it automatically after the generated __init__
    # finishes (in dataclasses).
    def __post_init__(self) -> None:
        """Validate that all numeric configuration fields are positive.

        Called automatically by the dataclass machinery after ``__init__``
        completes.  Raises :exc:`ValueError` (via :meth:`negative_value`)
        for any field that is zero or negative, because a log handler
        configured with non-positive values will fail silently at runtime.

        Raises
        ------
        ValueError
            If any of ``BACKUP_COUNT``, ``FILE_MB``, ``MEGABYTE``, or
            ``KILOBYTE`` is less than or equal to zero.

        Notes
        -----
        ``frozen=True`` dataclasses still support ``__post_init__`` —
        the freeze constraint applies to attribute *assignment after*
        init, not to the init process itself.  All validation here runs
        before the instance is returned to the caller.
        """
        if self.BACKUP_COUNT <= 0:
            raise self.negative_value("BACKUP_COUNT")
        if self.FILE_MB <= 0:
            raise self.negative_value("FILE_MB")
        if self.MEGABYTE <= 0:
            raise self.negative_value("MEGABYTE")
        if self.KILOBYTE <= 0:
            raise self.negative_value("KILOBYTE")
    
    
    @property  # Access function's return as an attribute
    def max_log_bytes(self) -> int:
        """Maximum log file size in bytes.
 
        Converts :attr:`FILE_MB` from megabytes to bytes using the
        standard definition: 1 MB = 1 024 × 1 024 bytes.  This is the
        value passed to :class:`~logging.handlers.RotatingFileHandler`
        as ``maxBytes``.
 
        Returns
        -------
        int
            Maximum size in bytes (default: 5 × 1 024 × 1 024 = 5 242 880).
        """
        return self.FILE_MB * self.MEGABYTE * self.KILOBYTE
    

# =====================================================
# Dataclass Instantiation
# =====================================================

file_dirs = FileDirectories()

try:
    fhandler_config = FileHandlerConfig()
except ValueError as e:
    sys.exit(f"Error: Invalid FileHandlerConfig setting: {e}")
