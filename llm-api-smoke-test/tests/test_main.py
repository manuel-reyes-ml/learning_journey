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

class TestLLMApiArgs:
    """LLMApiArgs is frozen + keyword-only — verify the shape."""
    
    def test_construction_all_fields(self) -> None:
        """All five fields, all keyword-only."""
        args = LLMApiArgs(
            prompts=["hello"],
            provider=["anthropic"],
            run_async=False,
            verbose=True,
            no_log_file=False,
        )
        
        assert args.prompts == ["hello"]
        assert args.provider == ["anthropic"]
        assert args.run_async is False
        assert args.verbose is True
        assert args.no_log_file is False
        
    def test_positional_construction_rejected(self) -> None:
        """KW_ONLY marker means positional construction must fail."""
        # All fields after the KW_ONLY marker are kw-only.  Trying to
        # pass them positionally raises TypeError.
        with pytest.raises(TypeError):
            LLMApiArgs(
                ["hello"], ["anthropic"], False, True, False  # type: ignore[misc]
            )
      
      
# =============================================================================
# _build_parser — the argparse parser
# =============================================================================

class TestBuildParser:
    """Test the parser's behaviour via parse_args() — DON'T patch internals."""
    
    def test_minimal_invocation_defaults(self) -> None:
        """``llm-api-smoke-test anthropic`` → sensible defaults."""
        parser = _build_parser()
        args = parser.parse_args(["anthropic"])
        
        assert args.provider == ["anthropic"]
        # No prompt flag → defaults to None (resolved later in _resolve_prompts).
        assert args.prompts is None
        assert args.prompt is None
        assert args.prompt_file is None
        # Defaults for booleans.
        assert args.run_async is False
        assert args.verbose is False
        assert args.no_log_file is False
        
    def test_multiple_providers_collected_as_list(self) -> None:
        """nargs='+' collects each positional arg into a list."""
        parser = _build_parser()
        args = parser.parse_args(["anthropic", "gemini"])
        
        assert args.provider == ["anthropic", "gemini"]
        
    def test_prompts_space_separated(self) -> None:
        """--prompts 'a' 'b' → list of two."""
        parser = _build_parser()
        args = parser.parse_args(["anthropic", "--prompts", "first", "second"])
        
        assert args.prompts == ["first", "second"]
        
    def test_prompt_repeated_falg(self) -> None:
        """--prompt 'a' --prompt 'b' → list of two (action='append')."""
        parser = _build_parser()
        args = parser.parse_args([
            "athropic", "--prompt", "first", "--prompt", "second",
        ])
        
        assert args.prompt == ["first", "second"]
        
    def test_mutually_exclusive_prompts_rejected(self) -> None:
        """--prompts AND --prompt at the same time → argparse error."""
        parser = _build_parser()
        
        # argparse calls sys.exit(2) on mutex group violation; pytest
        # captures it as a SystemExit.
        with pytest.raises(SystemExit):
            parser.parse_args([
                "anthropic", "--prompts", "a", "--prompt", "b",
            ])
            
    def test_async_flag_sets_run_async_attr(self) -> None:
        """--async → args.run_async = True (renamed via dest=)."""
        parser = _build_parser()
        args = parser.parse_args(["anthropic", "--async"])
        
         # Not args.async (reserved word) — args.run_async because dest=.
        assert args.run_async is True
        
    def test_verbose_short_and_long_form(self) -> None:
        """-v and --verbose are equivalent."""
        parser = _build_parser()
        
        args1 = parser.parse_args(["anthropic", "-v"])
        args2 = parser.parse_args(["anthropic", "--verbose"])
        
        assert args1.verbose is True
        assert args2.verbose is True
        

# =============================================================================
# _validate_providers
# =============================================================================

   