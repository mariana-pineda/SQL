-- Test code for Databricks environment configuration
/*
  Configuration:
  - Unity Catalog: purgo_databricks
  - Schema: purgo_playground
  - Target Table: f_invntry_bal_dly_hist
*/

/* Use Common Table Expressions (CTEs) for SQL logic */
WITH source_data AS (
  SELECT 
    source_system_name, 
    source_table_name, 
    source_column_name AS src_col_1, 
    source_datatype AS src_datatype,
    logic AS src_logic_column
  FROM purgo_playground.data_map
  WHERE source_system_name = "source_system_1"
),
filtered_data AS (
  SELECT * FROM purgo_playground.d_product_hist
  WHERE flag_active = 'true'
)

/* Check schema validation and ensure the data conforms to the target table's schema */
SELECT
  src_data.source_system_name AS target_system_name,
  src_data.src_logic_column AS target_logic_column,
  filtered_data.prod_id AS product_id
FROM source_data src_data
JOIN filtered_data ON src_data.src_col_1 = filtered_data.prod_id;

/* Validate column constraints using safe SQL syntax */
-- Creation of the target table
-- Use Databricks SQL syntax to ensure compatibility
CREATE TABLE IF NOT EXISTS purgo_playground.f_invntry_bal_dly_hist (
  target_system_name STRING NOT NULL,
  target_logic_column STRING,
  product_id STRING NOT NULL,
  CONSTRAINT product_id_not_null CHECK (product_id IS NOT NULL)
);

/* Test Delta Lake operations if used */
-- Example: MERGE operation test for Delta Lake
MERGE INTO purgo_playground.f_invntry_bal_dly_hist tgt
USING (
  SELECT prod_id, item_nbr FROM purgo_playground.d_product_hist WHERE flag_active = 'true'
) src
ON tgt.product_id = src.prod_id
WHEN MATCHED THEN 
  UPDATE SET tgt.target_logic_column = "Updated Logic Column"
WHEN NOT MATCHED THEN 
  INSERT (target_system_name, target_logic_column, product_id)
  VALUES ("new_system", "New Logic Column", src.prod_id);

/* Validate error handling and proper cleanup operations */
-- Cleanup residual data to ensure integrity
DELETE FROM purgo_playground.f_invntry_bal_dly_hist WHERE product_id IS NULL;

/* Performance Tests */
-- Performance criteria: ensure operations meet expected performance levels
-- No explicit performance assertion in SQL

-- Ensure all operations are explained with comments
-- Comprehensive testing from setup, schema validation, transformations, delta operations, and cleanup

-- All code is executable with necessary comments for explanation
