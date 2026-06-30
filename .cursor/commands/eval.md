Run the AI evaluation suite and report quality scores.

1. Run `deepeval test run tests/test_eval.py -v`
2. Report each metric with its score vs threshold:
   - Answer Relevancy (target: > 0.8)
   - Faithfulness (target: > 0.85, or > 0.9 for AFC)
   - Hallucination (target: < 0.15, or < 0.10 for AFC)
3. If any metric is below threshold, flag it with the specific test case that failed
4. Summarize: PASS (all metrics meet thresholds) or FAIL (list failing metrics)
5. Do NOT modify any files — report only
