-- Rank top 3 distributions per amount, per tax code and ppt
WITH aggregated AS (
    SELECT
            box7_code AS tax_code,
            participant_id,
            SUM(gross) AS gross_amt
        FROM distributions
        GROUP BY 1, 2
),
windowed AS (
    SELECT
            a.tax_code,
            COALESCE(a.participant_id, p.participant_id) AS participant_id,
            p.name,
            COALESCE(gross_amt, 0) AS gross_amt,
            DENSE_RANK() OVER (PARTITION BY a.tax_code ORDER BY gross_amt DESC) AS rank
        FROM participants AS p
        LEFT JOIN aggregated AS a USING (participant_id)
        ORDER BY a.tax_code DESC, a.gross_amt DESC
)
SELECT *
    FROM windowed
    WHERE rank <= 3;
