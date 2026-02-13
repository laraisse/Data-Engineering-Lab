SELECT
    {{ dbt_utils.generate_surrogate_key(['reviewId']) }} as review_key,
    reviewId as review_id,
    appId as app_id,
    appName as app_name,
    userName as user_name,
    CAST(score AS INTEGER) as rating_score,
    content as review_text,
    CAST(thumbsUpCount AS INTEGER) as thumbs_up_count,
    CAST(at AS TIMESTAMP) as review_timestamp,
    CAST(at AS DATE) as review_date
FROM read_json_auto('../data/raw/apps_reviews.json')
WHERE reviewId IS NOT NULL