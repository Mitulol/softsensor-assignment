{% snapshot snap_vehicle_maintenance %}

{{
  config(
    target_schema='snapshots',
    unique_key='vehicle_id',
    strategy='check',
    check_cols=['service_date', 'km_reading', 'tasks']
  )
}}

select
    vehicle_id,
    service_date,
    km_reading,
    maintenance_task
from {{ ref('stg_vehicles_maintenance') }}

{% endsnapshot %}
