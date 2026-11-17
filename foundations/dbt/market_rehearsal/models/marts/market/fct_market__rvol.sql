with acc_volume as (
    select
        ticker,
        session_date,
        volume,
        count(*) over prev_20 as n_prev_sessions,
        case when count(*) over prev_20 = 20
            then cast(sum(volume) over prev_20 as bigint)
            else null end as vol_last_20_sessions,
    from {{ ref('stg_market__bars') }}
    window prev_20 as (
        partition by ticker
        order by session_date
        rows between 20 preceding and 1 preceding
    )
),
avg_volume as (
    select
        ticker,
        session_date,
        volume,
        vol_last_20_sessions,
        n_prev_sessions,
        cast(vol_last_20_sessions / n_prev_sessions as bigint) as avg_vol_last_20_sessions
    from acc_volume
),
rolv as (
    select
        ticker,
        session_date,
        volume,
        vol_last_20_sessions,
        n_prev_sessions,
        avg_vol_last_20_sessions,
        round(volume / avg_vol_last_20_sessions, 2) as relative_vol
    from avg_volume
)
select
    ticker,
    session_date,
    volume,
    avg_vol_last_20_sessions,
    relative_vol
from rolv
order by ticker, session_date
