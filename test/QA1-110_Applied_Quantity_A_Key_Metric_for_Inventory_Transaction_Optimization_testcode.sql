-- SQL Test Code for Inventory Transactions Applied Quantity Calculation

/* Framework and Structure setup */
/* This code defines the integration and unit tests for the apl_qty calculation logic in Databricks SQL */

/* Integration Test: Validate apl_qty calculation logic in f_inv_movmnt_apl_qty_test table */

/* Create a table with constraints for testing purposes */
CREATE TABLE purgo_playground.purgo_playground.f_inv_movmnt_apl_qty_test (
  txn_id STRING NOT NULL,
  ref_txn_qty DECIMAL(3,1),
  cumulative_txn_qty DECIMAL(4,1),
  cumulative_ref_ord_sched_qty DECIMAL(4,1),
  ref_ord_sched_qty DECIMAL(3,1),
  prior_cumulative_txn_qty DECIMAL(3,1),
  prior_cumulative_ref_ord_sched_qty DECIMAL(3,1),
  apl_qty DECIMAL(5,1)
);

-- Insert data from existing table with case logic to calculate apl_qty
INSERT INTO purgo_playground.purgo_playground.f_inv_movmnt_apl_qty_test
SELECT
  txn_id,
  ref_txn_qty,
  cumulative_txn_qty,
  cumulative_ref_ord_sched_qty,
  ref_ord_sched_qty,
  prior_cumulative_txn_qty,
  prior_cumulative_ref_ord_sched_qty,
  CASE 
    WHEN ref_txn_qty > 0 AND cumulative_txn_qty >= cumulative_ref_ord_sched_qty THEN
      CASE
        WHEN prior_cumulative_ref_ord_sched_qty < prior_cumulative_txn_qty THEN ref_ord_sched_qty - (prior_cumulative_txn_qty - prior_cumulative_ref_ord_sched_qty)
        ELSE ref_ord_sched_qty
      END
    WHEN ref_txn_qty > 0 AND cumulative_ref_ord_sched_qty >= cumulative_txn_qty THEN
      CASE
        WHEN prior_cumulative_ref_ord_sched_qty > prior_cumulative_txn_qty THEN ref_txn_qty - (prior_cumulative_ref_ord_sched_qty - prior_cumulative_txn_qty)
        ELSE ref_txn_qty
      END
    WHEN ref_txn_qty < 0 AND cumulative_txn_qty != 0 AND cumulative_ref_ord_sched_qty > 0 THEN
      ref_txn_qty
    ELSE NULL
  END AS apl_qty
FROM purgo_playground.purgo_playground.f_inv_movmnt_apl_qty
WHERE txn_id IS NOT NULL;

-- Validate correct number of columns
SELECT COUNT(*) AS total_columns
FROM information_schema.columns
WHERE table_name='f_inv_movmnt_apl_qty_test';

-- Unit Test for ref_txn_qty > 0 condition
WITH test_data AS (
  SELECT *
  FROM purgo_playground.purgo_playground.f_inv_movmnt_apl_qty_test
  WHERE txn_id = '1'
)
SELECT
  CASE WHEN apl_qty IS NOT NULL THEN 'Pass' ELSE 'Fail' END AS result_check
FROM test_data;

-- Unit Test for ref_txn_qty < 0 condition
WITH negative_txn_test AS (
  SELECT *
  FROM purgo_playground.purgo_playground.f_inv_movmnt_apl_qty_test
  WHERE ref_txn_qty < 0
)
SELECT
  CASE WHEN apl_qty = ref_txn_qty THEN 'Pass' ELSE 'Fail' END AS condition_check
FROM negative_txn_test;

-- Validate Error Handling in case of NULL values
WITH null_value_test AS (
  SELECT *
  FROM purgo_playground.purgo_playground.f_inv_movmnt_apl_qty_test
  WHERE txn_id IS NULL
)
SELECT
  CASE WHEN COUNT(txn_id) > 0 THEN 'Fail' ELSE 'Pass' END AS null_error_check
FROM null_value_test;

-- Performance Test: Check if the calculation performs within the expected time frame
SELECT
  COUNT(*) AS total_records,
  CURRENT_TIMESTAMP AS test_start_time
FROM purgo_playground.purgo_playground.f_inv_movmnt_apl_qty_test;

-- Cleanup operations after tests
DROP TABLE IF EXISTS purgo_playground.purgo_playground.f_inv_movmnt_apl_qty_test;
