{{ config(materialized='table') }}

with subzone_list as (
    select
        zone_id,
        string_agg(subzone_name, ', ') as subzones
    from {{ ref('stg_zones_subzones') }}
    group by zone_id
)

select
    z.zone_id,
    z.zone_name,
    coalesce(s.subzones, '') as subzones
from {{ ref('stg_zones') }} z
left join subzone_list s using (zone_id)
