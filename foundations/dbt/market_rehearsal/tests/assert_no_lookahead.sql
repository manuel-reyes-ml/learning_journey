-- returns any entry whose session opened at or before
-- its filed_at 📈 accepted_at. Zero rows = pass.
select
    e.event_id,
    e.accepted_at,
    e.entry_session,
    e.session_open_at
from {{ ref('fct_market__event_entries') }} as e
where e.session_open_at <= e.accepted_at
