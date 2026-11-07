""" """

from __future__ import annotations

import json
from typing import Final

from anthropic.types import TextBlock
from pydantic import BaseModel, Field, ValidationError

from learning_journey.claude.client import get_client


class Box7Explanation(BaseModel):
    """The CONTRACT for what the model must return.

    pydantic raises ValidationError on any violation — wrong type, missing
    field, out-of-range value. The model doesn't get to be creative here.
    """

    code: str = Field(pattern=r"^[1-9A-Z]$")  # exactly one code char
    meaning: str = Field(min_length=10, max_length=300)
    taxable_generally: bool
    participant_action_needed: bool
    confidence: float = Field(ge=0.0, le=1.0)  # ge/le = bounds


SYSTEM: Final[str] = """You classify IRS 1099-R Box 7 codes. Respond with ONLY a JSON
object matching this schema, no prose, no markdown fences:
{"code": str, "meaning": str, "taxable_generally": bool,
 "participant_action_needed": bool, "confidence": float 0-1}"""


def explain_box7(code: str) -> Box7Explanation:
    client, settings = get_client()
    response = client.messages.create(
        model=settings.claude_model,
        max_tokens=settings.default_max_tokens,
        system=SYSTEM,
        messages=[
            {"role": "user", "content": f"Code: {code}"},
            {"role": "assistant", "content": "```json"},
        ],
        stop_sequences=["```"],
    )
    raw = "".join([block.text for block in response.content if isinstance(block, TextBlock)])

    try:
        return Box7Explanation.model_validate(json.loads(raw))
    except (json.JSONDecodeError, ValidationError) as err:
        # Boundary rule: report loudly, never pass unvalidated data on.
        # (Flagship version will retry-with-feedback here; v0 fails clean.)
        raise ValueError(f"Model returned invalid output for {code!r}: {err} - Got: {raw}") from err


if __name__ == "__main__":
    result = explain_box7("G")
    print(f"{result.code}: {result.meaning}")
    print(f"taxable={result.taxable_generally} confidence={result.confidence:.0%}")
