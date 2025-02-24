/* SQL query to extract fields from the JSON column 'product_details' in the 'purgo_playground.d_product_revenue' table */

/**
 * Description: This query extracts specific fields from the JSON string stored in the 
 * `product_details` column of `purgo_playground.d_product_revenue` table. Each JSON field is 
 * extracted and aliased for clarity, ensuring correct data types as well.
 */
SELECT 
  -- Extracting each field from the JSON and aliasing them with user-friendly names
  from_json(product_details, 
    'struct<batch_number:string, expiration_date:string, manufacturing_site:string, regulatory_approval:string, price:double>'
  ) AS product_details_json,
  
  -- Extract JSON fields into individual columns
  product_details_json.batch_number AS batch_number,
  product_details_json.expiration_date AS expiration_date,
  product_details_json.manufacturing_site AS manufacturing_site,
  product_details_json.regulatory_approval AS regulatory_approval,
  product_details_json.price AS price
  
FROM 
  purgo_playground.d_product_revenue

WHERE 
  -- Check for valid expiration_date by ensuring it follows the expected date format
  try_to_date(product_details_json.expiration_date, 'yyyy-MM-dd') IS NOT NULL

  -- Null handling: If product_details is NULL, ensure it's excluded from results
  OR product_details IS NULL;
