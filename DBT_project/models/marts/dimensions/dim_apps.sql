with source as (
    select distinct
        app_id,
        name,
        category,
        installs,
        rating,
        developer_name
    from {{ ref('stg_playstore_apps') }}
    where app_id is not null
),

-- Join category and developer keys to build the hierarchy
with_keys as (
    select
        s.app_id,
        s.name                                                          as app_name,
        s.installs,
        s.rating                                                        as catalog_rating,
        c.category_key,
        d.developer_key
    from source s
    left join {{ ref('dim_categories') }} c
        on s.category = c.category_name
    left join {{ ref('dim_developers') }} d
        on s.developer_name = d.developer_name
)

select
    {{ dbt_utils.generate_surrogate_key(['app_id']) }} as app_key,
    app_id,
    app_name,
    catalog_rating,
    installs,
    category_key,
    developer_key
from with_keys