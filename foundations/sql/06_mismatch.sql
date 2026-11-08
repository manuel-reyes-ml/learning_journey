-- find mismatch between distributions vs expected, same excercise as in Python matcher.py
WITH actual AS (
    SELECT participant_id,
           SUM(gross) AS  gross_amt
        FROM distributions
        GROUP BY 1
),
expected AS (
    SELECT participant_id,
           ROUND(salary * deferral_pct, 2) AS expected_amt
        FROM participants
),
comparison AS (
    SELECT COALESCE(e.participant_id, a.participant_id) AS participant_id,
           e.expected_amt,
           a.gross_amt,
           ROUND(COALESCE(e.expected_amt, 0) - COALESCE(a.gross_amt, 0), 2) AS difference
        FROM expected AS e
        FULL OUTER JOIN actual AS a USING (participant_id)
)
SELECT *
    FROM comparison
    WHERE ABS(difference) > 0.01
    ORDER BY participant_id;
