WITH fields AS (
    SELECT strftime('%Y-%m', dist_date) as month,
           box7_code AS tax_code,
           gross
        FROM distributions
),
monthly AS (
    SELECT month,
           tax_code,
           SUM(GROSS) AS monthly_gross
        FROM fields
        GROUP BY month, tax_code
),
running_total AS (
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
    ORDER BYtax_code, month;
