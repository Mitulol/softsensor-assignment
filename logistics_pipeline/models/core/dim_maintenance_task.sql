{{ config(materialized='table') }}

select
    vehicle_id,
    service_date,
    maintenance_task as task_name,
    cost
from {{ ref('stg_vehicles_maintenance') }}
