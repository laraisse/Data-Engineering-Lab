with date_bounds as (
    select
        cast(min(review_date) as date) as min_date,
        cast(max(review_date) as date) as max_date
    from {{ ref('stg_playstore_reviews') }}
),

    date_spine as (
    select
        unnest(
            generate_series(
                (select min_date from date_bounds),
                (select max_date from date_bounds),
                interval '1 day'
            )
        )::date as date_day
)

select
    cast(strftime(date_day, '%Y%m%d') as integer)   as date_key,
    date_day                                          as date,
    year(date_day)                                    as year,
    month(date_day)                                   as month,
    quarter(date_day)                                 as quarter,
    dayofweek(date_day)                               as day_of_week,
    case when dayofweek(date_day) in (0, 6)
         then true else false end                     as is_weekend
from date_spine
order by date_day