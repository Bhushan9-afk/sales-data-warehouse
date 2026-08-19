WITH date_spine AS (
    SELECT generate_series(
        '2010-01-01'::DATE,
        '2022-12-31'::DATE,
        '1 day'::INTERVAL
    )::DATE AS full_date
)

SELECT
    CAST(TO_CHAR(full_date, 'YYYYMMDD') AS INTEGER) AS date_key,
    full_date,
    EXTRACT(YEAR FROM full_date)::INTEGER AS year,
    EXTRACT(QUARTER FROM full_date)::INTEGER AS quarter,
    EXTRACT(MONTH FROM full_date)::INTEGER AS month,
    TO_CHAR(full_date, 'Month') AS month_name,
    EXTRACT(DAY FROM full_date)::INTEGER AS day,
    TO_CHAR(full_date, 'Day') AS day_of_week,
    CASE WHEN EXTRACT(ISODOW FROM full_date) IN (6, 7) THEN TRUE ELSE FALSE END AS is_weekend
FROM date_spine