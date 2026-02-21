{{ config(materialized='table') }}

select
    md5(coalesce(app_id, '') || coalesce(cast(dbt_valid_from as varchar), '')) as app_scd_key,
    app_id,
    app_name,
    catalog_rating,
    installs,
    category_key,
    developer_key,

    dbt_valid_from  as valid_from,
    dbt_valid_to    as valid_to,

    case when dbt_valid_to is null then true else false end as is_current

from {{ ref('snap_apps') }}