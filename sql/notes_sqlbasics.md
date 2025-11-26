# SQL = Structured Query Language
Programming language designed for managing data in a relational database. 

Broadly, within databases, tables are organized in schemas. Schemas are defined by usernames, so if your username is databass3000, all of the tables you upload will be stored under the databass3000 schema. For example, if databass3000 uploads a table on fish food sales called fish_food_sales, that table would be referenced as databass3000.fish_food_sales.

## Basic syntax: SELECT and FROM

There are two required ingredients in any SQL query: SELECT and FROM—and they have to be in that order. SELECT indicates which columns you'd like to view, and FROM identifies the table that they live in.

### Formatting convention

You might have noticed that the SELECT and `FROM' commands are capitalized. This isn't actually necessary—SQL will understand these commands if you type them in lowercase. Capitalizing commands is simply a convention that makes queries easier to read. Similarly, SQL treats one space, multiple spaces, or a line break as being the same thing. For example, SQL treats this the same way it does the previous query:

SELECT * FROM tutorial.us_housing_units

It also treats this the same way:

SELECT *
  FROM tutorial.us_housing_units

### Column names

If you'd like your results to look a bit more presentable, you can rename columns to include spaces. For example, if you want the west column to appear as West Region in the results, you would have to type:

SELECT west AS "West Region"     (review double quotes in SQLite for name with space)
  FROM tutorial.us_housing_units

## Comparison Operators SQL

Equal to	=
Not equal to	<> or !=
Greater than	>
Less than	<
Greater than or equal to	>=
Less than or equal to	<=

*All of the above operators work on non-numerical data as well. = and != make perfect sense—they allow you to select rows that match or don't match any value, respectively.

**There are some important rules when using these operators, though. If you're using an operator with values that are non-numeric, you need to put the value in single quotes: 'value'.

You can use >, <, and the rest of the comparison operators on non-numeric columns as well—they filter based on alphabetical order. Try it out a couple times with different operators:

SELECT *
  FROM tutorial.us_housing_units
 WHERE month_name > 'January'

If you're using >, <, >=, or <=, you don't necessarily need to be too specific about how you filter. Try this:

SELECT *
  FROM tutorial.us_housing_units
 WHERE month_name > 'J'

The way SQL treats alphabetical ordering is a little bit tricky. You may have noticed in the above query that selecting month_name > 'J' will yield only rows in which month_name starts with "j" or later in the alphabet. "Wait a minute," you might say. "January is included in the results—shouldn't I have to use month_name >= 'J' to make that happen?" SQL considers 'Ja' to be greater than 'J' because it has an extra letter. It's worth noting that most dictionaries would list 'Ja' after 'J' as well.

Note: SQL uses single quotes to reference column values.

## SQL Logical operators

You’ll likely also want to filter data using several conditions—possibly more often than you'll want to filter by only one condition. Logical operators allow you to use multiple comparison operators in one query.

Each logical operator is a special snowflake, so we'll go through them individually in the following lessons. Here's a quick preview:

LIKE allows you to match similar values, instead of exact values.

IN allows you to specify a list of values you'd like to include.

BETWEEN allows you to select only rows within a certain range.

IS NULL allows you to select rows that contain no data in a given column.

AND allows you to select only rows that satisfy two conditions.

OR allows you to select rows that satisfy either of two conditions.

NOT allows you to select rows that do not match a certain condition.

## IS NULL Operator

Is a logical operator in SQL that allows you to exclude rows with missing data from your results.

You can select rows that contain no data in a given column by using IS NULL.

SELECT *
FROM tutorial_billboard_top_100_year_end
WHERE artist IS NULL OR TRIM(artist) = '';

WHERE artist = NULL will not work—you can't perform arithmetic on null values.
TRIM() in SQL returns the string with leading and trailing spaces removed.
TRIM('  Manuel ')   --> 'Manuel'
TRIM('   a  ')      --> 'a'
TRIM('   ')         --> ''   -- only spaces → becomes empty string
TRIM('Rock Band')   --> 'Rock Band'  -- unchanged

TRIM(artist) = ''
you’re basically saying:
“Give me rows where artist is only spaces or already empty.”
and “This artist field is either empty or just whitespace (but not NULL).”

## The SQL AND operator

AND is a logical operator in SQL that allows you to select only rows that satisfy two conditions. 
Using data from the Billboard Music Charts, the following query will return all rows for top-10 recordings in 2012.

SELECT *
  FROM tutorial.billboard_top_100_year_end
 WHERE year = 2012 AND year_rank <= 10;

 You can use SQL's AND operator with additional AND statements or any other comparison operator, as many times as you want. If you run this query, you'll notice that all of the requirements are satisfied.

## The SQL BETWEEN operator

BETWEEN is a logical operator in SQL that allows you to select only rows that are within a specific range. It has to be paired with the AND operator, which you'll learn about in a later lesson. Here's what BETWEEN looks like on a Billboard Music Chart Dataset:

SELECT *
  FROM tutorial.billboard_top_100_year_end
 WHERE year_rank BETWEEN 5 AND 10

## The SQL LIKE operator

SELECT *
  FROM tutorial.billboard_top_100_year_end
 WHERE year = 2012
   AND year_rank <= 10
   AND "group_name" ILIKE '%feat%';

Note: "group_name" ILIKE '%string%' searches and selects all rows where group_name contains string.
It works like LIKE but case-insensitive.

  LIKE → case-sensitive ('Ludacris' ≠ 'ludacris')
  ILIKE → case-insensitive ('Ludacris', 'LUDACRIS', 'lUdAcRiS' all match)

will match:

  Ludacris Fan Club
  best of LUDACRIS
  My ludacris playlist

even though the case is different.

🎯 The pattern: '%ludacris%'

This is a string pattern with wildcards:

'ludacris' → exact match only
'ludacris%' → starts with "ludacris"
'%ludacris' → ends with "ludacris"
'%ludacris%' → contains "ludacris" anywhere
'% %' → contains " "(espace) in the string

The % used above represents any character or set of characters. In this case, % is referred to as a "wildcard."
% = any sequence of 0 or more characters
_ = exactly one character

## The SQL OR and XOR operator

OR is a logical operator in SQL that allows you to select rows that satisfy either of two conditions.
You can combine AND with OR using parenthesis. The following query will return rows that satisfy both of the following conditions:

You'll notice that each row will satisfy one of the two conditions. You can combine AND with OR using parenthesis. The following query will return rows that satisfy both of the following conditions:

SELECT *
  FROM tutorial.billboard_top_100_year_end
 WHERE year = 2013
   AND ("group_name" ILIKE '%macklemore%' OR "group_name" ILIKE '%timberlake%')
  
XOR is a logical operator in SL that allows you to select rows that satisfy either of two conditions BUT NOT BOTH.

## The SQL IN operator

IN is a logical operator in SQL that allows you to specify a list of values that you'd like to include in the results. For example, the following query of data from the Billboard Music Charts will return results for which the year_rank column is equal to one of the values in the list:

SELECT *
  FROM tutorial.billboard_top_100_year_end
 WHERE year_rank IN (1, 2, 3)

## The SQL NOT operator

NOT is a logical operator in SQL that you can put before any conditional statement to select rows for which that statement is false.

Here's what NOT looks like in action in a query of Billboard Music Charts data:

SELECT *
  FROM tutorial.billboard_top_100_year_end
 WHERE year = 2013
   AND year_rank NOT BETWEEN 2 AND 3

NOT is commonly used with LIKE. Run this query and check out how Macklemore magically disappears!

SELECT *
  FROM tutorial.billboard_top_100_year_end
 WHERE year = 2013
   AND "group_name" NOT ILIKE '%macklemore%'

NOT is also frequently used to identify non-null rows, but the syntax is somewhat special—you need to include IS beforehand. Here's how that looks:

SELECT *
  FROM tutorial.billboard_top_100_year_end
 WHERE year = 2013
   AND artist IS NOT NULL

## Sorting data with SQL ORDER BY

Once you've learned how to filter data, it's time to learn how to sort data. The ORDER BY clause allows you to reorder your results based on the data in one or more columns. SQL´s default is to sort in ascending order (from lower to greater values).

If you'd like your results in the opposite order (referred to as descending order), you need to add the DESC operator.

### Ordering data by multiple columns

You can also order by mutiple columns. This is particularly useful if your data falls into categories and you'd like to organize rows by date, for example, but keep all of the results within a given category together. This example query makes the most recent years come first but orders top-ranks songs before lower-ranked songs:

SELECT *
  FROM tutorial.billboard_top_100_year_end
  WHERE year_rank <= 3
 ORDER BY year DESC, year_rank

You can see a couple things from the above query: First, columns in the ORDER BY clause must be separated by commas. Second, the DESC operator is only applied to the column that precedes it. Finally, the results are sorted by the first column mentioned (year), then by year_rank afterward. You can see the difference the order makes by running the following query:

SELECT *
  FROM tutorial.billboard_top_100_year_end
 WHERE year_rank <= 3
 ORDER BY year_rank, year DESC

Finally, you can make your life a little easier by substituting numbers for column names in the ORDER BY clause. The numbers will correspond to the order in which you list columns in the SELECT clause. For example, the following query is exactly equivalent to the previous query:

SELECT *
  FROM tutorial.billboard_top_100_year_end
 WHERE year_rank <= 3
 ORDER BY 2, 1 DESC

 ## Limit

 The limit restricts how many rows the SQL query returns. The limiting functionality is built to prevent you from accidentally returning millions of rows without meaning to (we've all done it).

 ## Arithmetic in SQL

 You can perform arithmetic in SQL using the same operators you would in Excel: +, -, *, /. However, in SQL you can only perform arithmetic across columns on values in a given row. To clarify, you can only add values in multiple columns from the same row together using +—if you want to add values across multiple rows, you'll need to use aggregate functions.

SELECT year,
       month,
       west,
       south,
       west + south - 4 * year AS nonsense_column
  FROM tutorial.us_housing_units

The columns that contain the arithmetic functions are called "derived columns" because they are generated by modifying the information that exists in the underlying data.

As in Excel, you can use parentheses to manage the order of operations. For example, if you wanted to average the west and south columns, you could write something like this:

SELECT year,
       month,
       west,
       south,
       (west + south)/2 AS south_west_avg
  FROM tutorial.us_housing_units

ROUND function:

  ROUND(x, 2) → round to 2 decimal places (0.01)

  ROUND(x, 0) → round to nearest integer

  ROUND(x, -1) → round to nearest 10

  ROUND(x, -2) → round to nearest 100

  ROUND(x, -3) → round to nearest 1,000

  Examples:
    ROUND(1234, -1) → 1230

    ROUND(1234, -2) → 1200

    ROUND(1234, -3) → 1000

## The SQL GROUP BY clause

SQL aggregate function like COUNT, AVG, and SUM have something in common: they all aggregate across the entire table. But what if you want to aggregate only part of a table? For example, you might want to count the number of entries for each year.

In situations like this, you'd need to use the GROUP BY clause. GROUP BY allows you to separate data into groups, which can be aggregated independently of one another.

You can group by multiple columns, but you have to separate column names with commas—just as with ORDER BY):

SELECT year,
       month,
       COUNT(*) AS count
  FROM tutorial.aapl_historical_stock_price
 GROUP BY year, month

As with, you can substitute numbers for column names in the  clause. It's generally recommended to do this only when you're grouping many columns, or if something else is causing the text in the clause to be excessively long:

SELECT year,
       month,
       COUNT(*) AS count
  FROM tutorial.aapl_historical_stock_price
 GROUP BY 1, 2

 ## The length() function in SQL

 Returns the number of characters in a string. 