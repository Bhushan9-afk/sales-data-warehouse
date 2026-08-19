SELECT 
    d.year,
    SUM(f.sales_amount) AS total_sales,
    LAG(SUM(f.sales_amount)) OVER (ORDER BY d.year) AS prev_year_sales,
    CASE 
        WHEN LAG(SUM(f.sales_amount)) OVER (ORDER BY d.year) IS NOT NULL 
        THEN ROUND(
            (SUM(f.sales_amount) - LAG(SUM(f.sales_amount)) OVER (ORDER BY d.year)) 
            / LAG(SUM(f.sales_amount)) OVER (ORDER BY d.year) * 100, 2
        )
    END AS yoy_growth_pct
FROM {{ ref('fact_sales') }} f
JOIN {{ ref('dim_date') }} d ON f.date_key = d.date_key
GROUP BY d.year
ORDER BY d.year