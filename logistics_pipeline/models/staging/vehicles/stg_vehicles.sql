with base as (

    select
        _id as vehicle_id,
        type as vehicle_type,
        capacity_packages::int as vehicle_capacity
    from {{ source('softsensor', 'vehicles') }}

)

select *
from base
