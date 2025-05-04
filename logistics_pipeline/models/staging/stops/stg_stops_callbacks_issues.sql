with base as (

    select
        _id as stop_id,
        jsonb_array_elements(customer_callbacks::jsonb) as cb
    from {{ source('softsensor', 'stops') }}
    where jsonb_array_length(customer_callbacks::jsonb) > 0
),

issues as (

    select
        stop_id,
        (cb ->> 'callback_ts')::timestamptz as callback_time,
        jsonb_array_elements(cb -> 'issues') as issue
    from base

)

select
    stop_id,
    callback_time,
    issue ->> 'type' as issue_type,
    issue ->> 'detail' as issue_detail
from issues
