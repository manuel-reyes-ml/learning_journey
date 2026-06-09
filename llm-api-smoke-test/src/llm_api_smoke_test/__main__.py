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
    from typing import Final, Literal, overload, TYPE_CHECKING, NoReturn

    from llm_api_smoke_test.config import SmokeTestSettings
    from llm_api_smoke_test.logger import get_structured_logger

    from llm_api_smoke_test.batch_runner import batch_smoke_test
    from llm_api_smoke_test.register import dicts
    from llm_api_smoke_test.runner import DEFAULT_PROMPT, run_smoke_tests
    
except ImportError as e:
    sys.exit(f"Error missing llm_api_smoke_test module.\nDetails: {e}")
    
# Runtime skips, type checkers includes. 
if TYPE_CHECKING:
    from llm_api_smoke_test.providers import (
        LLMProvider,
        AsyncLLMProvider,
    )


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
    run_async: bool
    verbose: bool
    no_log_file: bool
    
    

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
            "   %(prog)s anthropic gemini\n"
            "   %(prog)s --prompts 'what is 2+2' 'hello world'\n"
            "   %(prog)s --prompt 'first' --prompt 'second'\n"
            "   %(prog)s --prompts-file prompts.txt\n"
            "   %(prog)s --async --verbose"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    
    # -- Positional: which providers --
    # nargs="+" means "one or more values". argparse calls type(value) on EACH
    # token, so type=str (per-element) is right; type=list[str] would crash.
    parser.add_argument(
        "provider",
        nargs="+",  # one or more arguments
        type=str,  # argparse calls type(value) per token
        default=list(dicts.keys()),
        help=f"LLM providers to use. Default runs all: {provider_list}.",
    )
    
    # -- Mutually exclusive group for prompt input --
    # An MX group means "at most one of these may be set" — argparse refuses to
    # parse if the user passes more than one. This prevents the ambiguity of
    # "which prompts do I run if both --prompts AND --prompts-file are given?"
    prompt_group = parser.add_mutually_exclusive_group()
    
    # OPTION A — space-separated list (current pattern, kept)
    # Best for: 1-3 short prompts, scripted use.
    prompt_group.add_argument(
        "--prompts",
        nargs="+",  # one or more
        type=str,  # argparse calls type(value) per token
        default=None,  # None = "user didn't pass --prompts" (vs an empty list)
        help=(
            "One or more prompts (space-separated). "
            "Quote each prompt that contains spaces."
        ),
    )
    
    # OPTION B — repeated flag (production pattern from git/docker/curl)
    # Best for: prompts with weird characters, interactive use.
    # action="append" means each --prompt invocation appends to a list.
    prompt_group.add_argument(
        "--prompt",
        action="append",
        type=str,
        default=None,
        help=(
            "A single prompt. Repeat the flag for multiple prompts: "
            "--prompt 'first' --prompt 'second'."
        ),
    )

    # OPTION C — file-based (for batch / programmatic use)
    # Best for: >5 prompts, prompts version-controlled with code.
    # type=argparse.FileType("r") opens the file and gives you a file object.
    # ⚠️ This leaks file handles in long-running programs; for a smoke test
    # that runs once and exits, it's fine.
    prompt_group.add_argument(
        "--prompts-file",
        type=argparse.FileType("r", encoding="utf-8"),
        default=None,
        help=(
            "Read prompts from a file, one per line. "
            "Lines starting with '#' are treated as comments and ignored."
        ),
        
    )
    
    # -- Mode flag: sync vs async --
    # Even with one prompt, async exercises the AsyncLLMProvider path —
    # important for smoke-testing the async adapters before the real
    # batch workload (DataVault) hits them.
    parser.add_argument(
        "--async",
        action="store_true",
        dest="run_async",  # 'async' is a reserved word - rename via dest
        default=False,
        help="Run the async batch runner with concurrency + rate-limit caps.",
    )
    
    # -- Standard flags --
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
    clean_names = [
        name.strip().strip(string.punctuation).lower()
        for name in providers
    ]
    
    for name in clean_names:
        # This validates against the actual registry,
        # which is the single source of truth.
        if name not in dicts:
            raise KeyError(f"Unknown provider '{name}'. Available: {provider_list}")
        
    return clean_names


