with source as (
    select distinct
        developer_name
    from {{ ref('stg_playstore_apps') }}
    where developer_name is not null
)
select
    md5(coalesce(developer_name, '')) as developer_key,
    developer_name
from source