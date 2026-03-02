-- ============================================================================
-- SQL BASICS — Operators, Functions & Query Patterns
-- ============================================================================
-- Author:       Manuel Reyes | github.com/manuel-reyes-ml
-- Repository:   learning_journey/courses/sql_mode_thoughtspot/queries/
-- Sources:      Mode Analytics SQL Tutorial, SQLZoo (sqlzoo.net)
-- Last Updated: 2026-03-01
-- Stage:        1 of 5 — AI-Powered Data Analyst (Roadmap v6)
--
-- PURPOSE:
--   Quick-reference of every SQL basic operator, clause, and function
--   practiced so far. Each section shows the SIGNATURE, a short note,
--   and hands-on exercises from Mode Analytics and SQLZoo.
--
-- CONVENTIONS:
--   • UPPER CASE  → SQL keywords (SELECT, FROM, WHERE ...)
--   • lower_case  → table and column identifiers
--   • 'single'    → string literals  (SQL standard)
--   • "double"    → column aliases with spaces only
--   • Every query ends with a semicolon
--   • Comments explain the WHY, not just the WHAT
--
-- NOTE: Detailed explanations live in notes/01_sql_basics.md
--       This file is queries + quick notes only.
-- ============================================================================


-- ════════════════════════════════════════════════════════════════════════════
-- TABLE OF CONTENTS
-- ════════════════════════════════════════════════════════════════════════════
--
--   1.  SELECT & FROM — Retrieving Data
--   2.  Column Aliases (AS)
--   3.  WHERE & Comparison Operators (=, <>, !=, <, >, <=, >=)
--   4.  Logical Operators (AND, OR, NOT, XOR)
--   5.  Pattern Matching (LIKE, ILIKE, Wildcards: %, _)
--   6.  Range & Membership Operators (BETWEEN, IN)
--   7.  NULL Handling (IS NULL, IS NOT NULL)
--   8.  DISTINCT — Removing Duplicate Rows
--   9.  ORDER BY — Sorting Results
--  10.  LIMIT — Constraining Output
--  11.  Arithmetic & Calculated Columns (+, -, *, /)
--  12.  Numeric Functions (ROUND)
--  13.  Aggregate Functions (COUNT, SUM, AVG, MIN, MAX)
--  14.  GROUP BY — Grouping & Aggregation
--  15.  String Functions (LENGTH, LEFT, RIGHT, CONCAT, ||)
--
-- ════════════════════════════════════════════════════════════════════════════


-- ============================================================================
-- 1. SELECT & FROM — Retrieving Data
-- ============================================================================
-- Signature:  SELECT column1, column2, ... FROM schema.table_name;
-- SELECT = which columns | FROM = which table
-- Use * for all columns (exploratory only — always name columns in production).
-- Required clause order: SELECT → FROM
-- ============================================================================

-- 1a. Select ALL columns (exploratory / quick look only)
SELECT *
  FROM sample_table;

-- 1b. Select SPECIFIC columns (preferred — explicit is better than implicit)
SELECT year,
       month,
       west
  FROM tutorial.us_housing_units;


-- ============================================================================
-- 2. Column Aliases (AS)
-- ============================================================================
-- Signature:  SELECT column AS alias_name
--             SELECT column AS "Alias With Spaces"
-- Renames columns in results. Does NOT change the actual table.
-- Use double quotes ONLY when the alias contains spaces.
-- ============================================================================

SELECT west  AS "West Region",
       south AS "South Region"
  FROM tutorial.us_housing_units;


-- ============================================================================
-- 3. WHERE & Comparison Operators
-- ============================================================================
-- Signature:  SELECT ... FROM ... WHERE condition;
-- Filters rows BEFORE they reach the result set.
-- Required clause order: SELECT → FROM → WHERE
--
-- COMPARISON OPERATORS:
--   =     Equal to
--   <>    Not equal to (SQL standard)
--   !=    Not equal to (widely supported alternative)
--   >     Greater than
--   <     Less than
--   >=    Greater than or equal to
--   <=    Less than or equal to
--
-- NOTE: Non-numeric comparisons use SINGLE QUOTES and sort alphabetically.
--       SQL considers 'Ja' > 'J' because it has an extra character.
-- ============================================================================

