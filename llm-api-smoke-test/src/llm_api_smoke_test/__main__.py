"""CLI entry point for the llm_api_smoke_test package.

Runs when the user executes::

    $ python -m llm_api_smoke_test [provider ...] [--prompts PROMPT ...]
    $ llm-api-smoke-test [provider ...]      (via pyproject.toml scripts)

This module is the COMPOSITION ROOT — the single place that:

1. Parses CLI arguments and converts them to a typed :class:`LLMApiArgs`.
2. Configures structlog + stdlib logging via
   :func:`~llm_api_smoke_test.logger.configure_structured_logging`.
3. Loads validated provider settings from environment via
   :class:`~llm_api_smoke_test.config.SmokeTestSettings`.
4. Resolves provider keys against :data:`~llm_api_smoke_test.register.dicts`
   and instantiates the chosen concrete adapters (sync or async, taken
   from the matching :class:`~llm_api_smoke_test.register.ProviderList`).
5. Dispatches to :func:`~llm_api_smoke_test.runner.run_smoke_tests` (sync)
   or :func:`~llm_api_smoke_test.batch_runner.batch_smoke_test` (async).
6. Maps domain exceptions to :class:`ExitCode` and returns it.

No other module imports from ``__main__.py`` — it imports from everything
else.  It sits at the top of the dependency chain.

Roadmap relevance
-----------------
The composition-root + typed-CLI-args + registry-lookup pattern carries
forward to DataVault (``QueryEngine`` provider selection), PolicyPulse
(vector-store selection), and every Stage 2+ project with swappable
backends.  The sync/async dual-registration pattern in particular shows
up again in DataVault where the same provider exposes both blocking
and concurrent code paths.
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
    sys.exit(f"Error missing llm_api_smoke_test module.\nDetails: {e}")
    

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
    """POSIX-aligned process exit codes for the llm-api-smoke-test CLI.

    ``IntEnum`` values are passed directly to ``sys.exit()``.
    ``@unique`` prevents accidental duplicate values at definition time.

    Attributes
    ----------
    SUCCESS : int
        ``0`` — normal completion; every provider returned a response.
    CONFIG_ERROR : int
        ``1`` — configuration failure.  Raised when
        :class:`~llm_api_smoke_test.config.SmokeTestSettings` cannot
        load required env vars or rejects a placeholder API key.
    PROVIDER_ERROR : int
        ``2`` — at least one provider's ``smoke_test()`` raised.
        Returned even if other providers succeeded, so CI runs fail
        loudly on any provider regression.
    KEYBOARD_INTERRUPT : int
        ``130`` — standard shell convention for Ctrl-C / SIGINT.

    Examples
    --------
    >>> sys.exit(ExitCode.SUCCESS)
    >>> ExitCode.SUCCESS == 0           # IntEnum compares to int
    True

    Notes
    -----
    Why fail on *any* provider error (not just all)?
        This is a smoke test — its job is to surface broken keys
        before downstream code burns time discovering them.  A
        partial failure means at least one credential is wrong;
        signal that to CI immediately rather than letting the user
        deploy with a half-working config.
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
    """Typed container for parsed CLI arguments.

    Converts ``argparse.Namespace`` — whose attributes are typed as
    ``Any`` — into a fully typed, immutable dataclass.  Pyright then
    has complete static coverage for every ``args.*`` access in
    ``main()`` and helper functions, catching typos and type
    mismatches at analysis time rather than at runtime.

    ``frozen=True`` prevents accidental mutation after construction.
    Constructed once in ``main()`` immediately after ``parse_args()``;
    passed by value to helper functions.

    Attributes
    ----------
    prompts : list of str
        One or more user messages to send to each selected provider.
        Defaults to ``[DEFAULT_PROMPT]`` when ``--prompts`` is omitted.
    provider : list of str
        Registry key(s) selecting which provider adapter(s) to run.
        Always a list (argparse ``nargs="+"``) even when one provider
        is requested.  Validated against
        :data:`~llm_api_smoke_test.register.dicts` by
        :func:`_validate_providers` before use.
    verbose : bool
        ``True`` enables ``DEBUG``-level console logging.

    Notes
    -----
    The same typed-dataclass CLI args pattern applies to every future
    project's CLI layer: ``DataVaultArgs``, ``PolicyPulseArgs``,
    ``FormSenseArgs``.  Reuses the pattern established in
    :mod:`speller.__main__`.
    """
    
    _: KW_ONLY  # Everything after is keyword-only
    prompts: list[str]
    provider: list[str]
    verbose: bool
    

