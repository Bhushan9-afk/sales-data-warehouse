WITH source AS (
    SELECT * FROM {{ source('raw', 'online_retail') }}
)

SELECT
    'online_retail' AS source_system,
    ROW_NUMBER() OVER (PARTITION BY invoice_no ORDER BY invoice_date) AS source_line_id,
    invoice_no AS source_order_id,
    CAST(invoice_date AS DATE) AS order_date,
    customer_id AS source_customer_id,
    NULL AS customer_name,
    NULL AS segment,
    stock_code AS source_product_id,
    description AS product_name,
    'Unknown' AS category,
    'Unknown' AS subcategory,
    quantity,
    unit_price,
    0 AS discount,
    quantity * unit_price AS sales_amount,
    NULL::NUMERIC AS cost_amount,
    NULL::NUMERIC AS profit_amount,
    country,
    NULL AS state,
    NULL AS city,
    NULL AS region
FROM source
WHERE quantity > 0
  AND unit_price > 0