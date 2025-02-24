/* 
  SQL query to extract fields from JSON string stored in the 
  `product_details` column of `purgo_playground.d_product_revenue` table 
*/

/**
 * This query extracts specific fields from the JSON structure stored in the 
 * `product_details` column. Each JSON field is extracted with the specified 
 * data types and aliases to ensure clarity in the output.
 */

SELECT 
  -- Extract JSON fields into individual columns for clarity and analysis
  from_json(product_details, 'struct<batch_number:string, expiration_date:string, manufacturing_site:string, regulatory_approval:string, price:double>') AS product_details_json,
  
  -- Extracting and aliasing each field for user-friendly column names
  product_details_json.batch_number AS batch_number,
  product_details_json.expiration_date AS expiration_date,
  product_details_json.manufacturing_site AS manufacturing_site,
  product_details_json.regulatory_approval AS regulatory_approval,
  product_details_json.price AS price
  
FROM 
  purgo_playground.d_product_revenue

WHERE 
  -- Data quality check: Validate the date format in the `expiration_date`
  try_to_date(product_details_json.expiration_date, 'yyyy-MM-dd') IS NOT NULL
 
  -- Null handling: Exclude entries with NULL `product_details`
  AND product_details IS NOT NULL;

