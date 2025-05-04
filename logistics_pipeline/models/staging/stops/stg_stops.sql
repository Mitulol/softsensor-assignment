with base as (

    select
        _id as stop_id,
        package_id,
        address
    from {{ source('softsensor', 'stops') }}

)

select * from base
