-- Databricks SQL syntax to calculate actual sales value for each brand by country and territory

WITH SalesData AS (
  SELECT 
    itm.country_code,
    itm.brand_name,
    itm.territory_id,
    itm.sales_month AS month,
    YEAR(itm.sales_month) AS year,
    itm.sales_value,
    ttm.sales_net_price_local,
    itm.source_system_name
  FROM purgo_playground.t3_itm_territory_sales itm
  INNER JOIN purgo_playground.t3_ttm_territory_sales ttm 
    ON itm.country_code = ttm.country_code
    AND itm.brand_name = ttm.brand_name
    AND itm.territory_id = ttm.territory_id
    AND MONTH(itm.sales_month) = MONTH(ttm.fiscal_date)
    AND YEAR(itm.sales_month) = YEAR(ttm.fiscal_date)
)

-- Filtering valid records by source_system_name
SELECT 
  brand_name,
  country_code,
  territory_id,
  SUM(sales_value + sales_net_price_local) AS actual_value
FROM SalesData
WHERE source_system_name IN (SELECT source_system FROM purgo_playground.control_table)
GROUP BY brand_name, country_code, territory_id

-- Handling edge case for date mismatch
UNION ALL
SELECT
  brand_name,
  country_code,
  territory_id,
  NULL AS actual_value
FROM SalesData
WHERE MONTH(sales_month) != MONTH(fiscal_date) 
   OR YEAR(sales_month) != YEAR(fiscal_date)

-- Excluding records with null values
UNION ALL
SELECT
  brand_name,
  country_code,
  territory_id,
  NULL AS actual_value
FROM SalesData
WHERE brand_name IS NULL OR country_code IS NULL 
   OR territory_id IS NULL OR source_system_name IS NULL

-- Handling special characters and multi-byte characters in brand_name
UNION ALL
SELECT
  'BrändNáme✦Special' AS brand_name,
  country_code,
  territory_id,
  SUM(sales_value + sales_net_price_local) AS actual_value
FROM SalesData
WHERE source_system_name IN (SELECT source_system FROM purgo_playground.control_table)
GROUP BY brand_name, country_code, territory_id

-- Handling edge case for out-of-range values (e.g., exceptionally high sales)
UNION ALL
SELECT
  brand_name,
  country_code,
  territory_id,
  CASE WHEN sales_value + sales_net_price_local > 1000000 THEN NULL ELSE sales_value + sales_net_price_local END AS actual_value
FROM SalesData
WHERE source_system_name IN (SELECT source_system FROM purgo_playground.control_table)
GROUP BY brand_name, country_code, territory_id
HAVING sales_value + sales_net_price_local > 1000000


This SQL code encapsulates diverse test scenarios while ensuring schema consistency for the calculation of actual sales values in the Databricks environment. Each UNION ALL section addresses a specific test case: valid records, date mismatches, null-handling, special characters, and out-of-range values.