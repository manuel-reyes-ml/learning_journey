-- ======================
-- 1. Select all columns from a sample table
-- ======================

SELECT * FROM sample_table;

--1.1 SELECT specific columns from TABLE_NAME
SELECT year,
       month,
       west
  FROM tutorial.us_housing_units

--1.2 SELECT all or specific columns from TABLE_NAME and change name for results
SELECT west AS "West Region",
       south AS "South Region"
  FROM tutorial.us_housing_units

-- ======================
-- 2. Filter by year - WHERE
-- ======================

SELECT *
FROM sample_table
WHERE year = 2025;
--Note: the clauses always need to be in this order: SELECT, FROM, WHERE.

-- ======================
-- 3. Select subset of columns
-- ======================

SELECT year, month, west
FROM sample_table
WHERE west > 500;

-- ======================
-- 4. Select with ILIKE operator
-- ======================

SELECT *
WHERE year <=10
AND group_name ILIKE "%ludacris%";

-- ======================
-- 5. Select with multiple operators and conditions
-- ======================

SELECT *   
FROM tutorial.billboard_top_100_year_end  
WHERE year_rank <= 10  AND ("group_name" ILIKE '%katy perry%' OR "group_name" ILIKE '%bon jovi%')
ORDER BY year_rank;

-- Version 5.1
SELECT *   
FROM tutorial.billboard_top_100_year_end  
WHERE song_name ILIKE "%california%"   AND ( (year >= 1990 AND year <= 1999) OR (year >= 1970 AND year <= 1979));

-- Version 5.2(simplified)
SELECT *   
FROM tutorial.billboard_top_100_year_end  
WHERE song_name ILIKE "%california%"   
AND ( (year BETWEEN 1970 AND 1979) OR  
           (year BETWEEN 1990 AND 1999) );

-- ======================
-- 6. Select with NOT Operator
-- ======================

SELECT *
  FROM tutorial.billboard_top_100_year_end
 WHERE year = 2013
   AND song_name NOT ILIKE '%a%';

-- ======================
-- 7. Sort Data
-- ======================

SELECT *
  FROM tutorial.billboard_top_100_year_end
 WHERE year = 2013
 ORDER BY year_rank;
-- Default (Ascending = from lower to greater numbers)

--If you'd like your results in the opposite order (referred to as descending order), you need to add the DESC operator:

SELECT *
  FROM tutorial.billboard_top_100_year_end
 WHERE year = 2013
 ORDER BY year_rank DESC;

-- 7.1 Ordering data by multiple columns

SELECT *
  FROM tutorial.billboard_top_100_year_end
  WHERE year_rank <= 3
 ORDER BY year DESC, year_rank;

 --7.1.1 Substituing numbers for column names. Numbers correspond to the order in which you list columns in SELECT.

SELECT *
  FROM tutorial.billboard_top_100_year_end
 WHERE year_rank <= 3
 ORDER BY 2, 1 DESC;

 /* ======================
    8. Limit
    ====================== */

SELECT  *   
FROM tutorial.us_housing_units
LIMIT 15;

 /* ======================
    9. Arithmetic in SQL
    ====================== */

SELECT year AS Year,
               month_name AS "Month Name",
               south + west + midwest + northeast AS "Total 4 Regions"
  FROM tutorial.us_housing_units;
  --Write a query that calculates the sum of all four regions in a separate column.

  SELECT year AS Year,
                month_name AS "Month Name",
                west AS "West Region",
                midwest + northeast AS "Mid + North"
  FROM tutorial.us_housing_units
  WHERE west > (midwest + northeast);              
  /* Write a query that returns all rows for which more units were produced in the West region than in 
  the Midwest and Northeast combined. */

  SELECT year AS Year,
    month_name AS "Month Name",
    ROUND((south / (south + west + midwest + northeast)) * 100, 2) AS "South %",
    ROUND((west / (south + west + midwest + northeast)) * 100, 2) AS "West %",
    ROUND((midwest / (south + west + midwest + northeast)) * 100, 2) AS "Midwest %",
    ROUND((northeast / (south + west + midwest + northeast)) * 100, 2) AS "Northeast %"
  FROM tutorial.us_housing_units
  WHERE year >= 2000;
  /*Write a query that calculates the percentage of all houses completed in the United States represented by each region. Only return results from the year 2000 and later.
  Hint: There should be four columns of percentages.*/

 /* ======================
    9. Make operations to a selected Group (by column)
    ====================== */

SELECT year AS Year,
               month AS Month,
               SUM(volume) AS "Shares Traded"
   FROM tutorial.aapl_historical_stock_price
   GROUP BY year, month
   ORDER BY year;

SELECT year,
       month,
       COUNT(*) AS count
  FROM tutorial.aapl_historical_stock_price
 GROUP BY year, month;

SELECT year AS Year,
               AVG(open - close) AS "Avg Daily Price"
   FROM tutorial.aapl_historical_stock_price
   GROUP BY year
   ORDER BY year;
 -- Write a query to calculate the average daily price change in Apple stock, grouped by year.

SELECT year AS Year,
               month AS Month,
               MIN(low) AS "Lowest Price",
               MAX(high) AS "Highest Price"
   FROM tutorial.aapl_historical_stock_price
   GROUP BY year, month
   ORDER BY month, year;
 -- Write a query that calculates the lowest and highest prices that Apple stock achieved each month.

 /* ======================
    10.Filter rows from values included in columns
    ====================== */

SELECT *   
   FROM tutorial.billboard_top_100_year_end  
   WHERE artist IN ("Elvis Presley", "Hammer", "M.C. Hammer");
/*Write a query that shows all of the entries for Elvis and M.C. Hammer.
Hint: M.C. Hammer is actually on the list.*/