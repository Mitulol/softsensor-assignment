with base as (

    select
        _id as inspection_id,
        jsonb_array_elements(issues_found::jsonb) as issue
    from {{ source('softsensor', 'inspections') }}

)

select
    inspection_id,
    issue ->> 'code' as issue_code,
    issue ->> 'description' as issue_description
from base
