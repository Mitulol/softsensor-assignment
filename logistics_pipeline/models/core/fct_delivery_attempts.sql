{{ config(materialized='table') }}

select
    a.stop_id,
    s.package_id,
    a.attempt_time,
    a.delivery_status,
    e.exception_code,
    e.exception_reason
from {{ ref('stg_stops_delivery_attempts') }} a
left join {{ ref('stg_stops') }} s
    on a.stop_id = s.stop_id
left join {{ ref('stg_stops_delivery_exceptions')}} e
    on e.stop_id = a.stop_id and e.attempt_time = a.attempt_time
