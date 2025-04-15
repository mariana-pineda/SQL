-- SQL Implementation for Calculating Applied Quantity (apl_qty) in Databricks Environment

-- Create Table if not exists for storing Inventory Transaction Data
CREATE TABLE IF NOT EXISTS purgo_playground.f_inv_movmnt_apl_qty (
  txn_id STRING COMMENT "Transaction ID",
  ref_txn_qty DECIMAL(3,1) COMMENT "Reference Transaction Quantity",
  cumulative_txn_qty DECIMAL(4,1) COMMENT "Cumulative Transaction Quantity",
  cumulative_ref_ord_sched_qty DECIMAL(4,1) COMMENT "Cumulative Reference Order Scheduled Quantity",
  ref_ord_sched_qty DECIMAL(3,1) COMMENT "Reference Order Scheduled Quantity",
  prior_cumulative_txn_qty DECIMAL(3,1) COMMENT "Prior Cumulative Transaction Quantity",
  prior_cumulative_ref_ord_sched_qty DECIMAL(3,1) COMMENT "Prior Cumulative Reference Order Scheduled Quantity",
  apl_qty DECIMAL(5,1) COMMENT "Applied Quantity"
);

-- Calculate the applied quantity based on the defined conditions
CREATE OR REPLACE TEMP VIEW vw_apl_qty_calculation AS
SELECT
  txn_id,
  ref_txn_qty,
  cumulative_txn_qty,
  cumulative_ref_ord_sched_qty,
  ref_ord_sched_qty,
  prior_cumulative_txn_qty,
  prior_cumulative_ref_ord_sched_qty,
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
  END AS apl_qty
FROM purgo_playground.f_inv_movmnt_apl_qty;

-- Insert calculated apl_qty back into the main table
MERGE INTO purgo_playground.f_inv_movmnt_apl_qty AS target
USING vw_apl_qty_calculation AS source
ON target.txn_id = source.txn_id
WHEN MATCHED THEN UPDATE SET
  target.apl_qty = source.apl_qty;

-- Validate Data Consistency
SELECT * FROM purgo_playground.f_inv_movmnt_apl_qty WHERE apl_qty IS NULL;

-- Clean up temporary view
DROP VIEW IF EXISTS vw_apl_qty_calculation;
