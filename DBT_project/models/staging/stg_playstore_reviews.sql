with raw_reviews as (
    select *
    from read_json_auto('data/apps_reviews.jsonl')
)
select
    row_number() over ()         as surrogate_id,
    reviewId::varchar            as review_id,
    appId::varchar               as app_id,
    appName::varchar             as appName,
    userName::varchar            as user_name,
    score::integer               as rating,
    content::varchar             as review_text,
    thumbsUpCount::integer       as thumbsUpCount,
    "at"::timestamp              as review_date
from raw_reviews
where reviewId is not null