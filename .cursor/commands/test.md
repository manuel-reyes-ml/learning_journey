Run the test suite and report results.

1. Run `uv run pytest tests/ -v --tb=short`
2. If any tests fail, for each failure:
   - Show the test name and file path
   - Show the assertion error or traceback (short format)
   - Suggest a likely fix in one sentence
3. Also flag, without fixing:
   - A missing `_reset_structlog` fixture in `conftest.py` — a cached bound logger
     (`cache_logger_on_first_use=True`) ignores later reconfiguration, so log assertions
     silently test stale config
   - A missing `_no_retry_sleeps` fixture (`stamina.set_active(False)`) — the suite is
     spending real seconds sleeping through retry backoffs
   - Any real participant data or secrets in fixtures — synthetic only
4. If all tests pass, report the count and coverage summary
5. Do NOT modify any test files or source files — report only