"""
"""

# =============================================================================
# IMPORTS
# =============================================================================

from __future__ import annotations

import logging
import structlog
import sys

from logging.handlers import RotatingFileHandler
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