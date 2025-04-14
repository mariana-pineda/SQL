-- Generating a diverse set of test data for the target table `purgo_playground.f_inv_movmnt_apl_qty`

SET spark.databricks.parseComplexTypes=true;

CREATE OR REPLACE TABLE purgo_playground.f_inv_movmnt_apl_qty_test AS
WITH test_data AS (
  SELECT
    '1' AS txn_id, -- Happy path scenario: Valid transaction id
    50.0 AS ref_txn_qty, -- Valid positive transaction quantity
    100.0 AS cumulative_txn_qty, -- Valid cumulative transaction quantity
    90.0 AS cumulative_ref_ord_sched_qty, -- Reference order scheduled quantity is less than cumulative
    50.0 AS ref_ord_sched_qty, -- Valid reference order scheduled quantity
    40.0 AS prior_cumulative_txn_qty, -- Prior cumulative transaction quantity
    30.0 AS prior_cumulative_ref_ord_sched_qty, -- Prior reference order scheduled quantity
    40.0 AS apl_qty -- Expected valid apl_qty calculation
  
  UNION ALL
  
  SELECT
    '2' AS txn_id, -- Edge case: Negative transaction quantity
    -10.0 AS ref_txn_qty, -- Valid negative transaction quantity
    80.0 AS cumulative_txn_qty, -- Valid cumulative transaction quantity
    70.0 AS cumulative_ref_ord_sched_qty, -- Reference order scheduled quantity
    30.0 AS ref_ord_sched_qty, -- Valid reference order scheduled quantity
    50.0 AS prior_cumulative_txn_qty, -- Prior cumulative transaction quantity
    45.0 AS prior_cumulative_ref_ord_sched_qty, -- Prior reference order scheduled quantity
    -10.0 AS apl_qty -- Directly assigned apl_qty as per logic

  UNION ALL
  
  SELECT
    '3' AS txn_id, -- Error case: Invalid positive transaction quantity scenario relation
    20.0 AS ref_txn_qty, -- Valid positive transaction quantity
    60.0 AS cumulative_txn_qty, -- Valid cumulative transaction quantity
    100.0 AS cumulative_ref_ord_sched_qty, -- Reference order scheduled quantity is greater
    30.0 AS ref_ord_sched_qty, -- Valid reference order scheduled quantity
    30.0 AS prior_cumulative_txn_qty, -- Equal prior cumulative transaction quantity
    25.0 AS prior_cumulative_ref_ord_sched_qty, -- Prior reference order scheduled quantity
    15.0 AS apl_qty -- Expected valid apl_qty calculation

  UNION ALL

  -- Special case scenario with NULL handling
  SELECT
    '4' AS txn_id,
    NULL AS ref_txn_qty, -- NULL transaction quantity handling
    NULL AS cumulative_txn_qty, -- NULL cumulative transaction handling
    NULL AS cumulative_ref_ord_sched_qty, -- NULL reference transaction handling
    NULL AS ref_ord_sched_qty, -- NULL scheduled reference handling
    NULL AS prior_cumulative_txn_qty, -- NULL prior cumulative transaction handling
    NULL AS prior_cumulative_ref_ord_sched_qty, -- NULL prior reference transaction handling
    NULL AS apl_qty -- Expected result NULL
   
  UNION ALL
  
  SELECT
    '5' AS txn_id, -- Special characters case
    10.0 AS ref_txn_qty, -- Valid positive transaction quantity with special checking
    10.0 AS cumulative_txn_qty, -- Valid cumulative transaction with edge validation
    10.0 AS cumulative_ref_ord_sched_qty, -- Valid reference order scheduled quantity
    10.0 AS ref_ord_sched_qty, -- Scheduled reference quantity same, to validate apl_qty
    10.0 AS prior_cumulative_txn_qty, -- Prior cumulative same for special validation
    10.0 AS prior_cumulative_ref_ord_sched_qty, -- Prior reference same for special validation
    10.0 AS apl_qty -- Expected valid apl_qty calculation

  UNION ALL
  
  SELECT
    '6' AS txn_id -- Multi-byte characters handling scenario
    '\u0F68' AS ref_txn_qty, -- Tibetan character encoding for test
    40.0 AS cumulative_txn_qty, -- Cumulative transaction without calculation
    40.0 AS cumulative_ref_ord_sched_qty, -- Matching cumulative reference transaction for test
    40.0 AS ref_ord_sched_qty, -- Scheduled reference quantity same
    40.0 AS prior_cumulative_txn_qty, -- Prior cumulative same
    40.0 AS prior_cumulative_ref_ord_sched_qty, -- Prior reference same
    NULL AS apl_qty -- Expected result NULL due to character encoding in ref_txn_qty
)
SELECT * FROM test_data;