def _resolve_prompts(args: argparse.Namespace) -> list[str]:
    """Pick the right prompt source from the mutually-exclusive group.

    Returns the user-supplied prompts, falling back to ``[DEFAULT_PROMPT]``
    if none of the three input flags were used.

    Parameters
    ----------
    args : argparse.Namespace
        Parsed CLI arguments — must have ``prompts``, ``prompt``, and
        ``prompts_file`` attributes (all may be ``None``).

    Returns
    -------
    list of str
        Non-empty list of prompts to run.  Whitespace-only lines from
        ``--prompts-file`` are filtered out; comments (lines starting
        with ``#``) are skipped.

    Raises
    ------
    ValueError
        If the prompts file is empty after filtering.
    """
    # Priority order matches argparse's mutual exclusion — at most ONE of
    # these three is non-None thanks to add_mutually_exclusive_group.
    
    # --- Case 1: --prompts "a" "b" "c" ---
    if args.prompts is not None:
        return args.prompts
    
    # --- Case 2: --prompt "a" --prompt "b" ---
    if args.prompt is not None:
        return args.prompt
    
    # --- Case 3: --prompts-file FILE ---
    if args.prompts_file is not None:
        # argparse already opened the file via FileType("r"). 'with' here
        # for the close — argparse doesn't close it automatically.
        with args.prompts_file as f:
            lines = [
                stripped
                for raw_line in f
                # Strip whitespace and skip empty lines + comments
                # ':=' is a walrus operator that assigns the value to the variable and returns it.
                # It is equivalent to:
                # stripped = raw_line.strip()
                # if stripped and not stripped.startswith("#"):
                #     return stripped
                if (stripped := raw_line.strip()) and not stripped.startswith("#")
            ] 
            
        # Fail fast if the file existed but had no real prompts.
        # ValueError is the right boundary signal — main() catches it and
        # exits with CONFIG_ERROR.
        if not lines:
            raise ValueError(
                "Prompts file is empty or contains only comments: "
                f"{args.prompts_file.name}"
            )
            
        return lines
    
    # --- Default: no prompt flag at all ---
    # Single-prompt list keeps the downstream loop uniform — runners
    # always iterate, never special-case "one vs many".
    return [DEFAULT_PROMPT]


# @overload decorator -- Tells the type checker "this signature is one of
# multiple possible shapes" — only the type checker sees overload variants;
# they're invisible at runtime.
# ─── Overload 1: run_async=True → async providers ─────────────────────
@overload
def _build_providers(
    provider_names: list[str],
    settings: SmokeTestSettings,
    *,
    run_async: Literal[True],       # ← the discriminator
) -> list[AsyncLLMProvider]: ...

# ─── Overload 2: run_async=False → sync providers ─────────────────────
@overload
def _build_providers(
    provider_names: list[str],
    settings: SmokeTestSettings,
    *,
    run_async: Literal[False],      # ← the discriminator
) -> list[LLMProvider]: ...

