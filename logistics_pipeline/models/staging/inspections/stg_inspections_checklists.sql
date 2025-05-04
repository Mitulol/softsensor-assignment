with base as (

    select
        _id as inspection_id,
        jsonb_array_elements(checklist::jsonb) as item
    from {{ source('softsensor', 'inspections') }}

)

select
    inspection_id,
    item ->> 'item' as checklist_item,
    item ->> 'status' as checklist_status,
    item ->> 'notes' as checklist_notes  -- may be null
from base
