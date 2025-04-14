/* Test code for apl_qty calculation logic in SQL using Databricks syntax */

/* Setup: Create a temporary view to hold test values for apl_qty calculations */
CREATE OR REPLACE TEMP VIEW f_inv_movmnt_apl_qty_test_view AS
SELECT 
  txn_id,
  ref_txn_qty,
  cumulative_txn_qty,
  cumulative_ref_ord_sched_qty,
  ref_ord_sched_qty,
  prior_cumulative_txn_qty,
  prior_cumulative_ref_ord_sched_qty,
  apl_qty
FROM VALUES
  ('1', 50.0, 100.0, 90.0, 50.0, 40.0, 30.0, 40.0),
  ('2', -10.0, 80.0, 70.0, NULL, NULL, NULL, -10.0),
  ('3', 20.0, 60.0, 100.0, 30.0, 30.0, 25.0, 15.0),
  ('4', NULL, NULL, NULL, NULL, NULL, NULL, NULL),
  ('5', 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0),
  ('6', NULL, 40.0, 40.0, 40.0, 40.0, 40.0, NULL)
AS test_data(txn_id, ref_txn_qty, cumulative_txn_qty, cumulative_ref_ord_sched_qty, ref_ord_sched_qty, prior_cumulative_txn_qty, prior_cumulative_ref_ord_sched_qty, apl_qty);

/* Testing apl_qty calculation logic with conditions */
WITH calculated_qty AS (
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
    END AS calculated_apl_qty

  FROM f_inv_movmnt_apl_qty_test_view
)

/* Validate calculated apl_qty with expected apl_qty */
SELECT
  cq.txn_id, 
  cq.calculated_apl_qty, 
  td.apl_qty AS expected_apl_qty,
  CASE WHEN cq.calculated_apl_qty = td.apl_qty THEN 'PASS' ELSE 'FAIL' END AS test_result
FROM calculated_qty AS cq
JOIN f_inv_movmnt_apl_qty_test_view AS td 
ON cq.txn_id = td.txn_id;

/* Clean up temporary view, if needed */
-- DROP VIEW IF EXISTS f_inv_movmnt_apl_qty_test_view; -- Uncomment if cleanup is required
