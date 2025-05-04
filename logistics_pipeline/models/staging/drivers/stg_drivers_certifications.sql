with base as (

    select
        _id as driver_id,
        jsonb_array_elements(certifications::jsonb) as cert_obj
    from {{ source('softsensor', 'drivers') }}

),

exploded as (

    select
        driver_id,
        cert_obj ->> 'type' as cert_type,
        jsonb_array_elements_text(cert_obj -> 'levels') as cert_level
    from base

)

select *
from exploded
