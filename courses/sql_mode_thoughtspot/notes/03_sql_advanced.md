# SQL Advanced — Complete Reference Notes

> **Author:** Manuel Reyes | [github.com/manuel-reyes-ml](https://github.com/manuel-reyes-ml)  
> **Source:** [Mode SQL Tutorial — Advanced (now hosted by ThoughtSpot)](https://www.thoughtspot.com/sql-tutorial/sql-data-types)  
> **Companion file:** `queries/03_practice_advanced.sql` (hands-on exercises)  
> **Previous file:** `notes/02_sql_intermediate.md`  
> **Stage:** 1 — Internal AI Builder ([Roadmap v10.0](https://manuel-reyes-ml.github.io/learning_journey/roadmap.html))  
> **Dialect:** PostgreSQL (Mode's engine). Every query also runs in DuckDB, the local practice stack, except where a section says otherwise.  
> **Last updated:** 2026-10-28

---

## What This File Covers

Mode's Advanced track has nine lessons. Its coverage of window functions, the topic analytics engineering leans on most, stops at the basics. It never explains **window frames**, so it never explains why a running total can "stall" on tied rows. This file covers every Mode lesson and adds the topics a production analytics engineer is expected to know. Those additions are marked **[Beyond Mode]**.

| Mode lesson | Section here | [Beyond Mode] additions |
| --- | --- | --- |
| Data Types | [3](#3-data-types-and-casting) | `NUMERIC` vs `DOUBLE` for money, `TRY_CAST` |
| Date Format | [5](#5-dates-and-times) | Half-open date ranges, date spines |
| Data Wrangling | [6](#6-string-functions-for-cleaning) | — (concept lesson) |
| String Functions | [4](#4-null-toolkit-coalesce-and-nullif), [6](#6-string-functions-for-cleaning) | `NULLIF`, `SPLIT_PART`, `REPLACE`, regex |
| Subqueries | [7](#7-subqueries) | Correlated subqueries |
| — | [8](#8-exists-not-exists-and-the-not-in-trap) | `EXISTS` / `NOT EXISTS`, the `NOT IN` NULL trap |
| — | [9](#9-ctes--the-with-clause) | **CTEs** and the dbt import / logical / final structure |
| — | [10](#10-set-operations-and-cross-join) | `INTERSECT`, `EXCEPT`, `CROSS JOIN` |
| Window Functions | [11](#11-window-functions--core-concepts)–[14](#14-offset-functions-lag-lead-first_value-last_value), [17](#17-window-alias--the-window-clause) | Aggregates inside windows, `FIRST_VALUE` / `LAST_VALUE` |
| — | [15](#15-window-frames-rows-range-groups-) ⭐ | **Window frames: `ROWS` / `RANGE` / `GROUPS`, defaults, ties, `EXCLUDE`** |
| — | [16](#16-filtering-on-window-results), [18](#18-production-window-patterns) | `QUALIFY`, top-N, dedup, period-over-period, gaps & islands |
| Performance Tuning | [19](#19-performance-tuning) | `EXPLAIN ANALYZE`, sargable filters |
| Pivoting | [20](#20-pivoting) | `FILTER`, `VALUES`, DuckDB `PIVOT` / `UNPIVOT` |

> **Label convention (same as `02_practice_intermediate.sql`):** `[Mode example]`, `[Mode practice]`, `[Extension]`. Extension queries use **inline `VALUES` data**, so they run anywhere, in Mode or DuckDB, with no table needed.

---

## Table of Contents

1. [Datasets Used in This Level](#1-datasets-used-in-this-level)
2. [Logical Execution Order (Final)](#2-logical-execution-order-final)
3. [Data Types and Casting](#3-data-types-and-casting)
4. [NULL Toolkit: COALESCE and NULLIF](#4-null-toolkit-coalesce-and-nullif)
5. [Dates and Times](#5-dates-and-times)
6. [String Functions for Cleaning](#6-string-functions-for-cleaning)
7. [Subqueries](#7-subqueries)
8. [EXISTS, NOT EXISTS and the NOT IN Trap](#8-exists-not-exists-and-the-not-in-trap)
9. [CTEs — the WITH Clause](#9-ctes--the-with-clause)
10. [Set Operations and CROSS JOIN](#10-set-operations-and-cross-join)
11. [Window Functions — Core Concepts](#11-window-functions--core-concepts)
12. [Aggregate Window Functions (SUM, COUNT, AVG)](#12-aggregate-window-functions-sum-count-avg)
13. [Ranking Functions (ROW_NUMBER, RANK, DENSE_RANK, NTILE)](#13-ranking-functions-row_number-rank-dense_rank-ntile)
14. [Offset Functions (LAG, LEAD, FIRST_VALUE, LAST_VALUE)](#14-offset-functions-lag-lead-first_value-last_value)
15. [Window Frames: ROWS, RANGE, GROUPS ⭐](#15-window-frames-rows-range-groups-)
16. [Filtering on Window Results](#16-filtering-on-window-results)
17. [Window Alias — the WINDOW Clause](#17-window-alias--the-window-clause)
18. [Production Window Patterns](#18-production-window-patterns)
19. [Performance Tuning](#19-performance-tuning)
20. [Pivoting](#20-pivoting)
21. [Full Clause Order Reference (Final)](#21-full-clause-order-reference-final)

---

## 1. Datasets Used in This Level

| Table | Grain (one row = …) | Key columns |
| --- | --- | --- |
| `tutorial.crunchbase_companies_clean_date` | One company (dates cleaned) | `permalink`, `category_code`, `funding_total_usd`, `founded_at` (raw string), `founded_at_clean` (string, `YYYY-MM-DD`) |
| `tutorial.crunchbase_acquisitions_clean_date` | One acquisition event | `company_permalink`, `acquired_at_cleaned` (timestamp) |
| `tutorial.crunchbase_companies` / `_acquisitions` | Same as Intermediate | adds `founded_quarter` / `acquired_quarter` (`'2012-Q1'`) |
| `tutorial.sf_crime_incidents_2014_01` | One reported incident (raw) | `incidnt_num`, `category`, `descript`, `day_of_week`, `date` (string `MM/DD/YYYY …`), `time` (`HH:MM`), `resolution`, `address`, `location` (`(lat, lon)`), `lat`, `lon` |
| `tutorial.sf_crime_incidents_cleandate` | Same incidents, cleaned | adds `cleaned_date` (timestamp) |
| `tutorial.dc_bikeshare_q1_2012` | One bike ride | `start_terminal`, `end_terminal`, `start_time`, `end_time` (timestamps), `duration_seconds`, `bike_number`, `rider_type` |
| `benn.sample_event_table` | One product event | `event_date`, … |
| `tutorial.worldwide_earthquakes` | One magnitude band (wide: `year_2000` … `year_2012`) | `magnitude`, `year_2000` … `year_2012` |
| `tutorial.crunchbase_investments_part1` / `_part2` | Same as Intermediate | `company_permalink`, `investor_name`, … |

> **Grain note for window functions:** The bikeshare `start_time` is **not unique within a terminal**. Mode's own `RANK()` lesson points out that the 4th and 5th rides from terminal 31000 share a start time. Ties in the `ORDER BY` column are exactly what makes the default window frame behave unexpectedly ([Section 15](#15-window-frames-rows-range-groups-)). Before writing any running total, check whether the `ORDER BY` column is unique within the partition.

---

## 2. Logical Execution Order (Final)

Window functions slot into the pipeline from `02_sql_intermediate.md` Section 4 **after** `HAVING` and **before** `DISTINCT` / `ORDER BY`:

| Step | Clause | What happens |
| --- | --- | --- |
| 1 | `WITH` (CTEs) | Named intermediate results become available |
| 2 | `FROM` + `JOIN` | Build the working set of rows |
| 3 | `WHERE` | Filter individual rows |
| 4 | `GROUP BY` | Split rows into groups |
| 5 | `HAVING` | Filter groups |
| 6 | **Window functions** | Compute `OVER (…)` columns on the rows that survived 1–5 |
| 7 | `QUALIFY` *(DuckDB / Snowflake / BigQuery)* | Filter on window results |
| 8 | `SELECT` | Final projection, aliases |
| 9 | `DISTINCT` | Remove duplicate result rows |
| 10 | `ORDER BY` | Sort the result |
| 11 | `LIMIT` / `OFFSET` | Cap the rows returned |

Three practical consequences:

1. **A window only sees rows that survived `WHERE`.** In Mode's bikeshare query, `WHERE start_time < '2012-01-08'` runs first, so the running total covers Jan 1–7 only.
2. **You can't put a window function in `WHERE`, `GROUP BY` or `HAVING`.** It hasn't been computed yet at those steps. Wrap the query in a subquery or CTE, or use `QUALIFY` ([Section 16](#16-filtering-on-window-results)).
3. **You *can* wrap an aggregate inside a window function.** Mode's lesson says you "can't use window functions and standard aggregations in the same query." That is too strong. The real rule is that the window runs *after* `GROUP BY`, so it can operate on aggregate results:

```sql
-- Each terminal's ride count AND its share of all rides — one query
SELECT start_terminal,
       COUNT(*)                                   AS rides,
       COUNT(*) * 100.0 / SUM(COUNT(*)) OVER ()   AS pct_of_all_rides
  FROM tutorial.dc_bikeshare_q1_2012
 GROUP BY start_terminal;
```

`SUM(COUNT(*)) OVER ()` reads as "sum the per-group counts across the whole grouped result." It's one of the most useful percent-of-total patterns in analytics engineering.

---

## 3. Data Types and Casting

A function only works when the data is **stored** as the right type, not just when it looks right. A column of numbers that contains a comma or a `$` is text, and `SUM` will fail on it.

### Mode's Storage Types

| Imported as | Stored as | Rule |
| --- | --- | --- |
| String | `VARCHAR(1024)` | Any characters, max 1,024 |
| Date/Time | `TIMESTAMP` | `YYYY-MM-DD hh:mm:ss` |
| Number | `DOUBLE PRECISION` | Up to ~17 significant digits |
| Boolean | `BOOLEAN` | `TRUE` / `FALSE` only |

### CAST vs `::`

```sql
SELECT CAST(funding_total_usd AS varchar) AS funding_total_usd_string,   -- SQL standard
       founded_at_clean::varchar          AS founded_at_string           -- PostgreSQL / DuckDB shorthand
  FROM tutorial.crunchbase_companies_clean_date;
```

| Syntax | Portability | Use when |
| --- | --- | --- |
| `CAST(x AS type)` | Every dialect | Shared / production code |
| `x::type` | PostgreSQL, DuckDB, Redshift, Snowflake | Quick work in those engines |
| `TRY_CAST(x AS type)` **[Beyond Mode]** | DuckDB, Snowflake, SQL Server (`SAFE_CAST` in BigQuery) | Messy input: returns `NULL` instead of failing the whole query |

> PostgreSQL has no `TRY_CAST`. A single unparseable value fails the entire query, which is useful as a hard data-quality gate.

### [Beyond Mode] Money Is Never DOUBLE

`DOUBLE PRECISION` is binary floating point, so `0.1 + 0.2` is not exactly `0.3`. That's fine for bike durations and fatal for dollars.

| Type | Exact? | Use for |
| --- | --- | --- |
| `NUMERIC(p, s)` / `DECIMAL(p, s)` | ✅ Exact | Money, tax amounts, anything reconciled to the cent |
| `DOUBLE PRECISION` / `FLOAT` | ❌ Approximate | Measurements, scientific values, ML features |
| `INTEGER` / `BIGINT` | ✅ Exact | Counts, IDs, cents stored as integers |

> **Production rule:** In a 1099 or distributions model, gross and taxable amounts are `NUMERIC(18, 2)`, and every reconciliation compares `NUMERIC` to `NUMERIC`. A float in a money column becomes a one-cent mismatch nobody can explain.

---

## 4. NULL Toolkit: COALESCE and NULLIF

### COALESCE — First Non-NULL Value

`COALESCE(a, b, c, …)` returns the first argument that is not `NULL`.

```sql
SELECT incidnt_num,
       descript,
       COALESCE(descript, 'No Description') AS descript_clean
  FROM tutorial.sf_crime_incidents_cleandate
 ORDER BY descript DESC;
```

Typical uses:

| Pattern | Example |
| --- | --- |
| Default for missing text | `COALESCE(descript, 'No Description')` |
| NULL means zero (business decision!) | `COALESCE(withholding_amt, 0)` |
| Combine keys after a `FULL JOIN` | `COALESCE(acquisitions.month, investments.month)` |

It replaces the `CASE WHEN col IS NULL THEN … ELSE col END` pattern from Intermediate.

### [Beyond Mode] NULLIF — Turn a Value INTO NULL

`NULLIF(a, b)` returns `NULL` when `a = b`, otherwise `a`. It's the inverse of `COALESCE`, with two classic uses:

```sql
-- 1. Divide-by-zero guard: x / 0 errors, x / NULL returns NULL
SELECT total_amt / NULLIF(record_count, 0) AS avg_amt ...

-- 2. Normalize empty strings to NULL before COALESCE
SELECT COALESCE(NULLIF(TRIM(artist), ''), 'Unknown') AS artist_clean ...
```

> The second pattern finishes the "NULL vs empty string" idea from `01_sql_basics.md` Section 8. `NULLIF(TRIM(x), '')` collapses `NULL`, `''` and `'   '` into a single `NULL`.

---

## 5. Dates and Times

### Why Dates Are Year-First

A string date like `MM/DD/YYYY` sorts alphabetically, not chronologically. ISO format (`YYYY-MM-DD`) sorts correctly whether it's stored as a string or as a date. That's why databases use it.

```sql
-- Raw string date: ORDER BY is NOT chronological
SELECT permalink, founded_at
  FROM tutorial.crunchbase_companies_clean_date
 ORDER BY founded_at;

-- Cleaned ISO string: sorts chronologically even though it's still text
SELECT permalink, founded_at, founded_at_clean
  FROM tutorial.crunchbase_companies_clean_date
 ORDER BY founded_at_clean;
```

### Date Arithmetic and INTERVAL

| Operation | Result type |
| --- | --- |
| `timestamp - timestamp` | `INTERVAL` (a span of time, not a date) |
| `timestamp + INTERVAL '1 week'` | `TIMESTAMP` |
| `date + integer` | `DATE` (adds days) |
| `NOW() - timestamp` | `INTERVAL` ("how long ago") |

```sql
-- Time from founding to acquisition (string → timestamp cast required)
SELECT companies.permalink,
       companies.founded_at_clean,
       acquisitions.acquired_at_cleaned,
       acquisitions.acquired_at_cleaned
         - companies.founded_at_clean::timestamp AS time_to_acquisition
  FROM tutorial.crunchbase_companies_clean_date companies
  JOIN tutorial.crunchbase_acquisitions_clean_date acquisitions
    ON acquisitions.company_permalink = companies.permalink
 WHERE founded_at_clean IS NOT NULL;

-- Add an interval written in plain English
SELECT companies.permalink,
       companies.founded_at_clean::timestamp + INTERVAL '1 week' AS plus_one_week
  FROM tutorial.crunchbase_companies_clean_date companies
 WHERE founded_at_clean IS NOT NULL;
```

### EXTRACT and DATE_TRUNC

| Function | Returns | Use for |
| --- | --- | --- |
| `EXTRACT('year' FROM ts)` | A number (`2014`) | Filtering or labeling by a date part |
| `DATE_TRUNC('month', ts)` | A timestamp at the **start** of the period (`2014-01-01 00:00`) | **Grouping by period** — keeps year + month together |

```sql
SELECT cleaned_date,
       EXTRACT('year'  FROM cleaned_date) AS year,
       EXTRACT('month' FROM cleaned_date) AS month,
       EXTRACT('dow'   FROM cleaned_date) AS day_of_week,   -- 0 = Sunday
       DATE_TRUNC('month', cleaned_date)  AS month_start,
       DATE_TRUNC('week',  cleaned_date)  AS week_start      -- weeks start Monday
  FROM tutorial.sf_crime_incidents_cleandate;
```

> **Grouping trap:** `GROUP BY EXTRACT('month' FROM d)` merges January 2013 with January 2014. Use `GROUP BY DATE_TRUNC('month', d)` whenever the data spans more than one year.

### Current Time and Time Zones

```sql
SELECT CURRENT_DATE      AS date,
       CURRENT_TIMESTAMP AS timestamp,
       NOW()             AS now;        -- Mode's server runs in UTC

SELECT CURRENT_TIME AT TIME ZONE 'PST' AS time_pst;   -- PostgreSQL only
```

> **DuckDB note:** DuckDB has no `LOCALTIME` / `LOCALTIMESTAMP` and no `TIME WITH TIME ZONE`, so convert **timestamps** rather than times. `AT TIME ZONE` and named zones need DuckDB's ICU extension (bundled in the Python package). Prefer IANA names (`'America/Los_Angeles'`) over abbreviations (`'PST'`). IANA names handle daylight saving time; `'PST'` is a fixed UTC−8 offset.

### [Beyond Mode] Half-Open Date Ranges

The safest date filter is `>= start AND < next_start`:

```sql
-- ✅ All of March 2014, including 23:59:59.999 on the 31st
 WHERE event_date >= '2014-03-01'
   AND event_date <  '2014-04-01'

-- ❌ BETWEEN on timestamps silently drops everything after 00:00 on the 31st
 WHERE event_date BETWEEN '2014-03-01' AND '2014-03-31'
```

Mode's performance lesson uses the half-open form. Make it a habit: it's correct for dates, timestamps and month-ends of any length.

### [Beyond Mode] Date Spines

A **date spine** is one row per day (or week, or month) with no gaps. Left-joining your facts onto it makes days with zero activity show up as `0` instead of disappearing.

```sql
-- PostgreSQL and DuckDB
SELECT spine.day::date AS day
  FROM generate_series(DATE '2014-01-01', DATE '2014-01-07', INTERVAL '1 day') AS spine(day);
```

> In dbt this is `dbt_utils.date_spine`. Every daily metrics model starts from one.

---

## 6. String Functions for Cleaning

`01_sql_basics.md` Section 16 introduced `LENGTH`, `LEFT`, `RIGHT` and `CONCAT`. The Advanced lesson uses them to **clean** data. Remember that functions nest and evaluate **inside-out**.

### Function Reference

| Function | Signature | Example → Result |
| --- | --- | --- |
| `LEFT` / `RIGHT` | `LEFT(str, n)` | `LEFT('01/31/2014 08:00', 10)` → `'01/31/2014'` |
| `LENGTH` | `LENGTH(str)` | Combine with `RIGHT`: `RIGHT(date, LENGTH(date) - 11)` |
| `TRIM` | `TRIM(both '()' FROM str)` | `'(37.7, -122.4)'` → `'37.7, -122.4'` (also `leading` / `trailing`) |
| `POSITION` | `POSITION('A' IN str)` | First position of `'A'` (1-based, **case-sensitive**, `0` if absent) |
| `STRPOS` | `STRPOS(str, 'A')` | Same as `POSITION`, argument order flipped |
| `SUBSTR` | `SUBSTR(str, start, length)` | `SUBSTR('01/31/2014', 4, 2)` → `'31'` |
| `CONCAT` / `\|\|` | `CONCAT(a, ', ', b)` | `CONCAT` treats `NULL` as `''`; **`\|\|` returns `NULL` if any part is `NULL`** |
| `UPPER` / `LOWER` | `UPPER(str)` | Case normalization |
| `SPLIT_PART` **[Beyond Mode]** | `SPLIT_PART(str, delim, n)` | `SPLIT_PART('37.7, -122.4', ', ', 2)` → `'-122.4'` |
| `REPLACE` **[Beyond Mode]** | `REPLACE(str, from, to)` | `REPLACE('$1,250.00', ',', '')` → `'$1250.00'` |
| `REGEXP_REPLACE` **[Beyond Mode]** | `REGEXP_REPLACE(str, pattern, repl, 'g')` | `REGEXP_REPLACE('(864) 555-0100', '[^0-9]', '', 'g')` → `'8645550100'` |
| `INITCAP` **[Beyond Mode]** | `INITCAP(str)` | `'LARCENY/THEFT'` → `'Larceny/Theft'` (capitalizes **every** word; PostgreSQL only, not in DuckDB) |

> **`CONCAT` vs `||` NULL behavior** is a real-world bug source. `'A' || NULL` is `NULL`; `CONCAT('A', NULL)` is `'A'`. Choose deliberately, and don't switch between them in a refactor without checking.

### Parsing a Coordinate String

```sql
-- location looks like '(37.7795, -122.4103)'
SELECT location,
       TRIM(leading '(' FROM LEFT(location, POSITION(',' IN location) - 1))               AS lat,
       TRIM(trailing ')' FROM RIGHT(location, LENGTH(location) - POSITION(',' IN location))) AS lon
  FROM tutorial.sf_crime_incidents_2014_01;
```

Read it inside-out: find the comma, take everything left of it, then strip the `(`.

### Turning Strings into Dates

Dates exported through Excel or typed by hand often arrive as `MM/DD/YYYY` text. Rebuild them in ISO order, then cast:

```sql
SELECT incidnt_num,
       date,
       (SUBSTR(date, 7, 4) || '-' || LEFT(date, 2) || '-' || SUBSTR(date, 4, 2))::date AS cleaned_date
  FROM tutorial.sf_crime_incidents_2014_01;
```

> **[Beyond Mode]** PostgreSQL's `TO_DATE(date, 'MM/DD/YYYY')` and DuckDB's `STRPTIME(date, '%m/%d/%Y')` parse in one step and fail loudly on bad input. Prefer them in production. The string-slicing version above is for understanding the mechanics.

### Data Wrangling (Mode Concept Lesson)

Mode's wrangling lesson is conceptual: get data into the shape the question needs before you analyze it. In practice that means type-casting, cleaning strings, standardizing NULLs and fixing the grain. In a dbt project, all of that belongs in the **staging layer** (`stg_*` models): one model per source table, light cleaning only, no joins.

---

## 7. Subqueries

A **subquery** (inner query, nested query) is a complete query inside another query. The inner query runs first. Its result becomes a table, a list or a single value for the outer query.

### Where Subqueries Can Go

| Location | Inner query must return | Alias required? | Example use |
| --- | --- | --- | --- |
| `FROM (…) sub` | A table (any shape) | ✅ Yes | Aggregate in stages |
| `JOIN (…) sub ON …` | A table | ✅ Yes | Pre-aggregate before joining |
| `WHERE col = (…)` | **One value** (one row, one column) | ❌ No | Compare to a global MIN / MAX / AVG |
| `WHERE col IN (…)` | **One column**, many rows | ❌ No | Membership in a computed list |
| `SELECT (…) AS x` | One value per outer row | ❌ No | Scalar lookup (see 16b in Intermediate) |

### Basic Subquery in FROM

```sql
SELECT sub.*
  FROM (
        SELECT *
          FROM tutorial.sf_crime_incidents_2014_01
         WHERE day_of_week = 'Friday'
       ) sub
 WHERE sub.resolution = 'NONE';
```

> **Debugging workflow (Mode's advice, and the right one):** write and run the inner query **alone** first. Only when its output is right do you wrap it.

### Aggregating in Multiple Stages

"Average incidents per day, by month and weekday" needs two aggregation passes: count per day, then average those counts. One `GROUP BY` can't do both.

```sql
SELECT LEFT(sub.date, 2)   AS cleaned_month,
       sub.day_of_week,
       AVG(sub.incidents)  AS average_incidents
  FROM (
        SELECT day_of_week,
               date,
               COUNT(incidnt_num) AS incidents
          FROM tutorial.sf_crime_incidents_2014_01
         GROUP BY day_of_week, date
       ) sub
 GROUP BY 1, 2
 ORDER BY 1, 2;
```

> **Mode bug note:** The live tutorial page writes `tutorial_sf_crime_incidents_2014_01` (underscore instead of dot). It must be `tutorial.sf_crime_incidents_2014_01`. The pivot lesson has the same typo for `tutorial.worldwide_earthquakes`.

### Subqueries in Conditional Logic

```sql
-- One-value subquery with =
SELECT *
  FROM tutorial.sf_crime_incidents_2014_01
 WHERE date = (SELECT MIN(date) FROM tutorial.sf_crime_incidents_2014_01);

-- Multi-row subquery requires IN
SELECT *
  FROM tutorial.sf_crime_incidents_2014_01
 WHERE date IN (SELECT date FROM tutorial.sf_crime_incidents_2014_01 ORDER BY date LIMIT 5);
```

> `date` here is a **string**, so `MIN(date)` is the alphabetically first value, not the earliest date. That's a live demonstration of why Section 5 matters.

### Joining Subqueries — Pre-Aggregate to Avoid Fan-Out

Joining two event tables on month first, then counting, produces a **cartesian explosion**. Mode measures 7,414 × 83,893 rows becoming 6.2 million. It also forces a slow `COUNT(DISTINCT)`. Aggregate each side first, then join one row per month to one row per month:

```sql
SELECT COALESCE(acquisitions.month, investments.month) AS month,
       acquisitions.companies_acquired,
       investments.companies_rec_investment
  FROM (
        SELECT acquired_month AS month,
               COUNT(DISTINCT company_permalink) AS companies_acquired
          FROM tutorial.crunchbase_acquisitions
         GROUP BY 1
       ) acquisitions
  FULL JOIN (
        SELECT funded_month AS month,
               COUNT(DISTINCT company_permalink) AS companies_rec_investment
          FROM tutorial.crunchbase_investments
         GROUP BY 1
       ) investments
    ON acquisitions.month = investments.month
 ORDER BY 1 DESC;
```

> This is the fan-out lesson from `02_sql_intermediate.md` Section 17 turned into a fix: **make both sides the same grain before you join them.**

### Subqueries and UNIONs

```sql
SELECT COUNT(*) AS total_rows
  FROM (
        SELECT * FROM tutorial.crunchbase_investments_part1
         UNION ALL
        SELECT * FROM tutorial.crunchbase_investments_part2
       ) sub;
```

### [Beyond Mode] Correlated Subqueries

A **correlated** subquery references the outer row, so it conceptually re-runs once per outer row:

```sql
-- Rides longer than their own terminal's average
SELECT rides.start_terminal, rides.duration_seconds
  FROM tutorial.dc_bikeshare_q1_2012 rides
 WHERE rides.duration_seconds > (
         SELECT AVG(inner_rides.duration_seconds)
           FROM tutorial.dc_bikeshare_q1_2012 inner_rides
          WHERE inner_rides.start_terminal = rides.start_terminal   -- ← correlation
       );
```

The same answer with a window function is usually clearer and faster: compute `AVG(duration_seconds) OVER (PARTITION BY start_terminal)` once, then filter ([Section 16](#16-filtering-on-window-results)).

---

## 8. EXISTS, NOT EXISTS and the NOT IN Trap

**[Beyond Mode]** — promised in `02_sql_intermediate.md` Section 17.

`EXISTS (subquery)` is TRUE if the subquery returns **at least one row**. The columns it selects don't matter (`SELECT 1` is the convention). It stops at the first match.

```sql
-- Semi-join: companies that WERE acquired (no fan-out, unlike an INNER JOIN)
SELECT companies.permalink, companies.name
  FROM tutorial.crunchbase_companies companies
 WHERE EXISTS (
         SELECT 1
           FROM tutorial.crunchbase_acquisitions acquisitions
          WHERE acquisitions.company_permalink = companies.permalink
       );

-- Anti-join: companies NEVER acquired (same result as LEFT JOIN … IS NULL)
SELECT companies.permalink, companies.name
  FROM tutorial.crunchbase_companies companies
 WHERE NOT EXISTS (
         SELECT 1
           FROM tutorial.crunchbase_acquisitions acquisitions
          WHERE acquisitions.company_permalink = companies.permalink
       );
```

### Why Not Just Use NOT IN?

| Pattern | If the subquery contains a `NULL` | Fan-out risk |
| --- | --- | --- |
| `WHERE x NOT IN (subquery)` | ❌ **Returns zero rows**: `x <> NULL` is never TRUE | None |
| `WHERE NOT EXISTS (…)` | ✅ Correct | None |
| `LEFT JOIN … WHERE right.key IS NULL` | ✅ Correct | None (only unmatched rows survive) |
| `WHERE EXISTS (…)` vs `INNER JOIN` | — | `EXISTS` never duplicates left rows; a join does |

> **Rule:** For "in A, not in B," use `NOT EXISTS` or the `LEFT JOIN` anti-join. Never use `NOT IN` against a column that can be NULL. The failure is silent: an empty result, no error.

---

## 9. CTEs — the WITH Clause

**[Beyond Mode]** — Mode never covers CTEs. They are how every dbt model is written.

A **Common Table Expression** is a named subquery declared up front with `WITH`. It reads top-to-bottom like a recipe instead of inside-out like nested parentheses.

```sql
WITH daily_incidents AS (
    SELECT day_of_week,
           date,
           COUNT(incidnt_num) AS incidents
      FROM tutorial.sf_crime_incidents_2014_01
     GROUP BY day_of_week, date
),

monthly_averages AS (
    SELECT LEFT(date, 2)   AS cleaned_month,
           day_of_week,
           AVG(incidents)  AS average_incidents
      FROM daily_incidents
     GROUP BY 1, 2
)

SELECT *
  FROM monthly_averages
 ORDER BY cleaned_month, day_of_week;
```

This is the multi-stage subquery from Section 7, rewritten. Same result, same performance in modern engines, much easier to review.

### Subquery vs CTE

| | Subquery | CTE |
| --- | --- | --- |
| Reads | Inside-out | Top-to-bottom |
| Reuse in one query | Must repeat the code | Reference the name many times |
| Debugging | Copy the inner block out | Change the final `SELECT` to any CTE name |
| Recursion | ❌ | ✅ `WITH RECURSIVE` (hierarchies, org charts) |
| Performance | Same in PostgreSQL 12+ / DuckDB (CTEs are inlined unless `MATERIALIZED`) | Same |

### The dbt Structure: Import → Logical → Final

The dbt Labs style guide organizes every model the same way:

```sql
WITH

-- 1. Import CTEs: one per source, named after the table, light filtering only
rides AS (
    SELECT start_terminal, start_time, duration_seconds
      FROM tutorial.dc_bikeshare_q1_2012
     WHERE start_time < '2012-01-08'
),

-- 2. Logical CTEs: one unit of work each, named for what they do
terminal_totals AS (
    SELECT start_terminal,
           SUM(duration_seconds) AS total_seconds
      FROM rides
     GROUP BY 1
),

-- 3. Final CTE: the model's output
final AS (
    SELECT *
      FROM terminal_totals
)

SELECT * FROM final
```

> **Why `SELECT * FROM final` as the last line?** To debug any step, change that one line to `SELECT * FROM rides` (or any CTE name) and run. That's the dbt convention, and it's what reviewers will expect in your DataVault models.

---

## 10. Set Operations and CROSS JOIN

**[Beyond Mode]** — Intermediate covered `UNION` / `UNION ALL`. The other set operators follow the same stacking rules (same column count, compatible types, names from the first query).

| Operator | Returns | Typical use |
| --- | --- | --- |
| `UNION ALL` | All rows from both | Append datasets |
| `UNION` | All rows, de-duplicated | Rarely; de-dup deliberately |
| `INTERSECT` | Rows in **both** results | "Which companies appear in both investment parts?" |
| `EXCEPT` | Rows in the first result **but not** the second | Reconciliation diffs: "in source, missing from target" |

```sql
-- Companies funded in part 1 but not in part 2
SELECT company_permalink FROM tutorial.crunchbase_investments_part1
EXCEPT
SELECT company_permalink FROM tutorial.crunchbase_investments_part2;
```

> **Reconciliation use:** `EXCEPT` run in **both directions** (`A EXCEPT B`, then `B EXCEPT A`) is the quickest way to prove two tables hold identical rows. It's a standard regression test when you refactor a model: old output `EXCEPT` new output should return nothing. Unlike `=`, set operators treat two `NULL`s as equal.

### CROSS JOIN — Every Row × Every Row

`CROSS JOIN` has no `ON`. It pairs every left row with every right row (a cartesian product). Usually that's a bug; deliberately, it's how you **expand** data. Mode's columns-to-rows pivot ([Section 20](#20-pivoting)) and date spines both depend on it.

---

## 11. Window Functions — Core Concepts

A **window function** calculates across a set of rows related to the current row, **without collapsing them**. `GROUP BY` turns many rows into one. A window function keeps every row and adds a column.

| | `GROUP BY` aggregate | Window function |
| --- | --- | --- |
| Rows out | One per group | **Same as rows in** |
| Can show row detail next to the total? | ❌ | ✅ |
| Syntax | `SUM(x) … GROUP BY g` | `SUM(x) OVER (PARTITION BY g)` |

### Anatomy of OVER

```sql
function_name(args) OVER (
    PARTITION BY ...      -- which rows form a group ("pile")       — optional
    ORDER BY ...          -- the order of rows inside each pile     — optional*
    frame_clause          -- which slice of the pile each row sees  — optional
)
```

\* Required for ranking and offset functions.

| Part | Plain-English meaning | If omitted |
| --- | --- | --- |
| `PARTITION BY` | Split rows into separate piles; the calculation restarts in each | The whole result is one pile |
| `ORDER BY` | Line the rows up inside each pile | No order: every row is a **peer** of every other |
| Frame | For *this* row, which rows of its pile count | Depends on whether `ORDER BY` is present ([Section 15](#15-window-frames-rows-range-groups-)) |

### The Two Key Facts

1. **`ORDER BY` inside `OVER` does not sort your output.** It orders rows for the calculation only. Add an outer `ORDER BY` to control what you see.
2. **Adding `ORDER BY` inside `OVER` changes what an aggregate means.** Without it, `SUM` is the pile's grand total on every row. With it, `SUM` becomes a running total, because the default frame changes ([Section 15](#15-window-frames-rows-range-groups-)).

### Window Function Families

| Family | Functions | Needs `ORDER BY`? | Uses the frame? |
| --- | --- | --- | --- |
| Aggregate | `SUM`, `COUNT`, `AVG`, `MIN`, `MAX` | Optional | ✅ Yes |
| Ranking | `ROW_NUMBER`, `RANK`, `DENSE_RANK`, `NTILE`, `PERCENT_RANK`, `CUME_DIST` | ✅ Yes | ❌ No (always whole partition) |
| Offset | `LAG`, `LEAD` | ✅ Yes | ❌ No |
| Value | `FIRST_VALUE`, `LAST_VALUE`, `NTH_VALUE` | ✅ Yes | ✅ **Yes — gotcha** |

---

## 12. Aggregate Window Functions (SUM, COUNT, AVG)

### Partition Total (No ORDER BY)

```sql
SELECT start_terminal,
       duration_seconds,
       SUM(duration_seconds) OVER (PARTITION BY start_terminal) AS start_terminal_total
  FROM tutorial.dc_bikeshare_q1_2012
 WHERE start_time < '2012-01-08';
```

Every row in a terminal shows the **same** total. There's no `ORDER BY`, so all rows are peers and each one sees the whole pile.

### Running Total (With ORDER BY)

```sql
SELECT start_terminal,
       start_time,                -- always SELECT the ORDER BY column you're windowing on
       duration_seconds,
       SUM(duration_seconds) OVER
         (PARTITION BY start_terminal ORDER BY start_time) AS running_total
  FROM tutorial.dc_bikeshare_q1_2012
 WHERE start_time < '2012-01-08';
```

> Mode's version leaves out `start_time` from the `SELECT`. That hides the ties that explain why `running_total` sometimes repeats instead of increasing. [Section 15](#15-window-frames-rows-range-groups-) walks through it step by step.

### Same Idea with COUNT and AVG

With `ORDER BY`, `COUNT` becomes a running count and `AVG` a running (cumulative) average. Without it, they're the partition's count and average on every row.

### Percent of Partition Total

```sql
SELECT start_terminal,
       duration_seconds,
       duration_seconds * 100.0
         / SUM(duration_seconds) OVER (PARTITION BY start_terminal) AS pct_of_terminal_time
  FROM tutorial.dc_bikeshare_q1_2012
 WHERE start_time < '2012-01-08';
```

> Multiply by `100.0` (not `100`) so the division is never integer division. Same rule as `02_sql_intermediate.md` Section 2.

---

## 13. Ranking Functions (ROW_NUMBER, RANK, DENSE_RANK, NTILE)

### How They Differ on Ties

Ordering by a column with ties (`duration = 300, 200, 200, 100`):

| duration | `ROW_NUMBER()` | `RANK()` | `DENSE_RANK()` |
| --- | --- | --- | --- |
| 300 | 1 | 1 | 1 |
| 200 | 2 | 2 | 2 |
| 200 | 3 ⚠️ *arbitrary which tie gets 2 vs 3* | 2 | 2 |
| 100 | 4 | **4** (skips 3) | **3** (no gap) |

| Function | Ties get | Gaps after ties | Use for |
| --- | --- | --- | --- |
| `ROW_NUMBER()` | Different numbers | — | Exactly-N per group, de-duplication |
| `RANK()` | Same number | ✅ Yes | Competition ranking ("tied for 2nd, next is 4th") |
| `DENSE_RANK()` | Same number | ❌ No | "Top 3 distinct values" |

> **Determinism rule:** `ROW_NUMBER()` over a column with ties is **non-deterministic**. Two runs can number tied rows differently. Always add a unique tiebreaker: `ORDER BY start_time, id`. In a dbt model, a non-deterministic `ROW_NUMBER` makes snapshots and incremental models flap between runs.

```sql
SELECT start_terminal,
       start_time,
       duration_seconds,
       ROW_NUMBER() OVER (PARTITION BY start_terminal ORDER BY start_time) AS row_number,
       RANK()       OVER (PARTITION BY start_terminal ORDER BY start_time) AS rank
  FROM tutorial.dc_bikeshare_q1_2012
 WHERE start_time < '2012-01-08';
```

Run this and look at terminal 31000. The tied start times show `RANK` repeating while `ROW_NUMBER` keeps counting. These are the same ties that make the running total repeat.

### NTILE — Buckets

`NTILE(n)` splits each partition into `n` roughly equal buckets in `ORDER BY` order:

```sql
SELECT start_terminal,
       duration_seconds,
       NTILE(4)   OVER (PARTITION BY start_terminal ORDER BY duration_seconds) AS quartile,
       NTILE(100) OVER (PARTITION BY start_terminal ORDER BY duration_seconds) AS percentile
  FROM tutorial.dc_bikeshare_q1_2012
 WHERE start_time < '2012-01-08'
 ORDER BY start_terminal, duration_seconds;
```

> **Small-partition caveat:** With fewer rows than buckets, `NTILE(100)` just numbers rows 1, 2, 3…. It isn't a real percentile. For true percentile **values**, use `PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY x)` (an aggregate). For a row's relative position from 0 to 1, use `PERCENT_RANK()` or `CUME_DIST()`.

---

## 14. Offset Functions (LAG, LEAD, FIRST_VALUE, LAST_VALUE)

### LAG and LEAD

| Function | Pulls a value from | Signature |
| --- | --- | --- |
| `LAG` | A **previous** row | `LAG(col, offset = 1, default = NULL)` |
| `LEAD` | A **following** row | `LEAD(col, offset = 1, default = NULL)` |

```sql
SELECT start_terminal,
       duration_seconds,
       duration_seconds
         - LAG(duration_seconds, 1) OVER (PARTITION BY start_terminal ORDER BY duration_seconds) AS difference
  FROM tutorial.dc_bikeshare_q1_2012
 WHERE start_time < '2012-01-08'
 ORDER BY start_terminal, duration_seconds;
```

The first row of each partition gets `NULL`, because there's no previous row. Either filter it out in an outer query or give `LAG` a default: `LAG(x, 1, 0)`.

> **Replaces self-joins:** The "compare to the previous row" self join from `02_sql_intermediate.md` Section 16 is one `LAG` here: a single pass over the data, no join.

> **Mode example caveat:** Mode's outer-query version puts `ORDER BY` **inside** the subquery. SQL doesn't guarantee that inner order survives into the outer result. Put the `ORDER BY` on the outermost query.

### [Beyond Mode] FIRST_VALUE and LAST_VALUE — the Frame Gotcha

These return the value from the first or last row **of the frame**, not of the partition. Under the default frame (which ends at the current row and its peers), `LAST_VALUE` simply returns the current row's value:

```sql
-- ❌ Looks right, returns the CURRENT row's value
LAST_VALUE(status) OVER (PARTITION BY ticket ORDER BY updated_at)

-- ✅ Extend the frame to the whole partition
LAST_VALUE(status) OVER (
    PARTITION BY ticket ORDER BY updated_at
    ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
)

-- ✅ Often simpler: flip the order and use FIRST_VALUE
FIRST_VALUE(status) OVER (PARTITION BY ticket ORDER BY updated_at DESC)
```

The PostgreSQL manual warns that the default frame "is likely to give unhelpful results for `last_value`." That's the frame concept in the next section.

---

## 15. Window Frames: ROWS, RANGE, GROUPS ⭐

**[Beyond Mode]** — the most important missing piece of Mode's window lesson.

### What a Frame Is

Once rows are partitioned and ordered, the **frame** answers one question for each row: *which rows in my pile do I include in my calculation?*

```
{ ROWS | RANGE | GROUPS } BETWEEN frame_start AND frame_end [ EXCLUDE … ]

frame_start / frame_end:
    UNBOUNDED PRECEDING   -- the first row of the partition
    n PRECEDING           -- n units before the current row
    CURRENT ROW           -- the current row (see below: depends on the unit!)
    n FOLLOWING           -- n units after the current row
    UNBOUNDED FOLLOWING   -- the last row of the partition
```

### The Three Units: How "1 Step Back" Is Measured

| Unit | Counts by | `CURRENT ROW` means | Best for |
| --- | --- | --- | --- |
| `ROWS` | Physical rows | **This exact row** | Running totals, "last N rows" moving averages |
| `RANGE` | **Values** of the `ORDER BY` column | This row **and all its peers** (same `ORDER BY` value) | Time windows: "last 7 days" |
| `GROUPS` | Peer groups (sets of tied rows) | This row's whole peer group | "Last N distinct dates" |

> **Peers** are rows with identical `ORDER BY` values in the same partition. Peers are the whole story behind the repeating running total.

### The Defaults (Memorize This Table)

| What you wrote | Default frame | Effect on `SUM` |
| --- | --- | --- |
| `OVER ()` or `OVER (PARTITION BY g)` | Entire partition (all rows are peers) | Partition grand total on every row |
| `OVER (… ORDER BY x)` | **`RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW`** | Running total **that includes all ties of the current row** |

This default is the SQL standard. PostgreSQL, DuckDB, MySQL, Snowflake and BigQuery all share it.

### Why the Running Total Repeats — Step by Step

Synthetic version of the bikeshare data (`03_practice_advanced.sql`, 15a, runs as-is):

| ride | terminal | start_time | duration |
| --- | --- | --- | --- |
| A | 31000 | 08:00 | 300 |
| B | 31000 | 08:05 | 200 |
| C | 31000 | 08:05 | 100 |
| D | 31000 | 08:10 | 400 |
| E | 31001 | 07:30 | 500 |
| F | 31001 | 09:00 | 250 |

**Step 1 — `WHERE`** keeps the rows above.  
**Step 2 — `PARTITION BY start_terminal`** makes two piles: {A, B, C, D} and {E, F}.  
**Step 3 — `ORDER BY start_time`** lines up each pile. **B and C are peers** (both 08:05).  
**Step 4 — Frame + `SUM`:** each row adds up its frame.

| ride | start_time | `RANGE` frame (default) | `RANGE` total | `ROWS` frame | `ROWS` total | `GROUPS 1 PRECEDING` frame | `GROUPS` total |
| --- | --- | --- | --- | --- | --- | --- | --- |
| A | 08:00 | A | **300** | A | **300** | A | 300 |
| B | 08:05 | A, B, **C** | **600** | A, B | **500** | A, B, C | 600 |
| C | 08:05 | A, **B**, C | **600** | A, B, C | **600** | A, B, C | 600 |
| D | 08:10 | A, B, C, D | **1000** | A, B, C, D | **1000** | B, C, D | 700 |
| E | 07:30 | E | 500 (reset) | E | 500 | E | 500 |
| F | 09:00 | E, F | 750 | E, F | 750 | E, F | 750 |

- **`RANGE` (default):** B and C are peers, so the frame for *each* of them stretches to the end of the peer group. Both show 600: the "stalled" running total.
- **`ROWS`:** every row stops at itself, so the total rises on every row. But which of B and C comes first is **arbitrary** unless you add a tiebreaker.
- **`GROUPS BETWEEN 1 PRECEDING AND CURRENT ROW`:** "my peer group plus the one before it." For D, that's {B, C} + {D} = 700.

### The Production-Grade Running Total

```sql
SUM(duration_seconds) OVER (
    PARTITION BY start_terminal
    ORDER BY start_time, id                                -- unique tiebreaker → deterministic
    ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW       -- explicit frame → no peer surprises
) AS running_total
```

Three rules, every time:

1. **Write the frame explicitly.** Don't rely on the default.
2. **Make `ORDER BY` unique** within the partition by appending a key column. (Check that a unique key exists with `SELECT * … LIMIT 5`. If there's no `id`, use a combination that is unique, e.g. `start_time, bike_number`.)
3. **Add an outer `ORDER BY`** with the same columns so the output matches the calculation order.

> **When `RANGE` is what you want:** if the business question is "total as of each timestamp," such as an account balance at the **end** of each day, then tied same-day transactions *should* all show the end-of-day balance. That's `RANGE`. Pick the unit on purpose, and leave a comment saying why.

### Moving Windows

```sql
-- Moving average of the last 3 rows (current + 2 before)
AVG(x) OVER (ORDER BY day ROWS BETWEEN 2 PRECEDING AND CURRENT ROW)

-- Centered 3-row average
AVG(x) OVER (ORDER BY day ROWS BETWEEN 1 PRECEDING AND 1 FOLLOWING)

-- Trailing 7 CALENDAR days (PostgreSQL 11+, DuckDB) — correct even with missing days
SUM(x) OVER (ORDER BY day RANGE BETWEEN INTERVAL '6 days' PRECEDING AND CURRENT ROW)
```

| Want | Use | Why |
| --- | --- | --- |
| Last 7 **rows** | `ROWS 6 PRECEDING` | Counts rows; wrong if a day has 0 rows or 3 rows |
| Last 7 **calendar days** | `RANGE INTERVAL '6 days' PRECEDING` | Measures distance in the `ORDER BY` value |
| Last 7 **distinct dates** | `GROUPS 6 PRECEDING` | Counts peer groups |

> **Gotcha:** `ROWS 6 PRECEDING` is a "7-day" average only if there is exactly one row per day with no gaps. Join to a date spine first ([Section 5](#5-dates-and-times)) or use `RANGE` with an interval.

### Frame Exclusion

`EXCLUDE` (PostgreSQL 11+, DuckDB) removes rows from inside the frame:

| Option | Removes |
| --- | --- |
| `EXCLUDE CURRENT ROW` | The current row |
| `EXCLUDE GROUP` | The current row and its peers |
| `EXCLUDE TIES` | Its peers, but keeps the current row |
| `EXCLUDE NO OTHERS` | Nothing (the default) |

```sql
-- Compare each ride to the average of all OTHER rides at its terminal
AVG(duration_seconds) OVER (
    PARTITION BY start_terminal
    ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
    EXCLUDE CURRENT ROW
) AS avg_of_other_rides
```

### Which Functions Use the Frame?

| Respect the frame | Ignore the frame (always use the whole partition) |
| --- | --- |
| `SUM`, `COUNT`, `AVG`, `MIN`, `MAX`, `FIRST_VALUE`, `LAST_VALUE`, `NTH_VALUE` | `ROW_NUMBER`, `RANK`, `DENSE_RANK`, `NTILE`, `PERCENT_RANK`, `CUME_DIST`, `LAG`, `LEAD` |

---

## 16. Filtering on Window Results

Window functions run after `WHERE` ([Section 2](#2-logical-execution-order-final)), so this fails:

```sql
-- ❌ ERROR: window functions are not allowed in WHERE
SELECT * FROM rides WHERE ROW_NUMBER() OVER (…) <= 5;
```

Two fixes:

| Approach | Works in | Example |
| --- | --- | --- |
| Subquery or CTE, then `WHERE` | **Everywhere** (PostgreSQL, Mode) | See below |
| `QUALIFY` | DuckDB, Snowflake, BigQuery, Databricks (**not** PostgreSQL) | `QUALIFY ROW_NUMBER() OVER (…) <= 5` |

```sql
-- Portable: CTE + WHERE
WITH ranked AS (
    SELECT start_terminal,
           start_time,
           duration_seconds,
           RANK() OVER (PARTITION BY start_terminal ORDER BY duration_seconds DESC) AS rank
      FROM tutorial.dc_bikeshare_q1_2012
     WHERE start_time < '2012-01-08'
)

SELECT *
  FROM ranked
 WHERE rank <= 5
 ORDER BY start_terminal, rank;
```

```sql
-- DuckDB / Snowflake: QUALIFY does the same in one block
SELECT start_terminal, start_time, duration_seconds
  FROM rides
QUALIFY RANK() OVER (PARTITION BY start_terminal ORDER BY duration_seconds DESC) <= 5;
```

> `QUALIFY` is to window functions what `HAVING` is to aggregates. Learn the CTE form first: it's portable and it's what Mode runs. Use `QUALIFY` in DuckDB and in Snowflake / BigQuery dbt projects.

> **`RANK` vs `ROW_NUMBER` for top-N:** `RANK() <= 5` can return **more** than 5 rows when there are ties at 5th place. Use `ROW_NUMBER` with a tiebreaker when you need **exactly** 5.

---

## 17. Window Alias — the WINDOW Clause

When several functions share the same window, name it once:

```sql
SELECT start_terminal,
       duration_seconds,
       NTILE(4)   OVER ntile_window AS quartile,
       NTILE(5)   OVER ntile_window AS quintile,
       NTILE(100) OVER ntile_window AS percentile
  FROM tutorial.dc_bikeshare_q1_2012
 WHERE start_time < '2012-01-08'
WINDOW ntile_window AS (PARTITION BY start_terminal ORDER BY duration_seconds)
 ORDER BY start_terminal, duration_seconds;
```

- `WINDOW` goes **after** `WHERE` / `GROUP BY` / `HAVING` and **before** `ORDER BY`.
- A named window can be extended: `OVER (ntile_window ROWS BETWEEN 2 PRECEDING AND CURRENT ROW)` adds a frame to the base window.
- One definition means one place to fix the tiebreaker.

---

## 18. Production Window Patterns

**[Beyond Mode]** — the five window patterns that show up most often in analytics engineering work and interviews. All are in `03_practice_advanced.sql` §18 with synthetic data.

### 18a. Top-N per Group

Covered in [Section 16](#16-filtering-on-window-results): rank in a CTE, filter in the outer query.

### 18b. De-duplicate: Keep the Latest Record per Key

The most common window pattern in staging models: a source sends the same record several times, and you keep the newest.

```sql
WITH ranked AS (
    SELECT *,
           ROW_NUMBER() OVER (
               PARTITION BY record_id
               ORDER BY loaded_at DESC, source_file DESC    -- tiebreaker
           ) AS rn
      FROM raw_records
)

SELECT * FROM ranked WHERE rn = 1;
```

> This is exactly how a dbt staging model de-duplicates a re-sent file. Pair it with a `unique` test on `record_id` downstream.

### 18c. Period-over-Period Change

```sql
WITH monthly AS (
    SELECT DATE_TRUNC('month', paid_at) AS month,
           SUM(gross_amt)               AS gross_amt
      FROM distributions
     GROUP BY 1
)

SELECT month,
       gross_amt,
       LAG(gross_amt) OVER (ORDER BY month)                         AS prior_month,
       gross_amt - LAG(gross_amt) OVER (ORDER BY month)             AS mom_change,
       ROUND((gross_amt / NULLIF(LAG(gross_amt) OVER (ORDER BY month), 0) - 1) * 100, 1) AS mom_pct
  FROM monthly
 ORDER BY month;
```

> Aggregate to the reporting grain **first**, then window. `LAG` over raw rows would compare individual transactions, not months. `NULLIF` guards against division by zero.

### 18d. Running Balance per Account (Year-to-Date)

```sql
SELECT participant_id,
       paid_at,
       gross_amt,
       SUM(gross_amt) OVER (
           PARTITION BY participant_id, EXTRACT(YEAR FROM paid_at)    -- resets each tax year
           ORDER BY paid_at, distribution_id
           ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
       ) AS ytd_gross
  FROM distributions
 ORDER BY participant_id, paid_at, distribution_id;
```

> The year-to-date gross per participant is the number that has to tie out to Box 1 of the 1099-R. Partitioning by participant **and** tax year makes the total reset on January 1st.

### 18e. Gaps and Islands — Consecutive Streaks

"Find each run of consecutive days with activity." The trick: subtract a row number from the date. Within a consecutive run both increase by 1 each row, so the difference stays **constant** and becomes a group key.

| activity_day | `ROW_NUMBER` | `activity_day - ROW_NUMBER` | island |
| --- | --- | --- | --- |
| Jan 1 | 1 | Dec 31 | A |
| Jan 2 | 2 | Dec 31 | A |
| Jan 3 | 3 | Dec 31 | A |
| Jan 6 | 4 | **Jan 2** | B |
| Jan 7 | 5 | Jan 2 | B |

```sql
WITH numbered AS (
    SELECT activity_day,
           activity_day - CAST(ROW_NUMBER() OVER (ORDER BY activity_day) AS INTEGER) AS island_key
      FROM daily_activity
)

SELECT MIN(activity_day) AS streak_start,
       MAX(activity_day) AS streak_end,
       COUNT(*)          AS streak_days
  FROM numbered
 GROUP BY island_key
 ORDER BY streak_start;
```

> Classic interview question ("longest login streak"). Production uses include consecutive trading days above a threshold and runs of failed pipeline loads. Requires one row per day: de-duplicate first.

---

## 19. Performance Tuning

A query gets faster when the database does **less work**. What you control:

| Lever | What to do |
| --- | --- |
| **Table size** | Filter early (`WHERE` on dates); select only the columns you need |
| **Joins** | Reduce rows **before** the join (pre-aggregate in a subquery or CTE) |
| **Aggregations** | Avoid `COUNT(DISTINCT)` on huge sets when an exact count isn't needed |

What you can't control: other users' concurrent load, and the database engine itself.

### Reduce Rows Early

```sql
SELECT *
  FROM benn.sample_event_table
 WHERE event_date >= '2014-03-01'
   AND event_date <  '2014-04-01';
```

> **`LIMIT` doesn't speed up aggregates.** `SELECT COUNT(*) … LIMIT 100` counts everything, then limits the one-row result. To test logic on a sample, put the `LIMIT` in the **innermost** subquery. Treat that result as a test, never as an answer.

### Pre-Aggregate Before Joining

```sql
-- 26,298 player rows → 252 school rows → join 252 instead of 26,298
SELECT teams.conference,
       sub.*
  FROM (
        SELECT players.school_name,
               COUNT(*) AS players
          FROM benn.college_football_players players
         GROUP BY 1
       ) sub
  JOIN benn.college_football_teams teams
    ON teams.school_name = sub.school_name;
```

> Correctness comes before speed. Pre-aggregation is only valid when the outer query doesn't need row-level detail.

### EXPLAIN — Read the Query Plan

```sql
EXPLAIN
SELECT *
  FROM benn.sample_event_table
 WHERE event_date >= '2014-03-01'
   AND event_date <  '2014-04-01'
 LIMIT 100;
```

- Read the plan **bottom-up**: the deepest or lowest step runs first.
- `cost=start..total` is a **relative** estimate. Use it to compare two versions of the same query, not as seconds.
- Workflow: `EXPLAIN` → change the expensive step → `EXPLAIN` again → compare costs.

| [Beyond Mode] Tool | What it adds |
| --- | --- |
| `EXPLAIN ANALYZE` | **Actually runs** the query and shows real row counts and timings. Never use it on `INSERT` / `UPDATE` / `DELETE` against data you care about. |
| Sargable filters | `WHERE event_date >= '2014-03-01'` can use an index; `WHERE EXTRACT(YEAR FROM event_date) = 2014` usually can't, because it wraps the column in a function. Filter on the **bare column**. |
| Partition / cluster pruning | In warehouses (Snowflake, BigQuery), filtering on the partition or cluster column skips whole files. Same idea as sargable, at warehouse scale. |
| DuckDB | `EXPLAIN` and `EXPLAIN ANALYZE` work the same; the output is a tree diagram. |

---

## 20. Pivoting

### Rows → Columns (Long → Wide)

Aggregate to long format in a subquery, then spread categories into columns with conditional aggregation. This is the same technique as `02_sql_intermediate.md` Section 6, applied to a pre-aggregated subquery:

```sql
SELECT conference,
       SUM(players)                                           AS total_players,
       SUM(CASE WHEN year = 'FR' THEN players ELSE NULL END)  AS fr,
       SUM(CASE WHEN year = 'SO' THEN players ELSE NULL END)  AS so,
       SUM(CASE WHEN year = 'JR' THEN players ELSE NULL END)  AS jr,
       SUM(CASE WHEN year = 'SR' THEN players ELSE NULL END)  AS sr
  FROM (
        SELECT teams.conference AS conference,
               players.year,
               COUNT(1)         AS players
          FROM benn.college_football_players players
          JOIN benn.college_football_teams teams
            ON teams.school_name = players.school_name
         GROUP BY 1, 2
       ) sub
 GROUP BY 1
 ORDER BY 2 DESC;
```

### Columns → Rows (Wide → Long)

`worldwide_earthquakes` has one column per year (`year_2000` … `year_2012`). That shape is built for reading, not for analysis. Unpivoting takes three steps:

1. Build a one-column list of the years.
2. `CROSS JOIN` it to the wide table, so each row is repeated 13 times.
3. Use `CASE` to pick the matching year's column for each repeated row.

```sql
SELECT years.year,
       earthquakes.magnitude,
       CASE years.year
         WHEN 2000 THEN year_2000  WHEN 2001 THEN year_2001  WHEN 2002 THEN year_2002
         WHEN 2003 THEN year_2003  WHEN 2004 THEN year_2004  WHEN 2005 THEN year_2005
         WHEN 2006 THEN year_2006  WHEN 2007 THEN year_2007  WHEN 2008 THEN year_2008
         WHEN 2009 THEN year_2009  WHEN 2010 THEN year_2010  WHEN 2011 THEN year_2011
         WHEN 2012 THEN year_2012
         ELSE NULL
       END AS number_of_earthquakes
  FROM tutorial.worldwide_earthquakes earthquakes
 CROSS JOIN (
        VALUES (2000),(2001),(2002),(2003),(2004),(2005),(2006),
               (2007),(2008),(2009),(2010),(2011),(2012)
       ) AS years(year);
```

> **[Beyond Mode]** `VALUES (…), (…) AS t(col)` builds the year list in one line instead of 13 `UNION ALL`s. It works in PostgreSQL and DuckDB.

### [Beyond Mode] Native PIVOT / UNPIVOT

| Engine | Rows → columns | Columns → rows |
| --- | --- | --- |
| PostgreSQL / Mode | `SUM(CASE …)` or `FILTER` | `CROSS JOIN` + `CASE` (above), or `CROSS JOIN LATERAL (VALUES …)` |
| DuckDB | `PIVOT tbl ON year USING SUM(players)` | `UNPIVOT tbl ON COLUMNS('year_.*') INTO NAME year VALUE n` |
| Snowflake / SQL Server | `PIVOT` / `UNPIVOT` operators | Same |
| dbt | `dbt_utils.pivot` / `dbt_utils.unpivot` macros | Same |

> **Analytics engineering rule:** store data **long** (one row per entity × attribute), because that's what joins, filters and BI tools want. Pivot to **wide** only at the very end, for presentation.

---

## 21. Full Clause Order Reference (Final)

| Order | Clause | Purpose | Required? |
| --- | --- | --- | --- |
| 0 | `WITH` | Named CTEs used by the query below | No |
| 1 | `SELECT` | Columns, expressions, `CASE`, window functions | Yes |
| 2 | `FROM` | Driving table, subquery or CTE | Yes |
| 3 | `JOIN … ON` | Additional tables / subqueries | No |
| 4 | `WHERE` | Filter rows (no aggregates, no window functions) | No |
| 5 | `GROUP BY` | Group rows | No |
| 6 | `HAVING` | Filter groups | No |
| 7 | `WINDOW` | Named window definitions | No |
| 8 | `QUALIFY` | Filter on window results *(DuckDB / Snowflake / BigQuery only)* | No |
| 9 | `ORDER BY` | Sort the final result | No |
| 10 | `LIMIT` / `OFFSET` | Cap rows | No |

```sql
-- Template showing every clause in written order (DuckDB — QUALIFY isn't PostgreSQL)
WITH source AS (
    SELECT key_col, group_col, order_col, unique_id, value_col
      FROM schema.table_name
     WHERE order_col >= '2026-01-01'
)

SELECT group_col,
       key_col,
       SUM(value_col)                                   AS total_value,
       RANK() OVER w                                    AS rank_in_group,
       SUM(SUM(value_col)) OVER (PARTITION BY group_col) AS group_total
  FROM source
 GROUP BY group_col, key_col
HAVING SUM(value_col) > 0
WINDOW w AS (PARTITION BY group_col ORDER BY SUM(value_col) DESC, key_col)
QUALIFY RANK() OVER w <= 10
 ORDER BY group_col, rank_in_group
 LIMIT 100;
```

---

## Sources

- [Mode / ThoughtSpot SQL Tutorial — Advanced](https://www.thoughtspot.com/sql-tutorial/sql-window-functions): Data Types, Date Format, String Functions, Subqueries, Window Functions, Performance Tuning, Pivoting
- [PostgreSQL docs — Window Function Calls (frame syntax)](https://www.postgresql.org/docs/current/sql-expressions.html#SYNTAX-WINDOW-FUNCTIONS) and [Window Functions](https://www.postgresql.org/docs/current/functions-window.html)
- [MySQL 8.0 Reference — Window Function Frame Specification](https://dev.mysql.com/doc/refman/8.0/en/window-functions-frames.html) (default frame and peers, stated clearly)
- [DuckDB docs — QUALIFY](https://duckdb.org/docs/stable/sql/query_syntax/qualify)
- [dbt Labs — How we style our SQL](https://docs.getdbt.com/best-practices/how-we-style/2-how-we-style-our-sql) (import / logical / final CTEs)

---

*Next: SQL Analytics Training (Mode's applied case studies), or HackerRank / DataLemur advanced problems (window functions and gaps-and-islands) as interview practice.*