# =============================================================================
# INTERNAL HELPER FUNCTIONS
# =============================================================================

# Extracting parser construction into its own function means tests can parse
# arguments without running the full program.
def _build_parser() -> argparse.ArgumentParser:
    """Build and return the CLI argument parser.

    Separated from ``main()`` for two reasons:

    1. Single responsibility — parsing logic is isolated and testable.
    2. Testability — tests can call ``_build_parser().parse_args([...])``
       without running ``main()``.

    Returns
    -------
    argparse.ArgumentParser
        Configured parser ready to parse ``sys.argv``.

    Notes
    -----
    Why ``RawDescriptionHelpFormatter``?
        Without it, argparse collapses newlines in ``epilog`` and
        wraps the example block.  The raw formatter preserves the
        formatting so the example list reads cleanly in ``--help``.

    Why ``nargs="+"`` (not ``nargs="*"``)?
        ``+`` requires at least one value when the flag is given;
        ``*`` would allow ``--prompts`` with no value.  Combined with
        a non-empty ``default``, this gives the user "select all" by
        omitting the flag entirely while still validating any
        explicit selection.

    Why ``default=list(dicts.keys())`` for ``provider``?
        Reading defaults from the registry — not a hard-coded literal —
        means new providers added via ``@register_class`` become
        available to the CLI without any change here.

    Why ``type=str`` for both list-valued options?
        ``argparse`` calls ``type(value)`` per token in an ``nargs="+"``
        argument, so the converter must be a per-element function
        (``str``), not a container type.  An earlier draft used
        ``type=list[str]`` which crashed at parse time.
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
        "--prompts",
        nargs="+",  # one or more
        type=str,  # argparse calls type(value) per token
        default=[DEFAULT_PROMPT],
        help=(
            "Enter one or more prompts to be sent to LLM provider(s). "
            "Use ',' to separate prompts."
        ),
    )
    
    # -- Optional flags --
    parser.add_argument(
        "-v", "--verbose",
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
    """Validate and normalise requested provider names.

    Strips whitespace and trailing punctuation from each name,
    lower-cases it, and checks the result against the live
    :data:`~llm_api_smoke_test.register.dicts` registry.

    Parameters
    ----------
    providers : list of str
        Raw provider keys from ``args.provider``.

    Returns
    -------
    list of str
        Cleaned, validated provider keys ready for registry lookup.
        Order matches the input.

    Raises
    ------
    KeyError
        If any name (after cleaning) is not in :data:`dicts`.
        The error message lists every available registered provider.

    Examples
    --------
    >>> _validate_providers(["anthropic"])
    ['anthropic']
    >>> _validate_providers(["Anthropic", "Gemini."])
    ['anthropic', 'gemini']
    >>> _validate_providers(["bogus"])
    Traceback (most recent call last):
        ...
    KeyError: "Unknown provider 'bogus'. Available: anthropic, gemini"

    Notes
    -----
    Cleaning lets users be sloppy with quoting and shell expansion
    (``"anthropic,"`` becomes ``"anthropic"``) without sacrificing
    strict validation against the registry.

    Each validated name returns a :class:`ProviderList` — to choose
    between the sync and async backend variants, the caller selects
    ``.sync_provider`` or ``.async_provider`` based on whether
    ``run_smoke_tests`` or ``batch_smoke_test`` is being dispatched.
    """
    clean_names = [name.strip().strip(string.punctuation).lower() for name in providers]
    
    for name in clean_names:
        # This validates against the actual registry,
        # which is the single source of truth.
        if name not in dicts:
            raise KeyError(f"Unknown provider '{name}. Available: {provider_list}")
        
    return clean_names