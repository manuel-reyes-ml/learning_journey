---
description: Run the test suite and report results (report only)
agent: plan
---

Run and interpret the test suite.

!`pytest tests/ -v --tb=short`

For any failure:
- Show the test name and file path
- Show the assertion error / short traceback
- Suggest a likely fix in one sentence

If all pass, report the count and any coverage summary shown.
Do **NOT** modify any test or source files — report only.
