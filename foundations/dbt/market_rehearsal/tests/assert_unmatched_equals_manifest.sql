-- the generator knows how many filings have no later session; dbt must agree.
with unmatched as (
    select count(*) as n
    from {{ ref('fct_market__event_entries') }}
    where entry_session is null
)

select
    u.n as unmatched,
    m.expected_unmatched
from unmatched as u
cross join {{ ref('gen_manifest') }} as m
where u.n <> m.expected_unmatched

-- A CROSS JOIN pairs every row in one table with every row in another.
-- The result is called a Cartesian product. It has no join condition
-- and returns every possible pairing of rows. An INNER JOIN filters
--that product down to only the pairs that match an ON condition.

-- If both tables have thousands of rows, one query can produce millions
-- of records and use a lot of memory and CPU.
