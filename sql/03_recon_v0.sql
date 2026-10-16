-- Recon v0: find the defects we planted on Day 16.
-- If these queries find EXACTLY the planted defects, the logic is proven.

-- Q1: Participants with NO distribution (the ~15% missing rows).
-- LEFT JOIN keeps every row from the LEFT table (participants) and fills
-- NULL where the right side has no match. Filtering WHERE right-side IS NULL
-- = "left rows with no partner" — THE find-the-missing-rows pattern.
-- You will write this shape a thousand times in your DE career.
SELECT p.participant_id, p.name
    FROM participants       AS p                -- AS p = table alias (shorthand)
    LEFT JOIN distributions AS d
        ON p.participant_id = d.participant_id  -- ON = the matching rule
    WHERE d.participant_id IS NULL;             -- NULL needs IS, not =

-- Q2: Distribution totals per Box-7 code (GROUP BY = collapse rows into
-- one summary row per group; aggregates like SUM/COUNT compute per group).
SELECT box7_code,
       COUNT(*)             AS n_distributions,
       SUM(gross)           AS total_gross,
       ROUND(AVG(gross), 2) AS avg_gross
    FROM distributions
    GROUP BY box7_code
    ORDER BY total_gross DESC;

-- Q3: Codes with unusually high totals — HAVING filters AFTER grouping
-- (WHERE filters rows BEFORE grouping; HAVING filters the groups).
SELECT box7_code, SUM(gross) AS total_gross
    FROM distributions
    GROUP BY box7_code
    HAVING SUM(gross) > 100000;

-- Q4 (stretch): expected vs actual — join and compare per participant.
SELECT p.participant_id,
       p.name,
       ROUND(p.salary * p.deferral_pct, 2) AS expected_annual_deferral,
       d.gross                         AS actual_distribution
    FROM participants  AS p
    JOIN distributions AS d USING (participant_id);
