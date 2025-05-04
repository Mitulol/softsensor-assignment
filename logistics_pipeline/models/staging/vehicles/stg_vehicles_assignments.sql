with base as (

    select
        _id as vehicle_id,
        jsonb_array_elements(current_assignments::jsonb) as assignment
    from {{ source('softsensor', 'vehicles') }}

)

select
    vehicle_id,
    assignment ->> 'route_id' as route_id,
    (assignment ->> 'start_date')::date as start_date
from base
