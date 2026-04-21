"""
"""

# =============================================================================
# IMPORTS
# =============================================================================

from __future__ import annotations

from logging.handlers import RotatingFileHandler
from typing import Final
import logging
import sys

import structlog
from structlog.types import Processor

from speller.config import (
    file_dirs,
    fhandler_config,
    FileDirectories,
    FileHandlerConfig,
)

# No ImportError sys.exit() on regular module so the
# error propagates to the caller (__main__.py).


# =============================================================================
# EXPORTS
# =============================================================================

__all__ = []


# =============================================================================
# MODULE CONFIGURATION
# =============================================================================
# =====================================================
# Shared Processor Chain
# =====================================================

