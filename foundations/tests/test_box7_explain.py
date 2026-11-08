""" """

from __future__ import annotations

from types import SimpleNamespace
from typing import Any, Final

from anthropic.types import TextBlock

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
