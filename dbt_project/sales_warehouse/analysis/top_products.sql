SELECT 
    p.product_name,
    p.category,
    p.subcategory,
    SUM(f.sales_amount) AS total_sales,
    SUM(f.quantity) AS total_qty,
    COUNT(*) AS transaction_count
FROM {{ ref('fact_sales') }} f
JOIN {{ ref('dim_product') }} p ON f.product_key = p.product_key
GROUP BY p.product_name, p.category, p.subcategory
ORDER BY total_sales DESC
LIMIT 20