with events as (
    select * from {{ source('market', 'insider_events') }}
)
select
    event_id,
    ticker,
    txn_code as code,
    cast(filing_date as date) as filing_date,
    cast(accepted_at as timestamp) as accepted_at,
    -- 'NULLIF(a, b)' means “give me a, unless it equals b, then give me NULL.” It’s mostly
    nullif(TRIM(boundary_case), '') as boundary_case  -- blank strings → NULL
from events
