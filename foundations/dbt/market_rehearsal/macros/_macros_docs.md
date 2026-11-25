{% docs generate_schema_name %}

Overrides dbt's built-in schema naming.

      | Target              | Node has `+schema` | Schema it builds in               |
      |---------------------|--------------------|-----------------------------------|
      | `prod`              | yes                | `<custom_schema>` (e.g. `marts`)  |
      | any other (dev, ci) | yes                | `<target_schema>_<custom_schema>` |
      | any                 | no                 | `<target_schema>`                 |

      Raises a compiler error instead of returning an empty schema name.

{% enddocs %}
