""" """

from __future__ import annotations

import json
from collections.abc import Callable
from types import SimpleNamespace
from typing import Any, Final
from unittest.mock import MagicMock, create_autospec

import anthropic
import pytest
from anthropic.resources import Messages
from anthropic.types import TextBlock
from pydantic import ValidationError

from learning_journey.claude import day36_structured
from learning_journey.claude.day36_structured import SYSTEM, Box7Explanation, explain_box7

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
    #
    # spec=, limits the mock to the attributes the real class has.
    client = MagicMock(spec=anthropic.Anthropic, name="anthropic_client")

    # spec= only applies to the top level. client.mesages now raises an error,
    # but client.messages.creat would still be accepted.
    #
    # create_autospec(Messages, instance=True) covers the next level. It copies the real messages resource,
    # including the real signature of create. That catches both typos (creat → AttributeError) and wrong
    # arguments (for example, a missing max_tokens → TypeError).
    client.messages = create_autospec(Messages, instance=True)

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
        # return_value makes a mock return something, after its set.

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


def test_request_is_built_from_settings_and_prompt(
    fake_client: MagicMock,
    fake_settings: SimpleNamespace,
    respond_with: Callable[..., None],
) -> None:
    respond_with(json.dumps(VALID_PAYLOAD))

    explain_box7("G")

    fake_client.messages.create.assert_called_once()

    # .call_args returns a named call tuple with the arguments used in .create()
    # .kwargs returns the call_args in a key-value dictionary ->
    #   {'model': 'claude-test-model', 'max_tokens': 256, ...} from .create()
    kwargs = fake_client.messages.create.call_args.kwargs
    assert kwargs["model"] == fake_settings.claude_model
    assert kwargs["max_tokens"] == fake_settings.default_max_tokens
    assert kwargs["system"] == SYSTEM
    assert kwargs["messages"][0] == {"role": "user", "content": "Code: G"}
    # Prefill + stop sequence are what keep markdown fences out of the reply.
    assert kwargs["messages"][-1] == {"role": "assistant", "content": "```json"}
    assert kwargs["stop_sequences"] == ["```"]


# =============================================================================
# Boundary: off-contract output must be refused, for the RIGHT reason
# =============================================================================


@pytest.mark.parametrize(
    "payload",
    [
        pytest.param(VALID_PAYLOAD | {"confidence": 1.7}, id="confidence-above-1"),
        pytest.param(VALID_PAYLOAD | {"confidence": -0.1}, id="confidence-below-0"),
        pytest.param(VALID_PAYLOAD | {"code": "GG"}, id="code-two-chars"),
        pytest.param(VALID_PAYLOAD | {"code": "g"}, id="code-lowercase"),
        pytest.param(VALID_PAYLOAD | {"taxable_generally": "maybe"}, id="bool-not-bool"),
        pytest.param(
            {k: v for k, v in VALID_PAYLOAD.items() if k != "meaning"},
            id="missing-field",
        ),
    ],
)
def test_schema_violation_is_rejected(
    respond_with: Callable[..., None], payload: dict[str, Any]
) -> None:
    respond_with(json.dumps(payload))

    with pytest.raises(ValueError, match=r"invalid output for 'G'") as exc_info:
        explain_box7("G")

    # Proves the failure came from pydantic, not from some earlier accident.
    assert isinstance(exc_info.value.__cause__, ValidationError)


@pytest.mark.parametrize(
    "raw",
    [
        pytest.param("Sure! Here's the JSON:", id="chatty-prose"),
        pytest.param("", id="empty-reply"),
        pytest.param('{"code": "G", "meaning": "Direct Roll', id="truncated-max-tokens"),
    ],
)
def test_non_json_is_rejected(respond_with: Callable[..., None], raw: str) -> None:
    respond_with(raw)

    with pytest.raises(ValueError, match=r"invalid output for 'G") as exc_info:
        explain_box7("G")

    assert isinstance(exc_info.value.__cause__, json.JSONDecodeError)


def test_error_message_includes_raw_output_for_debugging(
    respond_with: Callable[..., None],
) -> None:
    respond_with("Sure! Here's the JSON:")

    with pytest.raises(ValueError, match=r"Got: Sure! Here's the JSON:"):
        explain_box7("G")
