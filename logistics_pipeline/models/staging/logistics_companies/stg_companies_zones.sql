with base as (

    select
        _id as company_id,
        jsonb_array_elements_text(active_zones::jsonb) as zone_id
    from {{ source('softsensor', 'logistics_companies') }}

)

select *
from base
