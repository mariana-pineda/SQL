-- Test Code for Databricks Environment
/* 
Test Cases for SQL Calculations on table purgo_playground.f_inv_movmnt_apl_qty
Test specific conditions and data transformations
*/

-- Create initial test data table
CREATE TABLE IF NOT EXISTS purgo_playground.f_inv_movmnt_apl_qty_test (
  txn_id STRING,
  ref_txn_qty DECIMAL(3,1),
  cumulative_txn_qty DECIMAL(4,1),
  cumulative_ref_ord_sched_qty DECIMAL(4,1),
  ref_ord_sched_qty DECIMAL(3,1),
  prior_cumulative_txn_qty DECIMAL(3,1),
  prior_cumulative_ref_ord_sched_qty DECIMAL(3,1),
  calculated_apl_qty DECIMAL(5,1),
  apl_qty DECIMAL(5,1)
);

-- Set up test data for validation
INSERT INTO purgo_playground.f_inv_movmnt_apl_qty_test
SELECT 
  CAST(txn_id AS STRING),
  CAST(ref_txn_qty AS DECIMAL(3,1)),
  CAST(cumulative_txn_qty AS DECIMAL(4,1)),
  CAST(cumulative_ref_ord_sched_qty AS DECIMAL(4,1)),
  CAST(ref_ord_sched_qty AS DECIMAL(3,1)),
  CAST(prior_cumulative_txn_qty AS DECIMAL(3,1)),
  CAST(prior_cumulative_ref_ord_sched_qty AS DECIMAL(3,1)),
  CASE
    WHEN ref_txn_qty > 0 AND cumulative_txn_qty >= cumulative_ref_ord_sched_qty AND prior_cumulative_ref_ord_sched_qty < prior_cumulative_txn_qty THEN
      ref_ord_sched_qty - (prior_cumulative_txn_qty - prior_cumulative_ref_ord_sched_qty)
    WHEN ref_txn_qty > 0 AND cumulative_txn_qty >= cumulative_ref_ord_sched_qty THEN
      ref_ord_sched_qty
    WHEN ref_txn_qty > 0 AND cumulative_ref_ord_sched_qty >= cumulative_txn_qty AND prior_cumulative_ref_ord_sched_qty > prior_cumulative_txn_qty THEN
      ref_txn_qty - (prior_cumulative_ref_ord_sched_qty - prior_cumulative_txn_qty)
    WHEN ref_txn_qty > 0 AND cumulative_ref_ord_sched_qty >= cumulative_txn_qty THEN
      ref_txn_qty
    WHEN ref_txn_qty < 0 AND cumulative_txn_qty != 0 AND cumulative_ref_ord_sched_qty > 0 THEN
      ref_txn_qty
    ELSE NULL
  END AS calculated_apl_qty,
  CAST(NULL AS DECIMAL(5,1)) AS apl_qty
FROM (
  SELECT
    '1' AS txn_id,
    CAST(50.0 AS DECIMAL(3,1)) AS ref_txn_qty,
    CAST(100.0 AS DECIMAL(4,1)) AS cumulative_txn_qty,
    CAST(90.0 AS DECIMAL(4,1)) AS cumulative_ref_ord_sched_qty,
    CAST(50.0 AS DECIMAL(3,1)) AS ref_ord_sched_qty,
    CAST(40.0 AS DECIMAL(3,1)) AS prior_cumulative_txn_qty,
    CAST(30.0 AS DECIMAL(3,1)) AS prior_cumulative_ref_ord_sched_qty
  UNION ALL
  SELECT
    '2',
    CAST(-10.0 AS DECIMAL(3,1)),
    CAST(80.0 AS DECIMAL(4,1)),
    CAST(70.0 AS DECIMAL(4,1)),
    CAST(40.0 AS DECIMAL(3,1)),
    CAST(50.0 AS DECIMAL(3,1)),
    CAST(45.0 AS DECIMAL(3,1))
  UNION ALL
  SELECT
    '3',
    CAST(20.0 AS DECIMAL(3,1)),
    CAST(60.0 AS DECIMAL(4,1)),
    CAST(100.0 AS DECIMAL(4,1)),
    CAST(30.0 AS DECIMAL(3,1)),
    CAST(30.0 AS DECIMAL(3,1)),
    CAST(25.0 AS DECIMAL(3,1))
);

-- Validate APL_QTY values
SELECT 
  txn_id,
  ref_txn_qty,
  cumulative_txn_qty,
  cumulative_ref_ord_sched_qty,
  ref_ord_sched_qty,
  prior_cumulative_txn_qty,
  prior_cumulative_ref_ord_sched_qty,
  calculated_apl_qty AS calculated_apl_qty_SQL,
  apl_qty AS expected_apl_qty_SQL
FROM purgo_playground.f_inv_movmnt_apl_qty_test;

-- Validation via SQL assertions
CREATE OR REPLACE TEMP VIEW validated_transforms AS
SELECT *
FROM purgo_playground.f_inv_movmnt_apl_qty_test
WHERE calculated_apl_qty = apl_qty;

-- Validate that all records match expected calculations
SELECT * FROM validated_transforms;

-- Performance Test
-- Evaluate execution time and compare with expected thresholds
EXPLAIN SELECT txn_id, calculated_apl_qty FROM validated_transforms;

/*
Delete temporary data created for cleanliness
Ensure clean-up after execution of tests
*/
DROP TABLE IF EXISTS purgo_playground.f_inv_movmnt_apl_qty_test;
