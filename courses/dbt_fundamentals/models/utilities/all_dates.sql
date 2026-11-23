{{ config(materialized="table") }}  -- config line for specific model

with spine as (
    {{ dbt_utils.date_spine(
        datepart="day",
        start_date="cast('2020-01-01' as date)",
        end_date="cast('2021-01-01' as date)"
    )
    }}
)

select cast(date_day as date) as date_day
from spine

-- end_date= is exclusive
