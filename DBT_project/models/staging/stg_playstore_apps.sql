with raw_apps as (
    select *
    from read_json_auto('data/apps_metadata.jsonl')
)
select
    row_number() over ()     as surrogate_id,
    appId::varchar           as app_id,
    title::varchar           as title,
    score::varchar           as score,
    realInstalls::BIGINT    as installs,
    ratings::double          as ratings,
    price::float             as price,
    developer::varchar       as developer_name,
    genre::varchar           as genre
from raw_apps
where appId is not null