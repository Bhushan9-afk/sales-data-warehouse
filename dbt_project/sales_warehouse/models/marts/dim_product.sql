WITH all_products AS (
    SELECT source_system, source_product_id, product_name, category, subcategory
    FROM {{ ref('stg_superstore') }}
    UNION ALL
    SELECT source_system, source_product_id, product_name, category, subcategory
    FROM {{ ref('stg_online_retail') }}
    UNION ALL
    SELECT source_system, source_product_id, product_name, category, subcategory
    FROM {{ ref('stg_adventureworks') }}
),

deduplicated AS (
    SELECT DISTINCT ON (source_system, source_product_id)
        source_system,
        source_product_id,
        product_name,
        category,
        subcategory
    FROM all_products
    ORDER BY source_system, source_product_id
)

SELECT
    ROW_NUMBER() OVER (ORDER BY source_system, source_product_id) AS product_key,
    source_system,
    source_product_id,
    product_name,
    category,
    subcategory
FROM deduplicated