"""
"""

# =============================================================================
# IMPORTS
# =============================================================================

from __future__ import annotations
from logging.handlers import RotatingFileHandler
from pathlib import Path
import logging
import sys

try:
    from speller.config import (
        file_dirs,
        fhandler_config,
        FileDirectories,
        FileHandlerConfig,
        ColoredFormatter,
    )
except ImportError as e:
    sys.exit(f"Error: Cannot find relative modules.\nDetails: {e}")
    

# =============================================================================
# EXPORTS
# =============================================================================

__all__ = ["config_logging"]


# =============================================================================
# CORE FUNCTIONS
# =============================================================================

def config_logging(
    console_verbose: bool = False,
    log_to_file: bool = True,
    file_dirs: FileDirectories = file_dirs,
    fhandler_config: FileHandlerConfig = fhandler_config,
    custom_formatter: type[logging.Formatter] = ColoredFormatter,
) -> None:
    """
    """
    