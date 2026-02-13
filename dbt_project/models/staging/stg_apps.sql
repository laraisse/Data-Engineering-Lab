SELECT
    appId as app_id,
    title as app_name,
    developer,
    genre as category,
    score as app_score,
    ratings as total_ratings,
    installs,
    price
FROM read_json_auto('../data/raw/apps_metadata.json')
WHERE appId IS NOT NULL