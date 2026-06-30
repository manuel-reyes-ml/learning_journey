Run the test suite and report results.

1. Run `pytest tests/ -v --tb=short`
2. If any tests fail, for each failure:
   - Show the test name and file path
   - Show the assertion error or traceback (short format)
   - Suggest a likely fix in one sentence
3. If all tests pass, report the count and coverage summary
4. Do NOT modify any test files or source files — report only
