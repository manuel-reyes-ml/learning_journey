select
    orders.order_id,
    orders.customer_id,
    payments.amount

from {{ ref('stg_joffle_shop_orders'
)}} as orders
join {{ ref('stg_stripe_payments')}} as payments
