with base as (

    select
        _id as inspection_id,
        vehicle_id,
        (inspector ->> 'id') as inspector_id,
        (inspector ->> 'name') as inspector_name,
        date::date as inspection_date
    from {{ source('softsensor', 'inspections') }}

)

select *
from base
