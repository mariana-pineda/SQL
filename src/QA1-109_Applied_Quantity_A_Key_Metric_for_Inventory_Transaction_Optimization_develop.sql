/* SQL Code for APL_QTY Calculation in Databricks */

/* Scenario: Calculate Applied Quantity (APL_QTY) based on transaction logic
 * Considering conditions from inventory transaction allocations.
 */

/* Create table if not exists - f_inv_movmnt_apl_qty_result */
CREATE TABLE IF NOT EXISTS purgo_playground.f_inv_movmnt_apl_qty_result (
    txn_id STRING COMMENT "Transaction Identifier",
    ref_txn_qty DECIMAL(3,1) COMMENT "Referenced Transaction Quantity. Valid values: positive or negative decimal",
    cumulative_txn_qty DECIMAL(4,1) COMMENT "Cumulative Transaction Quantity. Can be zero or positive",
    cumulative_ref_ord_sched_qty DECIMAL(4,1) COMMENT "Cumulative Referenced Order Scheduled Quantity. Can be zero or positive",
    ref_ord_sched_qty DECIMAL(3,1) COMMENT "Referenced Order Scheduled Quantity. Valid non-negative decimal values",
    prior_cumulative_txn_qty DECIMAL(3,1) COMMENT "Prior Cumulative Transaction Quantity. Non-negative decimal",
    prior_cumulative_ref_ord_sched_qty DECIMAL(3,1) COMMENT "Prior Cumulative Referenced Order Scheduled Quantity. Non-negative decimal",
    apl_qty DECIMAL(5,1) COMMENT "Calculated Applied Quantity based on specified conditions"
);

/* Insert calculated values into the result table using CTE for validation and calculations */
WITH CalculatedAPLQTY AS (
  SELECT
    txn_id,
    ref_txn_qty,
    cumulative_txn_qty,
    cumulative_ref_ord_sched_qty,
    ref_ord_sched_qty,
    prior_cumulative_txn_qty,
    prior_cumulative_ref_ord_sched_qty,
    -- Calculation logic for assigning apl_qty
    CASE
      -- Condition 1: ref_txn_qty > 0 and cumulative_txn_qty >= cumulative_ref_ord_sched_qty
      WHEN ref_txn_qty > 0 AND cumulative_txn_qty >= cumulative_ref_ord_sched_qty THEN
        CASE
          WHEN prior_cumulative_ref_ord_sched_qty < prior_cumulative_txn_qty THEN
            ref_ord_sched_qty - (prior_cumulative_txn_qty - prior_cumulative_ref_ord_sched_qty)
          ELSE ref_ord_sched_qty
        END
      -- Condition 2: ref_txn_qty > 0 and cumulative_ref_ord_sched_qty >= cumulative_txn_qty
      WHEN ref_txn_qty > 0 AND cumulative_ref_ord_sched_qty >= cumulative_txn_qty THEN
        CASE
          WHEN prior_cumulative_ref_ord_sched_qty > prior_cumulative_txn_qty THEN
            ref_txn_qty - (prior_cumulative_ref_ord_sched_qty - prior_cumulative_txn_qty)
          ELSE ref_txn_qty
        END
      -- Condition 3: ref_txn_qty < 0, cumulative_txn_qty != 0, cumulative_ref_ord_sched_qty > 0
      WHEN ref_txn_qty < 0 AND cumulative_txn_qty != 0 AND cumulative_ref_ord_sched_qty > 0 THEN ref_txn_qty
      -- Default: Set apl_qty to NULL when none of conditions are met
      ELSE NULL
    END AS apl_qty
  FROM purgo_playground.f_inv_movmnt_apl_qty_test
)

/* Insert data into the result table */
INSERT INTO purgo_playground.f_inv_movmnt_apl_qty_result
SELECT * FROM CalculatedAPLQTY;

/* Verify result table insertion */
SELECT COUNT(*) FROM purgo_playground.f_inv_movmnt_apl_qty_result;

/* End of SQL Code */
