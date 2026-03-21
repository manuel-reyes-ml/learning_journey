"""
"""

# =============================================================================
# IMPORTS
# =============================================================================

from __future__ import annotations

import sys

# =====================================================
# Impor Guard
# =====================================================

# __main__.py is the FRONT DOOR — if imports fail, give a friendly
# error message and exit. This is the ONE place where sys.exit()
# on ImportError is correct, because the user explicitly ran the
# program and expects it to either work or explain why it can't.
#
# Every other module lets ImportError propagate upward to here.
try:
    from pathlib import Path
    import argparse
    import logging
    
    from speller.dictionaries import HashTableDictionary
    from speller.config import ExitCode, file_dirs
    from speller.logger import configure_logging
    from speller.speller import run_speller
    
except ImportError as e:
    sys.exit(f"Error missing speller module.\nDetails: {e}")
    

# =============================================================================
# LOGGER SETUP
# =============================================================================

# Logger is created here but NOT configured yet.
# config_logging() is called INSIDE main() after argparse determines
# the verbosity level. This ensures --verbose flag controls log output
logger = logging.getLogger(__name__)


# =============================================================================
# INTERNAL HELPER FUNCTIONS
# =============================================================================
    
