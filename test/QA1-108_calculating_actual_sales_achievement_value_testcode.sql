/* SQL query to calculate actual sales value for each brand by country and territory */

/* CTE to join sales data based on specified columns */
WITH SalesData AS (
  SELECT 
    itm.country_code,
    itm.brand_name,
    itm.territory_id,
    MONTH(itm.sales_month) AS sales_month,
    YEAR(itm.sales_month) AS sales_year,
    itm.sales_value,
    MONTH(ttm.fiscal_date) AS fiscal_month,
    YEAR(ttm.fiscal_date) AS fiscal_year,
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

/* Validating source_system existence in the control table and summing values */
SELECT 
  brand_name,
  country_code,
  territory_id,
  SUM(sales_value + sales_net_price_local) AS actual_value
FROM SalesData
WHERE source_system_name IN (SELECT source_system FROM purgo_playground.control_table)
GROUP BY brand_name, country_code, territory_id

/* Handling mismatched date records */
UNION ALL
SELECT
  brand_name,
  country_code,
  territory_id,
  NULL AS actual_value
FROM SalesData
WHERE sales_month != fiscal_month OR sales_year != fiscal_year

/* Excluding records with NULL fields */
UNION ALL
SELECT
  brand_name,
  country_code,
  territory_id,
  NULL AS actual_value
FROM SalesData
WHERE brand_name IS NULL OR country_code IS NULL 
   OR territory_id IS NULL OR source_system_name IS NULL

/* Example handling of special characters in brand names */
UNION ALL
SELECT
  'BrändNáme✦Special' AS brand_name,
  country_code,
  territory_id,
  SUM(sales_value + sales_net_price_local) AS actual_value
FROM SalesData
GROUP BY brand_name, country_code, territory_id

/* Filtering out records with exceptionally high calculated values to ensure data accuracy */
UNION ALL
SELECT
  brand_name,
  country_code,
  territory_id,
  CASE WHEN sales_value + sales_net_price_local > 1000000 THEN NULL ELSE sales_value + sales_net_price_local END AS actual_value
FROM SalesData
WHERE source_system_name IN (SELECT source_system FROM purgo_playground.control_table)
GROUP BY brand_name, country_code, territory_id
HAVING SUM(sales_value + sales_net_price_local) > 1000000


