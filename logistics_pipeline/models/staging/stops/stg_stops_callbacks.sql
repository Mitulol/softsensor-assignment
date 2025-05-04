with base as (

    select
        _id as stop_id,
        jsonb_array_elements(customer_callbacks::jsonb) as cb
    from {{ source('softsensor', 'stops') }}

)

select
    stop_id,
    (cb ->> 'callback_ts')::timestamptz as callback_time
from base
