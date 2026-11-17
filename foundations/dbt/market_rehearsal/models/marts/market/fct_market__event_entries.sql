-- DuckDB ASOF LEFT JOIN: for each filing, the nearest session open strictly AFTER
-- its acceptance time. LEFT keeps filings that have no later session (entry = NULL);
-- a plain ASOF JOIN is an INNER join and would drop them without a word.
select
    e.event_id,
    e.ticker,
    e.filing_date,
    e.accepted_at,
    e.boundary_case,
    o.session_date as entry_session,
    o.session_open_at
from {{ ref('stg_market__insider_events') }} as e
asof left join {{ ref('stg_session_opens') }} as o
on e.ticker = o.ticker
and e.accepted_at < o.session_open_at

-- ASOF LEFT matches each left row to the closest row on the right by an ordering column
-- (usually a timestamp), not to a row with an exact match.
-- And keeps the left rows that have no match, putting Null on the columns of the right.

-- You give it two kinds of conditions:
--  1. Equality keys (optional) group the rows first, for example ticker = ticker.
--  2. One inequality (>=, <=, >, <) on the time column says which direction to look.
