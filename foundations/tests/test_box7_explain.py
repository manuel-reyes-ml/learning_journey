""" """

from __future__ import annotations

import json
from collections.abc import Callable
from types import SimpleNamespace
from typing import Any, Final
from unittest.mock import MagicMock

import pytest
from anthropic.types import TextBlock

from learning_journey.claude import day36_structured
from learning_journey.claude.day36_structured import Box7Explanation, explain_box7

# =============================================================================
# Test data
# =============================================================================

VALID_PAYLOAD: Final[dict[str, Any]] = {
    "code": "G",
    "meaning": "Direct rollover to another qualified plan.",
    "taxable_generally": False,
    "participant_action_needed": False,
    "confidence": 0.97,
}


# SimpleNamespace is an empty object that you fill with attributes by passing keyword arguments.
# In your test it stands in for objects that explain_box7 reads: the SDK's response.
# 'response.content' -> list of blocks
#
# Your function never checks what type settings or response is. It only reads attributes from them.
# Python calls this duck typing: if it has the attributes your code reads, it works. So the fake only
# needs those attributes and nothing more.
def make_response(*texts: str) -> SimpleNamespace:
    """Build an object shaped like the SDK's Message: `.content` is a list of blocks.

    Real TextBlock objects, not MagicMocks, because explain_box7 filters with
    isinstance(block, TextBlock) and a MagicMock would be silently dropped.
    """
    # By using TextBlock your fake can't be malformed by accident. If the test builds it wrong,
    # pydantic raises an error right away, which is safer than a MagicMock.
    return SimpleNamespace(content=[TextBlock(type="text", text=t) for t in texts])


# =============================================================================
# Fixtures
# =============================================================================


@pytest.fixture
def fake_settings() -> SimpleNamespace:
    """Only the two attributes explain_box7 reads. Distinct values so we can assert on them."""
    return SimpleNamespace(claude_model="claude-test-model", default_max_tokens=256)


# monkeypatch is a fixture built into pytest. You get it by naming it as an argument,
# the same way you get fake_client.
# It lets a test temporarily replace something (a function, an attribute, an environment variable)
# and puts the original back when the test ends.
@pytest.fixture
def fake_client(monkeypatch: pytest.MonkeyPatch, fake_settings: SimpleNamespace) -> MagicMock:
    """Swap get_client *where explain_box7 looks it up* — no network, no API key needed.

    monkeypatch undoes the swap automatically when the test finishes.
    """
    # MagicMock(name="anthropic_client") makes error messages say anthropic_client.messages.create,
    # not <MagicMock id=1404...>. It's free debugging help.
    client = MagicMock(name="anthropic_client")

    # A module is just an object, and its global names are its attributes.
    # .setatr() It raises AttributeError if the attribute does not exist, unless you pass raising=False
    #
    # The replacement must accept the same arguments as 6the real call. The real get_client() takes none,
    # so the fake takes none. If they don't match, Python raises a TypeError.
    monkeypatch.setattr(day36_structured, "get_client", lambda: (client, fake_settings))
    #                   └─ which object ─┘ └─ which name ─┘ └─ new value ─────────────┘
    return client


@pytest.fixture
def respond_with(fake_client: MagicMock) -> Callable[..., None]:
    """Factory fixture: each test says what the "model" replies, in one line."""

    def _respond(*texts: str) -> None:
        fake_client.messages.create.return_value = make_response(*texts)
        #  client  → .messages (child) → .create (child) → "when called, return this"
        # return_value makes a mock return something.

    return _respond


# =============================================================================
# Happy path
# =============================================================================


def test_valid_payload_returns_validated_model(respond_with: Callable[..., None]) -> None:
    respond_with(json.dumps(VALID_PAYLOAD))

    result = day36_structured.explain_box7("G")

    assert isinstance(result, Box7Explanation)
    assert result == Box7Explanation(**VALID_PAYLOAD)  # every field, not just one


def test_text_split_across_blocks_is_joined(respond_with: Callable[..., None]) -> None:
    raw = json.dumps(VALID_PAYLOAD)
    respond_with(raw[:25], raw[25:])  # the SDK may return several text blocks

    assert explain_box7("G").code == "G"


def test_non_text_blocks_are_ignored(fake_client: MagicMock) -> None:
    other_block = SimpleNamespace(type="thinking", thinking="internal reasoning")
    text_block = TextBlock(type="text", text=json.dumps(VALID_PAYLOAD))
    fake_client.messages.create.return_value = SimpleNamespace(content=[other_block, text_block])

    assert explain_box7("G").code == "G"


# =============================================================================
# Request construction — the part of "prompt engineering" we CAN unit-test
# =============================================================================
