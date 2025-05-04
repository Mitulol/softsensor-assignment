{{ config(materialized='table') }}

with base as (

    select
        inspection_id,
        inspection_date,
        vehicle_id,
        inspector_id,
        inspector_name
    from {{ ref('stg_inspections') }}

),

check_counts as (

    select
        inspection_id,
        count(*) as total_checks,
        count(*) filter (where checklist_status = 'Fail') as failed_checks
    from {{ ref('stg_inspections_checklists') }}
    group by inspection_id

),

issue_counts as (

    select
        inspection_id,
        count(*) as issues_found_count
    from {{ ref('stg_inspections_issues') }}
    group by inspection_id

),

final as (

    select
        base.inspection_id,
        base.inspection_date,
        base.vehicle_id,
        base.inspector_id,
        base.inspector_name,
        coalesce(check_counts.total_checks, 0) as total_checks,
        coalesce(check_counts.failed_checks, 0) as failed_checks,
        coalesce(issue_counts.issues_found_count, 0) as issues_found_count,
        case
            when coalesce(check_counts.failed_checks, 0) = 0
             and coalesce(issue_counts.issues_found_count, 0) = 0
            then true
            else false
        end as passed
    from base
    left join check_counts using (inspection_id)
    left join issue_counts using (inspection_id)

)

select *
from final
