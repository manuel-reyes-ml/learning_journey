-- Production Grade: the .sql file holds no path

-- A view stores only the query, not the data. In my test I added a row to the CSV after creating
-- the view, and the next query saw it right away. A TABLE would have kept the old copy.
-- See 'SET VARIABLE...' in week05_bar_windows.ipynb
CREATE VIEW bars AS FROM read_csv(getvariable('bars_csv'));

WITH flagged AS (   -- query_1
    SELECT
            ticker,
            session_date,
            -- Make is_dry true only when the frame holds exactly 20 non-null volumes.
            -- A rolling window doesn’t fail when it has too few rows; it quietly averages
            -- fewer of them. Always check the window is full before trusting a rolling baseline.
            ROW_NUMBER() OVER (PARTITION BY ticker ORDER BY session_date) AS session_n,
            COUNT(volume) OVER w = 20
                AND volume < 0.5 * AVG(volume) OVER w AS is_dry
        FROM bars
        WINDOW w AS (
            PARTITION BY ticker
            ORDER BY session_date
            ROWS BETWEEN 20 PRECEDING AND 1 PRECEDING
        )
),
dry AS (            -- query_2
    -- consecutive dry sessions share one value of (session_n − row number among dry rows)
    SELECT
            ticker,
            session_date,
            session_n - ROW_NUMBER() OVER (
                PARTITION BY ticker
                ORDER BY session_date
            ) AS island
        FROM flagged
        WHERE is_dry
),
runs AS (           -- query_3
    SELECT
            ticker,
            island,
            MIN(session_date) AS run_start,
            MAX(session_date) AS run_end,
            COUNT(*) AS dry_sessions
        FROM dry
        GROUP BY ticker, island
)
SELECT ticker,
       run_start,
       run_end,
       dry_sessions
    FROM runs
    -- QUALIFY is a filter for window function results. It does for window functions what HAVING
    -- does for aggregates. A window function can’t go in the WHERE clause directly, so you use
    -- QUALIFY when you need to filter on one.
    QUALIFY ROW_NUMBER() OVER (PARTITION BY ticker ORDER BY dry_sessions DESC, run_start) = 1
    ORDER BY dry_sessions DESC;
