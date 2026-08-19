WITH source AS (
    SELECT * FROM {{ source('raw', 'adventureworks_sales') }}
)

SELECT
    'adventureworks' AS source_system,
    CAST(orderlineitem AS VARCHAR) AS source_line_id,
    ordernumber AS source_order_id,
    CAST(orderdate AS DATE) AS order_date,
    CAST(customerkey AS VARCHAR) AS source_customer_id,
    firstname || ' ' || lastname AS customer_name,
    occupation AS segment,
    CAST(productkey AS VARCHAR) AS source_product_id,
    productname AS product_name,
    categoryname AS category,
    subcategoryname AS subcategory,
    orderquantity AS quantity,
    productprice AS unit_price,
    0 AS discount,
    orderquantity * productprice AS sales_amount,
    orderquantity * productcost AS cost_amount,
    (orderquantity * productprice) - (orderquantity * productcost) AS profit_amount,
    country,
    NULL AS state,
    NULL AS city,
    region
FROM source
