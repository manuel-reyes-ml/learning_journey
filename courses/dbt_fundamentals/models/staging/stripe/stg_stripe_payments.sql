with payments as (
    select * from {{ source('stripe', 'payment') }}
)

select
    status,
    _batched_at,
    id as payment_id,
    orderid as order_id,
    paymentmethod as payment_method,
    created as created_at,

    -- amount is stored in cents, convert it to dollars
    amount / 100 as amount
from payments
