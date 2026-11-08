""" """

from __future__ import annotations

from collections.abc import Callable
from types import SimpleNamespace
from typing import Any, Final
from unittest.mock import MagicMock

import pytest
from anthropic.types import TextBlock

from learning_journey.claude import day36_structured

# =============================================================================
# Test data
# =============================================================================

VALID: Final[dict[str, Any]] = {
    "code": "G",
    "meaning": "Direct rollover to another qualified plan.",
    "taxable_generally": False,
    "participant_action_needed": False,
    "confidence": 0.97,
}


def make_response(*texts: str) -> SimpleNamespace:
    """Build an object shaped like the SDK's Message: `.content` is a list of blocks.

    Real TextBlock objects, not MagicMocks, because explain_box7 filters with
    isinstance(block, TextBlock) and a MagicMock would be silently dropped.
    """
    return SimpleNamespace(content=[TextBlock(type="text", text=t) for t in texts])


# =============================================================================
# Fixtures
# =============================================================================


@pytest.fixture
def fake_settings() -> SimpleNamespace:
    """Only the two attributes explain_box7 reads. Distinct values so we can assert on them."""
    return SimpleNamespace(claude_model="claude-test-model", default_max_tokens=256)


@pytest.fixture
def fake_client(monkeypatch: pytest.MonkeyPatch, fake_settings: SimpleNamespace) -> MagicMock:
    """Swap get_client *where explain_box7 looks it up* — no network, no API key needed.

    monkeypatch undoes the swap automatically when the test finishes.
    """
    client = MagicMock(name="anthropic_client")
    monkeypatch.setattr(day36_structured, "get_client", lambda: (client, fake_settings))
    return client


@pytest.fixture
def respond_with(fake_client: MagicMock) -> Callable[..., None]:
    """Factory fixture: each test says what the "model" replies, in one line."""

    def _respond(*texts: str) -> None:
        fake_client.messages.create.return_value = make_response(*texts)

    return _respond


# =============================================================================
# Happy path
# =============================================================================