-- 3a. Equal to (=)
SELECT *
  FROM sample_table
 WHERE year = 2025;

-- 3b. Greater than (>)
SELECT year,
       month,
       west
  FROM sample_table
 WHERE west > 500;

-- 3c. Not equal to (<>)
--     Countries where the capital starts with the same letter as the country
--     name, but is NOT the same word (SQLZoo)
SELECT name    AS "Country",
       capital AS "Capital"
  FROM world
 WHERE LEFT(name, 1) = LEFT(capital, 1)
   AND name <> capital;

-- 3d. Comparison on non-numeric columns (alphabetical order)
--     Months that come after 'January' alphabetically
SELECT *
  FROM tutorial.us_housing_units
 WHERE month_name > 'January';


-- ============================================================================
-- 4. Logical Operators (AND, OR, NOT, XOR)
-- ============================================================================
-- Combine multiple conditions in a WHERE clause.
--
-- OPERATOR PRECEDENCE (highest → lowest):  NOT → AND → OR
-- TIP: Always use parentheses to make intent explicit and avoid bugs.
--
-- AND  → Both conditions must be TRUE
-- OR   → At least one condition must be TRUE
-- NOT  → Negates the condition
-- XOR  → Exactly one condition is TRUE (not both)
-- ============================================================================

-- 4a. AND — both conditions required
SELECT *
  FROM tutorial.billboard_top_100_year_end
 WHERE year_rank <= 10
   AND "group_name" ILIKE '%katy perry%';

-- 4b. OR — at least one condition (use parentheses with AND!)
SELECT *
  FROM tutorial.billboard_top_100_year_end
 WHERE year_rank <= 10
   AND ("group_name" ILIKE '%katy perry%'
        OR "group_name" ILIKE '%bon jovi%')
 ORDER BY year_rank;

-- 4c. NOT — negate a condition
--     Songs from 2013 that do NOT contain the letter 'a'
SELECT *
  FROM tutorial.billboard_top_100_year_end
 WHERE year = 2013
   AND song_name NOT ILIKE '%a%';

-- 4d. XOR — exactly one condition true, NOT both
--     Countries big by area OR population, but not both (SQLZoo)
SELECT name       AS "Country",
       population AS "Population",
       area       AS "Size"
  FROM world
 WHERE area > 3000000 XOR population > 250000000;

-- 4e. Combining AND + OR with parentheses to control precedence
--     California songs from either the 70s or 90s
SELECT *
  FROM tutorial.billboard_top_100_year_end
 WHERE song_name ILIKE '%california%'
   AND ((year >= 1970 AND year <= 1979)
        OR (year >= 1990 AND year <= 1999));


-- ============================================================================
-- 5. Pattern Matching (LIKE, ILIKE, Wildcards)
-- ============================================================================
-- Signature:  WHERE column LIKE  'pattern'    (case-sensitive)
--             WHERE column ILIKE 'pattern'    (case-INsensitive, PostgreSQL)
--
-- WILDCARDS:
--   %  → matches zero or more characters   ('A%' → starts with A)
--   _  → matches exactly ONE character      ('_a%' → second letter is a)
--
-- NOTE: ILIKE is PostgreSQL-specific. In MySQL, LIKE is already
--       case-insensitive on non-binary string columns.
-- ============================================================================

-- 5a. ILIKE — case-insensitive match (PostgreSQL)
SELECT *
  FROM tutorial.billboard_top_100_year_end
 WHERE year_rank <= 10
   AND "group_name" ILIKE '%ludacris%';

-- 5b. LIKE with % — find names containing at least 3 letter 'a's
SELECT name
  FROM world
 WHERE name LIKE '%a%a%a%';

