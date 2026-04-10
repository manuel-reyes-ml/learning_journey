"""
"""

from __future__ import annotations

import pytest

from speller.config import (
    MAX_WORD_LENGTH,
    ExitCode,
    FileHandlerConfig,
    file_dirs,
    fhandler_config,
)


# =============================================================================
# CONSTANTS
# =============================================================================

class TestConstants:
    """Test module-level constants.

    Grouping related tests in a class is OPTIONAL in pytest.
    Benefits:
    - Visual organization in test output
    - Can share setup via class-level fixtures
    - Collapsible in IDE test explorer

    No __init__ needed — pytest instantiates it automatically.
    """
    
    def test_max_word_length_values(self) -> None:
        assert MAX_WORD_LENGTH == 45
        
    def test_max_word_length_is_int(self) -> None:
        assert isinstance(MAX_WORD_LENGTH, int)
        
    