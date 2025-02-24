/*
 * SQL query to extract fields from the JSON column 'product_details'
 * in the 'purgo_playground.d_product_revenue' table.
 * This query selects JSON fields, ensuring correct data types and aliases.
 */

SELECT 
  -- Original product information
  product_id,
  product_name,
  product_type,
  revenue,
  country,
  customer_id,
  purchased_date,
  invoice_date,
  invoice_number,
  is_returned,
  customer_satisfaction_score,
  customer_first_purchased_date,
  customer_first_product,
  customer_first_revenue,

  -- Extracting JSON fields into separate columns
  product_details_json.batch_number AS batch_number,
  try_to_date(product_details_json.expiration_date, 'yyyy-MM-dd') AS expiration_date,
  product_details_json.manufacturing_site AS manufacturing_site,
  product_details_json.regulatory_approval AS regulatory_approval,
  CAST(product_details_json.price AS DECIMAL(10,2)) AS price

FROM (
  SELECT *,
    -- Convert JSON string to struct to facilitate field extraction
    from_json(product_details, 
      'struct<batch_number:string, expiration_date:string, manufacturing_site:string, regulatory_approval:string, price:double>'
    ) AS product_details_json
  FROM purgo_playground.d_product_revenue
) AS derived_table

WHERE 
  -- Filter rows where JSON was parsed successfully and expiration_date is valid
  product_details_json IS NOT NULL
  AND try_to_date(product_details_json.expiration_date, 'yyyy-MM-dd') IS NOT NULL;

