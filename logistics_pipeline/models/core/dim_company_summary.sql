{{ config(materialized='table') }}

with vehicle_counts as (
    select
        company_id,
        count(distinct vehicle_id) as num_vehicles
    from {{ ref('stg_companies_fleet') }}
    group by company_id
),

driver_counts as (
    select
        company_id,
        count(distinct driver_id) as num_drivers
    from {{ ref('stg_companies_drivers') }}
    group by company_id
),

zone_counts as (
    select
        company_id,
        count(distinct zone_id) as num_zones
    from {{ ref('stg_companies_zones') }}
    group by company_id
)

select
    c.company_id,
    c.company_name,
    c.company_region,
    coalesce(v.num_vehicles, 0) as num_vehicles,
    coalesce(d.num_drivers, 0) as num_drivers,
    coalesce(z.num_zones, 0) as num_zones
from {{ ref('stg_companies') }} c
left join vehicle_counts v using (company_id)
left join driver_counts d using (company_id)
left join zone_counts z using (company_id)
