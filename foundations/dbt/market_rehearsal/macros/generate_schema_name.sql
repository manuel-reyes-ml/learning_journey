{#-
    Where dbt builds each node.
      dev / ci : <target schema>_<custom schema>   (isolated per developer)
      prod     : <custom schema>                    (plain: raw, staging, marts)
      no custom schema -> the target schema, in every environment
    Fails at compile time if the result would be empty, instead of letting
    the database reject an empty identifier later.

    target.name = --target prod

    Adding the '-' signs removes that white space line from the code on the
    compiled result.
-#}
{% macro generate_schema_name(custom_schema_name, node) -%}
    {%- set default_schema = target.schema | trim -%}
    {%- set custom_schema = (custom_schema_name or '') | trim -%}

    {%- if not custom_schema -%}
        {%- set schema_name = default_schema -%}
    {%- elif target.name == 'prod' -%}
        {%- set schema_name = custom_schema -%}
    {%- else -%}
        {%- set schema_name = default_schema ~ '_' ~ custom_schema -%}
    {%- endif -%}

    {%- if not schema_name -%}
        {{ exceptions.raise_compiler_error(
            "generate_schema_name produced an empty schema for '" ~ node.name
            ~ "' (target=" ~ target.name ~ ", custom_schema=" ~ custom_schema_name ~ ")"

        ) }}
    {%- endif -%}

    {{- schema_name -}}
{%- endmacro %}
