-- Every bar must be internally consistent: low <= open/close <= high,
-- prices positive, volume not negative. Returns the bad rows.
select *
from {{ ref('stg_market__bars') }}
where
    low > least(open, closed)
    or high < greatest(open, closed)
    or low <= 0
    or volume < 0

-- The tests check the content after the build: nulls, the grain, and business rules.
