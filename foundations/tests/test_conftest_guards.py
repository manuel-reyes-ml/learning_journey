"""Tests for the safety guards in conftest.py — test infrastructure deserves tests too.

If someone deletes or breaks the guard, these fail first, before a forgotten mock
quietly starts spending API credits.
"""

# =============================================================================
# IMPORTS
# =============================================================================

from __future__ import annotations

from unittest.mock import MagicMock

import anthropic
import pytest

# =============================================================================
# EVALUATE Guard Fixture in conftest.py
# =============================================================================


@pytest.mark.parametrize(
    "client_cls",
    [
        pytest.param(anthropic.Anthropic, id="sync"),
        pytest.param(anthropic.AsyncAnthropic, id="async"),
        pytest.param(anthropic.Client, id="sync-alias"),
    ],
)
def test_real_client_construction_is_blocked(client_cls: type) -> None:
    with pytest.raises(RuntimeError, match=r"tried to build a real .*live_api"):
        client_cls(api_key="sk-ant-test-not-real")


def test_specced_mock_still_works() -> None:
    # spec= reads the class's attributes; it never calls __init__, so the guard allows it.
    fake = MagicMock(spec=anthropic.Anthropic)

    assert hasattr(fake, "messages")


@pytest.mark.live_api
def test_live_marker_opts_out_of_the_guard() -> None:
    # Only runs with `pytest --run-live`. Building a client costs nothing; calls do.
    client = anthropic.Anthropic(api_key="sk-ant-test-not-real")

    assert isinstance(client, anthropic.Anthropic)
