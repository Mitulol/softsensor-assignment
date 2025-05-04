{% snapshot snap_license_status %}
{{
    config(
      target_schema='snapshots',
      unique_key='driver_id',
      strategy='check',
      check_cols=['license_class', 'license_expiry']
    )
}}

select
    driver_id,
    license_class,
    license_expiry
from {{ ref('stg_drivers') }}

{% endsnapshot %}
