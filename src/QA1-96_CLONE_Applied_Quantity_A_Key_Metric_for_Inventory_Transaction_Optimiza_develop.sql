-- SQL Implementation for Calculating Applied Quantity (apl_qty) in Inventory Transactions

-- Establish connection to Unity Catalog purgo_databricks and utilize schema purgo_playground

-- Create the table for storing applied quantity calculations if it doesn't already exist
CREATE TABLE IF NOT EXISTS purgo_playground.f_inv_movmnt_apl_qty (
  txn_id STRING COMMENT "Transaction ID",
  ref_txn_qty DECIMAL(3,1) COMMENT "Reference transaction quantity",
  cumulative_txn_qty DECIMAL(4,1) COMMENT "Cumulative transaction quantity",
  cumulative_ref_ord_sched_qty DECIMAL(4,1) COMMENT "Cumulative reference order schedule quantity",
  ref_ord_sched_qty DECIMAL(3,1) COMMENT "Reference order schedule quantity",
  prior_cumulative_txn_qty DECIMAL(3,1) COMMENT "Prior cumulative transaction quantity",
  prior_cumulative_ref_ord_sched_qty DECIMAL(3,1) COMMENT "Prior cumulative reference order schedule quantity",
  apl_qty DECIMAL(5,1) COMMENT "Calculated applied quantity"
);

-- Insert data into the table with calculated apl_qty using conditions provided
INSERT INTO purgo_playground.f_inv_movmnt_apl_qty (txn_id, ref_txn_qty, cumulative_txn_qty, cumulative_ref_ord_sched_qty, ref_ord_sched_qty, prior_cumulative_txn_qty, prior_cumulative_ref_ord_sched_qty, apl_qty)
WITH txn_data AS (
  SELECT * FROM VALUES
  ("1", 50, 100, 90, 50, 40, 30), -- Example data row
  ("2", -10, 80, 70, 40, 50, 45), -- Example data row
  ("3", 20, 60, 100, 30, 30, 25)  -- Example data row
  AS t(txn_id, ref_txn_qty, cumulative_txn_qty, cumulative_ref_ord_sched_qty, ref_ord_sched_qty, prior_cumulative_txn_qty, prior_cumulative_ref_ord_sched_qty)
)
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
      CASE WHEN prior_cumulative_ref_ord_sched_qty < prior_cumulative_txn_qty THEN
        ref_ord_sched_qty - (prior_cumulative_txn_qty - prior_cumulative_ref_ord_sched_qty)
      ELSE ref_ord_sched_qty
      END
    WHEN ref_txn_qty > 0 AND cumulative_ref_ord_sched_qty >= cumulative_txn_qty THEN
      CASE WHEN prior_cumulative_ref_ord_sched_qty > prior_cumulative_txn_qty THEN
        ref_txn_qty - (prior_cumulative_ref_ord_sched_qty - prior_cumulative_txn_qty)
      ELSE ref_txn_qty
      END
    WHEN ref_txn_qty < 0 AND cumulative_txn_qty != 0 AND cumulative_ref_ord_sched_qty > 0 THEN
      ref_txn_qty
    ELSE NULL
  END AS apl_qty
FROM txn_data;

-- End of SQL implementation for applied quantity calculation