-- 5c. _ wildcard — match exactly one character
--     Five-letter European country names (SQLZoo)
SELECT name,
       LENGTH(name) AS name_length
  FROM world
 WHERE name LIKE '_____'
   AND region = 'Europe';


-- ============================================================================
-- 6. Range & Membership (BETWEEN, IN)
-- ============================================================================
-- BETWEEN:
--   Signature:  WHERE column BETWEEN low AND high
--   Inclusive range filter. Cleaner than: column >= low AND column <= high
--
-- IN:
--   Signature:  WHERE column IN ('value1', 'value2', ...)
--   Match against a list of values. Cleaner than chaining multiple OR conditions.
-- ============================================================================

-- 6a. BETWEEN — inclusive range (simplifies >= AND <=)
--     California songs from the 70s or 90s (simplified from section 4e)
SELECT *
  FROM tutorial.billboard_top_100_year_end
 WHERE song_name ILIKE '%california%'
   AND (year BETWEEN 1970 AND 1979
        OR year BETWEEN 1990 AND 1999);

-- 6b. IN — match against a value list
--     Population of France, Germany, Italy (SQLZoo)
SELECT name,
       population
  FROM world
 WHERE name IN ('France', 'Germany', 'Italy');

-- 6c. IN — filter for multiple artists (Mode Analytics)
SELECT *
  FROM tutorial.billboard_top_100_year_end
 WHERE artist IN ('Elvis Presley', 'Hammer', 'M.C. Hammer');


-- ============================================================================
-- 7. NULL Handling (IS NULL, IS NOT NULL)
-- ============================================================================
-- Signature:  WHERE column IS NULL
--             WHERE column IS NOT NULL
--
-- NULL = missing/unknown data. It is NOT the same as zero or empty string.
-- IMPORTANT: You cannot use = or <> to compare with NULL.
--            WHERE column = NULL   ← WRONG (always returns nothing)
--            WHERE column IS NULL  ← CORRECT
-- ============================================================================

-- 7a. IS NULL — find rows with missing data
SELECT *
  FROM tutorial.us_housing_units
 WHERE south IS NULL;

-- 7b. IS NOT NULL — exclude rows with missing data
SELECT year,
       month,
       west
  FROM tutorial.us_housing_units
 WHERE west IS NOT NULL;


-- ============================================================================
-- 8. DISTINCT — Removing Duplicate Rows
-- ============================================================================
-- Signature:  SELECT DISTINCT column1, column2 FROM table_name;
-- Returns unique combinations of the selected columns.
-- Useful for exploring unique values in a column before deeper analysis.
-- ============================================================================

-- 8a. DISTINCT — unique years available in the dataset
SELECT DISTINCT year
  FROM tutorial.us_housing_units
 ORDER BY year;

-- 8b. DISTINCT on multiple columns — unique year + month combinations
SELECT DISTINCT year,
                month
  FROM tutorial.aapl_historical_stock_price
 ORDER BY year, month;


-- ============================================================================
-- 9. ORDER BY — Sorting Results
-- ============================================================================
-- Signature:  SELECT ... FROM ... ORDER BY column1 [ASC|DESC], column2 ...;
--
-- ASC  = ascending  (A→Z, 1→9, oldest→newest) — this is the DEFAULT
-- DESC = descending (Z→A, 9→1, newest→oldest)
--
-- You can sort by: column name, column alias, or column POSITION number.
-- Column position = order in which columns appear in the SELECT list.
-- ============================================================================

-- 9a. ORDER BY ascending (default — lowest to highest)
SELECT *
  FROM tutorial.billboard_top_100_year_end
 WHERE year = 2013
 ORDER BY year_rank;

-- 9b. ORDER BY descending
SELECT *
  FROM tutorial.billboard_top_100_year_end
 WHERE year = 2013
 ORDER BY year_rank DESC;

-- 9c. Multi-column sort — year descending, then rank ascending within each year
SELECT *
  FROM tutorial.billboard_top_100_year_end
 WHERE year_rank <= 3
 ORDER BY year DESC, year_rank;

