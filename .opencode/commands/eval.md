---
description: Run the AI evaluation suite and report quality scores vs thresholds
agent: eval-guardian
---

Run the AI evaluation suite and report quality scores.

!`deepeval test run tests/test_eval.py -v`

Report each metric as `score vs threshold` with PASS/FAIL:
- Answer Relevancy   target > 0.80
- Faithfulness       target > 0.85  (> 0.90 for AFC)
- Hallucination      target < 0.15  (< 0.10 for AFC)

For any metric below threshold, name the specific failing test case.
Conclude with **PASS** (all thresholds met) or **FAIL** (list failing metrics).
Do **NOT** modify any files — report only.
