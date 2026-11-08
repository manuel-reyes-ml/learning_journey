WITH fields AS (
    SELECT strftime('%m', dist_date) as month,
           box7_code AS tax_code,
           gross
        FROM distributions
),
running_total AS (
    SELECT month,
           tax_code,
           SUM(gross) OVER (
            PARTITION BY tax_code
            ORDER BY month
            ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
            ) AS running_total
        FROM fields
        GROUP BY month, tax_code
)
SELECT *
    FROM running_total
    ORDER BY month;
