{{ config(materialized='table') }}

with shifts as (

    select
        sched.driver_id,
        drv.driver_name,
        sched.day,
        sched.shift_start,
        sched.shift_end,
        (sched.shift_end::time - sched.shift_start::time) as shift_duration
    from {{ ref('stg_drivers_schedules') }} as sched
    left join {{ ref('stg_drivers') }} as drv
        on sched.driver_id = drv.driver_id

)

select *
from shifts
