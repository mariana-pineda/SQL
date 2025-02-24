-- SQL query to extract fields from the JSON column `product_details` in the `purgo_playground.d_product_revenue` table
SELECT 
  -- Extracting JSON fields and aliasing them with appropriate names
  from_json(product_details, 
    'struct<batch_number:string, expiration_date:string, manufacturing_site:string, regulatory_approval:string, price:double>'
  ) AS product_details_json,
  
  -- Extracting each individual field from the JSON
  product_details_json.batch_number AS batch_number,
  product_details_json.expiration_date AS expiration_date,
  product_details_json.manufacturing_site AS manufacturing_site,
  product_details_json.regulatory_approval AS regulatory_approval,
  product_details_json.price AS price
  
FROM 
  purgo_playground.d_product_revenue

-- Validating JSON extraction by comparing with expected data types
WHERE 
  -- Check for valid expiration_date by ensuring it follows the expected date format
  try_to_date(product_details_json.expiration_date, 'yyyy-MM-dd') IS NOT NULL
  OR
  -- Error handling for invalid JSON formats
  product_details IS NULL

