with source as (
    select distinct
        developer_name
    from {{ ref('stg_playstore_apps') }}
    where developer_name is not null
)
select
    {{ dbt_utils.generate_surrogate_key(['developer_name']) }} as developer_key,
    developer_name
from source