# ─── Implementation: NO @overload decorator, accepts plain bool ──────
def _build_providers(
    provider_names: list[str],
    settings: SmokeTestSettings,
    *,
    run_async: bool,
) -> list[LLMProvider] | list[AsyncLLMProvider]:
    """Instantiate provider adapters from registry keys + settings.

    Parameters
    ----------
    provider_names : list of str
        Validated registry keys (output of :func:`_validate_providers`).
    settings : SmokeTestSettings
        Loaded API keys and model names from environment.
    run_async : bool
        ``True`` picks ``async_provider`` slots; ``False`` picks
        ``sync_provider`` slots from each
        :class:`~llm_api_smoke_test.register.ProviderList`.

    Returns
    -------
    list of LLMProvider or list of AsyncLLMProvider
        Instances ready to be passed to the runner.  The return type
        depends on ``run_async``.

    Raises
    ------
    ValueError
        If the requested ``kind`` slot is ``None`` for any provider —
        means the user asked for ``--async`` but no async adapter
        was registered for that provider name.
    """
    # Adapter to the per-provider settings shape (each provider needs
    # its own ProviderSettings with name + api_key + model).
    config = settings.to_smoke_test_config()
    
    # Map registry key → its ProviderSettings. Centralised here so
    # __main__ doesn't need to know how SmokeTestConfig is structured.
    settings_map = {
        "anthropic": config.anthropic,
        "gemini": config.gemini,
    }
    
    # Choose which slot to read from each ProviderList.
    # f-string ensures kind matches the field name exactly.
    kind = "async" if run_async else "sync"
    slot_attr = f"{kind}_provider"
    
    instances = []
    for name in provider_names:
        bundle = dicts[name]      # ProviderList
        # Looks up an attribute by string name. 
        # Equivalent to writing bundle.sync_provider or
        # bundle.async_provider based on the runtime kind.
        #
        # it's how you write code that handles dynamic attribute names cleanly.
        info = getattr(bundle, slot_attr)       # DictInfo | None
        
        # Fail loudly if the requested kind isn't registered.
        # This catches "user asked for --async but only sync exists".
        if info is None:
            raise ValueError(
                f"No {kind} provider registered for '{name}'. "
                f"Either register one with @register_class('{name}', '{kind}', ...) "
                f"or omit --{kind} from the command line."
            )
          
        # info.provider_class is the CLASS (e.g. AnthropicProvider).
        # Calling it with (ProviderSettings) constructs an instance,
        # to access the Api key for that provider.
        # The type checker knows this returns LLMProvider | AsyncLLMProvider.
        instance = info.provider_class(settings_map[name])
        instances.append(instance)
        
        # Structured event — one per provider built, useful for diagnosing
        # "did the provider even initialize?" before the API call runs.
        slogger.info(
            "provider_built",
            registry_key=name,
            class_name=info.class_name,
            kind=kind,
        )
        
    return instances


# =============================================================================
# MAIN FUNCTION
# =============================================================================

