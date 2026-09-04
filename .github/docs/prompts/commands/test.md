Run and interpret the test suite.

All context you need has already been injected above this text by
`.github/scripts/test_context.sh`.

**Do not attempt to load any of it yourself.** This body contains no `!` blocks and no
`@` references by design: command-template substitution is single-pass, so either would
arrive as literal text and silently never run (ADR-0001).

**Check the context first.** If a block above is missing, empty, or shows a line
beginning `CONTEXT_ERROR`, **STOP and report which one**. Do not infer, reconstruct, or
reason from the rules files in place of the missing output.

The `PYTEST RUN` block is the pytest output. Interpret it — do not re-run it.

For any failure:
- Show the test name and file path
- Show the assertion error / short traceback
- Suggest a likely fix in one sentence

Also flag, without fixing (use the `CONFTEST FIXTURES PRESENT` block — do not guess):
- Missing `_reset_structlog` fixture in `conftest.py` (a cached bound logger makes log
  assertions test stale config)
- Missing `_no_retry_sleeps` fixture (`stamina.set_active(False)`) — the suite is
  spending real seconds sleeping through backoffs
- Any real participant data or secrets in fixtures — synthetic only

If all pass, report the count and any coverage summary shown.
Do **NOT** modify any test or source files — report only.