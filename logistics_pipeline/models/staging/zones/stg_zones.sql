with base as (

    select
        _id as zone_id,
        name as zone_name
    from {{ source('softsensor', 'zones') }}

)

select * from base
