{{ config(materialized='table') }}

with base as (

    select
        vehicle_id,
        service_date,
        km_reading,
        maintenance_task,
        cost
    from {{ ref('stg_vehicles_maintenance') }}

),

aggregated as (

    select
        vehicle_id,
        service_date,
        min(km_reading) as km_reading,
        sum(cost) as total_maintenance_cost,
        count(*) as num_tasks
    from base
    group by vehicle_id, service_date

)

select *
from aggregated
