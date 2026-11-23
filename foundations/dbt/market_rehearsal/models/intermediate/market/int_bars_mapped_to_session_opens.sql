-- Moved from models/staging/market/stg_market__session_opens.sql (logic unchanged).
-- One row per ticker per session: the moment that session opened (09:30 ET, naive).
-- Derived from stg_market__bars, so a session exists only if a bar exists.
with stg_bars as (
    select * from {{ ref('stg_market__bars') }}
)

select
    ticker,
    session_date,
    cast(session_date as timestamp)
    + interval '9 hours 30 minutes' as session_open_at
from stg_bars
