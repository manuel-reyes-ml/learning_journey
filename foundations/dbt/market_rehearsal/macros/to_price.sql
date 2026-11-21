{#- One definition of "a price" for every model: DECIMAL(18,4). -#}
{#-
    What macros are: reusable Jinja functions in macros/. Some you call;
    some, like generate_schema_name, dbt calls itself, and your version
    replaces dbt’s.

-#}
{% macro to_price(column_name) -%}
    cast({{ column_name }} as decimal(18, 4))
{%- endmacro %}
