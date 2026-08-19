SELECT 
    c.segment,
    c.source_system,
    COUNT(DISTINCT c.customer_key) AS customer_count,
    SUM(f.sales_amount) AS total_sales,
    SUM(f.sales_amount) / COUNT(DISTINCT c.customer_key) AS avg_sales_per_customer
FROM {{ ref('fact_sales') }} f
JOIN {{ ref('dim_customer') }} c ON f.customer_key = c.customer_key
WHERE c.source_customer_id != 'unknown'
GROUP BY c.segment, c.source_system
ORDER BY total_sales DESC