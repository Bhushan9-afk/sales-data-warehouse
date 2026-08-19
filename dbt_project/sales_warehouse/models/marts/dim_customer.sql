WITH all_customers AS (
    SELECT source_system, source_customer_id, customer_name, segment, country
    FROM {{ ref('stg_superstore') }}
    UNION ALL
    SELECT source_system, source_customer_id, customer_name, segment, country
    FROM {{ ref('stg_online_retail') }}
    UNION ALL
    SELECT source_system, source_customer_id, customer_name, segment, country
    FROM {{ ref('stg_adventureworks') }}
),

deduplicated AS (
    SELECT DISTINCT ON (source_system, source_customer_id)
        source_system,
        source_customer_id,
        customer_name,
        segment,
        country
    FROM all_customers
    WHERE source_customer_id IS NOT NULL
    ORDER BY source_system, source_customer_id
),

source_systems AS (
    SELECT DISTINCT source_system FROM all_customers
),

unknown_customers AS (
    SELECT 
        source_system,
        'unknown' AS source_customer_id,
        'Unknown Customer' AS customer_name,
        'Unknown' AS segment,
        NULL AS country
    FROM source_systems
),

with_unknown AS (
    SELECT * FROM deduplicated
    UNION ALL
    SELECT * FROM unknown_customers
),

final AS (
    SELECT
        ROW_NUMBER() OVER (ORDER BY source_system, source_customer_id) AS customer_key,
        source_system,
        source_customer_id,
        customer_name,
        segment,
        country
    FROM with_unknown
)

SELECT * FROM final
