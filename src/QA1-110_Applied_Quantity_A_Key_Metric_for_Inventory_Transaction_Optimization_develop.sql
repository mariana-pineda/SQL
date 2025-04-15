-- Databricks SQL Implementation for Calculating Applied Quantity (apl_qty)

/* Header comments:
   Implementation of the Applied Quantity (apl_qty) calculation based on the transactional
   and cumulative quantity fields using Databricks SQL.
   Schema: purgo_playground
   Unity Catalog: purgo_databricks
*/

/* Create the 'f_inv_movmnt_apl_qty_test' table for testing purposes */
CREATE TABLE IF NOT EXISTS purgo_playground.f_inv_movmnt_apl_qty_test (
  txn_id STRING NOT NULL COMMENT "Transaction ID",
  ref_txn_qty DECIMAL(3,1) COMMENT "Reference transaction quantity",
  cumulative_txn_qty DECIMAL(4,1) COMMENT "Cumulative transaction quantity",
  cumulative_ref_ord_sched_qty DECIMAL(4,1) COMMENT "Cumulative reference order schedule quantity",
  ref_ord_sched_qty DECIMAL(3,1) COMMENT "Reference order schedule quantity",
  prior_cumulative_txn_qty DECIMAL(3,1) COMMENT "Prior cumulative transaction quantity",
  prior_cumulative_ref_ord_sched_qty DECIMAL(3,1) COMMENT "Prior cumulative reference order schedule quantity",
  apl_qty DECIMAL(5,1) COMMENT "Calculated applied quantity"
);

/* Insert data with logic for calculating apl_qty */
INSERT INTO purgo_playground.f_inv_movmnt_apl_qty_test
SELECT
  txn_id,
  ref_txn_qty,
  cumulative_txn_qty,
  cumulative_ref_ord_sched_qty,
  ref_ord_sched_qty,
  prior_cumulative_txn_qty,
  prior_cumulative_ref_ord_sched_qty,
  CASE
    /* Condition 1: ref_txn_qty > 0 and cumulative_txn_qty >= cumulative_ref_ord_sched_qty */
    WHEN ref_txn_qty > 0 AND cumulative_txn_qty >= cumulative_ref_ord_sched_qty THEN
      CASE
        WHEN prior_cumulative_ref_ord_sched_qty < prior_cumulative_txn_qty THEN ref_ord_sched_qty - (prior_cumulative_txn_qty - prior_cumulative_ref_ord_sched_qty)
        ELSE ref_ord_sched_qty
      END
    /* Condition 2: ref_txn_qty > 0 and cumulative_ref_ord_sched_qty >= cumulative_txn_qty */
    WHEN ref_txn_qty > 0 AND cumulative_ref_ord_sched_qty >= cumulative_txn_qty THEN
      CASE
        WHEN prior_cumulative_ref_ord_sched_qty > prior_cumulative_txn_qty THEN ref_txn_qty - (prior_cumulative_ref_ord_sched_qty - prior_cumulative_txn_qty)
        ELSE ref_txn_qty
      END
    /* Condition 3: ref_txn_qty < 0, cumulative_txn_qty != 0, and cumulative_ref_ord_sched_qty > 0 */
    WHEN ref_txn_qty < 0 AND cumulative_txn_qty != 0 AND cumulative_ref_ord_sched_qty > 0 THEN
      ref_txn_qty
    /* Default: none of the above conditions are met */
    ELSE NULL
  END AS apl_qty
FROM purgo_playground.f_inv_movmnt_apl_qty
WHERE txn_id IS NOT NULL;

/* Validation to ensure correct setup: Check number of columns */
SELECT COUNT(*) AS total_columns
FROM information_schema.columns
WHERE table_name='f_inv_movmnt_apl_qty_test';

/* Verify data insertion by checking row count */
SELECT COUNT(*) AS row_count
FROM purgo_playground.f_inv_movmnt_apl_qty_test;

/* Cleanup section: Uncomment the following line to drop the test table after validation */
-- DROP TABLE IF EXISTS purgo_playground.f_inv_movmnt_apl_qty_test;

-- End of Databricks SQL script
