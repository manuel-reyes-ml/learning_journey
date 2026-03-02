# SQL Basics — Complete Reference Notes

> **Author:** Manuel Reyes | [github.com/manuel-reyes-ml](https://github.com/manuel-reyes-ml)  
> **Sources:** [Mode Analytics SQL Tutorial](https://mode.com/sql-tutorial), [SQLZoo](https://sqlzoo.net)  
> **Companion file:** `queries/01_practice_basics.sql` (hands-on exercises)  
> **Stage:** 1 of 5 — AI-Powered Data Analyst ([Roadmap v6](https://manuel-reyes-ml.github.io/learning_journey/roadmap.html))  
> **Last updated:** 2026-03-01

---

## Table of Contents

1. [What Is SQL?](#1-what-is-sql)
2. [SELECT and FROM](#2-select-and-from)
3. [Column Aliases (AS)](#3-column-aliases-as)
4. [WHERE and Comparison Operators](#4-where-and-comparison-operators)
5. [Logical Operators (AND, OR, NOT, XOR)](#5-logical-operators-and-or-not-xor)
6. [Pattern Matching (LIKE, ILIKE, Wildcards)](#6-pattern-matching-like-ilike-wildcards)
7. [Range and Membership (BETWEEN, IN)](#7-range-and-membership-between-in)
8. [NULL Handling (IS NULL, IS NOT NULL, TRIM)](#8-null-handling-is-null-is-not-null-trim)
9. [DISTINCT](#9-distinct)
10. [ORDER BY](#10-order-by)
11. [LIMIT](#11-limit)
12. [Arithmetic and Derived Columns](#12-arithmetic-and-derived-columns)
13. [Numeric Functions (ROUND)](#13-numeric-functions-round)
14. [Aggregate Functions (COUNT, SUM, AVG, MIN, MAX)](#14-aggregate-functions-count-sum-avg-min-max)
15. [GROUP BY](#15-group-by)
16. [String Functions (LENGTH, LEFT, RIGHT, CONCAT)](#16-string-functions-length-left-right-concat)
17. [Full Clause Order Reference](#17-full-clause-order-reference)

---

## 1. What Is SQL?

**SQL (Structured Query Language)** is a programming language designed for managing data in a **relational database** — a database that stores data in tables made up of rows and columns.

### Databases, Schemas, and Tables

Within databases, tables are organized into **schemas**. Schemas are typically defined by usernames or logical groupings. For example, if your username is `databass3000` and you upload a table called `fish_food_sales`, it would be referenced as:

```sql
SELECT * FROM databass3000.fish_food_sales;
```

Think of it like a file system: the **database** is the hard drive, the **schema** is the folder, and the **table** is the file inside that folder.

---

## 2. SELECT and FROM

The two **required** ingredients in any SQL query. They must appear in this order:

- **`SELECT`** — which columns you want to see
- **`FROM`** — which table those columns live in

```sql
-- Select specific columns
SELECT year, month, west
  FROM tutorial.us_housing_units;

-- Select ALL columns (exploratory only — avoid in production)
SELECT *
  FROM tutorial.us_housing_units;
```

> **Best practice:** Always name your columns explicitly instead of using `*`. It makes queries faster, more readable, and protects you if the table structure changes later.

### Formatting Conventions

SQL is **not case-sensitive** for keywords — `SELECT` and `select` work identically. Capitalizing keywords is a convention that makes queries easier to read. SQL also treats one space, multiple spaces, and line breaks the same way:

```sql
-- These are identical to SQL:
SELECT * FROM tutorial.us_housing_units;

SELECT *
  FROM tutorial.us_housing_units;
```

> **Convention used in this repo:** SQL keywords in `UPPER CASE`, table/column names in `lower_case`, and each major clause on its own line indented for readability.

---

## 3. Column Aliases (AS)

Aliases rename columns **in the result set only** — they do not change the actual table. Use `AS` followed by the alias name:

```sql
SELECT west  AS "West Region",
       south AS "South Region"
  FROM tutorial.us_housing_units;
```

### Quoting Rules for Aliases

| Scenario | Syntax | Example |
|---|---|---|
| Single-word alias | No quotes needed | `SELECT west AS region` |
| Alias with spaces | **Double quotes** required | `SELECT west AS "West Region"` |
| String literal value | **Single quotes** always | `WHERE name = 'France'` |

> **Key rule:** Single quotes `' '` = **data values** (strings). Double quotes `" "` = **identifiers** (column/table names or aliases with spaces). Mixing them up is one of the most common SQL bugs.

### Alias Behavior Across Dialects

| Dialect | Alias with spaces |
|---|---|
| PostgreSQL | `"West Region"` (double quotes) |
| MySQL | `` `West Region` `` (backticks) or `"West Region"` |
| SQLite (CS50) | `"West Region"` (double quotes) |
| SQL Server | `[West Region]` (square brackets) |

---

## 4. WHERE and Comparison Operators

`WHERE` filters rows **before** they reach the result set. Only rows where the condition evaluates to `TRUE` are included.

```sql
SELECT *
  FROM sample_table
 WHERE year = 2025;
```

> **Required clause order:** `SELECT` → `FROM` → `WHERE` (always this order).

### Comparison Operators

| Operator | Meaning | Example |
|:---:|---|---|
| `=` | Equal to | `WHERE year = 2025` |
| `<>` | Not equal to (SQL standard) | `WHERE region <> 'West'` |
| `!=` | Not equal to (widely supported) | `WHERE region != 'West'` |
| `>` | Greater than | `WHERE west > 500` |
| `<` | Less than | `WHERE year_rank < 10` |
| `>=` | Greater than or equal to | `WHERE year >= 2000` |
| `<=` | Less than or equal to | `WHERE year_rank <= 3` |

### Comparing Non-Numeric Values

All comparison operators work on text — they filter based on **alphabetical (lexicographic) order**. Non-numeric values must be wrapped in **single quotes**:

```sql
SELECT *
  FROM tutorial.us_housing_units
 WHERE month_name > 'January';
```

**Why does `> 'J'` include January?** SQL considers `'Ja'` to be greater than `'J'` because it has an extra character. Just like a dictionary would list "January" after "J." This means `> 'J'` returns anything starting with `'J'` plus one or more additional characters, as well as any letter after `'J'`.

```sql
-- This returns January, July, June, March, May, November, October, September
SELECT *
  FROM tutorial.us_housing_units
 WHERE month_name > 'J';
```

---

## 5. Logical Operators (AND, OR, NOT, XOR)

Logical operators combine multiple conditions in a single `WHERE` clause.

### Operator Precedence (highest → lowest)

| Priority | Operator | Evaluates |
|:---:|:---:|---|
| 1st | `NOT` | Negates the next condition |
| 2nd | `AND` | Both sides must be TRUE |
| 3rd | `OR` | At least one side must be TRUE |

> **Always use parentheses** to make your intent explicit. Without them, `AND` is evaluated before `OR`, which can produce unexpected results.

### AND — Both Conditions Must Be TRUE

```sql
SELECT *
  FROM tutorial.billboard_top_100_year_end
 WHERE year = 2012
   AND year_rank <= 10;
```

You can chain as many `AND` statements as you need. Every condition must be satisfied for a row to appear in the results.

### OR — At Least One Condition Must Be TRUE

```sql
SELECT *
  FROM tutorial.billboard_top_100_year_end
 WHERE year = 2013
   AND ("group_name" ILIKE '%macklemore%'
        OR "group_name" ILIKE '%timberlake%');
```

> **Parentheses matter!** Without them, this query would be read as: `(year = 2013 AND group_name ILIKE '%macklemore%') OR (group_name ILIKE '%timberlake%')` — which would return ALL Timberlake rows from ANY year, not just 2013. The parentheses force SQL to evaluate the `OR` first.

### NOT — Negates a Condition

`NOT` flips any condition to its opposite. It can be combined with almost any operator:

```sql
-- NOT with ILIKE
SELECT *
  FROM tutorial.billboard_top_100_year_end
 WHERE year = 2013
   AND "group_name" NOT ILIKE '%macklemore%';

-- NOT with BETWEEN
SELECT *
  FROM tutorial.billboard_top_100_year_end
 WHERE year = 2013
   AND year_rank NOT BETWEEN 2 AND 3;

-- NOT with NULL (special syntax: IS NOT NULL)
SELECT *
  FROM tutorial.billboard_top_100_year_end
 WHERE year = 2013
   AND artist IS NOT NULL;
```

### XOR — Exactly One Condition True (Not Both)

`XOR` (Exclusive OR) returns rows where **one** condition is true but **not both**. Useful for "either/or but not both" logic:

```sql
-- Countries big by area OR population, but NOT both (SQLZoo)
SELECT name       AS "Country",
       population AS "Population",
       area       AS "Size"
  FROM world
 WHERE area > 3000000 XOR population > 250000000;
```

> **Dialect note:** `XOR` is supported in MySQL and SQLZoo. In PostgreSQL, you can achieve the same result with: `WHERE (condition_a OR condition_b) AND NOT (condition_a AND condition_b)`.

---

## 6. Pattern Matching (LIKE, ILIKE, Wildcards)

`LIKE` lets you match **patterns** instead of exact values, using wildcard characters.

### Wildcards

| Wildcard | Matches | Example | Would Match |
|:---:|---|---|---|
| `%` | Zero or more characters | `'A%'` | `Apple`, `A`, `Ant` |
| `_` | Exactly **one** character | `'_a%'` | `Santa`, `Bank` (second letter is `a`) |

### Wildcard Patterns Explained

| Pattern | Meaning |
|---|---|
| `'ludacris'` | Exact match only |
| `'ludacris%'` | Starts with "ludacris" |
| `'%ludacris'` | Ends with "ludacris" |
| `'%ludacris%'` | Contains "ludacris" **anywhere** |
| `'% %'` | Contains a space anywhere |
| `'_____'` | Exactly 5 characters (5 underscores) |

### LIKE vs ILIKE

| Operator | Case Behavior | Example |
|---|---|---|
| `LIKE` | Case-**sensitive** | `'Ludacris'` ≠ `'ludacris'` |
| `ILIKE` | Case-**insensitive** (PostgreSQL only) | `'Ludacris'` = `'LUDACRIS'` = `'lUdAcRiS'` |

```sql
-- Case-insensitive search for any group featuring an artist
SELECT *
  FROM tutorial.billboard_top_100_year_end
 WHERE year = 2012
   AND year_rank <= 10
   AND "group_name" ILIKE '%feat%';
```

### Chaining Wildcards for Multiple Matches

Each `%a%` means "any characters, then an `a`." Chaining three of them guarantees **at least three `a` characters** exist anywhere in the string:

```sql
SELECT name
  FROM world
 WHERE name LIKE '%a%a%a%';
-- Matches: 'Banana', 'Amanda', 'Saratoga'
```

### Case Sensitivity Across Dialects

| Dialect | `LIKE` behavior | Case-insensitive option |
|---|---|---|
| **PostgreSQL** | Case-sensitive | Use `ILIKE` |
| **MySQL** | Case-insensitive by default (most collations) | `LIKE` already works |
| **SQLite (CS50)** | Case-insensitive for ASCII | `LIKE` already works |

---

## 7. Range and Membership (BETWEEN, IN)

### BETWEEN — Inclusive Range Filter

`BETWEEN` selects rows within a range, **including both endpoints**. It must be paired with `AND`:

```sql
SELECT *
  FROM tutorial.billboard_top_100_year_end
 WHERE year_rank BETWEEN 5 AND 10;
-- Equivalent to: WHERE year_rank >= 5 AND year_rank <= 10
```

> `BETWEEN` is inclusive on **both** sides. `BETWEEN 5 AND 10` includes rows where the value is 5 or 10.

### IN — Match Against a List

`IN` replaces multiple `OR` conditions with a clean list. Works with both numbers and strings:

```sql
-- Numeric list
SELECT *
  FROM tutorial.billboard_top_100_year_end
 WHERE year_rank IN (1, 2, 3);

-- String list (use single quotes!)
SELECT name, population
  FROM world
 WHERE name IN ('France', 'Germany', 'Italy');
```

> **When to use which:** `BETWEEN` is best for continuous ranges (years, prices, ranks). `IN` is best for discrete, unrelated values (specific names, categories, IDs).

---

## 8. NULL Handling (IS NULL, IS NOT NULL, TRIM)

### What Is NULL?

`NULL` represents **missing or unknown** data. It is **not** the same as zero, empty string, or the word "null" — it means "no value exists here."

### The Golden Rule: You Cannot Use `=` with NULL

```sql
-- WRONG — this ALWAYS returns zero rows, even if NULLs exist
WHERE artist = NULL

-- CORRECT — use IS NULL
WHERE artist IS NULL

-- CORRECT — find rows that DO have data
WHERE artist IS NOT NULL
```

> **Why?** `NULL` isn't a value — it's the **absence** of a value. Any comparison with `NULL` using `=`, `<>`, `>`, etc. evaluates to `NULL` (not TRUE or FALSE), so the row is excluded. Only `IS NULL` and `IS NOT NULL` can detect it.

### NULL vs Empty Strings

In real data, "missing" data can look like either `NULL` or an empty/whitespace-only string. To catch both:

```sql
SELECT *
  FROM tutorial.billboard_top_100_year_end
 WHERE artist IS NULL
    OR TRIM(artist) = '';
```

### TRIM() — Remove Leading and Trailing Spaces

`TRIM()` strips whitespace from both ends of a string:

| Input | Output | Notes |
|---|---|---|
| `TRIM('  Manuel ')` | `'Manuel'` | Spaces removed from both sides |
| `TRIM('   a  ')` | `'a'` | Only leading/trailing spaces removed |
| `TRIM('   ')` | `''` | All spaces → empty string |
| `TRIM('Rock Band')` | `'Rock Band'` | No change — no leading/trailing spaces |

So `TRIM(artist) = ''` means: "Give me rows where the artist field is only whitespace or already empty (but not NULL)."

---

## 9. DISTINCT

`DISTINCT` removes duplicate rows from the result set. It returns only **unique combinations** of the selected columns.

```sql
-- What unique years exist in the dataset?
SELECT DISTINCT year
  FROM tutorial.us_housing_units
 ORDER BY year;

-- Unique year + month combinations
SELECT DISTINCT year, month
  FROM tutorial.aapl_historical_stock_price
 ORDER BY year, month;
```

> **When to use it:** `DISTINCT` is most useful for **exploration** — understanding what values exist in a column before doing deeper analysis. In production queries, if you need `DISTINCT` it sometimes means your JOINs are creating unintended duplicates (something to watch for in intermediate SQL).

---

## 10. ORDER BY

`ORDER BY` sorts the result set based on one or more columns. It is applied **after** all filtering is done.

### Sort Directions

| Keyword | Direction | Default? |
|:---:|---|:---:|
| `ASC` | Ascending (A→Z, 1→9, oldest→newest) | Yes |
| `DESC` | Descending (Z→A, 9→1, newest→oldest) | No |

```sql
-- Ascending (default — you can omit ASC)
SELECT *
  FROM tutorial.billboard_top_100_year_end
 WHERE year = 2013
 ORDER BY year_rank;

-- Descending — must specify DESC explicitly
SELECT *
  FROM tutorial.billboard_top_100_year_end
 WHERE year = 2013
 ORDER BY year_rank DESC;
```

### Multi-Column Sorting

When sorting by multiple columns, SQL sorts by the **first** column, then breaks ties using the **second** column, and so on. Each column can have its own sort direction:

```sql
-- Most recent years first, then top-ranked songs within each year
SELECT *
  FROM tutorial.billboard_top_100_year_end
 WHERE year_rank <= 3
 ORDER BY year DESC, year_rank;
```

> **Important:** `DESC` only applies to the column **immediately before it**. In the example above, `year` sorts descending but `year_rank` sorts ascending (default).

### Sorting by Column Position

You can substitute **column position numbers** for column names. The number refers to the column's order in the `SELECT` clause (1 = first column, 2 = second, etc.):

```sql
SELECT *
  FROM tutorial.billboard_top_100_year_end
 WHERE year_rank <= 3
 ORDER BY 2, 1 DESC;
```

> **When to use this:** Useful when column names are very long or when grouping many columns. Otherwise, prefer column names for readability.

---

## 11. LIMIT

`LIMIT` restricts how many rows the query returns. It's a safety net that prevents accidentally loading millions of rows.

```sql
SELECT *
  FROM tutorial.us_housing_units
 LIMIT 15;
```

> **Practical use:** Always use `LIMIT` when exploring a new table for the first time. Start with `LIMIT 10` or `LIMIT 100` to understand the structure before running full queries. This is especially critical in production databases where tables can have millions of rows.

### Dialect Differences

| Dialect | Syntax |
|---|---|
| PostgreSQL, MySQL, SQLite | `LIMIT 15` |
| SQL Server | `SELECT TOP 15 * FROM table` |
| Oracle | `WHERE ROWNUM <= 15` (or `FETCH FIRST 15 ROWS ONLY` in 12c+) |

---

## 12. Arithmetic and Derived Columns

SQL supports basic arithmetic directly in `SELECT` and `WHERE` using the same operators as Excel:

| Operator | Operation |
|:---:|---|
| `+` | Addition |
| `-` | Subtraction |
| `*` | Multiplication |
| `/` | Division |

### Row-Level Only

Arithmetic in SQL works **across columns within the same row**. You cannot add values from different rows using `+` — that requires aggregate functions (see [Section 14](#14-aggregate-functions-count-sum-avg-min-max)).

```sql
-- Add columns together to create a "derived column"
SELECT year,
       month,
       west,
       south,
       west + south - 4 * year AS nonsense_column
  FROM tutorial.us_housing_units;
```

The new column `nonsense_column` is called a **derived column** — it's generated on the fly from existing data and doesn't exist in the actual table.

### Order of Operations

SQL follows standard math precedence: multiplication and division before addition and subtraction. Use **parentheses** to control the order:

```sql
-- Without parentheses: west + (south / 2)  ← division happens first
-- With parentheses:    (west + south) / 2   ← addition happens first
SELECT year,
       month,
       (west + south) / 2 AS south_west_avg
  FROM tutorial.us_housing_units;
```

### Arithmetic in WHERE

You can also use arithmetic expressions to **filter** rows:

```sql
-- Rows where West region output exceeds Midwest + Northeast combined
SELECT year       AS "Year",
       month_name AS "Month Name",
       west       AS "West Region",
       midwest + northeast AS "Mid + North"
  FROM tutorial.us_housing_units
 WHERE west > (midwest + northeast);
```

---

## 13. Numeric Functions (ROUND)

### ROUND(value, decimal_places)

Rounds a number to the specified precision:

| `decimal_places` | Effect | Example | Result |
|:---:|---|---|:---:|
| `2` | 2 decimal places | `ROUND(3.14159, 2)` | `3.14` |
| `0` | Nearest integer | `ROUND(3.7, 0)` | `4` |
| `-1` | Nearest 10 | `ROUND(1234, -1)` | `1230` |
| `-2` | Nearest 100 | `ROUND(1234, -2)` | `1200` |
| `-3` | Nearest 1,000 | `ROUND(1234, -3)` | `1000` |

**Midpoint rounding:** At the exact midpoint, SQL rounds **up** (e.g., `ROUND(1500, -3)` → `2000`).

### Common Use Case: Percentages

```sql
SELECT year       AS "Year",
       month_name AS "Month Name",
       ROUND((south / (south + west + midwest + northeast)) * 100, 2) AS "South %",
       ROUND((west  / (south + west + midwest + northeast)) * 100, 2) AS "West %"
  FROM tutorial.us_housing_units
 WHERE year >= 2000;
```

> **Watch for integer division!** In some SQL dialects, dividing two integers truncates the decimal: `5 / 2` = `2`, not `2.5`. To fix this, multiply by `1.0` first: `5 * 1.0 / 2` = `2.5`. PostgreSQL handles this correctly, but MySQL and SQLite may truncate.

---

## 14. Aggregate Functions (COUNT, SUM, AVG, MIN, MAX)

Aggregate functions **collapse multiple rows** into a single summary value. They are almost always used with `GROUP BY` (see [Section 15](#15-group-by)).

| Function | Returns | NULL Handling |
|---|---|---|
| `COUNT(*)` | Total number of rows | Counts ALL rows including NULLs |
| `COUNT(column)` | Number of non-NULL values | **Ignores** NULL values |
| `SUM(column)` | Total of all values | Ignores NULLs |
| `AVG(column)` | Arithmetic mean | Ignores NULLs |
| `MIN(column)` | Smallest value | Ignores NULLs |
| `MAX(column)` | Largest value | Ignores NULLs |

> **Critical distinction:** `COUNT(*)` counts **all rows** (including those with NULLs). `COUNT(column)` counts only rows where that specific column is **not NULL**. This distinction matters when your data has gaps.

### Examples from Mode Analytics (AAPL Stock Data)

```sql
-- Total trading days recorded
SELECT COUNT(*) AS total_records
  FROM tutorial.aapl_historical_stock_price;

-- Total shares traded per year/month
SELECT year, month,
       SUM(volume) AS "Shares Traded"
  FROM tutorial.aapl_historical_stock_price
 GROUP BY year, month
 ORDER BY year;

-- Average daily price change per year
SELECT year,
       AVG(open - close) AS "Avg Daily Price Change"
  FROM tutorial.aapl_historical_stock_price
 GROUP BY year
 ORDER BY year;

-- Monthly price range (lowest and highest)
SELECT year, month,
       MIN(low)  AS "Lowest Price",
       MAX(high) AS "Highest Price"
  FROM tutorial.aapl_historical_stock_price
 GROUP BY year, month
 ORDER BY year, month;
```

---

## 15. GROUP BY

`GROUP BY` splits rows into groups based on column values, then applies aggregate functions to **each group independently** instead of across the entire table.

```sql
SELECT year,
       month,
       COUNT(*) AS count
  FROM tutorial.aapl_historical_stock_price
 GROUP BY year, month;
```

### The GROUP BY Rule

**Every column in `SELECT` must either:**

1. Be inside an aggregate function (`COUNT`, `SUM`, `AVG`, `MIN`, `MAX`), **OR**
2. Be listed in the `GROUP BY` clause

No exceptions. If you select `year` and `month` alongside `COUNT(*)`, both `year` and `month` must appear in `GROUP BY`.

### Grouping by Column Position

Just like `ORDER BY`, you can use column position numbers instead of names. This is recommended only when you have many columns or very long column names:

```sql
SELECT year,
       month,
       COUNT(*) AS count
  FROM tutorial.aapl_historical_stock_price
 GROUP BY 1, 2;
-- 1 = year (first column in SELECT), 2 = month (second column)
```

### How GROUP BY Executes

Think of it as a three-step process:

1. **Split** — SQL divides all rows into groups based on the `GROUP BY` columns
2. **Apply** — the aggregate function runs on each group separately
3. **Combine** — results from each group are assembled into the final output

> For example, `GROUP BY year, month` creates one group per unique year-month pair, then `SUM(volume)` adds up the volume **within each** of those groups.

---

## 16. String Functions (LENGTH, LEFT, RIGHT, CONCAT)

### LENGTH(string) — Character Count

Returns the number of characters in a string:

```sql
-- Find 5-letter European country names (SQLZoo)
SELECT name, LENGTH(name) AS name_length
  FROM world
 WHERE LENGTH(name) = 5
   AND region = 'Europe';
```

### LEFT(string, n) and RIGHT(string, n) — Slice Characters

Extract the first `n` or last `n` characters from a string:

| Function | Extracts | Example | Result |
|---|---|---|---|
| `LEFT('Mexico', 3)` | First 3 characters | `LEFT(name, 1)` | `'M'` |
| `RIGHT('Mexico', 3)` | Last 3 characters | `RIGHT(name, 2)` | `'co'` |

```sql
-- Countries where country and capital start with the same letter,
-- but the capital is not the same word (SQLZoo)
SELECT name    AS "Country",
       capital AS "Capital"
  FROM world
 WHERE LEFT(name, 1) = LEFT(capital, 1)
   AND name <> capital;
```

### CONCAT(str1, str2, ...) — Join Strings

Merges two or more strings into one:

```sql
-- Countries whose capital is the country name + ' City' (SQLZoo)
-- Example: Mexico → Mexico City
SELECT name
  FROM world
 WHERE capital = CONCAT(name, ' City');
```

### || Operator — Standard SQL Concatenation

The `||` (double pipe) operator does the same thing as `CONCAT` and is the **SQL standard** syntax. Preferred in PostgreSQL and SQLite:

```sql
SELECT name
  FROM world
 WHERE capital = name || ' City';
```

| Dialect | Concatenation method |
|---|---|
| **PostgreSQL** | `CONCAT()` or `\|\|` (both work) |
| **MySQL** | `CONCAT()` (preferred) or `\|\|` with `PIPES_AS_CONCAT` mode |
| **SQLite (CS50)** | `\|\|` (preferred) |
| **SQL Server** | `+` or `CONCAT()` |

---

## 17. Full Clause Order Reference

SQL clauses **must** appear in this specific order. Not all are required — only `SELECT` and `FROM` are mandatory for basics:

| Order | Clause | Purpose | Required? |
|:---:|---|---|:---:|
| 1 | `SELECT` | Which columns / calculations to return | Yes |
| 2 | `FROM` | Which table to query | Yes |
| 3 | `WHERE` | Filter rows **before** grouping | No |
| 4 | `GROUP BY` | Group rows for aggregation | No |
| 5 | `ORDER BY` | Sort the final result set | No |
| 6 | `LIMIT` | Cap the number of rows returned | No |

```sql
-- Template showing the full clause order
SELECT   column1, column2, AGGREGATE(column3)
  FROM   schema.table_name
 WHERE   condition
 GROUP BY column1, column2
 ORDER BY column1 DESC
 LIMIT  100;
```

> **Coming in Intermediate SQL:** `HAVING` (filters groups **after** `GROUP BY`) slots in between `GROUP BY` and `ORDER BY`. Also: `CASE` statements, JOINs, UNION, and subqueries.

---

*Next file: `02_sql_intermediate.md` — HAVING, CASE, JOINs (INNER, LEFT, RIGHT, FULL OUTER), UNION, subqueries*