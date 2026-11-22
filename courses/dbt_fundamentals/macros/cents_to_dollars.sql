{%- macro cents_to_dollars(column_name, round=2) -%}
    round({{ column_name }} / 100, {{ round }})
{%- endmacro %}
