/* SQL code to calculate applied quantity (apl_qty) for inventory transactions in Databricks environment */

/* Setup: Create a temporary view for transaction details to calculate applied quantity */
CREATE OR REPLACE TEMP VIEW transaction_details AS 
SELECT 
  txn_id,
  CAST(ref_txn_qty AS DECIMAL(3,1)) AS ref_txn_qty,
  CAST(cumulative_txn_qty AS DECIMAL(4,1)) AS cumulative_txn_qty,
  CAST(cumulative_ref_ord_sched_qty AS DECIMAL(4,1)) AS cumulative_ref_ord_sched_qty,
  CAST(ref_ord_sched_qty AS DECIMAL(3,1)) AS ref_ord_sched_qty,
  CAST(prior_cumulative_txn_qty AS DECIMAL(3,1)) AS prior_cumulative_txn_qty,
  CAST(prior_cumulative_ref_ord_sched_qty AS DECIMAL(3,1)) AS prior_cumulative_ref_ord_sched_qty
FROM purgo_playground.purgo_playground.f_inv_movmnt_apl_qty_test;

/* Main CTE for apl_qty calculation logic */
WITH appl_qty_calculation AS (
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
          WHEN prior_cumulative_ref_ord_sched_qty < prior_cumulative_txn_qty THEN
            ref_ord_sched_qty - (prior_cumulative_txn_qty - prior_cumulative_ref_ord_sched_qty)
          ELSE
            ref_ord_sched_qty
        END
      WHEN ref_txn_qty > 0 AND cumulative_ref_ord_sched_qty >= cumulative_txn_qty THEN
        CASE
          WHEN prior_cumulative_ref_ord_sched_qty > prior_cumulative_txn_qty THEN
            ref_txn_qty - (prior_cumulative_ref_ord_sched_qty - prior_cumulative_txn_qty)
          ELSE
            ref_txn_qty
        END
      WHEN ref_txn_qty < 0 AND cumulative_txn_qty <> 0 AND cumulative_ref_ord_sched_qty > 0 THEN
        ref_txn_qty
      ELSE
        NULL
    END AS apl_qty
  FROM transaction_details
)

/* Insert calculated applied quantities into the result table */
INSERT INTO purgo_playground.purgo_playground.f_inv_movmnt_apl_qty_result
(txn_id, ref_txn_qty, cumulative_txn_qty, cumulative_ref_ord_sched_qty, ref_ord_sched_qty, 
prior_cumulative_txn_qty, prior_cumulative_ref_ord_sched_qty, apl_qty)
SELECT
  txn_id,
  ref_txn_qty,
  cumulative_txn_qty,
  cumulative_ref_ord_sched_qty,
  ref_ord_sched_qty,
  prior_cumulative_txn_qty,
  prior_cumulative_ref_ord_sched_qty,
  apl_qty
FROM appl_qty_calculation;

/* Validate the result by comparing with expected values in the test data */
SELECT
  ar.txn_id,
  ar.apl_qty AS calculated_apl_qty,
  td.apl_qty AS expected_apl_qty,
  CASE WHEN ar.apl_qty = td.apl_qty THEN 'PASS' ELSE 'FAIL' END AS test_result
FROM purgo_playground.purgo_playground.f_inv_movmnt_apl_qty_result AS ar
JOIN purgo_playground.purgo_playground.f_inv_movmnt_apl_qty_test AS td 
ON ar.txn_id = td.txn_id;

/* Clean up by dropping temporary views if necessary */
-- DROP VIEW IF EXISTS transaction_details; -- Uncomment if cleanup is required
