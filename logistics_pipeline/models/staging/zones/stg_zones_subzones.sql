with base as (

    select
        _id as zone_id,
        jsonb_array_elements(subzones::jsonb) as sub
    from {{ source('softsensor', 'zones') }}

)

select
    zone_id,
    sub ->> 'id' as subzone_id,
    sub ->> 'name' as subzone_name
from base
