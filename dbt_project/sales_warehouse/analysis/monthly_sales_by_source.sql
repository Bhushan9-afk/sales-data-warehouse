SELECT 
    d.year,
    d.month,
    d.month_name,
    f.source_system,
    SUM(f.sales_amount) AS total_sales,
    SUM(f.quantity) AS total_qty,
    COUNT(DISTINCT f.source_order_id) AS order_count
FROM {{ ref('fact_sales') }} f
JOIN {{ ref('dim_date') }} d ON f.date_key = d.date_key
JOIN {{ ref('dim_source') }} s ON f.source_key = s.source_key
GROUP BY d.year, d.month, d.month_name, f.source_system
ORDER BY d.year, d.month, f.source_system