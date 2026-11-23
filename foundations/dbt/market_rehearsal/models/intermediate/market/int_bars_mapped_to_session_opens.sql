-- One row per ticker per session: the moment that session opened (09:30 ET, naive).
-- Derived from stg_bars, so a session exists only if a bar exists.
select
    ticker,
    session_date,
    cast(session_date as timestamp) + interval '9 hours 30 minutes' as session_open_at
from {{ ref('stg_market__bars') }}
