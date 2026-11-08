WITH fields AS (
    SELECT strftime('%Y-%m', dist_date) as month,
           box7_code AS tax_code,
           gross
        FROM distributions
),
monthly AS (            -- get monthly Gross amt per month and tax code first
    SELECT month,
           tax_code,
           SUM(GROSS) AS monthly_gross
        FROM fields
        GROUP BY month, tax_code
),
running_total AS (      -- run window SUM() over months per tax code to get running total
    SELECT month,
           tax_code,
           monthly_gross,
           SUM(monthly_gross) OVER (
            PARTITION BY tax_code
            ORDER BY month
            ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
           ) AS running_total
        FROM monthly
)
SELECT *
    FROM running_total
    ORDER BY tax_code, month;
