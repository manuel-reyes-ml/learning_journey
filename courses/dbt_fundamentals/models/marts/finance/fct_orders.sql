with orders as (
    select * from {{ref('stg_joffle_shop_orders')}}
),

payments as (
    select * from {{ref('stg_stripe_payments')}}
),

order_payments as (
    select
        order_id,
        sum(case when status = 'success' then amount end) as amount

    from payments
    group by 1
),

final as (
    select
        orders.order_id,
        orders.customer_id,
        orders.order_date,
        order_payments.amount

    from orders

    left join order_payments using (order_id)
)

select * from final
