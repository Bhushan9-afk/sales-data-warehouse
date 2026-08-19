WITH source AS (
    SELECT * FROM {{ source('raw', 'superstore_sales') }}
)

SELECT
    'superstore' AS source_system,
    CAST(row_id AS VARCHAR) AS source_line_id,
    order_id AS source_order_id,
    to_date(order_date, 'MM/DD/YYYY') AS order_date,
    customer_id AS source_customer_id,
    customer_name,
    segment,
    product_id AS source_product_id,
    product_name,
    category,
    sub_category AS subcategory,
    quantity,
    sales / NULLIF(quantity, 0) AS unit_price,
    COALESCE(discount, 0) AS discount,
    sales AS sales_amount,
    NULL::NUMERIC AS cost_amount,
    profit AS profit_amount,
    country,
    state,
    city,
    region
FROM source