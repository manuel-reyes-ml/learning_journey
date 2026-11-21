select count(*) as n_rows
from {{ ref('gen_manifest') }}
having count(*) <> 1
