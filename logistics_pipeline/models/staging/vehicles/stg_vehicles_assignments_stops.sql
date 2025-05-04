with base as (

    select
        _id as vehicle_id,
        jsonb_array_elements(current_assignments::jsonb) as assignment
    from {{ source('softsensor', 'vehicles') }}

),

exploded_stops as (

    select
        vehicle_id,
        assignment ->> 'route_id' as route_id,
        jsonb_array_elements_text(assignment -> 'details' -> 'planned_stops') as planned_stop
    from base

)

select *
from exploded_stops
