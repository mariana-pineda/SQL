-- Test Data Generation for Databricks Environment using SQL 
-- Ensure data matches the target table schema: purgo_playground.purgo_playground.f_inv_movmnt_apl_qty_test

-- Test 1: Happy Path scenario where ref_txn_qty is positive and conditions are met
WITH happy_path AS (
  SELECT
    txn_id,
    CAST(ref_txn_qty AS DECIMAL(3,1)),
    CAST(cumulative_txn_qty AS DECIMAL(4,1)),
    CAST(cumulative_ref_ord_sched_qty AS DECIMAL(4,1)),
    CAST(ref_ord_sched_qty AS DECIMAL(3,1)),
    CAST(prior_cumulative_txn_qty AS DECIMAL(3,1)),
    CAST(prior_cumulative_ref_ord_sched_qty AS DECIMAL(3,1)),
    CAST(calculated_apl_qty AS DECIMAL(5,1)),
    CASE WHEN ref_txn_qty > 0 AND cumulative_txn_qty >= cumulative_ref_ord_sched_qty 
         AND prior_cumulative_ref_ord_sched_qty < prior_cumulative_txn_qty THEN 
         CAST(ref_ord_sched_qty - (prior_cumulative_txn_qty - prior_cumulative_ref_ord_sched_qty) AS DECIMAL(5,1))
         ELSE CAST(ref_ord_sched_qty AS DECIMAL(5,1))
    END AS apl_qty
  FROM VALUES
    (1, 50, 100, 90, 50, 40, 30)
) AS t(txn_id, ref_txn_qty, cumulative_txn_qty, cumulative_ref_ord_sched_qty, ref_ord_sched_qty, prior_cumulative_txn_qty, prior_cumulative_ref_ord_sched_qty, calculated_apl_qty),

-- Test 2: Edge case scenario with ref_txn_qty positive and different conditions
edge_case AS (
  SELECT
    txn_id,
    CAST(ref_txn_qty AS DECIMAL(3,1)),
    CAST(cumulative_txn_qty AS DECIMAL(4,1)),
    CAST(cumulative_ref_ord_sched_qty AS DECIMAL(4,1)),
    CAST(ref_ord_sched_qty AS DECIMAL(3,1)),
    CAST(prior_cumulative_txn_qty AS DECIMAL(3,1)),
    CAST(prior_cumulative_ref_ord_sched_qty AS DECIMAL(3,1)),
    CAST(calculated_apl_qty AS DECIMAL(5,1)),
    CASE WHEN ref_txn_qty > 0 AND cumulative_ref_ord_sched_qty >= cumulative_txn_qty 
         AND prior_cumulative_ref_ord_sched_qty > prior_cumulative_txn_qty THEN 
         CAST(ref_txn_qty - (prior_cumulative_ref_ord_sched_qty - prior_cumulative_txn_qty) AS DECIMAL(5,1))
         ELSE CAST(ref_txn_qty AS DECIMAL(5,1))
    END AS apl_qty
  FROM VALUES
    (3, 20, 60, 100, 30, 30, 25)
) AS t(txn_id, ref_txn_qty, cumulative_txn_qty, cumulative_ref_ord_sched_qty, ref_ord_sched_qty, prior_cumulative_txn_qty, prior_cumulative_ref_ord_sched_qty, calculated_apl_qty),

-- Test 3: Error case for negative ref_txn_qty
error_case AS (
  SELECT
    txn_id,
    CAST(ref_txn_qty AS DECIMAL(3,1)),
    CAST(cumulative_txn_qty AS DECIMAL(4,1)),
    CAST(cumulative_ref_ord_sched_qty AS DECIMAL(4,1)),
    CAST(ref_ord_sched_qty AS DECIMAL(3,1)),
    CAST(prior_cumulative_txn_qty AS DECIMAL(3,1)),
    CAST(prior_cumulative_ref_ord_sched_qty AS DECIMAL(3,1)),
    NULL AS calculated_apl_qty,
    CASE WHEN ref_txn_qty < 0 AND cumulative_txn_qty != 0 AND cumulative_ref_ord_sched_qty > 0 THEN 
         CAST(ref_txn_qty AS DECIMAL(5,1))
         ELSE NULL
    END AS apl_qty
  FROM VALUES
    (2, -10, 80, 70, 40, 50, 45)
) AS t(txn_id, ref_txn_qty, cumulative_txn_qty, cumulative_ref_ord_sched_qty, ref_ord_sched_qty, prior_cumulative_txn_qty, prior_cumulative_ref_ord_sched_qty, NULL),

-- Test 4: NULL handling scenario for default conditions
null_handling AS (
  SELECT
    txn_id,
    CAST(ref_txn_qty AS DECIMAL(3,1)),
    CAST(cumulative_txn_qty AS DECIMAL(4,1)),
    CAST(cumulative_ref_ord_sched_qty AS DECIMAL(4,1)),
    CAST(ref_ord_sched_qty AS DECIMAL(3,1)),
    CAST(prior_cumulative_txn_qty AS DECIMAL(3,1)),
    CAST(prior_cumulative_ref_ord_sched_qty AS DECIMAL(3,1)),
    NULL AS calculated_apl_qty,
    NULL AS apl_qty
  FROM VALUES
    (4, NULL, NULL, NULL, NULL, NULL, NULL)
) AS t(txn_id, ref_txn_qty, cumulative_txn_qty, cumulative_ref_ord_sched_qty, ref_ord_sched_qty, prior_cumulative_txn_qty, prior_cumulative_ref_ord_sched_qty, NULL)

-- Combine all test data categories
SELECT * FROM happy_path
UNION
SELECT * FROM edge_case
UNION
SELECT * FROM error_case
UNION
SELECT * FROM null_handling 

