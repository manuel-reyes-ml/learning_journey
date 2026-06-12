"""Tests for llm_api_smoke_test.__main__.
 
Covers the composition root: CLI parsing, prompt resolution, provider
validation, build dispatch.  The actual main() function is harder to
test (it's the integration point) so we focus on the testable helpers.
 
Strategy
--------
- Test _build_parser() by parsing crafted argv lists and inspecting
  the resulting Namespace.
- Test _validate_providers and _resolve_prompts as pure functions.
- Skip main() integration here — covered in test_integration.py.
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

from llm_api_smoke_test.config import SmokeTestSettings

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
        assert args.prompts_file is None
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

class TestValidateProviders:
    """Test the cleaning + registry check."""
    
    def test_clean_lowercase_passes(self) -> None:
        """Lowercase known keys pass through unchanged."""
        result = _validate_providers(["anthropic"])
        assert result == ["anthropic"]
        
    def test_uppercase_normalized(self) -> None:
        """Case normalisation strips, lowercases."""
        result = _validate_providers(["ANTHROPIC"])
        assert result == ["anthropic"]
        
    def test_punctuation_stripped(self) -> None:
        """Trailing punctuation (e.g., shell comma) is stripped."""
        # User typed "anthropic," — shell quoted it as one token.
        result = _validate_providers(["anthropic,"])
        assert result == ["anthropic"]
        
    def test_unknown_provider_raises_keyerror(self) -> None:
        """Unregistered name → KeyError with the available list."""
        # NB: KeyError repr wraps the message in quotes; use the
        # 'match' regex to test substring presence.
        with pytest.raises(KeyError, match="bogus"):
            _validate_providers(["bogus"])
        
    def test_order_preserved(self) -> None:
        """Validation must not reorder input — composition root relies
        on positional correspondence later.
        """
        # Reverse-alphabetical input should come out reverse-alphabetical.
        result = _validate_providers(["gemini", "anthropic"])
        assert result == ["gemini", "anthropic"]
        

# =============================================================================
# _resolve_prompts
# =============================================================================

class TestResolvePrompts:
    """Test the mutual-exclusivity resolver and file-reading fallback."""
    
    def test_returns_prompts_list_when_set(self) -> None:
        """--prompts 'a' 'b' → returns the list as-is."""
        # Build a Namespace by hand — _resolve_prompts only reads
        # attributes, doesn't care about the parser context.
        import argparse
        ns = argparse.Namespace(
            prompts=["a", "b"],
            prompt=None,
            prompts_file=None,
        )
        
        assert _resolve_prompts(ns) == ["a", "b"]
        
    def test_returns_prompt_list_when_set(self) -> None:
        """--prompt 'a' --prompt 'b' → returns the appended list."""
        import argparse
        ns = argparse.Namespace(
            prompts=None,
            prompt=["a", "b"],
            prompts_file=None,
        )
        
        assert _resolve_prompts(ns) == ["a", "b"]
        
    def test_reads_from_file(self, tmp_path: Path) -> None:
        """--prompts-file FILE → reads, strips blanks + comments.
        
        tmp_path is pytest's built-in fixture for a temporary directory
        unique to this test.  Cleaned up automatically.
        """
        # Build a fake prompts file with mixed content.
        prompts_file = tmp_path / "prompts.txt"
        prompts_file.write_text(
            "first prompt\n"
            "# this is a comment, should be skipped\n"
            "\n"                # blank line, should be skipped
            "second prompt\n"
        )
        
        # Open the file the way argparse.FileType would.
        import argparse
        ns = argparse.Namespace(
            prompts=None,
            prompt=None,
            prompts_file=prompts_file.open("r", encoding="utf-8"),
        )
        
        result = _resolve_prompts(ns)
        # Only the real prompts came back — no comments, no blanks.
        assert result == ["first prompt", "second prompt"]
        
    def test_empty_file_raises_valueerror(self, tmp_path: Path) -> None:
        """File with only comments → ValueError, not silent empty result."""
        empty_file = tmp_path / "empty.text"
        empty_file.write_text("# onlt comments\n#nothing else\n")
        
        import argparse
        ns = argparse.Namespace(
            prompts=None,
            prompt=None,
            prompts_file=empty_file.open("r", encoding="utf-8"),
        )
        
        with pytest.raises(ValueError, match="empty"):
            _resolve_prompts(ns)
            
    def tet_no_flag_returns_default(self) -> None:
        """No prompt flag at all → falls back to [DEFAULT_PROMPT]."""
        from llm_api_smoke_test.runner import DEFAULT_PROMPT
        import argparse
        
        ns = argparse.Namespace(
            prompts=None,
            prompt=None,
            prompt_file=None,
        )
        
        result = _resolve_prompts(ns)
        assert result == [DEFAULT_PROMPT]
        
        
# =============================================================================
# _build_providers
# =============================================================================

class TestBuildProviders:
    """Verify the registry → instance dispatch.
    
    Uses real SmokeTestSettings (from conftest's settings fixture) but
    the providers themselves never make HTTP calls in their __init__ —
    they just configure the client.
    """
    
    def test_sync_path_returns_sync_instances(self, settings: SmokeTestSettings) -> None:
        """run_async=False → list of LLMProvider (sync) instances."""
        from llm_api_smoke_test.providers import AnthropicProvider
        
        instances = _build_providers(
            provider_names=["anthropic"],
            settings=settings,
            run_async=False,
        )
        
        assert len(instances) == 1
        # Specific class - the SYNC adapter.
        assert isinstance(instances[0], AnthropicProvider)
        
    def test_async_path_returns_async_instances(self, settings: SmokeTestSettings) -> None:
        """run_async=True → list of AsyncLLMProvider instances."""
        from llm_api_smoke_test.providers import AsyncAnthropicProvider
        
        instances = _build_providers(
            provider_names=["anthropic"],
            settings=settings,
            run_async=True,
        )
        
        assert isinstance(instances[0], AsyncAnthropicProvider)
        
    def test_unknown_provider_raises_keyerror(self, settings: SmokeTestSettings) -> None:
        """Provider name not in dicts → KeyError from the registry lookup.
        
        NB: this assumes _validate_providers wasn't called first.
        In main(), _validate_providers catches this earlier — but
        _build_providers is defensive in case it's called directly.
        """
        # The dict lookup itself raises KeyError on missing key.
        with pytest.raises(KeyError):
            _build_providers(
                provider_names=["nonexistent_provider"],
                settings=settings,
                run_async=False,
            )