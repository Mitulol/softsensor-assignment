with base as (

    select
        _id as stop_id,
        jsonb_array_elements(events::jsonb) as event
    from {{ source('softsensor', 'stops') }}
),

delivery_attempts as (

    select
        stop_id,
        jsonb_array_elements(event -> 'attempts') as attempt
    from base
    where event ->> 'type' = 'delivery_attempts'

)

select
    stop_id,
    (attempt ->> 'ts')::timestamptz as attempt_time,
    attempt ->> 'status' as delivery_status
from delivery_attempts
