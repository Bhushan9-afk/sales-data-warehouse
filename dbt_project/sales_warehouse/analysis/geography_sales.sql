SELECT 
    g.country,
    g.state,
    g.city,
    g.region,
    SUM(f.sales_amount) AS total_sales,
    SUM(f.quantity) AS total_qty,
    COUNT(DISTINCT f.customer_key) AS customer_count
FROM {{ ref('fact_sales') }} f
JOIN {{ ref('dim_geography') }} g ON f.geography_key = g.geography_key
GROUP BY g.country, g.state, g.city, g.region
ORDER BY total_sales DESC