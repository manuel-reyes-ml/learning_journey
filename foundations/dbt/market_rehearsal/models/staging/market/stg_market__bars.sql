with bars as (
    select * from {{ source('market', 'bars_daily') }}  -- with seed is ref()
)
select
    cast(ticker as varchar)         as ticker,
    cast(session_date as date)      as session_date,
    cast(open as decimal(18, 4))    as open,
    cast (high as decimal(18, 4))   as high,
    cast(low as decimal(18, 4))     as low,
    cast(close as decimal(18, 4))   as close,
    cast(volume as bigint)          as volume
from bars