-- 9d. Sort by column POSITION instead of name
--     Numbers correspond to the SELECT column order (1 = first column, etc.)
SELECT *
  FROM tutorial.billboard_top_100_year_end
 WHERE year_rank <= 3
 ORDER BY 2, 1 DESC;


-- ============================================================================
-- 10. LIMIT — Constraining Output
-- ============================================================================
-- Signature:  SELECT ... FROM ... LIMIT n;
-- Returns only the first n rows. Essential for exploring large tables
-- without waiting for millions of rows to load.
-- ============================================================================

SELECT *
  FROM tutorial.us_housing_units
 LIMIT 15;


-- ============================================================================
-- 11. Arithmetic & Calculated Columns
-- ============================================================================
-- Operators:  +  (add)   -  (subtract)   *  (multiply)   /  (divide)
-- Create new calculated columns on the fly in your SELECT statement.
-- You can also use arithmetic expressions inside WHERE to filter.
-- ============================================================================

-- 11a. Calculated column — sum of all four regions
SELECT year       AS "Year",
       month_name AS "Month Name",
       south + west + midwest + northeast AS "Total 4 Regions"
  FROM tutorial.us_housing_units;

-- 11b. Arithmetic in WHERE — west exceeds midwest + northeast combined
SELECT year       AS "Year",
       month_name AS "Month Name",
       west       AS "West Region",
       midwest + northeast AS "Mid + North"
  FROM tutorial.us_housing_units
 WHERE west > (midwest + northeast);

-- 11c. Division — per capita GDP for countries with GDP > 1 trillion (SQLZoo)
SELECT name AS "Country",
       ROUND(gdp / population, -3) AS "Per Capita GDP"
  FROM world
 WHERE gdp > 1000000000000;

-- 11d. Percentage calculation — regional share of total housing units
SELECT year       AS "Year",
       month_name AS "Month Name",
       ROUND((south     / (south + west + midwest + northeast)) * 100, 2) AS "South %",
       ROUND((west      / (south + west + midwest + northeast)) * 100, 2) AS "West %",
       ROUND((midwest   / (south + west + midwest + northeast)) * 100, 2) AS "Midwest %",
       ROUND((northeast / (south + west + midwest + northeast)) * 100, 2) AS "Northeast %"
  FROM tutorial.us_housing_units
 WHERE year >= 2000;


-- ============================================================================
-- 12. Numeric Functions — ROUND
-- ============================================================================
-- Signature:  ROUND(value, decimal_places)
--
-- decimal_places > 0  → rounds to that many decimal places
-- decimal_places = 0  → rounds to nearest integer
-- decimal_places < 0  → rounds to nearest 10, 100, 1000, etc.
--
-- Examples:
--   ROUND(1234,  -3) → 1000     (nearest thousand)
--   ROUND(1500,  -3) → 2000     (nearest thousand, rounds up at midpoint)
--   ROUND(3.14159, 2) → 3.14    (two decimal places)
-- ============================================================================

-- Quick reference — rounding to nearest 1,000
SELECT ROUND(1234,  -3) AS r1,   -- 1000
       ROUND(1499,  -3) AS r2,   -- 1000
       ROUND(1500,  -3) AS r3,   -- 2000
       ROUND(17890, -3) AS r4;   -- 18000


-- ============================================================================
-- 13. Aggregate Functions (COUNT, SUM, AVG, MIN, MAX)
-- ============================================================================
-- Aggregate functions collapse multiple rows into a single summary value.
--
--   COUNT(*)        → total number of rows
--   COUNT(column)   → number of NON-NULL values in that column
--   SUM(column)     → total of all values
--   AVG(column)     → arithmetic mean
--   MIN(column)     → smallest value
--   MAX(column)     → largest value
--
-- NOTE: Aggregates ignore NULL values (except COUNT(*)).
--       Almost always used with GROUP BY (see section 14).
-- ============================================================================

-- 13a. COUNT — total trading days recorded
SELECT COUNT(*) AS total_records
  FROM tutorial.aapl_historical_stock_price;

