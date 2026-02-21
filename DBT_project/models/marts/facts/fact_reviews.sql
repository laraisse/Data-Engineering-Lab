with reviews as (
    select *
    from {{ ref('stg_playstore_reviews') }}
    where review_id is not null
),

-- Retrieve surrogate keys from dimensions using natural keys
joined as (
    select
        r.review_id,
        r.user_name,
        r.rating,
        r.review_text,
        r.review_date,

        -- App surrogate key (natural key: app_id)
        a.app_key,

        -- Developer surrogate key (via app dimension)
        a.developer_key,

        -- Date key in YYYYMMDD integer format (Kimball standard)
        cast(strftime(cast(r.review_date as date), '%Y%m%d') as integer) as date_key

    from reviews r

    -- Join to dim_apps on natural key
    left join {{ ref('dim_apps') }} a
        on r.app_id = a.app_id

    -- Join to dim_date on YYYYMMDD key
    left join {{ ref('dim_date') }} d
        on cast(strftime(cast(r.review_date as date), '%Y%m%d') as integer) = d.date_key
)

-- Filter out rows with missing foreign keys (referential integrity)
select
    md5(coalesce(review_id, ''))  as review_key,
    review_id,
    app_key,
    developer_key,
    date_key,
    user_name,
    rating,
    review_text
from joined
where
    app_key     is not null
    and date_key    is not null
    and developer_key is not null