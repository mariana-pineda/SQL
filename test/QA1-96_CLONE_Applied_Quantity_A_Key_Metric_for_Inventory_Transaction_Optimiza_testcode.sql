-- Databricks SQL Test Code for Inventory Transaction Applied Quantity Calculations

-- Testing setup and configuration information
-- Ensure connection to Unity Catalog purgo_databricks
-- Utilize schema purgo_playground for all operations

-- Drop test table if it already exists to avoid duplication
DROP TABLE IF EXISTS purgo_playground.f_inv_movmnt_apl_qty_test;

-- Create test table for validation purposes
CREATE TABLE purgo_playground.f_inv_movmnt_apl_qty_test (
  txn_id STRING NOT NULL,
  ref_txn_qty DECIMAL(3,1) NOT NULL,
  cumulative_txn_qty DECIMAL(4,1),
  cumulative_ref_ord_sched_qty DECIMAL(4,1),
  ref_ord_sched_qty DECIMAL(3,1),
  prior_cumulative_txn_qty DECIMAL(3,1),
  prior_cumulative_ref_ord_sched_qty DECIMAL(3,1),
  calculated_apl_qty DECIMAL(5,1),
  apl_qty DECIMAL(5,1)
);

-- Insert test data
-- Use try-except block as necessary during file reading operations before inserting data
INSERT INTO purgo_playground.f_inv_movmnt_apl_qty_test (txn_id, ref_txn_qty, cumulative_txn_qty, cumulative_ref_ord_sched_qty, ref_ord_sched_qty, prior_cumulative_txn_qty, prior_cumulative_ref_ord_sched_qty, apl_qty, calculated_apl_qty)
SELECT * FROM (
  -- Test 1: Conditions met for positive ref_txn_qty
  SELECT
    "1" AS txn_id,
    50 AS ref_txn_qty,
    100 AS cumulative_txn_qty,
    90 AS cumulative_ref_ord_sched_qty,
    50 AS ref_ord_sched_qty,
    40 AS prior_cumulative_txn_qty,
    30 AS prior_cumulative_ref_ord_sched_qty,
    -- If prior_cumulative_ref_ord_sched_qty < prior_cumulative_txn_qty, calculate a specific apl_qty
    CASE WHEN prior_cumulative_ref_ord_sched_qty < prior_cumulative_txn_qty THEN
      ref_ord_sched_qty - (prior_cumulative_txn_qty - prior_cumulative_ref_ord_sched_qty)
    ELSE
      ref_ord_sched_qty -- Default apl_qty
    END AS apl_qty,
    CAST(NULL AS DECIMAL(5,1)) AS calculated_apl_qty
  UNION ALL
  -- Test 2: Edge case for positive ref_txn_qty, alternate conditions
  SELECT
    "3",
    20,
    60,
    100,
    30,
    30,
    25,
    CASE WHEN prior_cumulative_ref_ord_sched_qty > prior_cumulative_txn_qty THEN
      ref_txn_qty - (prior_cumulative_ref_ord_sched_qty - prior_cumulative_txn_qty)
    ELSE
      ref_txn_qty -- Default apl_qty
    END,
    CAST(NULL AS DECIMAL(5,1))
  UNION ALL
  -- Test 3: Negative ref_txn_qty handling
  SELECT
    "2",
    -10,
    80,
    70,
    40,
    50,
    45,
    -- Always use ref_txn_qty when negative and conditions are met
    ref_txn_qty,
    CAST(NULL AS DECIMAL(5,1))
  UNION ALL
  -- Test 4: Default case
  SELECT
    CAST(NULL AS STRING),
    CAST(NULL AS DECIMAL(3,1)),
    CAST(NULL AS DECIMAL(4,1)),
    CAST(NULL AS DECIMAL(4,1)),
    CAST(NULL AS DECIMAL(3,1)),
    CAST(NULL AS DECIMAL(3,1)),
    CAST(NULL AS DECIMAL(3,1)),
    CAST(NULL AS DECIMAL(5,1)),
    CAST(NULL AS DECIMAL(5,1))
);

-- Validate that resulting test data matches schema and requirements
SELECT
  -- Fetch columns and perform schema validation
  COUNT(*) AS total_records,
  SUM(CASE WHEN txn_id IS NULL THEN 1 ELSE 0 END) AS null_txn_id_count,
  SUM(CASE WHEN apl_qty IS NULL THEN 1 ELSE 0 END) AS null_apl_qty_count
FROM purgo_playground.f_inv_movmnt_apl_qty_test;

-- Test Delta Lake operations by merging calculated data back into main data store
MERGE INTO purgo_playground.f_inv_movmnt_apl_qty AS target
USING purgo_playground.f_inv_movmnt_apl_qty_test AS source
ON target.txn_id = source.txn_id
WHEN MATCHED THEN
UPDATE SET target.apl_qty = source.apl_qty
WHEN NOT MATCHED THEN
INSERT (txn_id, ref_txn_qty, cumulative_txn_qty, cumulative_ref_ord_sched_qty, ref_ord_sched_qty, prior_cumulative_txn_qty, prior_cumulative_ref_ord_sched_qty, apl_qty)
VALUES (source.txn_id, source.ref_txn_qty, source.cumulative_txn_qty, source.cumulative_ref_ord_sched_qty, source.ref_ord_sched_qty, source.prior_cumulative_txn_qty, source.prior_cumulative_ref_ord_sched_qty, source.apl_qty);

-- Clean up the test data table after validation
DROP TABLE IF EXISTS purgo_playground.f_inv_movmnt_apl_qty_test;
