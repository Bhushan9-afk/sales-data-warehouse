{{ config(
    materialized='incremental',
    unique_key='sales_key',
    on_schema_change='sync_all_columns'
) }}

WITH all_sales AS (
    SELECT
        source_system,
        source_line_id::VARCHAR AS source_line_id,
        source_order_id,
        order_date,
        COALESCE(NULLIF(source_customer_id, ''), 'unknown') AS source_customer_id,
        customer_name,
        segment,
        source_product_id,
        product_name,
        category,
        subcategory,
        quantity,
        unit_price,
        discount,
        sales_amount,
        cost_amount,
        profit_amount,
        country,
        state,
        city,
        region
    FROM {{ ref('stg_superstore') }}
    UNION ALL
    SELECT
        source_system,
        source_line_id::VARCHAR AS source_line_id,
        source_order_id,
        order_date,
        COALESCE(NULLIF(source_customer_id, ''), 'unknown') AS source_customer_id,
        customer_name,
        segment,
        source_product_id,
        product_name,
        category,
        subcategory,
        quantity,
        unit_price,
        discount,
        sales_amount,
        cost_amount,
        profit_amount,
        country,
        state,
        city,
        region
    FROM {{ ref('stg_online_retail') }}
    UNION ALL
    SELECT
        source_system,
        source_line_id::VARCHAR AS source_line_id,
        source_order_id,
        order_date,
        COALESCE(NULLIF(source_customer_id, ''), 'unknown') AS source_customer_id,
        customer_name,
        segment,
        source_product_id,
        product_name,
        category,
        subcategory,
        quantity,
        unit_price,
        discount,
        sales_amount,
        cost_amount,
        profit_amount,
        country,
        state,
        city,
        region
    FROM {{ ref('stg_adventureworks') }}
),

final AS (
    SELECT
        ROW_NUMBER() OVER (ORDER BY s.source_system, s.source_order_id, s.source_line_id) AS sales_key,
        s.source_system,
        s.source_order_id,
        s.source_line_id,
        CAST(TO_CHAR(s.order_date, 'YYYYMMDD') AS INTEGER) AS date_key,
        c.customer_key,
        p.product_key,
        g.geography_key,
        src.source_key,
        s.quantity,
        s.unit_price,
        s.discount,
        s.sales_amount,
        s.cost_amount,
        s.profit_amount
    FROM all_sales s
    LEFT JOIN {{ ref('dim_customer') }} c
        ON s.source_system = c.source_system AND s.source_customer_id = c.source_customer_id
    LEFT JOIN {{ ref('dim_product') }} p
        ON s.source_system = p.source_system AND s.source_product_id = p.source_product_id
    LEFT JOIN {{ ref('dim_geography') }} g
        ON COALESCE(s.country, '') = COALESCE(g.country, '')
        AND COALESCE(s.state, '') = COALESCE(g.state, '')
        AND COALESCE(s.city, '') = COALESCE(g.city, '')
        AND COALESCE(s.region, '') = COALESCE(g.region, '')
    LEFT JOIN {{ ref('dim_source') }} src
        ON s.source_system = src.source_system
    {% if is_incremental() %}
    LEFT JOIN {{ this }} existing
        ON s.source_system = existing.source_system
        AND s.source_order_id = existing.source_order_id
        AND s.source_line_id = existing.source_line_id
    WHERE existing.sales_key IS NULL
    {% endif %}
)

SELECT * FROM final
