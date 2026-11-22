{#
The dashes in {%- and -%} tell Jinja to delete all whitespace and newlines next to the tag.
'{%-' removes the whitespace on the line and '-%}' deletes the newline.

Inside {{ }} you're writing Jinja, not SQL. Jinja runs first, and only its output ends up in the SQL.
Either quote works. In Jinja, {{ "," if not loop.last }} and {{ ',' if not loop.last }} do
exactly the same thing. Both output a bare comma, and no quote marks reach the compiled SQL.
#}
{%- set order_status_types = [
    'returned', 'return_pending', 'completed',
    'shipped', 'placed',
] -%}

with orders as (
    select * from {{ ref('stg_jaffle_shop_orders') }}
),

pivoted as (
    select
        customer_id,
    {% for status in order_status_types -%}
        count(case when status = '{{ status }}' then 1 end)
            as orders_{{ status }}{{ "," if not loop.last }}

    
    {% endfor -%}
    from orders
    group by 1
)

select * from pivoted
