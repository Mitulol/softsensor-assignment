with base as (

    select
        _id as vehicle_id,
        jsonb_array_elements(sensor_streams::jsonb) as stream
    from {{ source('softsensor', 'vehicles') }}
    where sensor_streams is not null
),

gps_streams as (

    select
        vehicle_id,
        jsonb_array_elements(stream -> 'points') as inner_points
    from base
    where stream ->> 'stream_type' = 'gps'

),

flattened as (

    select
        vehicle_id,
        jsonb_array_elements(inner_points) as point
    from gps_streams

)

select
    vehicle_id,
    (point ->> 'ts')::timestamptz as timestamp,
    (point ->> 'lat')::numeric as lat,
    (point ->> 'lng')::numeric as lng
from flattened
