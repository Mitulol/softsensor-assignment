with base as (

    select
        _id as vehicle_id,
        jsonb_array_elements(current_assignments::jsonb) as assignment
    from {{ source('softsensor', 'vehicles') }}

),

exploded_backups as (

    select
        vehicle_id,
        assignment ->> 'route_id' as route_id,
        jsonb_array_elements_text(assignment -> 'details' -> 'backup_vehicles') as backup_vehicle_id
    from base

)

select *
from exploded_backups
