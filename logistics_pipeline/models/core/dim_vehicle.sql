{{ config(materialized='table') }}

select
    vehicle_id,
    vehicle_type,
    vehicle_capacity
from {{ ref('stg_vehicles') }}
