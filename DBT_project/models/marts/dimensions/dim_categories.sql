with source as (
    select distinct
        genre
    from {{ ref('stg_playstore_apps') }}
    where genre is not null
)
select
    md5(coalesce(genre, '')) as category_key,
    genre                                             as category_name
from source