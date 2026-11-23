select
    ticker,
    session_date,
    session_open_at
from {{ ref('int_bars_mapped_to_session_opens') }}
where
    cast(session_open_at as date) <> session_date
    or cast(session_open_at as time) <> time '09:30:00'
