with bars as (
    select * from {{ source('market', 'bars_daily') }}  -- with seed is ref()
)

select
    ticker,
    session_date,
    {{ to_price('open') }} as open,
    {{ to_price('high') }} as high,
    {{ to_price('low') }} as low,
    {{ to_price('close') }} as closed,
    volume
from bars
