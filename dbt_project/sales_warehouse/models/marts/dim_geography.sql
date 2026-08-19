WITH all_locations AS (
    SELECT country, state, city, region
    FROM {{ ref('stg_superstore') }}
    UNION ALL
    SELECT country, state, city, region
    FROM {{ ref('stg_online_retail') }}
    UNION ALL
    SELECT country, state, city, region
    FROM {{ ref('stg_adventureworks') }}
),

deduplicated AS (
    SELECT DISTINCT ON (country, state, city, region)
        country,
        state,
        city,
        region
    FROM all_locations
    ORDER BY country, state, city, region
)

SELECT
    ROW_NUMBER() OVER (ORDER BY country, region, state, city) AS geography_key,
    country,
    state,
    city,
    region
FROM deduplicated