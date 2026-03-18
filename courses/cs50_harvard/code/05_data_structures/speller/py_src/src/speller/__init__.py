"""
"""
# Adding public API exports makes the package more professional

from __future__ import annotations
import logging
import sys

try:
    from speller.main import main
except ImportError as e:
    sys.exit(f"Error: cannot find relative modules.\nDetails: {e}")
    

__all__ = ["main"]


logging.getLogger(__name__).addHandler(logging.NullHandler())
