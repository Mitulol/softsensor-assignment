with base as (

    select
        _id as driver_id,
        jsonb_array_elements(weekly_schedule::jsonb) as day_obj
    from {{ source('softsensor', 'drivers') }}

),

day_shift as (

    select
        driver_id,
        day_obj ->> 'day' as day,
        jsonb_array_elements(day_obj -> 'shifts') as shift_obj
    from base

),

exploded as (

    select
        driver_id,
        day,
        (shift_obj ->> 'start')::time as shift_start,
        (shift_obj ->> 'end')::time as shift_end
    from day_shift

)

select *
from exploded
