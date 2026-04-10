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
        """MAX_WORD_LENGTH matches CS50's #define LENGTH 45."""
        assert MAX_WORD_LENGTH == 45
        
    def test_max_word_length_is_int(self) -> None:
        """MAX_WORD_LENGTH is an integer, not a string or float."""
        assert isinstance(MAX_WORD_LENGTH, int)
        

# =============================================================================
# ENUMS
# =============================================================================

class TestExitCode:
    """Test ExitCode enum values and behavior."""
    
    def test_success_is_zero(self) -> None:
        """Unix convention: success is exit code 0."""
        assert ExitCode.SUCCESS == 0
        
    def test_all_codes_are_unique(self) -> None:
        """No two exit codes share the same value.

        The @unique decorator on ExitCode should prevent this,
        but we test it explicitly for documentation and safety.
        """
        values = [code.value for code in ExitCode]
        assert len(values) == len(set(values))
        
    def test_exit_codes_are_integers(self) -> None:
        """All exit codes are integers (IntEnum guarantee)."""
        for code in ExitCode:
            assert isinstance(code, int)
            
    def test_known_exit_codes(self) -> None:
        """Verify all expected exit codes exist.

        This test catches accidental removal of an exit code.
        If someone deletes LOAD_FAILED, this test fails.
        """
        expected = {
            "SUCCESS",
            "USAGE_ERROR",
            "FILE_NOT_FOUND",
            "LOAD_FAILED",
            "FAILURE",
            "KEYBOARD_INTERRUPT",
        }
        actual = {code.name for code in ExitCode}  # Set comprehension
        assert actual == expected
        

# =============================================================================
# FROZEN DATACLASSES
# =============================================================================

