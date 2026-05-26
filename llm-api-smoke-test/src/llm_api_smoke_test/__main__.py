"""
"""

# =============================================================================
# IMPORTS
# =============================================================================

from __future__ import annotations

import sys

# =====================================================
# Import Guard
# =====================================================

# __main__.py is the FRONT DOOR — if imports fail, give a friendly
# error message and exit. This is the ONE place where sys.exit()
# on ImportError is correct, because the user explicitly ran the
# program and expects it to either work or explain why it can't.
#
# Every other module lets ImportError propagate upward to here.
try:
    import argparse
    import logging
    import string

    from dataclasses import dataclass, KW_ONLY
    from enum import IntEnum, unique
    from typing import Final, NoReturn

    from llm_api_smoke_test.config import SmokeTestSettings
    from llm_api_smoke_test.logger import get_structured_logger
    
    from llm_api_smoke_test.providers import (
        AnthropicProvider,
        GeminiProvider,
        LLMProvider,
        AsyncAnthropicProvider,
        AsyncGeminiProvider,
        AsyncLLMProvider,
    )

    from llm_api_smoke_test.batch_runner import batch_smoke_test
    from llm_api_smoke_test.register import dicts
    from llm_api_smoke_test.runner import DEFAULT_PROMPT, run_smoke_tests
    
except ImportError as e:
    sys.exit(f"Error missing speller module.\nDetails: {e}")
    

# =============================================================================
# LOGGER SETUP
# =============================================================================

# Use structlog on Python's stdlib since some external packages
# use stdlib still.
slogger = get_structured_logger(__name__)
logger = logging.getLogger(__name__)


# =============================================================================
# CONSTANTS CONFIGURATION
# =============================================================================
# =====================================================
# Constants
# =====================================================

provider_list: Final[str] = ", ".join(dicts.keys())


# =====================================================
# Class Constants Configuration
# =====================================================

@unique
class ExitCode(IntEnum):
    """POSIX-aligned process exit codes for the speller CLI.

    ``IntEnum`` values are passed directly to ``sys.exit()``.
    ``@unique`` prevents accidental duplicate values at definition time.

    Attributes
    ----------
    SUCCESS : int
        ``0`` — normal completion.
    USAGE_ERROR : int
        ``1`` — bad arguments or unknown operation name.
    FILE_NOT_FOUND : int
        ``2`` — dictionary or text file does not exist.
    LOAD_FAILED : int
        ``3`` — dictionary file found but ``load()`` returned ``False``.
    FAILURE : int
        ``4`` — unexpected exception caught in ``main()``.
    KEYBOARD_INTERRUPT : int
        ``130`` — standard shell convention for Ctrl-C / SIGINT.

    Examples
    --------
    >>> sys.exit(ExitCode.SUCCESS)       # process exits with code 0
    >>> ExitCode.SUCCESS == 0            # True — IntEnum compares to int
    True
    """
    
    SUCCESS = 0
    CONFIG_ERROR = 1
    PROVIDER_ERROR = 2
    KEYBOARD_INTERRUPT = 130
    

# =====================================================
# CLI Args Frozen Dataclass
# =====================================================

@dataclass(frozen=True)
class LLMApiArgs:
    """
    """
    
    _: KW_ONLY  # Everything after is keyword-only
    prompts: list[str]
    provider: str
    verbose: bool
    

# =============================================================================
# INTERNAL HELPER FUNCTIONS
# =============================================================================

# Extracting parser construction into its own function means tests can parse
# arguments without running the full program.
def _build_parser() -> argparse.ArgumentParser:
    """
    """
    # Without RawDescriptionHelpFormatter, argparse reformats your epilog text
    # — collapsing newlines and wrapping. It preserves your formatting so the
    # examples display cleanly.
    parser = argparse.ArgumentParser(
        prog="llm-api-smoke-test",
        description="Verify Anthropic + Gemini API keys with a single round trip each.",
        epilog=(
            "Examples:\n"
            "   %(prog)s --prompt What's the largest country in the world?\n"
            "   %(prog)s Anthropic\n"
            "   %(prog)s -v"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    
    # -- Positional arguments --
    parser.add_argument(
        "provider",
        nargs="+",  # one or more arguments
        type=str,  # argparse calls type(value) per token
        default=list(dicts.keys()),
        help=f"LLM providers to use. Default runs all: {provider_list}.",
    )
    
    # -- Keyword arguments --
    parser.add_argument(
        "--prp",
        nargs="+",  # one or more
        type=str,  # argparse calls type(value) per token
        default=[DEFAULT_PROMPT],
        metavar="PROMPTS",
        help=(
            "Enter one or more prompts to be sent to LLM provider(s). "
            "Use ',' to separate prompts."
        ),
    )
    
    # -- Optional flags --
    parser.add_argument(
        "--v", "--verbose",
        action="store_true",
        default=False,
        help="Enable verbose output (DEBUG-level logging).",
    )
    
    parser.add_argument(
        "--no-log-file",
        action="store_true",
        default=False,
        help="Disable file logging (console only).",
    )
    
    return parser


def _validate_providers(providers: list[str]) -> list[str]:
    """
    """
    clean_names = [name.strip().strip(string.punctuation).lower() for name in providers]
    
    for name in clean_names:
        # This validates against the actual registry,
        # which is the single source of truth.
        if name not in dicts:
            raise KeyError(f"Unknown provider '{name}. Available: {provider_list}")
        
    return clean_names