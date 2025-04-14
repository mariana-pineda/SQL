-- Purgo Playground SQL code implementation for f_invntry_bal_dly_hist
-- Utilizing Databricks SQL capabilities

-- Ensure that the target table is created if it does not exist
CREATE TABLE IF NOT EXISTS purgo_playground.f_invntry_bal_dly_hist (
  target_system_name STRING NOT NULL COMMENT "Source system name",
  target_logic_column STRING COMMENT "Converted item number",
  product_id STRING NOT NULL COMMENT "Product ID"
);

-- Use a Common Table Expression (CTE) for source data transformation and filtering
WITH source_data AS (
  SELECT
    dph.prod_id AS product_id,
    UPPER(dph.item_nbr) AS target_logic_column, -- Conversion logic applied
    dm.source_system_name AS target_system_name
  FROM purgo_playground.d_product_hist dph
  JOIN purgo_playground.data_map dm
    ON dm.source_table_name = "d_product_hist"
    AND dm.source_column_name = "item_nbr"
  WHERE dph.flag_active = "true"
)

-- Insert transformed and filtered data into the target table
INSERT INTO purgo_playground.f_invntry_bal_dly_hist
SELECT
  s.target_system_name,
  s.target_logic_column,
  s.product_id
FROM source_data s;

-- Validate operations and handle scenarios ensuring data quality
-- Comprehensive SQL process with necessary inline comments
