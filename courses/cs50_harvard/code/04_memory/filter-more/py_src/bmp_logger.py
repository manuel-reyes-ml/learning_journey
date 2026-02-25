"""
"""

from __future__ import annotations
from typing import Final
import logging
import sys

try:
    from .bmp_config import ColoredFormatter
except ImportError as e:
    sys.exit(f"Error: Cannot find relative modules.\nDetails: {e}")
    

# =============================================================================
# Module Configuration
# =============================================================================

# Exports
__all__ = [
    "setup_logging"
]

# Program Constants
LEVEL_DEFAULT = logging.INFO
FORMATTER_CLASS: Final[type[logging.Formatter]] = ColoredFormatter


# =============================================================================
# Core Functions
# =============================================================================

def setup_logging(
    formatter_class: type[logging.Formatter] | None = FORMATTER_CLASS, 
    level=LEVEL_DEFAULT,
) -> None:
    """Configures the base logger for the entire py_src packages."""
    if not formatter_class:
        raise ValueError("formatter_class cannot be empty")
    
    # 1. Grab the top-level logger for your package
    package_logger = logging.getLogger("py_src")
    package_logger.setLevel(level)
    
    # 2. Prevent duplicate handlers if this function is called multiple times
    if package_logger.hasHandlers():
        package_logger.handlers.clear()
        
    # 3. Create your handler and attach the ColoredFormatter
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter_class(
        fmt='%(asctime)s : %(levelname)s : %(message)s',
        datefmt='%H:%M:%S',
    ))
    
    # 4. Attach the handler to the package logger
    package_logger.addHandler(console_handler)
    
    # 5. Prevent logs from bubblig up to Python's default root logger
    # (prevents duplicate printing in some environments)
    package_logger.propagate = False
    
