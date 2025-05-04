with base as (

    select
        _id as company_id,
        name as company_name,
        region as company_region
    from {{ source('softsensor', 'logistics_companies') }}

)

select *
from base
