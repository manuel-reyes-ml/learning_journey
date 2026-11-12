-- 1) Open for inspection (read-only)
ATTACH 'foundations/dbt/market_rehearsal/market.duckdb' AS rehearsal (READ_ONLY);

-- 2) Look around
SUMMARIZE rehearsal.main.your_model;
SELECT * FROM rehearsal.main.your_model LIMIT 20;

-- 3) Release the lock before dbt build
DETACH rehearsal


-- Run one statement at a time through the extension; Cmd+Shift+P → type “DuckDB” shows
-- its run-query commands. If the relative path doesn’t resolve, use the full
-- /Users/manuelreyes/... path from your error message.