-- 13b. SUM — total shares traded per year/month
SELECT year       AS "Year",
       month      AS "Month",
       SUM(volume) AS "Shares Traded"
  FROM tutorial.aapl_historical_stock_price
 GROUP BY year, month
 ORDER BY year;

-- 13c. AVG — average daily price change per year
SELECT year                  AS "Year",
       AVG(open - close)     AS "Avg Daily Price Change"
  FROM tutorial.aapl_historical_stock_price
 GROUP BY year
 ORDER BY year;

-- 13d. MIN & MAX — monthly price range
SELECT year     AS "Year",
       month    AS "Month",
       MIN(low)  AS "Lowest Price",
       MAX(high) AS "Highest Price"
  FROM tutorial.aapl_historical_stock_price
 GROUP BY year, month
 ORDER BY year, month;


-- ============================================================================
-- 14. GROUP BY — Grouping & Aggregation
-- ============================================================================
-- Signature:  SELECT column, AGGREGATE(column) FROM table GROUP BY column;
--
-- Splits rows into groups based on column values, then applies the
-- aggregate function to EACH group independently.
--
-- RULE: Every column in SELECT must EITHER be inside an aggregate function
--       OR listed in the GROUP BY clause. No exceptions.
--
-- FULL CLAUSE ORDER: SELECT → FROM → WHERE → GROUP BY → ORDER BY → LIMIT
-- ============================================================================

-- 14a. GROUP BY single column — trades per year
SELECT year,
       COUNT(*) AS trading_days
  FROM tutorial.aapl_historical_stock_price
 GROUP BY year
 ORDER BY year;

-- 14b. GROUP BY multiple columns — records per year + month
SELECT year,
       month,
       COUNT(*) AS count
  FROM tutorial.aapl_historical_stock_price
 GROUP BY year, month
 ORDER BY year, month;


-- ============================================================================
-- 15. String Functions (LENGTH, LEFT, RIGHT, CONCAT, ||)
-- ============================================================================
--
-- LENGTH(string)       → number of characters
-- LEFT(string, n)      → first n characters from the left
-- RIGHT(string, n)     → last n characters from the right
-- CONCAT(str1, str2)   → joins two strings (MySQL, PostgreSQL)
-- str1 || str2         → concatenation operator (PostgreSQL, SQLite standard)
--
-- ============================================================================

-- 15a. LENGTH — find 5-letter country names in Europe (SQLZoo)
SELECT name,
       LENGTH(name) AS name_length
  FROM world
 WHERE LENGTH(name) = 5
   AND region = 'Europe';

-- 15b. LEFT — compare first letter of country and capital (SQLZoo)
--     (Full query shown in section 3c above — repeated here for reference)
SELECT name    AS "Country",
       capital AS "Capital"
  FROM world
 WHERE LEFT(name, 1) = LEFT(capital, 1)
   AND name <> capital;

-- 15c. CONCAT — find countries whose capital is the country name + ' City'
--     Example: Mexico → Mexico City (SQLZoo)
SELECT name
  FROM world
 WHERE capital = CONCAT(name, ' City');

-- 15d. || operator — same as CONCAT, standard SQL concatenation
--     Works in PostgreSQL, SQLite. Preferred in standard SQL.
SELECT name
  FROM world
 WHERE capital = name || ' City';


-- ============================================================================
-- FULL CLAUSE ORDER REFERENCE (basics)
-- ============================================================================
--
-- SELECT    → which columns / calculations to return
-- FROM      → which table to query
-- WHERE     → filter rows BEFORE grouping
-- GROUP BY  → group rows for aggregation
-- ORDER BY  → sort the final results
-- LIMIT     → cap the number of rows returned
--
-- ============================================================================


-- ============================================================================
-- END OF BASICS
-- ============================================================================
-- NEXT FILE: 02_practice_intermediate.sql
--   Topics: HAVING, CASE, JOINs (INNER, LEFT, RIGHT, FULL OUTER),
--           UNION, subqueries
-- ============================================================================