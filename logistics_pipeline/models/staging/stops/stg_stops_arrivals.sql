with base as (

    select
        _id as stop_id,
        jsonb_array_elements(events::jsonb) as event
    from {{ source('softsensor', 'stops') }}
),

arrivals as (

    select
        stop_id,
        (event ->> 'ts')::timestamptz as arrival_time
    from base
    where event ->> 'type' = 'arrival'

)

select * from arrivals
