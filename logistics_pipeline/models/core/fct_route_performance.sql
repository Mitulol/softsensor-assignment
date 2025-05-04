{{ config(materialized='table') }}

with planned_stops as (
    select
        route_id,
        count(*) as planned_stop_count
    from {{ ref('stg_vehicles_assignments_stops') }}
    group by route_id
),

successful_deliveries as (
    select
        stop_id,
        count(*) filter (where delivery_status = 'Delivered') as delivery_success
    from {{ ref('stg_stops_delivery_attempts') }}
    group by stop_id
),

deliveries_by_route as (
    select
        vas.route_id,
        count(*) filter (where sd.delivery_success > 0) as completed_deliveries
    from {{ ref('stg_vehicles_assignments_stops') }} vas
    left join successful_deliveries sd
        on vas.planned_stop = sd.stop_id
    group by vas.route_id
),

exceptions_by_route as (
    select
        vas.route_id,
        sum(coalesce(e.count, 0)) as exception_count
    from {{ ref('stg_vehicles_assignments_stops') }} vas
    left join (
        select stop_id, count(*) as count
        from {{ ref('stg_stops_delivery_exceptions') }}
        group by stop_id
    ) e
        on vas.planned_stop = e.stop_id
    group by vas.route_id
),

backups as (
    select
        route_id,
        true as used_backup
    from {{ ref('stg_vehicles_assignments_backups') }}
    group by route_id
),

base as (
    select
        va.route_id,
        va.vehicle_id,
        va.start_date,
        coalesce(ps.planned_stop_count, 0) as planned_stop_count,
        coalesce(dbr.completed_deliveries, 0) as completed_deliveries,
        coalesce(ebr.exception_count, 0) as exception_count,
        coalesce(b.used_backup, false) as used_backup,
        case
            when coalesce(ps.planned_stop_count, 0) = coalesce(dbr.completed_deliveries, 0)
            then true else false
        end as all_stops_delivered,
        case
            when ps.planned_stop_count = 0 then null
            else 1.0 * coalesce(dbr.completed_deliveries, 0) / ps.planned_stop_count
        end as delivery_success_rate
    from {{ ref('stg_vehicles_assignments') }} va
    left join planned_stops ps using (route_id)
    left join deliveries_by_route dbr using (route_id)
    left join exceptions_by_route ebr using (route_id)
    left join backups b using (route_id)
)

select *
from base
