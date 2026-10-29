-- Window functions: aggregate WITHOUT collapsing rows.
-- GROUP BY answers "total per code"; a window answers "each row AND its
-- share of the total" — both rows and context survive.

-- Q1: Running total of distributions by date:
SELECT dist_date,
       gross,
       SUM(gross) OVER (
        ORDER BY dist_date
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
       ) AS running_total
  FROM distributions
  ORDER BY 1;                 -- OVER (...) = "the window"


-- Q2: Rank distributions within each Box-7 code:
SELECT box7_code,
       gross,
       RANK() OVER (
        PARTITION BY box7_code
        ORDER BY gross DESC
       ) AS rank
  FROM distributions;       -- PARTITION BY = "restart per group"
-- Interview-famous shape: "top N per group" = wrap this + WHERE rank <= N.
