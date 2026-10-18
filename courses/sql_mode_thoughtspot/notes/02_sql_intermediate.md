# SQL Intermediate — Complete Reference Notes

> **Author:** Manuel Reyes | [github.com/manuel-reyes-ml](https://github.com/manuel-reyes-ml)  
> **Source:** [Mode SQL Tutorial — Intermediate (now hosted by ThoughtSpot)](https://www.thoughtspot.com/sql-tutorial/intro-to-intermediate-sql)  
> **Companion file:** `queries/02_practice_intermediate.sql` (hands-on exercises)  
> **Previous file:** `notes/01_sql_basics.md`  
> **Stage:** 1 — Internal AI Builder ([Roadmap v10.0](https://manuel-reyes-ml.github.io/learning_journey/roadmap.html))  
> **Dialect:** PostgreSQL (Mode's engine) — every query also runs in DuckDB, the local practice stack  
> **Last updated:** 2026-10-14

---



## Table of Contents

1. [Datasets Used in This Level](#1-datasets-used-in-this-level)
2. [Aggregation Nuances (Beyond the Basics)](#2-aggregation-nuances-beyond-the-basics)
3. [HAVING](#3-having)
4. [Logical Execution Order](#4-logical-execution-order)
5. [CASE — Conditional Logic](#5-case--conditional-logic)
6. [CASE with Aggregates (Conditional Aggregation and Pivoting)](#6-case-with-aggregates-conditional-aggregation-and-pivoting)
7. [DISTINCT Inside Aggregates](#7-distinct-inside-aggregates)
8. [Joins — Core Concepts](#8-joins--core-concepts)
9. [INNER JOIN](#9-inner-join)
10. [Outer Joins — LEFT and RIGHT](#10-outer-joins--left-and-right)
11. [Filtering in ON vs WHERE](#11-filtering-in-on-vs-where)
12. [FULL OUTER JOIN](#12-full-outer-join)
13. [UNION and UNION ALL](#13-union-and-union-all)
14. [Joins with Comparison Operators](#14-joins-with-comparison-operators)
15. [Joins on Multiple Keys](#15-joins-on-multiple-keys)
16. [Self Joins](#16-self-joins)
17. [Production Patterns: Anti-Joins, Fan-Out and Duplicate Checks](#17-production-patterns-anti-joins-fan-out-and-duplicate-checks)
18. [Full Clause Order Reference (Updated)](#18-full-clause-order-reference-updated)

---



## 1. Datasets Used in This Level

Intermediate SQL moves from single-table queries to **multiple related tables**. These are the tables used throughout this file:


| Table                                              | Grain (one row = …)                              | Key columns                                                                                                                     |
| -------------------------------------------------- | ------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------- |
| `tutorial.aapl_historical_stock_price`             | One trading day of Apple stock                   | `date`, `year`, `month`, `open`, `high`, `low`, `close`, `volume`                                                               |
| `benn.college_football_players`                    | One player                                       | `player_name`, `school_name`, `position`, `height`, `weight`, `year` (FR/SO/JR/SR), `state`                                     |
| `benn.college_football_teams`                      | One school                                       | `school_name`, `division`, `conference`                                                                                         |
| `tutorial.crunchbase_companies`                    | One company                                      | `permalink`, `name`, `status`, `state_code`, `founded_year`                                                                     |
| `tutorial.crunchbase_acquisitions`                 | One acquisition event                            | `company_permalink`, `acquirer_permalink`, `acquired_at`                                                                        |
| `tutorial.crunchbase_investments`                  | One investment (company × investor × round)      | `company_permalink`, `company_name`, `investor_name`, `investor_permalink`, `investor_country_code`, `funded_at`, `funded_year` |
| `tutorial.crunchbase_investments_part1` / `_part2` | Same as above, split in two for the UNION lesson | Same columns                                                                                                                    |


> **Schema note:** The college football tables now live in the `benn` schema on the ThoughtSpot-hosted tutorial. Older versions of the tutorial (and many blog posts) reference them as `tutorial.college_football_players` / `tutorial.college_football_teams`. Same data, different schema prefix.

> **Why "grain" matters:** The **grain** of a table is what one row represents. Before every join, state the grain of both tables out loud. Most join bugs (duplicated rows, inflated sums) come from joining tables with different grains without realizing it — see [Section 17](#17-production-patterns-anti-joins-fan-out-and-duplicate-checks).

---



## 2. Aggregation Nuances (Beyond the Basics)

The core aggregate functions were covered in `01_sql_basics.md` (Sections 14–15). Intermediate SQL adds the details that cause real bugs.

### COUNT Works on Any Data Type

`COUNT` does not care whether a column holds numbers, text, or dates — it only checks for `NULL`:

```sql
-- Non-null rows in the low column
SELECT COUNT(low) AS low_count
  FROM tutorial.aapl_historical_stock_price;

-- COUNT(*) vs COUNT(column) side by side reveals missing data
SELECT COUNT(*)     AS total_rows,
       COUNT(high)  AS high_non_null,
       COUNT(low)   AS low_non_null,
       COUNT(close) AS close_non_null
  FROM tutorial.aapl_historical_stock_price;
```

> **Profiling tip:** Comparing `COUNT(*)` against `COUNT(column)` for every column is the fastest way to profile NULLs in a new table. `COUNT(*) - COUNT(column)` = number of NULLs in that column.



### SUM Only Works on Numeric Columns

`SUM` ignores NULLs. If **every** value in the group is NULL, `SUM` returns `NULL` (not `0`).

### MIN and MAX Work on Text and Dates


| Data type | `MIN` returns                   | `MAX` returns    |
| --------- | ------------------------------- | ---------------- |
| Numeric   | Smallest number                 | Largest number   |
| Text      | Closest to `'A'` (alphabetical) | Closest to `'Z'` |
| Date      | Earliest date                   | Latest date      |


```sql
-- Apple's lowest price and largest single-day increase
SELECT MIN(low)          AS lowest_price,
       MAX(close - open) AS biggest_daily_gain
  FROM tutorial.aapl_historical_stock_price;
```



### AVG Ignores NULLs Completely

`AVG(column)` = `SUM(column) / COUNT(column)` — NULL rows are excluded from **both** the numerator and the denominator. They are **not** treated as zero.


| Values         | `AVG` result  | If NULL were treated as 0 |
| -------------- | ------------- | ------------------------- |
| `10, 20, NULL` | `15` (30 / 2) | `10` (30 / 3)             |


> **Decision point:** If a NULL really means "zero" in your business logic (e.g., no distributions processed that day), convert it first with `CASE WHEN col IS NULL THEN 0 ELSE col END` (or `COALESCE(col, 0)`, covered in Advanced). If it means "unknown," leave it alone. This is a business decision, not a syntax decision — document it.



### Integer Division in PostgreSQL

PostgreSQL **truncates** integer ÷ integer: `5 / 2` returns `2`. `COUNT` returns an integer (`bigint`), so `SUM(int_col) / COUNT(int_col)` silently truncates. Cast one side first:

```sql
SELECT 5 / 2           AS truncated,   -- 2 in PostgreSQL (2.5 in DuckDB)
       5 * 1.0 / 2     AS decimal_1,   -- 2.5
       5::numeric / 2  AS decimal_2;   -- 2.5 (PostgreSQL cast syntax)
```


| Dialect                        | `5 / 2` | Integer division operator    |
| ------------------------------ | ------- | ---------------------------- |
| PostgreSQL, SQL Server, SQLite | `2`     | `/` on two integers          |
| DuckDB (v0.8+), MySQL          | `2.5`   | `//` (DuckDB), `DIV` (MySQL) |


> **Portability rule:** Never rely on either behavior. Cast explicitly (`* 1.0` or `::numeric`) when you want decimals, so the same query gives the same answer in Mode's PostgreSQL and in your local DuckDB.

> **ROUND tip:** In PostgreSQL, `ROUND(value, n)` with a decimal-places argument only accepts `numeric`. If the column is `double precision`, cast it: `ROUND(AVG(volume)::numeric, 2)`.

---



## 3. HAVING

`WHERE` filters **rows** before grouping. It cannot filter on aggregate results, because the aggregates don't exist yet when `WHERE` runs. `HAVING` filters **groups** after aggregation.

```sql
-- Months where Apple's stock price exceeded $400
SELECT year,
       month,
       MAX(high) AS month_high
  FROM tutorial.aapl_historical_stock_price
 GROUP BY year, month
HAVING MAX(high) > 400
 ORDER BY year, month;
```



### WHERE vs HAVING


|                     | `WHERE`              | `HAVING`                  |
| ------------------- | -------------------- | ------------------------- |
| Filters             | Individual rows      | Groups (after `GROUP BY`) |
| Runs                | Before aggregation   | After aggregation         |
| Can use aggregates? | ❌ No                 | ✅ Yes                     |
| Typical use         | `WHERE year >= 2010` | `HAVING COUNT(*) > 1`     |




### Using Both Together

```sql
-- Only 2012+ data, and only months that had at least one $600+ high
SELECT year,
       month,
       MAX(high) AS month_high
  FROM tutorial.aapl_historical_stock_price
 WHERE year >= 2012
 GROUP BY year, month
HAVING MAX(high) >= 600
 ORDER BY year, month;
```

> **Performance rule:** Put every filter that does **not** need an aggregate in `WHERE`, not `HAVING`. Filtering rows early means fewer rows get grouped.

> **PostgreSQL alias rule:** You **cannot** reference a `SELECT` alias inside `HAVING` (`HAVING month_high > 400` fails). Repeat the aggregate expression instead.

---



## 4. Logical Execution Order

SQL is **written** in one order but **evaluated** in another. Knowing the evaluation order explains most "why doesn't my alias work here?" errors.


| Written order  | Logical execution order | What happens                         |
| -------------- | ----------------------- | ------------------------------------ |
| 1. `SELECT`    | 1. `FROM` + `JOIN`      | Build the working set of rows        |
| 2. `FROM`      | 2. `WHERE`              | Filter individual rows               |
| 3. `JOIN … ON` | 3. `GROUP BY`           | Split rows into groups               |
| 4. `WHERE`     | 4. `HAVING`             | Filter groups                        |
| 5. `GROUP BY`  | 5. `SELECT`             | Compute columns, aggregates, aliases |
| 6. `HAVING`    | 6. `DISTINCT`           | Remove duplicate result rows         |
| 7. `ORDER BY`  | 7. `ORDER BY`           | Sort the result                      |
| 8. `LIMIT`     | 8. `LIMIT`              | Cap the rows returned                |




### Where Can I Use a Column Alias? (PostgreSQL)


| Clause     | Alias allowed? | Why                                          |
| ---------- | -------------- | -------------------------------------------- |
| `WHERE`    | ❌              | Runs before `SELECT` creates the alias       |
| `GROUP BY` | ✅              | PostgreSQL extension — resolves output names |
| `HAVING`   | ❌              | Repeat the expression                        |
| `ORDER BY` | ✅              | Runs after `SELECT`                          |


> **Mental model:** The database is a pipeline. Each step only sees what the previous step produced. Aliases are created at step 5, so steps 2 and 4 can't see them.

---



## 5. CASE — Conditional Logic

`CASE` is SQL's **if / then / else**. It evaluates conditions in order and returns the value for the **first** condition that is TRUE.

### Syntax

```sql
CASE WHEN condition_1 THEN result_1
     WHEN condition_2 THEN result_2
     ELSE default_result          -- optional
END AS column_alias
```


| Rule           | Detail                                                                                    |
| -------------- | ----------------------------------------------------------------------------------------- |
| Required parts | At least one `WHEN … THEN`, and `END`                                                     |
| `ELSE`         | Optional — if omitted, unmatched rows return `NULL`                                       |
| Location       | Usually in `SELECT`; also valid in `WHERE`, `GROUP BY`, `ORDER BY`, and inside aggregates |
| Evaluation     | Top to bottom; **stops at the first match**                                               |
| Conditions     | Any condition valid in `WHERE`: `=`, `>`, `IN`, `LIKE`, `AND`, `OR`, `IS NULL` …          |
| Result types   | All `THEN`/`ELSE` values must be the same data type                                       |




### Simple Flag Column

```sql
SELECT player_name,
       year,
       CASE WHEN year = 'SR' THEN 'yes'
            ELSE 'no' END AS is_a_senior
  FROM benn.college_football_players;
```



### Multiple Conditions — Ordered Buckets

```sql
SELECT player_name,
       weight,
       CASE WHEN weight > 250 THEN 'over 250'
            WHEN weight > 200 THEN '201-250'
            WHEN weight > 175 THEN '176-200'
            ELSE '175 or under' END AS weight_group
  FROM benn.college_football_players;
```

A 260-lb player matches **both** `> 250` and `> 200`, but only gets `'over 250'` because evaluation stops at the first TRUE condition.

> **Best practice — non-overlapping ranges:** Relying on evaluation order works, but explicit ranges are easier to review and safer to reorder:
>
> ```sql
> CASE WHEN weight > 250                  THEN 'over 250'
>      WHEN weight > 200 AND weight <= 250 THEN '201-250'
>      WHEN weight > 175 AND weight <= 200 THEN '176-200'
>      ELSE '175 or under' END
> ```



### Combining Conditions with AND / OR

```sql
SELECT player_name,
       CASE WHEN year = 'FR' AND position = 'WR' THEN 'frosh_wr'
            ELSE NULL END AS sample_case_statement
  FROM benn.college_football_players;
```



### CASE in ORDER BY — Custom Sort Orders

Text sorts alphabetically (FR, JR, SO, SR), which is wrong for class years. `CASE` defines a business order:

```sql
SELECT player_name, year
  FROM benn.college_football_players
 ORDER BY CASE year WHEN 'FR' THEN 1
                    WHEN 'SO' THEN 2
                    WHEN 'JR' THEN 3
                    WHEN 'SR' THEN 4
                    ELSE 5 END;
```

> The form `CASE column WHEN value THEN …` is the **simple CASE** — shorthand for equality checks on one column. The `CASE WHEN condition THEN …` form is the **searched CASE** and handles any condition.

> **NULL trap:** `CASE WHEN year = NULL THEN …` never matches. Use `CASE WHEN year IS NULL THEN …`. Same golden rule as `01_sql_basics.md` Section 8.

---



## 6. CASE with Aggregates (Conditional Aggregation and Pivoting)

This is where `CASE` becomes genuinely powerful — and it's one of the most common patterns in analytics engineering.

### Grouping by a CASE Expression

```sql
SELECT CASE WHEN year = 'FR' THEN 'FR'
            WHEN year = 'SO' THEN 'SO'
            WHEN year = 'JR' THEN 'JR'
            WHEN year = 'SR' THEN 'SR'
            ELSE 'No Year Data' END AS year_group,
       COUNT(1) AS count
  FROM benn.college_football_players
 GROUP BY 1;
```

Three equivalent ways to group by a `CASE` result in PostgreSQL:


| Style           | Example                    | Notes                                                                                                              |
| --------------- | -------------------------- | ------------------------------------------------------------------------------------------------------------------ |
| Position        | `GROUP BY 1`               | Short; the **dbt Labs style guide's preferred form**; breaks if `SELECT` columns are reordered without updating it |
| Alias           | `GROUP BY year_group`      | Readable; PostgreSQL/DuckDB/Snowflake/BigQuery (not SQL Server)                                                    |
| Full expression | `GROUP BY CASE WHEN … END` | Portable to every dialect; verbose                                                                                 |


> `COUNT(1)` **vs** `COUNT(*)`**:** Identical results and performance in PostgreSQL. Both count every row. Pick one and use it consistently.



### Conditional Counting — Pivoting Rows into Columns

`COUNT` ignores NULLs. So if `CASE` returns `1` for matches and `NULL` otherwise, `COUNT` counts only the matches. Repeat for each category to turn **rows into columns**:

```sql
-- One row, four columns — a horizontal pivot
SELECT COUNT(CASE WHEN year = 'FR' THEN 1 ELSE NULL END) AS fr_count,
       COUNT(CASE WHEN year = 'SO' THEN 1 ELSE NULL END) AS so_count,
       COUNT(CASE WHEN year = 'JR' THEN 1 ELSE NULL END) AS jr_count,
       COUNT(CASE WHEN year = 'SR' THEN 1 ELSE NULL END) AS sr_count
  FROM benn.college_football_players;
```


| Layout                                   | Query shape                  | Best for                          |
| ---------------------------------------- | ---------------------------- | --------------------------------- |
| **Vertical** (one row per category)      | `GROUP BY CASE …`            | Further processing, joins, charts |
| **Horizontal** (one column per category) | `COUNT(CASE …)` per category | Reports, side-by-side comparison  |




### Conditional SUM

Same idea with `SUM` — return the value to add, or `0`/`NULL` to skip:

```sql
SELECT SUM(CASE WHEN year IN ('FR', 'SO') THEN weight ELSE 0 END) AS underclass_weight,
       SUM(CASE WHEN year IN ('JR', 'SR') THEN weight ELSE 0 END) AS upperclass_weight
  FROM benn.college_football_players
 WHERE state = 'CA';
```



### How to Build a CASE Aggregation (Mode's Workflow)

1. Write the `CASE` alone with `SELECT CASE … END AS grp, *` and inspect the output
2. Confirm every row lands in the right bucket (check the `ELSE` rows especially)
3. Replace `*` with the aggregate and add `GROUP BY`



### PostgreSQL Shortcut: the FILTER Clause

PostgreSQL (9.4+) and DuckDB support a cleaner syntax for conditional aggregates:

```sql
SELECT COUNT(*) FILTER (WHERE year = 'FR') AS fr_count,
       COUNT(*) FILTER (WHERE year = 'SO') AS so_count
  FROM benn.college_football_players;
```


| Approach                        | Portability                                                | Readability |
| ------------------------------- | ---------------------------------------------------------- | ----------- |
| `COUNT(CASE WHEN … THEN 1 END)` | Works everywhere (MySQL, SQL Server, Snowflake, BigQuery…) | Good        |
| `COUNT(*) FILTER (WHERE …)`     | PostgreSQL, DuckDB, SQLite 3.30+                           | Excellent   |


> **Recommendation:** Learn the `CASE` form first — it's universal and it's what interviewers expect. Use `FILTER` in PostgreSQL/DuckDB code where readability matters.

---



## 7. DISTINCT Inside Aggregates

`DISTINCT` was introduced in `01_sql_basics.md` Section 9 as `SELECT DISTINCT`. Its most common intermediate use is **inside** an aggregate.

```sql
-- How many distinct months appear in the data?
SELECT COUNT(DISTINCT month) AS unique_months
  FROM tutorial.aapl_historical_stock_price;

-- Separate distinct counts in one query
SELECT COUNT(DISTINCT year)  AS years_count,
       COUNT(DISTINCT month) AS months_count
  FROM tutorial.aapl_historical_stock_price;
```



### Placement Rule


| Correct                        | Wrong                          |
| ------------------------------ | ------------------------------ |
| `SELECT COUNT(DISTINCT month)` | `SELECT DISTINCT COUNT(month)` |


`DISTINCT` goes **inside** the parentheses. `SELECT DISTINCT COUNT(month)` counts all non-null months and then de-duplicates a single-row result — not what you want.

### Which Aggregates Benefit from DISTINCT?


| Aggregate                   | With `DISTINCT`               | Practical?                      |
| --------------------------- | ----------------------------- | ------------------------------- |
| `COUNT(DISTINCT col)`       | Number of unique values       | ✅ Extremely common              |
| `SUM(DISTINCT col)`         | Sum of unique values only     | ⚠️ Rarely what you mean         |
| `AVG(DISTINCT col)`         | Average of unique values only | ⚠️ Rarely what you mean         |
| `MIN` / `MAX(DISTINCT col)` | Same result as without        | ❌ Pure overhead — never do this |


> **Performance note:** `COUNT(DISTINCT …)` must sort or hash every value, so it gets expensive on large tables. On warehouse-scale data, engines offer approximate versions (`APPROX_COUNT_DISTINCT` in Snowflake/BigQuery, `approx_count_distinct` in DuckDB) when an exact count isn't required.

> **Code smell (from the basics):** If you find yourself adding `SELECT DISTINCT` to "fix" duplicate rows after a join, stop and check the join's grain instead. `DISTINCT` hides fan-out bugs instead of fixing them — see [Section 17](#17-production-patterns-anti-joins-fan-out-and-duplicate-checks).

---



## 8. Joins — Core Concepts



### Why Joins Exist

Relational databases **split data across tables** to avoid repeating information. Player rows don't repeat each school's conference; that lives once in the teams table. A **join** re-combines them at query time.

### Anatomy of a Join

```sql
SELECT teams.conference     AS conference,
       AVG(players.weight)  AS average_weight
  FROM benn.college_football_players players      -- left table + alias
  JOIN benn.college_football_teams   teams        -- right table + alias
    ON teams.school_name = players.school_name    -- join condition
 GROUP BY teams.conference
 ORDER BY AVG(players.weight) DESC;
```


| Part                                 | Purpose                                                                                   |
| ------------------------------------ | ----------------------------------------------------------------------------------------- |
| **Table alias** (`players`, `teams`) | Short name for a table; written after the table name (`AS` optional)                      |
| `JOIN`                               | Names the second table                                                                    |
| `ON`                                 | The condition that matches rows between the tables                                        |
| **Join key**                         | The column(s) that link the tables (`school_name` here)                                   |
| `alias.column`                       | Tells SQL which table a column comes from — required when both tables share a column name |




### Selecting Columns After a Join


| Syntax                                         | Returns                           |
| ---------------------------------------------- | --------------------------------- |
| `SELECT *`                                     | All columns from **both** tables  |
| `SELECT players.*`                             | All columns from `players` only   |
| `SELECT players.player_name, teams.conference` | Exactly those columns (preferred) |


> **Convention used in this repo** (aligned with the [dbt Labs SQL style guide](https://docs.getdbt.com/best-practices/how-we-style/2-how-we-style-our-sql)): alias tables with a descriptive word (`players`, `teams`, `companies`) — never initialisms like `c` or `a`/`b`. Prefix every column with its table alias once a query touches more than one table. Mode's tutorial omits `AS` before table aliases (`FROM … companies`); dbt prefers writing it (`FROM … AS companies`). Both are valid SQL — pick one per project and stay consistent.



### The Join Types at a Glance


| Join                     | Returns                                                   | Unmatched rows                   |
| ------------------------ | --------------------------------------------------------- | -------------------------------- |
| `INNER JOIN` (or `JOIN`) | Only rows that match in **both** tables                   | Dropped from both sides          |
| `LEFT JOIN`              | **All** rows from the left table + matches from the right | Right-side columns become `NULL` |
| `RIGHT JOIN`             | **All** rows from the right table + matches from the left | Left-side columns become `NULL`  |
| `FULL OUTER JOIN`        | **All** rows from **both** tables                         | Missing side becomes `NULL`      |


> **"Left" and "right"** simply mean: the table in `FROM` is left; the table after `JOIN` is right.

---



## 9. INNER JOIN

Returns only rows where the join condition is TRUE in **both** tables. Think of it as the **intersection**.

```sql
SELECT players.player_name,
       players.school_name,
       teams.conference
  FROM benn.college_football_players players
  JOIN benn.college_football_teams teams
    ON teams.school_name = players.school_name
 WHERE teams.division = 'FBS (Division I-A Teams)';
```

`JOIN` and `INNER JOIN` are **identical**. Writing `INNER JOIN` explicitly is clearer in production code.

### Duplicate Column Names

When both tables have a column with the same name, alias each one so they don't collide in the output:

```sql
SELECT players.school_name AS players_school_name,
       teams.school_name   AS teams_school_name
  FROM benn.college_football_players players
  JOIN benn.college_football_teams teams
    ON teams.school_name = players.school_name;
```



### One-to-Many Matches Multiply Rows

If a key appears **once** in the left table and **three times** in the right table, the result has **three** rows for that key. This is correct behavior — not a bug — but it changes the grain of the result.

> **NULL keys never match.** `NULL = NULL` evaluates to `NULL`, not TRUE, so rows with a NULL join key are always dropped by an inner join (and get no match in outer joins). If you genuinely need NULLs to match, PostgreSQL offers `ON a.key IS NOT DISTINCT FROM b.key`.

---



## 10. Outer Joins — LEFT and RIGHT

Outer joins keep **unmatched** rows. They answer questions like "which companies were **never** acquired?"

### LEFT JOIN

Keeps **every** row from the left (`FROM`) table. Where no match exists, the right table's columns are `NULL`.

```sql
SELECT companies.permalink           AS companies_permalink,
       companies.name                AS companies_name,
       acquisitions.company_permalink AS acquisitions_permalink,
       acquisitions.acquired_at      AS acquired_date
  FROM tutorial.crunchbase_companies companies
  LEFT JOIN tutorial.crunchbase_acquisitions acquisitions
    ON companies.permalink = acquisitions.company_permalink;
```



### Comparing INNER vs LEFT with Counts

`COUNT(column)` ignores NULLs, which makes it a precise tool for measuring match rates:

```sql
SELECT COUNT(companies.permalink)            AS companies_rowcount,
       COUNT(acquisitions.company_permalink) AS acquisitions_rowcount
  FROM tutorial.crunchbase_companies companies
  LEFT JOIN tutorial.crunchbase_acquisitions acquisitions
    ON companies.permalink = acquisitions.company_permalink;
```

With `LEFT JOIN`, `companies_rowcount` stays high (every company kept) while `acquisitions_rowcount` counts only matched rows. Run the same query with `INNER JOIN` and both counts are equal.

### RIGHT JOIN

The mirror image: keeps every row from the right table. Any `RIGHT JOIN` can be rewritten as a `LEFT JOIN` by swapping the table order:

```sql
-- These two queries return the same rows
SELECT …
  FROM tutorial.crunchbase_acquisitions acquisitions
 RIGHT JOIN tutorial.crunchbase_companies companies
    ON companies.permalink = acquisitions.company_permalink;

SELECT …
  FROM tutorial.crunchbase_companies companies
  LEFT JOIN tutorial.crunchbase_acquisitions acquisitions
    ON companies.permalink = acquisitions.company_permalink;
```

> **Convention:** Use `LEFT JOIN` almost exclusively. Reading "start from this table, then attach optional data" top-to-bottom is far easier to review. `RIGHT JOIN` is rare in production codebases; the dbt Labs style guide says to always move left to right and rewrite right joins as left joins. The same guide asks for explicit `INNER JOIN` rather than bare `JOIN`.

> `LEFT OUTER JOIN` **=** `LEFT JOIN`**.** The word `OUTER` is optional everywhere.

---



## 11. Filtering in ON vs WHERE

This is the most important subtle concept in joins. For **inner** joins, putting a filter in `ON` or `WHERE` gives the same result. For **outer** joins, it does **not**.


| Filter location          | When it applies              | Effect on a LEFT JOIN                                                                      |
| ------------------------ | ---------------------------- | ------------------------------------------------------------------------------------------ |
| `ON … AND right.col = x` | **Before / during** the join | Right-side rows that fail the filter don't match — but the **left row is kept** with NULLs |
| `WHERE right.col = x`    | **After** the join           | Rows that fail the filter are removed **entirely**, including the left row                 |




### Filter in ON — Left Rows Survive

```sql
SELECT companies.permalink            AS companies_permalink,
       companies.name                 AS companies_name,
       acquisitions.company_permalink AS acquisitions_permalink,
       acquisitions.acquired_at       AS acquired_date
  FROM tutorial.crunchbase_companies companies
  LEFT JOIN tutorial.crunchbase_acquisitions acquisitions
    ON companies.permalink = acquisitions.company_permalink
   AND acquisitions.company_permalink != '/company/1000memories'
 ORDER BY 1;
```

1000memories still appears — with NULL acquisition columns.

### Filter in WHERE — Left Rows Can Disappear

```sql
SELECT companies.permalink            AS companies_permalink,
       companies.name                 AS companies_name,
       acquisitions.company_permalink AS acquisitions_permalink,
       acquisitions.acquired_at       AS acquired_date
  FROM tutorial.crunchbase_companies companies
  LEFT JOIN tutorial.crunchbase_acquisitions acquisitions
    ON companies.permalink = acquisitions.company_permalink
 WHERE acquisitions.company_permalink != '/company/1000memories'
    OR acquisitions.company_permalink IS NULL
 ORDER BY 1;
```

1000memories is gone. The `OR … IS NULL` is needed to keep never-acquired companies — without it, `NULL != '/company/1000memories'` evaluates to `NULL`, which silently turns the `LEFT JOIN` into an `INNER JOIN`.

> **The silent-INNER-JOIN bug:** A `WHERE` condition on a **right-table** column in a `LEFT JOIN` removes all the NULL rows the LEFT JOIN was supposed to keep. If you meant to keep them, move the condition into `ON`.

> **Rule of thumb:**
>
> - Filters on the **left** (preserved) table → `WHERE`
> - Filters on the **right** (optional) table → `ON`, unless you deliberately want to drop unmatched rows

---



## 12. FULL OUTER JOIN

Keeps unmatched rows from **both** tables. Most commonly used with aggregation to **measure overlap** between two datasets.

```sql
SELECT COUNT(CASE WHEN companies.permalink IS NOT NULL
                   AND acquisitions.company_permalink IS NULL
                  THEN companies.permalink ELSE NULL END) AS companies_only,
       COUNT(CASE WHEN companies.permalink IS NOT NULL
                   AND acquisitions.company_permalink IS NOT NULL
                  THEN companies.permalink ELSE NULL END) AS both_tables,
       COUNT(CASE WHEN companies.permalink IS NULL
                   AND acquisitions.company_permalink IS NOT NULL
                  THEN acquisitions.company_permalink ELSE NULL END) AS acquisitions_only
  FROM tutorial.crunchbase_companies companies
  FULL JOIN tutorial.crunchbase_acquisitions acquisitions
    ON companies.permalink = acquisitions.company_permalink;
```


| Bucket              | Condition                        | Meaning                                     |
| ------------------- | -------------------------------- | ------------------------------------------- |
| `companies_only`    | left key present, right key NULL | In companies, never acquired                |
| `both_tables`       | both keys present                | Matched                                     |
| `acquisitions_only` | left key NULL, right key present | Acquisition with no matching company record |


> **Count the right column:** For the `acquisitions_only` bucket, count `acquisitions.company_permalink` — counting `companies.permalink` returns 0 because it is always NULL in those rows.

> **Why this matters:** This exact three-bucket shape is a **reconciliation report** — "only in source A / in both / only in source B." It's the core query behind any two-system reconciliation (e.g., ledger vs. tax-form data). See [Section 17](#17-production-patterns-anti-joins-fan-out-and-duplicate-checks).

> **Dialect note:** MySQL does **not** support `FULL OUTER JOIN` (emulate it with `LEFT JOIN … UNION … RIGHT JOIN`). PostgreSQL, DuckDB, SQL Server, Snowflake, BigQuery, and SQLite 3.39+ do.

---



## 13. UNION and UNION ALL

Joins combine tables **side by side** (adding columns). `UNION` stacks query results **on top of each other** (adding rows).

```sql
SELECT *
  FROM tutorial.crunchbase_investments_part1

 UNION ALL

SELECT *
  FROM tutorial.crunchbase_investments_part2;
```



### UNION vs UNION ALL


| Operator    | Duplicates                         | Speed                            | When to use                         |
| ----------- | ---------------------------------- | -------------------------------- | ----------------------------------- |
| `UNION`     | **Removed** (exact duplicate rows) | Slower — must sort/hash all rows | You explicitly need de-duplication  |
| `UNION ALL` | **Kept**                           | Faster                           | Default choice — appending datasets |


> **Default to** `UNION ALL`**.** Plain `UNION` silently deletes legitimate rows that happen to be identical (e.g., two equal distributions on the same day for the same participant). If you need de-duplication, do it deliberately and document why.



### Rules for Stacking

1. Both queries must return the **same number of columns**
2. Columns must be in the **same order** with **compatible data types**
3. Output column names come from the **first** query
4. Each `SELECT` can have its own `WHERE`, `GROUP BY`, `HAVING`
5. A single `ORDER BY` at the very end sorts the **combined** result



### Filtering Each Part Separately

```sql
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
```



### Labeling the Source

Add a literal column so you can tell which query each row came from — essential when combining data from multiple systems:

```sql
SELECT 'part_1' AS source_dataset, company_name, investor_name
  FROM tutorial.crunchbase_investments_part1
 UNION ALL
SELECT 'part_2' AS source_dataset, company_name, investor_name
  FROM tutorial.crunchbase_investments_part2;
```

---



## 14. Joins with Comparison Operators

`ON` accepts **any** condition — not just `=`. Adding a comparison operator restricts which rows count as a match.

```sql
-- Investors per company, counting only investments made
-- more than 5 years after the company was founded
SELECT companies.permalink,
       companies.name,
       companies.status,
       COUNT(investments.investor_permalink) AS investors
  FROM tutorial.crunchbase_companies companies
  LEFT JOIN tutorial.crunchbase_investments_part1 investments
    ON companies.permalink = investments.company_permalink
   AND investments.funded_year > companies.founded_year + 5
 GROUP BY 1, 2, 3;
```

Because the extra condition is in `ON` (not `WHERE`), companies with no qualifying investments are still returned with a count of `0`.

### Common Non-Equi Join Uses


| Pattern      | Example condition                                  | Real-world use                                |
| ------------ | -------------------------------------------------- | --------------------------------------------- |
| Time window  | `b.event_date BETWEEN a.start_date AND a.end_date` | Which rate/plan/price was in effect on a date |
| Range lookup | `a.amount >= b.min_amt AND a.amount < b.max_amt`   | Assigning tiers or tax brackets               |
| Sequencing   | `b.funded_at > a.funded_at`                        | "Happened after" comparisons (see self joins) |


> **Performance note:** Equality joins can use fast hash joins. Pure inequality joins (`>`/`<` only) can explode into many-to-many comparisons. Always include at least one equality condition when possible.

---



## 15. Joins on Multiple Keys

Sometimes one column isn't enough to identify a match. List every key column in `ON`, combined with `AND`:

```sql
SELECT companies.permalink,
       companies.name,
       investments.company_name,
       investments.company_permalink
  FROM tutorial.crunchbase_companies companies
  LEFT JOIN tutorial.crunchbase_investments_part1 investments
    ON companies.permalink = investments.company_permalink
   AND companies.name = investments.company_name;
```



### Two Reasons to Join on Multiple Keys


| Reason          | Explanation                                                                                                                                                                     |
| --------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Accuracy**    | When the true key is **composite** — e.g., `(plan_id, participant_id)` or `(year, month)` — joining on only part of it creates false matches                                    |
| **Performance** | If the database has an **index** on the column combination, the extra condition can speed up the join even when it doesn't change the results (little effect on small datasets) |


> **Composite keys in practice:** In operational data, the natural key is frequently composite. A participant ID alone may repeat across plans; `participant_id` + `plan_id` (+ sometimes `tax_year`) is what's actually unique. Joining on the partial key is one of the most common sources of inflated totals.

---



## 16. Self Joins

A **self join** joins a table to itself, using **two different aliases** so SQL can treat it as two separate tables. It's used to compare rows **within** the same table.

```sql
-- Companies that received a British investment
-- AFTER receiving a Japanese investment
SELECT DISTINCT japan_investments.company_name,
       japan_investments.company_permalink
  FROM tutorial.crunchbase_investments_part1 japan_investments
  JOIN tutorial.crunchbase_investments_part1 gb_investments
    ON japan_investments.company_name = gb_investments.company_name
   AND gb_investments.investor_country_code = 'GBR'
   AND gb_investments.funded_at > japan_investments.funded_at
 WHERE japan_investments.investor_country_code = 'JPN'
 ORDER BY 1;
```



### How to Read It

1. `japan_investments` = every row where the investor is Japanese (from `WHERE`)
2. `gb_investments` = rows for the **same company** (`ON` equality) with a British investor (`ON` filter) that happened **later** (`ON` comparison)
3. `DISTINCT` collapses multiple qualifying investment pairs into one row per company



### Typical Self-Join Use Cases


| Use case                       | Join condition                                         |
| ------------------------------ | ------------------------------------------------------ |
| Employee → manager (hierarchy) | `emp.manager_id = mgr.employee_id`                     |
| Event A followed by event B    | same entity + `b.ts > a.ts`                            |
| Pairs within a group           | same group + `a.id < b.id` (avoid mirrored duplicates) |


> **Coming in Advanced:** Many "compare to the previous row" self joins are written more efficiently with **window functions** (`LAG`, `LEAD`, `ROW_NUMBER`). Self joins remain the right tool for hierarchies and arbitrary pairings.

---



## 17. Production Patterns: Anti-Joins, Fan-Out and Duplicate Checks

> This section goes **beyond** the Mode tutorial. It collects the join patterns that show up daily in analytics engineering and data-pipeline work, built only from concepts covered in this file.



### Anti-Join — "Rows in A with No Match in B"

A `LEFT JOIN` followed by `WHERE right.key IS NULL` returns only the **unmatched** left rows:

```sql
-- Companies that were never acquired
SELECT companies.permalink,
       companies.name
  FROM tutorial.crunchbase_companies companies
  LEFT JOIN tutorial.crunchbase_acquisitions acquisitions
    ON companies.permalink = acquisitions.company_permalink
 WHERE acquisitions.company_permalink IS NULL;
```

Here, filtering a right-table column in `WHERE` is **intentional** — we want only the NULL rows (compare with [Section 11](#11-filtering-in-on-vs-where)).

> Advanced SQL adds the `NOT EXISTS (subquery)` form, which is equivalent and often preferred. Avoid `NOT IN (subquery)` when the subquery column can contain NULLs — it returns zero rows.



### Reconciliation Template (Illustrative)

The FULL JOIN overlap query from [Section 12](#12-full-outer-join), applied to a generic two-system reconciliation. Table names here are **hypothetical** placeholders:

```sql
-- Illustrative only: ledger_records and form_records are placeholder tables
SELECT CASE WHEN ledger.record_id IS NULL THEN 'only_in_forms'
            WHEN forms.record_id  IS NULL THEN 'only_in_ledger'
            WHEN ledger.amount <> forms.amount THEN 'amount_mismatch'
            ELSE 'matched' END     AS recon_status,
       COUNT(*)                    AS records
  FROM ledger_records ledger
  FULL JOIN form_records forms
    ON ledger.record_id = forms.record_id
   AND ledger.tax_year  = forms.tax_year
 GROUP BY 1
 ORDER BY 1;
```

This single query combines **FULL JOIN + multiple keys + CASE + GROUP BY** — almost every concept in this file.

### Fan-Out Check — Did My Join Multiply Rows?

When joining a "one" table to a "many" table, the result takes the grain of the "many" side. Summing a column from the "one" side then **double-counts**.

```sql
-- Step 1: row count of the driving table
SELECT COUNT(*) AS companies FROM tutorial.crunchbase_companies;

-- Step 2: row count after the join
SELECT COUNT(*) AS joined_rows
  FROM tutorial.crunchbase_companies companies
  LEFT JOIN tutorial.crunchbase_acquisitions acquisitions
    ON companies.permalink = acquisitions.company_permalink;

-- If joined_rows > companies, the join fanned out.
-- Any SUM of a companies-level column (e.g., funding_total_usd) is now inflated.
```



### Duplicate-Key Check with HAVING

Before trusting a column as a join key, prove it is unique:

```sql
-- Any permalink appearing more than once is NOT a safe one-to-one key
SELECT permalink,
       COUNT(*) AS occurrences
  FROM tutorial.crunchbase_companies
 GROUP BY permalink
HAVING COUNT(*) > 1;
```

Zero rows returned = the key is unique. This is exactly what dbt's built-in `unique` test runs under the hood.

### Join Review Checklist


| #   | Check                                             | How                                               |
| --- | ------------------------------------------------- | ------------------------------------------------- |
| 1   | What is the grain of each table?                  | Write it in a comment above the query             |
| 2   | Is the join key unique on the "one" side?         | `GROUP BY key HAVING COUNT(*) > 1` returns 0 rows |
| 3   | Is the key complete (composite)?                  | Every key column appears in `ON`                  |
| 4   | Did the row count change unexpectedly?            | Count before and after the join                   |
| 5   | Are right-table filters in `ON` (for LEFT JOINs)? | No silent INNER JOIN                              |
| 6   | Am I using `DISTINCT` to hide duplicates?         | Fix the grain instead                             |
| 7   | `UNION` or `UNION ALL`?                           | `UNION ALL` unless de-dup is deliberate           |


---



## 18. Full Clause Order Reference (Updated)

The basics clause order, extended with joins and `HAVING`:


| Order | Clause      | Purpose                                               | Required? |
| ----- | ----------- | ----------------------------------------------------- | --------- |
| 1     | `SELECT`    | Columns / calculations / `CASE` expressions to return | Yes       |
| 2     | `FROM`      | Driving (left) table + alias                          | Yes       |
| 3     | `JOIN … ON` | Additional tables and match conditions (repeatable)   | No        |
| 4     | `WHERE`     | Filter rows **before** grouping                       | No        |
| 5     | `GROUP BY`  | Group rows for aggregation                            | No        |
| 6     | `HAVING`    | Filter groups **after** aggregation                   | No        |
| 7     | `ORDER BY`  | Sort the final result set                             | No        |
| 8     | `LIMIT`     | Cap the number of rows returned                       | No        |


`UNION ALL` sits **between** complete `SELECT` statements; the final `ORDER BY` / `LIMIT` apply to the combined result.

```sql
-- Template showing the full intermediate clause order
SELECT   left_tbl.col1,
         right_tbl.col2,
         CASE WHEN left_tbl.col3 > 0 THEN 'positive' ELSE 'non-positive' END AS col3_sign,
         COUNT(right_tbl.id) AS match_count
  FROM   schema.left_table  left_tbl
  LEFT JOIN schema.right_table right_tbl
    ON   right_tbl.left_id = left_tbl.id
   AND   right_tbl.status  = 'active'          -- right-table filter in ON
 WHERE   left_tbl.created_year >= 2020          -- left-table filter in WHERE
 GROUP BY 1, 2, 3
HAVING   COUNT(right_tbl.id) > 0
 ORDER BY match_count DESC
 LIMIT   100;
```

> **Coming in Advanced SQL:** data types and casting, date formatting, string functions for cleaning (`LOWER`, `TRIM`, `SUBSTR`, `COALESCE`), **subqueries** and CTEs (`WITH`), **window functions** (`ROW_NUMBER`, `RANK`, `LAG`, `LEAD`, running totals), performance tuning (`EXPLAIN`), and pivoting.

---

*Next file:* `03_sql_advanced.md` *— data types, dates, string cleaning, subqueries/CTEs, window functions, performance tuning, pivoting*