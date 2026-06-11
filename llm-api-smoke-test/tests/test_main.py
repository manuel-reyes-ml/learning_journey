"""
"""

# =============================================================================
# IMPORTS
# =============================================================================

from __future__ import annotations

import pytest

from pathlib import Path

from llm_api_smoke_test.__main__ import (
    ExitCode,
    LLMApiArgs,
    _build_parser,
    _build_providers,
    _resolve_prompts,
    _validate_providers,
)

# =============================================================================
# ExitCode — the IntEnum contract
# =============================================================================

class TestExitCode:
    """ExitCode is an IntEnum — verify members and POSIX alignment."""
    
    def test_sucess_is_zero(self) -> None:
        """Exit 0 = POSIX success."""
        assert ExitCode.SUCCESS == 0
        
    def test_keyboard_interrupt_is_130(self) -> None:
        """POSIX convention: 130 = Ctrl-C interrupt."""
        assert ExitCode.KEYBOARD_INTERRUPT == 130
        
    def test_all_members_are_unique(self) -> None:
        """@unique guards against duplicate values at definition time.
        
        If someone adds a new member with a duplicate value, this test
        catches it instantly.
        """
        # e.value to access the int inside an IntEnum class (ExitCode)
        values = [e.value for e in ExitCode]
        assert len(values) == len(set(values))
        
        
# =============================================================================
# LLMApiArgs — the typed CLI args dataclass
# =============================================================================

