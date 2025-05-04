with base as (

    select
        _id as vehicle_id,
        jsonb_array_elements(sensor_streams::jsonb) as stream
    from {{ source('softsensor', 'vehicles') }}
    where sensor_streams is not null
),

fuel_streams as (

    select
        vehicle_id,
        jsonb_array_elements(stream -> 'readings') as reading
    from base
    where stream ->> 'stream_type' = 'fuel'

)

select
    vehicle_id,
    (reading ->> 'ts')::timestamptz as timestamp,
    (reading ->> 'liters')::numeric as liters
from fuel_streams
