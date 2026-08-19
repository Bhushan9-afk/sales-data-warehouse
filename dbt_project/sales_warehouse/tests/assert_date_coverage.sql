{{ config(severity='warn') }}

SELECT d.date_key
FROM {{ ref('dim_date') }} d
LEFT JOIN {{ ref('fact_sales') }} f ON d.date_key = f.date_key
WHERE f.date_key IS NULL
  AND d.full_date <= CURRENT_DATE
  