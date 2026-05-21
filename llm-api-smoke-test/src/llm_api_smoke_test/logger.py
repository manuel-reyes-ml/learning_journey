"""
"""

# =============================================================================
# IMPORTS
# =============================================================================

from __future__ import annotations

import logging
import structlog
import sys

from dataclasses import dataclass
from logging.handlers import RotatingFileHandler
from pathlib import Path

from platformdirs import PlatformDirs
from structlog.types import EventDict, Processor, WrappedLogger
from typing import Any, Final, TextIO

# =============================================================================
# EXPORTS
# =============================================================================

__all__ = []


# =============================================================================
# CONSTANTS CONFIGURATION
# =============================================================================
# =====================================================
# Constants
# =====================================================

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
    appname="llm-api-smoke-test",
    appauthor="manuelreyes",  # Used on windows only; harmless on Unix
    ensure_exists=True,  # Create dirs on first access
)


# =====================================================
# Dataclass Frozen Constants
# =====================================================

@dataclass(frozen=True, slots=True)
class FileDirectories:
    """
    """
    
    # --- Writable, per-user paths (resolved by platformdirs) --------
    LOG_DIR: Final[Path] = _PLATFORM_DIRS.user_log_path
    
    # `CUR_DIR` is no longer needed by path resolution, but keep it
    # for the existing `create_log_fname()` method which uses
    # `self.CUR_DIR.name` for the log filename. It's now purely a
    # naming helper, not a path anchor.
    CUR_DIR: Final[Path] = Path(__file__).resolve().parent  # llm_api_smoke_test/
    
    @property  # Access function's return as an attribute
    def log_file_name(self) -> Path:
        """
        """
        return self.LOG_DIR / f"{self.CUR_DIR}.log"


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
        return ValueError(f"{var} must be positive (>0)")
    
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
    

