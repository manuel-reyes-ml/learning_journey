-- the 18:00 acceptance and the one at exactly 09:30:00 must both trade on a later session.
select
    event_id,
    boundary_case,
    filing_date,
    accepted_at,
    entry_session
from {{ ref('fct_market__event_entries') }}
where boundary_case is not null
  and (entry_session is null or entry_session <= filing_date)
