# Test files must start with 'test_' so they are auto-discovery by pytest

"""Tests for speller.config module.

Tests constants, enums, frozen dataclasses, and path resolution.
These tests verify the foundation of the entire package — if config
is wrong, everything built on top breaks.

Pytest Patterns Introduced
--------------------------
- Basic assertions (assert value == expected)
- Testing enum values and membership
- Testing frozen dataclass immutability
- Testing @property computed values
- Testing __post_init__ validation
- pytest.raises() for expected exceptions
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

# Test classes must start with capital T, colleted by class-name pattern
# Test functions/methods must start with 'test_', collected by function-name pattern

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

class TestFileDirectories:
    """Test FileDirectories frozen dataclass."""
    
    def test_instance_exists(self) -> None:
        """Module-level file_dirs instance is created at import time."""
        assert file_dirs is not None
        
    def test_cur_dir_exists(self) -> None:
        """CUR_DIR points to an existing directory (src/speller/)."""
        assert file_dirs.CUR_DIR.exists()
        
    def test_cur_dir_is_speller(self) -> None:
        """CUR_DIR name is 'speller' (the package directory)."""
        assert file_dirs.CUR_DIR.name == "speller"
        
    def test_frozen_immutability(self) -> None:
        """Frozen dataclass prevents attribute mutation.

        pytest.raises() is a CONTEXT MANAGER that verifies an
        exception is raised. If the exception is NOT raised,
        the test FAILS.

        Pattern:
            with pytest.raises(ExpectedException):
                code_that_should_raise()
        """
        with pytest.raises(AttributeError):
            file_dirs.CUR_DIR = "hacked"  # type: ignore[misc]
            
    def test_log_file_path(self) -> None:
        """log_file property returns a Path in LOG_DIR."""
        log_file = file_dirs.log_file
        assert log_file.parent == file_dirs.LOG_DIR
        assert log_file.name == "speller.log"
        
        
class TestFileHandlerConfig:
    """Test FileHandlerConfig frozen dataclass with validation."""
       
    def test_default_values(self) -> None:
        """Default config values are sensible."""
        assert fhandler_config.ENCODING == "utf-8"
        assert fhandler_config.BACKUP_COUNT == 3
        assert fhandler_config.FILE_MB == 5
        
    def test_max_log_bytes_computation(self) -> None:
        """max_log_bytes property computes correctly.

        5 MB * 1024 KB * 1024 bytes = 5,242,880 bytes
        """
        expected = 5 * 1024 * 1024
        assert fhandler_config.max_log_bytes == expected
        
    def test_negative_backup_count_raises(self) -> None:
        """Negative BACKUP_COUNT raises ValueError in __post_init__.

        This tests the VALIDATION logic — frozen dataclass fields
        are validated during construction, not after.
        """
        # match= checks that the exception's error message contains a specific
        # pattern, not just that the right exception type was raised.
        #
        # This only passes if a ValueError is raised and its message
        # contains "BACKUP_COUNT".If the wrong ValueError fires, the test fails.
        with pytest.raises(ValueError, match="BACKUP_COUNT"):
            FileHandlerConfig(BACKUP_COUNT=-1)
            
    def test_zero_file_mb_raises(self) -> None:
        """Zero FILE_MB raises ValueError."""
        with pytest.raises(ValueError, match="FILE_MB"):
            FileHandlerConfig(FILE_MB=0)
            
    def test_custom_valid_config(self) -> None:
        """Custom config with valid values succeeds."""
        config = FileHandlerConfig(FILE_MB=10, BACKUP_COUNT=5)
        assert config.FILE_MB == 10
        assert config.BACKUP_COUNT == 5
        assert config.max_log_bytes == 10 * 1024 * 1024
        


# =============================================================================
# REFERENCE GUIDES
# =============================================================================
# =====================================================
# pytest.raises(Exception, match=)
# =====================================================  

# What match= actually does
# match= is a regex pattern run against str(exception). It uses re.search(),
# which means it looks for the pattern anywhere in the message — you don't
# need to match the full string.

# All of these would match ValueError("BACKUP_COUNT must be positive (> 0)")
#   match="BACKUP_COUNT"           # substring match
#   match="must be positive"       # different part of the message
#   match=r"BACKUP_COUNT.*positive" # regex — anything between the two words
#   match="BACKUP"                 # partial word match

# Use match= when the same exception type can be raised from multiple paths and
# you need to confirm you hit the right one. In your FileHandlerConfig, four fields
# each raise ValueError — without match=, you can't tell which guard fired.