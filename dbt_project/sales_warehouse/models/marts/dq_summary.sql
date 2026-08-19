WITH fact_counts AS (
    SELECT 
        'fact_sales' AS table_name,
        COUNT(*) AS row_count,
        COUNT(DISTINCT source_system) AS source_count,
        MIN(d.full_date) AS min_date,
        MAX(d.full_date) AS max_date,
        SUM(sales_amount) AS total_sales,
        SUM(quantity) AS total_qty
    FROM {{ ref('fact_sales') }} f
    LEFT JOIN {{ ref('dim_date') }} d ON f.date_key = d.date_key
),

dim_checks AS (
    SELECT 'dim_customer' AS table_name, COUNT(*) AS row_count FROM {{ ref('dim_customer') }}
    UNION ALL
    SELECT 'dim_product', COUNT(*) FROM {{ ref('dim_product') }}
    UNION ALL
    SELECT 'dim_geography', COUNT(*) FROM {{ ref('dim_geography') }}
    UNION ALL
    SELECT 'dim_date', COUNT(*) FROM {{ ref('dim_date') }}
    UNION ALL
    SELECT 'dim_source', COUNT(*) FROM {{ ref('dim_source') }}
),

null_checks AS (
    SELECT 'fact_sales.customer_key' AS column_name, COUNT(*) AS null_count
    FROM {{ ref('fact_sales') }} WHERE customer_key IS NULL
    UNION ALL
    SELECT 'fact_sales.product_key', COUNT(*) FROM {{ ref('fact_sales') }} WHERE product_key IS NULL
    UNION ALL
    SELECT 'fact_sales.geography_key', COUNT(*) FROM {{ ref('fact_sales') }} WHERE geography_key IS NULL
    UNION ALL
    SELECT 'fact_sales.date_key', COUNT(*) FROM {{ ref('fact_sales') }} WHERE date_key IS NULL
    UNION ALL
    SELECT 'fact_sales.sales_amount', COUNT(*) FROM {{ ref('fact_sales') }} WHERE sales_amount IS NULL
),

dup_checks AS (
    SELECT 'dim_customer' AS table_name, COUNT(*) - COUNT(DISTINCT customer_key) AS dup_count FROM {{ ref('dim_customer') }}
    UNION ALL
    SELECT 'dim_product', COUNT(*) - COUNT(DISTINCT product_key) FROM {{ ref('dim_product') }}
    UNION ALL
    SELECT 'dim_geography', COUNT(*) - COUNT(DISTINCT geography_key) FROM {{ ref('dim_geography') }}
    UNION ALL
    SELECT 'dim_date', COUNT(*) - COUNT(DISTINCT date_key) FROM {{ ref('dim_date') }}
    UNION ALL
    SELECT 'fact_sales', COUNT(*) - COUNT(DISTINCT sales_key) FROM {{ ref('fact_sales') }}
)

SELECT * FROM fact_counts
UNION ALL
SELECT table_name, row_count, NULL, NULL, NULL, NULL, NULL FROM dim_checks
UNION ALL
SELECT 'null_' || column_name, null_count, NULL, NULL, NULL, NULL, NULL FROM null_checks
UNION ALL
SELECT 'dup_' || table_name, dup_count, NULL, NULL, NULL, NULL, NULL FROM dup_checks
