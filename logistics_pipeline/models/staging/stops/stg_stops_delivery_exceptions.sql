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
),

exceptions as (

    select
        stop_id,
        (attempt ->> 'ts')::timestamptz as attempt_time,
        attempt -> 'exception' as ex
    from delivery_attempts
    where attempt ? 'exception'

)

select
    stop_id,
    attempt_time,
    ex ->> 'code' as exception_code,
    ex ->> 'reason' as exception_reason
from exceptions