def main(argv: list[str] | None = None) -> ExitCode:
    """
    """
    # ─── 1. Parse arguments ─────────────────────────────────────────
    # argparse owns argv=None → sys.argv[1:] resolution.
    # Tests pass argv=["anthropic", "--verbose"] to skip sys.argv.
    parser = _build_parser()
    raw = parser.parse_args(argv)
    
    # ─── 2. Resolve prompts from whichever flag was used ─────────────
    # Wrapped in try/except so file-not-found and empty-file errors
    # become CONFIG_ERROR (1) — they're user input problems.
    try:
        prompts = _resolve_prompts(raw)
    except (ValueError, FileNotFoundError) as exc:
        # `print` to stderr because logging isn't configured yet
        # — argparse and prompt resolution happen BEFORE configure_logging.
        print(f"Configuration Error: {exc}", file=sys.stderr)
        return ExitCode.CONFIG_ERROR
    
    # ─── 3. Validate provider names against the registry ─────────────
    try:
        provider_names = _validate_providers(raw.provider)
    except KeyError as exc:
        print(f"Configuration error: {exc}", file=sys.stderr)
        return ExitCode.CONFIG_ERROR
    
    # ─── 4. Build the typed args dataclass ────────────────────────────
    # Everything that touches args from here on gets full Pyright
    # coverage. raw.* has type Any; args.* has concrete types.
    args = LLMApiArgs(
        prompts=prompts,
        provider=provider_names,
        run_async=raw.run_async,
        verbose=raw.verbose,
        no_log_file=raw.no_log_file,
    )
    
    # ─── 5. Configure logging ─────────────────────────────────────────
    # NOW the structured logger is live — every subsequent log call
    # routes through structlog + the file handler.
    from llm_api_smoke_test.logger import configure_structured_logging
    configure_structured_logging(
        console_verbose=args.verbose,
        log_to_file=not args.no_log_file,
    )
    
    logger.debug(f"Parsed arguments: {raw}")
    slogger.info(
       "smoke_test_started",
       providers=args.provider,
       prompt_count=len(args.prompts),
       run_async=args.run_async, 
    )
    
    # ─── 6. Load settings (Pydantic validates env vars) ──────────────
    try:
        # SmokeTestSettings reads ANTHROPIC_API_KEY, GEMINI_API_KEY,
        # ANTHROPIC_MODEL, GEMINI_MODEL from env / .env file.
        # Placeholder check runs inside ProviderSettings._reject_placeholder.
        settings = SmokeTestSettings()  # type: ignore[call-arg]
        # ↑ Pydantic populates from env, but mypy doesn't see that — the
        # type: ignore is the standard documented workaround.
    except Exception as exc:
        # ValidationError is a Pydantic class — catching Exception is
        # broad on purpose because we don't want to import the specific
        # Pydantic exception type at the top of __main__.
        slogger.error("settings_load_failed", error=str(exc))
        return ExitCode.CONFIG_ERROR
    
    
    # ─── 7. Dispatch to the right runner ──────────────────────────────
    # The branches return DIFFERENT tuple shapes but BOTH conform to
    # tuple[list[SmokeTestResult], list[CallFailure]] — so the
    # downstream success/failure check below is identical.
    try:
        # You must branch on the bool BEFORE the call and pass True / False
        # literals — not a variable holding a bool — for the type checker
        # to pick the right overload.
        if args.run_async:
            providers = _build_providers(
                provider_names=args.provider,
                settings=settings,
                run_async=True,     # explicit Literal
            )
            
            # asyncio.run creates a new event loop, runs the coroutine,
            # and tears the loop down. The only place we touch the
            # event-loop lifecycle in this whole package.
            import asyncio
            successes, failures = asyncio.run(
                batch_smoke_test(
                    providers=providers,  # Iterable(list), not Iterator
                    prompts=args.prompts,
                )
            )
            # Pass an iterator — recipient gets a one-shot cursor over the container
            # iter(container) returns a fresh iterator object — a stateful
            # cursor that yields elements one at a time and remembers its position.
            # A list is the container itself; iterating it creates a new iterator
            # each time under the hood.
            
        else:
            providers = _build_providers(
                provider_names=args.provider,
                settings=settings,
                run_async=False,     # explicit Literal
            )
            
            # Sync path — run one prompt against all providers.
            # For multiple prompts in sync mode, iterate the prompts
            # list and accumulate. Simplest possible shape.
            successes = []
            failures = []
            for prompt in args.prompts:
                s, f = run_smoke_tests(
                    providers=providers,  # Iterable(list), not Iterator
                    prompt=prompt,
                )
                successes.extend(s)
                failures.extend(f)

    except KeyboardInterrupt:
        # User pressed Ctrl-C — graceful exit with the POSIX 130 code.
        logger.warning("interrupted_by_user")
        return ExitCode.KEYBOARD_INTERRUPT
    
    except ValueError as exc:
        slogger.error("provider_build_failed", error=str(exc))
        return ExitCode.CONFIG_ERROR
    
    # ─── 8. Summarise + decide exit code ──────────────────────────────
    slogger.info(
        "smoke_test_completed",
        success_count=len(successes),
        failure_count=len(failures),
        success_providers=[r.provider_name for r in successes],
        failure_providers=[name for name, _ in failures],
    )
    
    # Any failure → exit non-zero so CI catches it.
    # This is the "fail on any provider error" rule documented on ExitCode.
    if failures:
        return ExitCode.PROVIDER_ERROR
    
    return ExitCode.SUCCESS


# =============================================================================
# CONSOLE ENTRY
# =============================================================================

# NoReturn annotation honesty:
#   sys.exit() raises SystemExit — it never returns control. The NoReturn type tells
#   the type checker (and human readers) "no code after this line will execute."
#   Mypy and Pyright use this to suppress unreachable-code warnings and to
#   type-check exhaustively.
def cli_entry() -> NoReturn:
    """Console-script entry point. Calls main() and exits with its code.
    
    Notes
    -----
    Declared as ``NoReturn`` because ``sys.exit`` always raises
    ``SystemExit``. Referenced by ``[project.scripts]`` in
    ``pyproject.toml``.
    """
    # sys.exit translates the int return code into the process exit code
    # the shell sees. Returning from main() is preferred over calling
    # sys.exit() inside main() because it makes main() unit-testable.
    sys.exit(main())
    # any code here would be flagged as unreachable by the type checker
    
# ─── Module-level entry point ────────────────────────────────────────
# This block runs ONLY when the file is executed directly
# (python -m llm_api_smoke_test or python -m __main__.py).
# It does NOT run when the module is imported (Guard).
if __name__ == "__main__":
    cli_entry()