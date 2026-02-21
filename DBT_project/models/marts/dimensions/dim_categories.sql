with source as (
    select distinct
        category
    from {{ ref('stg_playstore_apps') }}
    where category is not null
)
select
    {{ dbt_utils.generate_surrogate_key(['category']) }} as category_key,
    category                                             as category_name
from source