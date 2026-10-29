-- Production Grade: the .sql file holds no path

-- A view stores only the query, not the data. In my test I added a row to the CSV after creating
-- the view, and the next query saw it right away. A TABLE would have kept the old copy.
CREATE VIEW bars AS FROM read_csv(getvariable('bars_csv'));

-- Daily return, overnight gap, next open — and the RVOL leak, side by side
SELECT ticker,
       session_date,
       close,
       close / LAG(close) OVER w - 1 AS daily_return,
       open / LAG(close) OVER w - 1  AS overnight_gap,   -- today's open vs yesterday's close
       LEAD(open) OVER w             AS next_open,       -- fine in a LABEL, a leak in a FEATURE
       volume / AVG(volume) OVER (
            PARTITION BY ticker
            ORDER BY session_date
            ROWS BETWEEN 20 PRECEDING AND 1 PRECEDING
       ) AS rvol_clean,
       volume / AVG(volume) OVER (
            PARTITION BY ticker
            ORDER BY session_date
            ROWS BETWEEN 19 PRECEDING AND CURRENT ROW
       ) AS rvol_leaky
  FROM bars                                              -- the CSV IS the table
  WINDOW w AS (PARTITION BY ticker ORDER BY session_date)
  ORDER BY ticker, session_date


  -- SQL doesn’t look for the CSV starting from where the .sql file lives. It looks starting from
  -- the folder the program is running in (the working directory). Write the path relative to your
  -- repo root, and always run from the repo root.
