"""Shared pytest fixtures and hooks for the foundations test suite.

Why a guard against real API clients?
-------------------------------------
Unit tests must be fast, free and deterministic. A test that forgets to mock
``get_client()`` would build a real ``anthropic.Anthropic`` and, with a key in the
environment (your laptop's .env, a CI secret), spend real credits on every run.

The autouse fixture below makes that mistake LOUD: building a real client inside a
test raises immediately, with a message that says how to fix it. Tests that really
must call the API opt in with ``@pytest.mark.live_api`` and only run when pytest
is started with ``--run-live``, so CI never runs them by accident.
"""

# =============================================================================
# IMPORTS
# =============================================================================

from __future__ import annotations

from typing import Any, Final, NoReturn

import anthropic
import pytest

# =============================================================================
# CONSTANTS
# =============================================================================

LIVE_API_MARKER: Final[str] = "live_api"  # registered in pyproject.toml [tool.pytest.ini_options]
RUN_LIVE_FLAG: Final[str] = "--run-live"

# anthropic.Client / AsyncClient are aliases of these same class objects, so
# patching these two covers every import style.
_REAL_CLIENT_CLASSES: Final[tuple[type, ...]] = (anthropic.Anthropic, anthropic.AsyncAnthropic)

# =============================================================================
# HOOKS
# =============================================================================

# How it works: at startup pytest loads every conftest.py and installed plugin.
# It checks each function whose name starts with pytest_ against its list of known
# hook names. A match is registered and called at its fixed point in the run.
# A pytest_ name that doesn't match is reported as an error, so typos fail loudly.
# Arguments are passed by name, just like fixtures.
#
# A hook is a function with a name pytest knows. Because it's in conftest.py,
# pytest finds it and calls it at a fixed moment: after collecting all tests
# and before running any. You don't call it. As with fixtures, pytest matches
# the parameter names parser, config and items and passes in the right objects.


# pytest_addoption is a hook that runs at startup, before pytest reads the command line.
# parser.addoption adds --run-live to the list of flags pytest accepts, the same way
# Python's argparse works.
def pytest_addoption(parser: pytest.Parser) -> None:
    """Register ``--run-live`` so pytest accepts it (unknown flags are a usage error)."""
    parser.addoption(
        RUN_LIVE_FLAG,
        action="store_true",  # flag present -> True, absent -> False
        default=False,
        help="run @pytest.mark.live_api tests that call the real Anthropic API (costs money)",
    )


# - pytest.Config is the settings for the whole run: pyproject + CLI flags + plugins.
# - pytest.Item is one collected test -> Each test case becomes one Item. Parametrized
#   tests become several: your guard file has 3 test functions but collected 5 Items,
#   because the parametrize became [sync], [async] and [sync-alias].
def pytest_collection_modifyitems(config: pytest.Config, items: list[pytest.Item]) -> None:
    """Skip every ``@pytest.mark.live_api`` test unless pytest was run with --run-live."""
    if config.getoption(RUN_LIVE_FLAG):  # was: os.environ.get("RUN_LIVE_API") == "1"
        return
    skip_live = pytest.mark.skip(reason=f"live API test: pass {RUN_LIVE_FLAG} to run")

    for item in items:
        # Returns the marker if the test has it, else None. That's the check in your hook.
        if item.get_closest_marker(LIVE_API_MARKER):
            # Attaches a marker after collection. Look at the last line of the demo: 'skip'
            # sits next to 'live_api'. That's your hook adding it. When pytest runs that Item,
            # it sees skip and reports it as skipped instead of running it.
            item.add_marker(skip_live)


# =============================================================================
# GUARD FIXTURES
# =============================================================================


@pytest.fixture(autouse=True)
def _block_real_anthropic_clients(
    request: pytest.FixtureRequest, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Fail any test that builds a real Anthropic client, unless marked ``live_api``.

    autouse=True: runs for every test in this folder without being requested.
    Patches the CLASS's __init__ (not a module name), so it catches the client no
    matter how it was imported: ``anthropic.Anthropic``, ``from anthropic import
    Anthropic``, or inside a third-party library such as pydantic-ai.
    """
    # The hook checks it before the run (to skip), and the fixture checks it during
    # the run (to let the test through)
    if request.node.get_closest_marker(LIVE_API_MARKER):
        return

    def _refuse(self: object, *args: Any, **kwargs: Any) -> NoReturn:
        # .node.nodeid is its full address, tests/test_conftest_guards.py::test_…[sync].
        # That's what -k filters and what the failure reports print.
        raise RuntimeError(
            f"{request.node.nodeid} tried to build a real {type(self).__name__}. "
            "Mock get_client() (see the fake_client fixture), "
            f"or mark the test @pytest.mark.{LIVE_API_MARKER} if it must call the API."
        )

    # Replacing all Anthropic and AsyncAnthropic classes __init__ therefore blocks every
    # import style at once, including clients that pydantic-ai builds internally.
    # MagicMock(spec=anthropic.Anthropic) still works, because spec= only reads the
    # class's attributes and never calls __init__.
    for cls in _REAL_CLIENT_CLASSES:
        monkeypatch.setattr(cls, "__init__", _refuse)
