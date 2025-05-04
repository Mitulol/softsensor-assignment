with base as (

    select
        _id as zone_id,
        boundaries::jsonb as boundary_rings
    from {{ source('softsensor', 'zones') }}

),

rings as (

    select
        zone_id,
        ring_element as ring,
        ring_number
    from base,
    jsonb_array_elements(boundary_rings) with ordinality as ring(ring_element, ring_number)

),

points as (

    select
        zone_id,
        ring_number,
        point_number,
        (point ->> 'lat')::numeric as latitude,
        (point ->> 'lng')::numeric as longitude
    from rings,
    jsonb_array_elements(ring) with ordinality as point(point, point_number)

)

select
    zone_id,
    ring_number,
    point_number,
    latitude,
    longitude
from points
