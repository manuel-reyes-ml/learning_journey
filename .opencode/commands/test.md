---
description: Run the test suite and report results (report only)
agent: plan
---

Run and interpret the test suite.

!`uv run pytest tests/ -v --tb=short`

For any failure:
- Show the test name and file path
- Show the assertion error / short traceback
- Suggest a likely fix in one sentence

Also flag, without fixing:
- Missing `_reset_structlog` fixture in `conftest.py` (a cached bound logger makes log
  assertions test stale config)
- Missing `_no_retry_sleeps` fixture (`stamina.set_active(False)`) — the suite is spending
  real seconds sleeping through backoffs
- Any real participant data or secrets in fixtures — synthetic only

If all pass, report the count and any coverage summary shown.
Do **NOT** modify any test or source files — report only.