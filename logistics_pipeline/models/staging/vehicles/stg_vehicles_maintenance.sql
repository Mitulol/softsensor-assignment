with base as (

    select
        _id as vehicle_id,
        jsonb_array_elements(maintenance_logs::jsonb) as log
    from {{ source('softsensor', 'vehicles') }}

),

with_details as (

    select
        vehicle_id,
        (log ->> 'service_date')::date as service_date,
        (log -> 'details' ->> 'km_reading')::int as km_reading,
        jsonb_array_elements(log -> 'details' -> 'tasks') as task
    from base

),

final as (

    select
        vehicle_id,
        service_date,
        km_reading,
        task ->> 'task' as maintenance_task,
        (task ->> 'cost')::numeric as cost
    from with_details

)

select *
from final
