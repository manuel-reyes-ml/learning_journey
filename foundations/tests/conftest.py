""" """

# =============================================================================
# IMPORTS
# =============================================================================

from __future__ import annotations

import os
from typing import Any, Final, NoReturn

import anthropic
import pytest

# =============================================================================
# CONSTANTS
# =============================================================================

LIVE_API_MARKER: Final[str] = "live_api"  # registered in pyproject.toml [tool.pytest.ini_options]
LIVE_API_ENV_VAR: Final[str] = "RUN_LIVE_API"

# anthropic.Client / AsyncClient are aliases of these same class objects, so
# patching these two covers every import style.
_REAL_CLIENT_CLASSES: Final[tuple[type, ...]] = (anthropic.Anthropic, anthropic.AsyncAnthropic)

# =============================================================================
# HOOKS
# =============================================================================


def pytest_collection_modifyitems(config: pytest.Config, items: list[pytest.Item]) -> None:
    """Skip every ``@pytest.mark.live_api`` test unless RUN_LIVE_API=1 is set."""
    if os.environ.get(LIVE_API_ENV_VAR) == "1":
        return
    skip_live = pytest.mark.skip(reason=f"live API test: set {LIVE_API_ENV_VAR}=1 to run")

    for item in items:
        if item.get_closest_marker(LIVE_API_MARKER):
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
    if request.node.get_closest_marker(LIVE_API_MARKER):
        return

    def _refuse(self: object, *args: Any, **kwargs: Any) -> NoReturn:
        raise RuntimeError(
            f"{request.node.nodeid} tried to build a real {type(self).__name__}. "
            "Mock get_client() (see the fake_client fixture), "
            f"or mark the test @pytest.mark.{LIVE_API_MARKER} if it must call the API."
        )

        for cls in _REAL_CLIENT_CLASSES:
            monkeypatch.setattr(cls, "__init__", _refuse)
