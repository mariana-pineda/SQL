-- Corrected SQL code to select fields from the product_details JSON column in the d_product_revenue table in the purgo_playground catalog

SELECT 
  -- Extract each attribute from the JSON string and handle potential missing attributes
  COALESCE(get_json_object(product_details, "$.batch_number"), "Unknown") AS batch_number,
  COALESCE(get_json_object(product_details, "$.expiration_date"), "Unknown") AS expiration_date,
  COALESCE(get_json_object(product_details, "$.manufacturing_site"), "Unavailable") AS manufacturing_site,
  COALESCE(get_json_object(product_details, "$.regulatory_approval"), "Pending") AS regulatory_approval,
  COALESCE(CAST(get_json_object(product_details, "$.price") AS DOUBLE), 0.0) AS price
FROM 
  -- Specify the fully qualified table name in Unity Catalog
  purgo_playground.d_product_revenue;

-- Note: COALESCE is used to provide default values in case of null/unavailable JSON attributes
-- JSON attributes are accessed using the get_json_object function for strings and then cast for numbers
-- Ensure the Unity Catalog and Schema are accurate and have the correct access permissions
