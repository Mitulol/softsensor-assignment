with base as (

    select
        _id as driver_id,
        name as driver_name,
        license::jsonb ->> 'class' as license_class,
        (license::jsonb ->> 'expiry')::date as license_expiry
    from {{ source('softsensor', 'drivers') }}

)

select *
from base
