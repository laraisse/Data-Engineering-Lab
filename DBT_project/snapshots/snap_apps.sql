{% snapshot snap_apps %}

{{
    config(
        target_schema='snapshots',
        unique_key='app_id',
        strategy='check',
        check_cols=['app_name', 'catalog_rating', 'installs', 'category_key', 'developer_key']
    )
}}

select
    app_id,
    app_name,
    catalog_rating,
    installs,
    category_key,
    developer_key
from {{ ref('dim_apps') }}

{% endsnapshot %}