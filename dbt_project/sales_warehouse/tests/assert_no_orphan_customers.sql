SELECT c.customer_key
FROM {{ ref('dim_customer') }} c
LEFT JOIN {{ ref('fact_sales') }} f ON c.customer_key = f.customer_key
WHERE f.customer_key IS NULL
  AND c.source_customer_id != 'unknown'
  