SELECT *
FROM {{ ref('fact_sales') }}
WHERE sales_amount < 0