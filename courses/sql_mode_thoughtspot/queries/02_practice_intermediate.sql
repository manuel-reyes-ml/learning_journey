-- ============================================================================
-- SQL INTERMEDIATE — Aggregation, CASE, Joins & UNION
-- ============================================================================
-- Author:       Manuel Reyes | github.com/manuel-reyes-ml
-- Repository:   learning_journey/courses/sql_mode_thoughtspot/queries/
-- Source:       Mode SQL Tutorial — Intermediate (hosted by ThoughtSpot)
--               https://www.thoughtspot.com/sql-tutorial/intro-to-intermediate-sql
-- Last Updated: 2026-10-14
-- Stage:        1 — Internal AI Builder (Roadmap v10.0)
-- Dialect:      PostgreSQL (Mode) — also runs in DuckDB
--
-- PURPOSE:
--   Quick-reference of every intermediate SQL clause and pattern practiced.
--   Each section shows the SIGNATURE, a short note, Mode's lesson examples,
--   and my worked solutions to the Mode practice problems.
--
-- CONVENTIONS:
--   • UPPER CASE  → SQL keywords (SELECT, FROM, JOIN ...)
--   • lower_case  → table and column identifiers
--   • 'single'    → string literals  (SQL standard)
--   • "double"    → column aliases with spaces only
--   • Table aliases are descriptive words (players, companies) — never a, b, c
--   • Every column is prefixed with its table alias once 2+ tables are involved
--   • INNER JOIN written explicitly in my solutions (Mode's examples use JOIN)
--   • Every query ends with a semicolon
--   • Comments explain the WHY, not just the WHAT
--
-- LABELS:
--   [Mode example]   → lesson example from the tutorial
--   [Mode practice]  → tutorial practice problem (prompt paraphrased),
--                      solution written by me
--   [Extension]      → production pattern beyond the tutorial
--
-- NOTE: Detailed explanations live in notes/02_sql_intermediate.md
--       This file is queries + quick notes only.
-- ============================================================================


-- ════════════════════════════════════════════════════════════════════════════
-- TABLE OF CONTENTS
-- ════════════════════════════════════════════════════════════════════════════
--
--   1.  Aggregation Nuances (COUNT on any type, MIN/MAX, AVG and NULLs)
--   2.  HAVING — Filtering Groups
--   3.  CASE — Conditional Logic
--   4.  CASE with Aggregates (Conditional Aggregation & Pivoting)
--   5.  DISTINCT Inside Aggregates (COUNT DISTINCT)
--   6.  Joins — Core Concepts & Aliases
--   7.  INNER JOIN
--   8.  LEFT JOIN
--   9.  RIGHT JOIN
--  10.  Filtering in ON vs WHERE
--  11.  FULL OUTER JOIN
--  12.  UNION & UNION ALL
--  13.  Joins with Comparison Operators
--  14.  Joins on Multiple Keys
--  15.  Self Joins
--  16.  Production Patterns (Anti-Join, Fan-Out, Duplicate Keys)
--
-- ════════════════════════════════════════════════════════════════════════════


-- ============================================================================
-- 1. Aggregation Nuances
-- ============================================================================
-- Core aggregates were covered in 01_practice_basics.sql (sections 13–14).
-- Intermediate details:
--
--   COUNT(column)  → works on ANY data type; counts non-NULL values only
--   SUM(column)    → numeric only; ignores NULLs; all-NULL group → NULL
--   MIN / MAX      → work on numbers, text (alphabetical), and dates
--   AVG(column)    → ignores NULLs in numerator AND denominator
--                    (NULL is NOT treated as zero)
--
-- POSTGRESQL GOTCHAS:
--   • int / int truncates:  5 / 2 = 2   → cast: 5::numeric / 2 = 2.5
--     (DuckDB returns 2.5 for 5 / 2 — cast explicitly so both agree)
--   • ROUND(x, n) needs numeric → ROUND(x::numeric, 2)
-- ============================================================================

-- 1a. [Mode practice] Count the non-null rows in the low column
SELECT COUNT(low) AS low_count
  FROM tutorial.aapl_historical_stock_price;

-- 1b. [Mode practice] Count every column to see which has the most NULLs
--     COUNT(*) - COUNT(col) = number of NULLs in that column
SELECT COUNT(*)      AS total_rows,
       COUNT(date)   AS date_count,
       COUNT(year)   AS year_count,
       COUNT(month)  AS month_count,
       COUNT(open)   AS open_count,
       COUNT(high)   AS high_count,
       COUNT(low)    AS low_count,
       COUNT(close)  AS close_count,
       COUNT(volume) AS volume_count
  FROM tutorial.aapl_historical_stock_price;

-- 1c. [Mode practice] Average opening price using SUM and COUNT
--     (equivalent to AVG(open) because both ignore the same NULL rows)
SELECT SUM(open) / COUNT(open) AS avg_open_price,
       AVG(open)               AS avg_open_check
  FROM tutorial.aapl_historical_stock_price;

-- 1d. [Mode practice] Apple's lowest price in the dataset
SELECT MIN(low) AS lowest_price
  FROM tutorial.aapl_historical_stock_price;

-- 1e. [Mode practice] Highest single-day increase in share value
SELECT MAX(close - open) AS biggest_daily_gain
  FROM tutorial.aapl_historical_stock_price;

-- 1f. [Mode practice] Average daily trade volume
SELECT ROUND(AVG(volume)::numeric, 0) AS avg_daily_volume
  FROM tutorial.aapl_historical_stock_price;

-- 1g. MIN / MAX on dates — first and last trading day in the data
SELECT MIN(date) AS first_day,
       MAX(date) AS last_day
  FROM tutorial.aapl_historical_stock_price;

-- 1h. Integer division gotcha (runs without a table)
--     PostgreSQL truncates int/int; DuckDB returns a decimal (uses // for int division)
--     → always cast explicitly so both engines agree
SELECT 5 / 2          AS truncated,    -- 2 in PostgreSQL | 2.5 in DuckDB
       5 * 1.0 / 2    AS decimal_1,    -- 2.5
       5::numeric / 2 AS decimal_2;    -- 2.5


-- ============================================================================
-- 2. HAVING — Filtering Groups
-- ============================================================================
-- Signature:  SELECT col, AGG(col) FROM t GROUP BY col HAVING AGG(col) <op> value;
--
-- WHERE  → filters ROWS before grouping (no aggregates allowed)
-- HAVING → filters GROUPS after aggregation (aggregates allowed)
--
-- PostgreSQL: cannot use a SELECT alias inside HAVING — repeat the aggregate.
-- Clause order: SELECT → FROM → WHERE → GROUP BY → HAVING → ORDER BY → LIMIT
-- ============================================================================

-- 2a. [Mode example] Months where Apple's high exceeded $400
SELECT year,
       month,
       MAX(high) AS month_high
  FROM tutorial.aapl_historical_stock_price
 GROUP BY year, month
HAVING MAX(high) > 400
 ORDER BY year, month;

-- 2b. WHERE + HAVING together — row filter first, then group filter
SELECT year,
       month,
       MAX(high) AS month_high
  FROM tutorial.aapl_historical_stock_price
 WHERE year >= 2012
 GROUP BY year, month
HAVING MAX(high) >= 600
 ORDER BY year, month;

-- 2c. Years with fewer than 250 recorded trading days (data-completeness check)
SELECT year,
       COUNT(*) AS trading_days
  FROM tutorial.aapl_historical_stock_price
 GROUP BY year
HAVING COUNT(*) < 250
 ORDER BY year;


-- ============================================================================
-- 3. CASE — Conditional Logic
-- ============================================================================
-- Signature:
--   CASE WHEN condition_1 THEN result_1
--        WHEN condition_2 THEN result_2
--        ELSE default_result            -- optional; missing ELSE → NULL
--   END AS alias
--
-- • Evaluated top to bottom — STOPS at the first TRUE condition
-- • All THEN / ELSE results must share a data type
-- • Prefer non-overlapping ranges for readability
-- • Simple form: CASE col WHEN 'x' THEN ... (equality on one column only)
-- ============================================================================

-- 3a. [Mode example] Simple flag column
SELECT player_name,
       year,
       CASE WHEN year = 'SR' THEN 'yes'
            ELSE 'no' END AS is_a_senior
  FROM benn.college_football_players;

-- 3b. [Mode example] Multiple conditions — ordered weight buckets
SELECT player_name,
       weight,
       CASE WHEN weight > 250 THEN 'over 250'
            WHEN weight > 200 THEN '201-250'
            WHEN weight > 175 THEN '176-200'
            ELSE '175 or under' END AS weight_group
  FROM benn.college_football_players;

-- 3c. [Mode example] AND inside a CASE condition
SELECT player_name,
       CASE WHEN year = 'FR' AND position = 'WR' THEN 'frosh_wr'
            ELSE NULL END AS sample_case_statement
  FROM benn.college_football_players;

-- 3d. [Mode practice] Flag players from California and list them first
SELECT player_name,
       state,
       CASE WHEN state = 'CA' THEN 'yes'
            ELSE NULL END AS from_california
  FROM benn.college_football_players
 ORDER BY 3;   -- NULLs sort LAST in ascending order (PostgreSQL), so 'yes' comes first

-- 3e. [Mode practice] Four height categories (non-overlapping ranges)
SELECT player_name,
       height,
       CASE WHEN height > 74                  THEN 'over 74'
            WHEN height > 72 AND height <= 74 THEN '73-74'
            WHEN height > 70 AND height <= 72 THEN '71-72'
            ELSE 'under 71' END AS height_group
  FROM benn.college_football_players;

-- 3f. [Mode practice] All columns + the player's name only if JR or SR
SELECT *,
       CASE WHEN year IN ('JR', 'SR') THEN player_name
            ELSE NULL END AS upperclass_player_name
  FROM benn.college_football_players;

-- 3g. CASE in ORDER BY — custom business sort order (FR → SO → JR → SR)
SELECT player_name,
       year
  FROM benn.college_football_players
 ORDER BY CASE year WHEN 'FR' THEN 1
                    WHEN 'SO' THEN 2
                    WHEN 'JR' THEN 3
                    WHEN 'SR' THEN 4
                    ELSE 5 END,
          player_name;


-- ============================================================================
-- 4. CASE with Aggregates (Conditional Aggregation & Pivoting)
-- ============================================================================
-- Patterns:
--   GROUP BY CASE ...                         → vertical (one row per bucket)
--   COUNT(CASE WHEN cond THEN 1 ELSE NULL END) → horizontal pivot (one col per bucket)
--   SUM(CASE WHEN cond THEN value ELSE 0 END)  → conditional totals
--   COUNT(*) FILTER (WHERE cond)               → PostgreSQL / DuckDB shortcut
--
-- WORKFLOW: build the CASE with SELECT CASE ... AS grp, * first → verify →
--           then swap * for the aggregate and add GROUP BY.
-- ============================================================================

-- 4a. [Mode example] Vertical — players per class year
--     GROUP BY 1 = group by the first SELECT column (the CASE result)
SELECT CASE WHEN year = 'FR' THEN 'FR'
            WHEN year = 'SO' THEN 'SO'
            WHEN year = 'JR' THEN 'JR'
            WHEN year = 'SR' THEN 'SR'
            ELSE 'No Year Data' END AS year_group,
       COUNT(1) AS count
  FROM benn.college_football_players
 GROUP BY 1;

-- 4b. [Mode example] Horizontal pivot — one row, one column per class year
SELECT COUNT(CASE WHEN year = 'FR' THEN 1 ELSE NULL END) AS fr_count,
       COUNT(CASE WHEN year = 'SO' THEN 1 ELSE NULL END) AS so_count,
       COUNT(CASE WHEN year = 'JR' THEN 1 ELSE NULL END) AS jr_count,
       COUNT(CASE WHEN year = 'SR' THEN 1 ELSE NULL END) AS sr_count
  FROM benn.college_football_players;

-- 4c. [Mode practice] Count 300lb+ players by region: West Coast, Texas, Other
SELECT CASE WHEN state IN ('CA', 'OR', 'WA') THEN 'West Coast'
            WHEN state = 'TX'                THEN 'Texas'
            ELSE 'Other' END AS region_group,
       COUNT(1) AS players_300_plus
  FROM benn.college_football_players
 WHERE weight >= 300
 GROUP BY 1;

-- 4d. [Mode practice] Combined weight of underclass vs upperclass players in CA
SELECT SUM(CASE WHEN year IN ('FR', 'SO') THEN weight ELSE 0 END) AS underclass_weight,
       SUM(CASE WHEN year IN ('JR', 'SR') THEN weight ELSE 0 END) AS upperclass_weight
  FROM benn.college_football_players
 WHERE state = 'CA';

-- 4e. [Mode practice] Players per state, one column per class year + total,
--     most players first
SELECT state,
       COUNT(CASE WHEN year = 'FR' THEN 1 ELSE NULL END) AS fr_count,
       COUNT(CASE WHEN year = 'SO' THEN 1 ELSE NULL END) AS so_count,
       COUNT(CASE WHEN year = 'JR' THEN 1 ELSE NULL END) AS jr_count,
       COUNT(CASE WHEN year = 'SR' THEN 1 ELSE NULL END) AS sr_count,
       COUNT(1)                                         AS total_players
  FROM benn.college_football_players
 GROUP BY state
 ORDER BY total_players DESC;

-- 4f. [Mode practice] Players at schools starting A–M vs N–Z
--     UPPER(LEFT(...)) avoids collation surprises with lower-case comparisons
SELECT CASE WHEN UPPER(LEFT(school_name, 1)) < 'N'  THEN 'A-M'
            WHEN UPPER(LEFT(school_name, 1)) >= 'N' THEN 'N-Z'
            ELSE NULL END AS school_name_group,
       COUNT(1) AS players
  FROM benn.college_football_players
 GROUP BY 1;

-- 4g. FILTER clause — same result as 4b with cleaner syntax (PostgreSQL / DuckDB)
SELECT COUNT(*) FILTER (WHERE year = 'FR') AS fr_count,
       COUNT(*) FILTER (WHERE year = 'SO') AS so_count,
       COUNT(*) FILTER (WHERE year = 'JR') AS jr_count,
       COUNT(*) FILTER (WHERE year = 'SR') AS sr_count
  FROM benn.college_football_players;


-- ============================================================================
-- 5. DISTINCT Inside Aggregates (COUNT DISTINCT)
-- ============================================================================
-- Signature:  SELECT COUNT(DISTINCT column) FROM table;
--
-- • DISTINCT goes INSIDE the parentheses: COUNT(DISTINCT col)
-- • MIN/MAX(DISTINCT col) = same result, slower → never do it
-- • COUNT(DISTINCT) is expensive on big tables (sort/hash every value)
-- ============================================================================

-- 5a. [Mode practice] Unique years in chronological order
SELECT DISTINCT year
  FROM tutorial.aapl_historical_stock_price
 ORDER BY year;

-- 5b. [Mode practice] Unique months recorded within each year
SELECT year,
       COUNT(DISTINCT month) AS months_count
  FROM tutorial.aapl_historical_stock_price
 GROUP BY year
 ORDER BY year;

-- 5c. [Mode practice] Distinct years and distinct months, separately, one query
SELECT COUNT(DISTINCT year)  AS years_count,
       COUNT(DISTINCT month) AS months_count
  FROM tutorial.aapl_historical_stock_price;

-- 5d. [Mode example] Average volume by month (no DISTINCT needed —
--     GROUP BY already produces one row per month)
SELECT month,
       AVG(volume) AS avg_trade_volume
  FROM tutorial.aapl_historical_stock_price
 GROUP BY month
 ORDER BY 2 DESC;


-- ============================================================================
-- 6. Joins — Core Concepts & Aliases
-- ============================================================================
-- Signature:
--   SELECT left_alias.col, right_alias.col
--     FROM schema.left_table  left_alias
--     JOIN schema.right_table right_alias
--       ON right_alias.key = left_alias.key;
--
-- • Alias every table with a descriptive word
-- • ON = the match condition; join key = the shared column(s)
-- • SELECT *        → all columns from both tables
--   SELECT alias.*  → all columns from one table
-- • Aggregate and GROUP BY using columns from either table
-- ============================================================================

-- 6a. [Mode example] Average player weight by conference
SELECT teams.conference    AS conference,
       AVG(players.weight) AS average_weight
  FROM benn.college_football_players players
  JOIN benn.college_football_teams teams
    ON teams.school_name = players.school_name
 GROUP BY teams.conference
 ORDER BY AVG(players.weight) DESC;

-- 6b. [Mode practice] Georgia players, heaviest first, using a table alias
--     for every column (single table — alias practice only)
SELECT players.school_name,
       players.player_name,
       players.position,
       players.weight
  FROM benn.college_football_players players
 WHERE players.state = 'GA'
 ORDER BY players.weight DESC;


-- ============================================================================
-- 7. INNER JOIN
-- ============================================================================
-- Signature:  FROM a INNER JOIN b ON a.key = b.key
--
-- • Returns ONLY rows that match in BOTH tables (intersection)
-- • JOIN = INNER JOIN (write INNER explicitly in production code)
-- • One-to-many keys multiply rows; NULL keys never match
-- • Duplicate column names → alias each one explicitly
-- ============================================================================

-- 7a. [Mode example] Alias identically named columns from both tables
SELECT players.school_name AS players_school_name,
       teams.school_name   AS teams_school_name
  FROM benn.college_football_players players
  JOIN benn.college_football_teams teams
    ON teams.school_name = players.school_name;

-- 7b. [Mode practice] Player names, schools and conferences for FBS schools only
SELECT players.player_name,
       players.school_name,
       teams.conference
  FROM benn.college_football_players players
 INNER JOIN benn.college_football_teams teams
    ON teams.school_name = players.school_name
 WHERE teams.division = 'FBS (Division I-A Teams)';


-- ============================================================================
-- 8. LEFT JOIN
-- ============================================================================
-- Signature:  FROM a LEFT JOIN b ON a.key = b.key
--
-- • Keeps ALL rows from the left (FROM) table
-- • Unmatched right-side columns → NULL
-- • LEFT OUTER JOIN = LEFT JOIN
-- • COUNT(right_table.col) counts only matched rows → measures match rate
-- ============================================================================

-- 8a. [Mode example] Companies with their acquisition date (if any)
SELECT companies.permalink             AS companies_permalink,
       companies.name                  AS companies_name,
       acquisitions.company_permalink  AS acquisitions_permalink,
       acquisitions.acquired_at        AS acquired_date
  FROM tutorial.crunchbase_companies companies
  LEFT JOIN tutorial.crunchbase_acquisitions acquisitions
    ON companies.permalink = acquisitions.company_permalink;

-- 8b. [Mode practice] INNER JOIN — count non-null rows from each table
SELECT COUNT(companies.permalink)             AS companies_rowcount,
       COUNT(acquisitions.company_permalink)  AS acquisitions_rowcount
  FROM tutorial.crunchbase_companies companies
 INNER JOIN tutorial.crunchbase_acquisitions acquisitions
    ON companies.permalink = acquisitions.company_permalink;

-- 8c. [Mode practice] Same query as LEFT JOIN — compare with 8b
--     companies_rowcount grows; acquisitions_rowcount stays the same
SELECT COUNT(companies.permalink)             AS companies_rowcount,
       COUNT(acquisitions.company_permalink)  AS acquisitions_rowcount
  FROM tutorial.crunchbase_companies companies
  LEFT JOIN tutorial.crunchbase_acquisitions acquisitions
    ON companies.permalink = acquisitions.company_permalink;

-- 8d. [Mode practice] Unique companies and unique acquired companies by state,
--     excluding rows without a state, most acquired first
SELECT companies.state_code,
       COUNT(DISTINCT companies.permalink)            AS unique_companies,
       COUNT(DISTINCT acquisitions.company_permalink) AS unique_companies_acquired
  FROM tutorial.crunchbase_companies companies
  LEFT JOIN tutorial.crunchbase_acquisitions acquisitions
    ON companies.permalink = acquisitions.company_permalink
 WHERE companies.state_code IS NOT NULL
 GROUP BY 1
 ORDER BY 3 DESC;


-- ============================================================================
-- 9. RIGHT JOIN
-- ============================================================================
-- Signature:  FROM a RIGHT JOIN b ON a.key = b.key
--
-- • Keeps ALL rows from the right (JOIN) table
-- • Any RIGHT JOIN = a LEFT JOIN with the table order swapped
-- • Convention: prefer LEFT JOIN (read left → right)
-- ============================================================================

-- 9a. [Mode practice] Rewrite 8d with RIGHT JOIN — identical results
SELECT companies.state_code,
       COUNT(DISTINCT companies.permalink)            AS unique_companies,
       COUNT(DISTINCT acquisitions.company_permalink) AS unique_companies_acquired
  FROM tutorial.crunchbase_acquisitions acquisitions
 RIGHT JOIN tutorial.crunchbase_companies companies
    ON companies.permalink = acquisitions.company_permalink
 WHERE companies.state_code IS NOT NULL
 GROUP BY 1
 ORDER BY 3 DESC;


-- ============================================================================
-- 10. Filtering in ON vs WHERE
-- ============================================================================
-- ON    → applied DURING the join: left rows survive (right side → NULL)
-- WHERE → applied AFTER the join: whole rows removed
--
-- RULE OF THUMB (LEFT JOIN):
--   • Filter on LEFT table  → WHERE
--   • Filter on RIGHT table → ON  (unless you WANT to drop unmatched rows)
--   • A WHERE filter on a right-table column silently becomes an INNER JOIN
-- ============================================================================

-- 10a. [Mode example] Filter in ON — 1000memories stays, with NULLs
SELECT companies.permalink             AS companies_permalink,
       companies.name                  AS companies_name,
       acquisitions.company_permalink  AS acquisitions_permalink,
       acquisitions.acquired_at        AS acquired_date
  FROM tutorial.crunchbase_companies companies
  LEFT JOIN tutorial.crunchbase_acquisitions acquisitions
    ON companies.permalink = acquisitions.company_permalink
   AND acquisitions.company_permalink != '/company/1000memories'
 ORDER BY 1;

-- 10b. [Mode example] Filter in WHERE — 1000memories disappears
--      OR ... IS NULL keeps never-acquired companies
SELECT companies.permalink             AS companies_permalink,
       companies.name                  AS companies_name,
       acquisitions.company_permalink  AS acquisitions_permalink,
       acquisitions.acquired_at        AS acquired_date
  FROM tutorial.crunchbase_companies companies
  LEFT JOIN tutorial.crunchbase_acquisitions acquisitions
    ON companies.permalink = acquisitions.company_permalink
 WHERE acquisitions.company_permalink != '/company/1000memories'
    OR acquisitions.company_permalink IS NULL
 ORDER BY 1;

-- 10c. [Mode practice] New York companies: name, status, unique investors,
--      most investors first (state filter is on the LEFT table → WHERE)
SELECT companies.name                              AS company_name,
       companies.status,
       COUNT(DISTINCT investments.investor_name)   AS unique_investors
  FROM tutorial.crunchbase_companies companies
  LEFT JOIN tutorial.crunchbase_investments investments
    ON companies.permalink = investments.company_permalink
 WHERE companies.state_code = 'NY'
 GROUP BY 1, 2
 ORDER BY 3 DESC;

-- 10d. [Mode practice] Investors ranked by companies invested in,
--      with a 'No Investors' row for companies that have none
SELECT CASE WHEN investments.investor_name IS NULL THEN 'No Investors'
            ELSE investments.investor_name END   AS investor,
       COUNT(DISTINCT companies.permalink)       AS companies_invested_in
  FROM tutorial.crunchbase_companies companies
  LEFT JOIN tutorial.crunchbase_investments investments
    ON companies.permalink = investments.company_permalink
 GROUP BY 1
 ORDER BY 2 DESC;


-- ============================================================================
-- 11. FULL OUTER JOIN
-- ============================================================================
-- Signature:  FROM a FULL JOIN b ON a.key = b.key
--
-- • Keeps unmatched rows from BOTH tables
-- • Classic use: measure overlap → only_in_a / both / only_in_b
-- • Count the column from the side that is NOT NULL in each bucket
-- • MySQL has no FULL JOIN (emulate with LEFT JOIN UNION RIGHT JOIN)
-- ============================================================================

-- 11a. [Mode example] Overlap between companies and acquisitions
SELECT COUNT(CASE WHEN companies.permalink IS NOT NULL
                   AND acquisitions.company_permalink IS NULL
                  THEN companies.permalink ELSE NULL END)             AS companies_only,
       COUNT(CASE WHEN companies.permalink IS NOT NULL
                   AND acquisitions.company_permalink IS NOT NULL
                  THEN companies.permalink ELSE NULL END)             AS both_tables,
       COUNT(CASE WHEN companies.permalink IS NULL
                   AND acquisitions.company_permalink IS NOT NULL
                  THEN acquisitions.company_permalink ELSE NULL END)  AS acquisitions_only
  FROM tutorial.crunchbase_companies companies
  FULL JOIN tutorial.crunchbase_acquisitions acquisitions
    ON companies.permalink = acquisitions.company_permalink;

-- 11b. [Mode practice] Same overlap analysis: companies vs investments_part1
SELECT COUNT(CASE WHEN companies.permalink IS NOT NULL
                   AND investments.company_permalink IS NULL
                  THEN companies.permalink ELSE NULL END)            AS companies_only,
       COUNT(CASE WHEN companies.permalink IS NOT NULL
                   AND investments.company_permalink IS NOT NULL
                  THEN companies.permalink ELSE NULL END)            AS both_tables,
       COUNT(CASE WHEN companies.permalink IS NULL
                   AND investments.company_permalink IS NOT NULL
                  THEN investments.company_permalink ELSE NULL END)  AS investments_only
  FROM tutorial.crunchbase_companies companies
  FULL JOIN tutorial.crunchbase_investments_part1 investments
    ON companies.permalink = investments.company_permalink;


-- ============================================================================
-- 12. UNION & UNION ALL
-- ============================================================================
-- Signature:  SELECT ... FROM a  UNION ALL  SELECT ... FROM b;
--
-- • Stacks results vertically (adds rows); JOIN adds columns
-- • UNION     → removes exact duplicate rows (slower)
-- • UNION ALL → keeps everything (faster) — DEFAULT CHOICE
-- • Same column count, same order, compatible types
-- • Column names come from the FIRST query
-- • Each SELECT can filter / group on its own; one ORDER BY at the end
-- ============================================================================

-- 12a. [Mode example] Append both investment tables, keeping duplicates
SELECT *
  FROM tutorial.crunchbase_investments_part1

 UNION ALL

SELECT *
  FROM tutorial.crunchbase_investments_part2;

-- 12b. [Mode practice] Part 1 companies starting with 'T' + part 2 companies
--      starting with 'M' (case-insensitive), three columns, keep duplicates
SELECT company_permalink,
       company_name,
       investor_name
  FROM tutorial.crunchbase_investments_part1
 WHERE company_name ILIKE 'T%'

 UNION ALL

SELECT company_permalink,
       company_name,
       investor_name
  FROM tutorial.crunchbase_investments_part2
 WHERE company_name ILIKE 'M%';

-- 12c. [Mode practice] Investor counts by dataset and company status
--      A literal column labels which part each row came from
SELECT 'investments_part1'                         AS dataset_name,
       companies.status,
       COUNT(DISTINCT investments.investor_permalink) AS investors
  FROM tutorial.crunchbase_companies companies
  LEFT JOIN tutorial.crunchbase_investments_part1 investments
    ON companies.permalink = investments.company_permalink
 GROUP BY 1, 2

 UNION ALL

SELECT 'investments_part2'                         AS dataset_name,
       companies.status,
       COUNT(DISTINCT investments.investor_permalink) AS investors
  FROM tutorial.crunchbase_companies companies
  LEFT JOIN tutorial.crunchbase_investments_part2 investments
    ON companies.permalink = investments.company_permalink
 GROUP BY 1, 2

 ORDER BY 1, 2;


-- ============================================================================
-- 13. Joins with Comparison Operators
-- ============================================================================
-- Signature:  ON a.key = b.key AND b.col > a.col
--
-- • ON accepts ANY condition (>, <, BETWEEN, !=), not just =
-- • Keep at least one equality condition for performance
-- • Condition in ON (not WHERE) → unmatched left rows still return
-- ============================================================================

-- 13a. [Mode example] Investors per company, counting only investments made
--      more than 5 years after the company was founded
SELECT companies.permalink,
       companies.name,
       companies.status,
       COUNT(investments.investor_permalink) AS investors
  FROM tutorial.crunchbase_companies companies
  LEFT JOIN tutorial.crunchbase_investments_part1 investments
    ON companies.permalink = investments.company_permalink
   AND investments.funded_year > companies.founded_year + 5
 GROUP BY 1, 2, 3;


-- ============================================================================
-- 14. Joins on Multiple Keys
-- ============================================================================
-- Signature:  ON a.key1 = b.key1 AND a.key2 = b.key2
--
-- Two reasons:
--   1. ACCURACY    → the true key is composite (e.g., plan_id + participant_id)
--   2. PERFORMANCE → can use a multi-column index (little effect on small data)
-- ============================================================================

-- 14a. [Mode example] Same result with or without the second condition here —
--      but the composite join can use an index on (permalink, name)
SELECT companies.permalink,
       companies.name,
       investments.company_name,
       investments.company_permalink
  FROM tutorial.crunchbase_companies companies
  LEFT JOIN tutorial.crunchbase_investments_part1 investments
    ON companies.permalink = investments.company_permalink
   AND companies.name = investments.company_name;


-- ============================================================================
-- 15. Self Joins
-- ============================================================================
-- Signature:  FROM t alias_1 JOIN t alias_2 ON alias_1.key = alias_2.key ...
--
-- • Same table, TWO different aliases
-- • Used to compare rows within one table (sequences, hierarchies, pairs)
-- • Many "previous row" self joins become window functions (LAG) in Advanced
-- ============================================================================

-- 15a. [Mode example] Companies that got a British investment
--      AFTER a Japanese investment
SELECT DISTINCT japan_investments.company_name,
       japan_investments.company_permalink
  FROM tutorial.crunchbase_investments_part1 japan_investments
  JOIN tutorial.crunchbase_investments_part1 gb_investments
    ON japan_investments.company_name = gb_investments.company_name
   AND gb_investments.investor_country_code = 'GBR'
   AND gb_investments.funded_at > japan_investments.funded_at
 WHERE japan_investments.investor_country_code = 'JPN'
 ORDER BY 1;


-- ============================================================================
-- 16. Production Patterns (Anti-Join, Fan-Out, Duplicate Keys)   [Extension]
-- ============================================================================
-- Patterns used daily in analytics engineering / pipeline work,
-- built only from the concepts above.
--
--   ANTI-JOIN     → LEFT JOIN + WHERE right.key IS NULL  ("in A, not in B")
--   FAN-OUT CHECK → compare row counts before vs after a join
--   UNIQUE KEY    → GROUP BY key HAVING COUNT(*) > 1  returns 0 rows
--                   (this is what dbt's `unique` test runs)
-- ============================================================================

-- 16a. [Extension] Anti-join — companies never acquired
SELECT companies.permalink,
       companies.name
  FROM tutorial.crunchbase_companies companies
  LEFT JOIN tutorial.crunchbase_acquisitions acquisitions
    ON companies.permalink = acquisitions.company_permalink
 WHERE acquisitions.company_permalink IS NULL;

-- 16b. [Extension] Fan-out check — does the join multiply company rows?
--      If joined_rows > company_rows, any SUM of a company-level column
--      (e.g., funding_total_usd) after this join is inflated.
SELECT (SELECT COUNT(*) FROM tutorial.crunchbase_companies) AS company_rows,
       COUNT(*)                                             AS joined_rows
  FROM tutorial.crunchbase_companies companies
  LEFT JOIN tutorial.crunchbase_acquisitions acquisitions
    ON companies.permalink = acquisitions.company_permalink;
--      (The inline SELECT in the first column is a scalar subquery — an
--       Advanced topic. Run the two COUNTs separately if preferred.)

-- 16c. [Extension] Duplicate-key check — is permalink safe as a 1:1 join key?
SELECT permalink,
       COUNT(*) AS occurrences
  FROM tutorial.crunchbase_companies
 GROUP BY permalink
HAVING COUNT(*) > 1;

-- 16d. [Extension] Which companies were acquired more than once?
--      (Explains why the acquisitions join fans out in 16b)
SELECT company_permalink,
       COUNT(*) AS times_acquired
  FROM tutorial.crunchbase_acquisitions
 GROUP BY company_permalink
HAVING COUNT(*) > 1
 ORDER BY times_acquired DESC;


-- ============================================================================
-- FULL CLAUSE ORDER REFERENCE (intermediate)
-- ============================================================================
--
-- SELECT    → columns / calculations / CASE expressions to return
-- FROM      → driving (left) table + alias
-- JOIN ... ON → additional tables + match conditions (repeatable)
-- WHERE     → filter rows BEFORE grouping
-- GROUP BY  → group rows for aggregation
-- HAVING    → filter groups AFTER aggregation
-- ORDER BY  → sort the final results
-- LIMIT     → cap the number of rows returned
--
-- LOGICAL EXECUTION ORDER:
--   FROM/JOIN → WHERE → GROUP BY → HAVING → SELECT → DISTINCT → ORDER BY → LIMIT
--
-- ============================================================================


-- ============================================================================
-- END OF INTERMEDIATE
-- ============================================================================
-- NEXT FILE: 03_practice_advanced.sql
--   Topics: data types & casting, dates, string cleaning, subqueries & CTEs,
--           window functions, performance tuning (EXPLAIN), pivoting
-- ============================================================================
