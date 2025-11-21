# SQL = Structured Query Language
Programming language designed for managing data in a relational database. 

Broadly, within databases, tables are organized in schemas. Schemas are defined by usernames, so if your username is databass3000, all of the tables you upload will be stored under the databass3000 schema. For example, if databass3000 uploads a table on fish food sales called fish_food_sales, that table would be referenced as databass3000.fish_food_sales.

## IS NULL Operator

Is a logical operator in SQL that allows you to exclude rows with missing data from your results.

You can select rows that contain no data in a given column by using IS NULL.

SELECT *
FROM tutorial_billboard_top_100_year_end
WHERE artist IS NULL OR TRIM(artist) = '';

WHERE artist = NULL will not work—you can't perform arithmetic on null values.

## The SQL AND operator

AND is a logical operator in SQL that allows you to select only rows that satisfy two conditions. 
Using data from the Billboard Music Charts, the following query will return all rows for top-10 recordings in 2012.

SELECT *
  FROM tutorial.billboard_top_100_year_end
 WHERE year = 2012 AND year_rank <= 10;

 You can use SQL's AND operator with additional AND statements or any other comparison operator, as many times as you want. If you run this query, you'll notice that all of the requirements are satisfied.

SELECT *
  FROM tutorial.billboard_top_100_year_end
 WHERE year = 2012
   AND year_rank <= 10
   AND "group_name" ILIKE '%feat%';

Note: "group_name" ILIKE '%string%' searches and selects all rows where group_name contains string.
