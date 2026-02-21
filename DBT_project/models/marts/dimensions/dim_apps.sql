with source as (
    select distinct
        app_id,
        title,
        genre,
        installs,
        ratings,
        developer_name
    from {{ ref('stg_playstore_apps') }}
    where app_id is not null
),

with_keys as (
    select
        s.app_id,
        s.title          as app_name,
        s.installs,
        s.ratings        as catalog_rating,
        c.category_key,
        d.developer_key
    from source s
    left join {{ ref('dim_categories') }} c
        on s.genre = c.category_name
    left join {{ ref('dim_developers') }} d
        on s.developer_name = d.developer_name
)

select
    md5(coalesce(app_id, '')) as app_key,
    app_id,
    app_name,
    catalog_rating,
    installs,
    category_key,
    developer_key
from with_keys