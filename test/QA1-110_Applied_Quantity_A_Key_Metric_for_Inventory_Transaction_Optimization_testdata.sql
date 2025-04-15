-- Generate test data using Databricks native data types for table purgo_playground.f_inv_movmnt_apl_qty

WITH base_data AS (
  SELECT
    CAST('1' AS STRING) AS txn_id,
    CAST(50.0 AS DECIMAL(3,1)) AS ref_txn_qty,
    CAST(100.0 AS DECIMAL(4,1)) AS cumulative_txn_qty,
    CAST(90.0 AS DECIMAL(4,1)) AS cumulative_ref_ord_sched_qty,
    CAST(50.0 AS DECIMAL(3,1)) AS ref_ord_sched_qty,
    CAST(40.0 AS DECIMAL(3,1)) AS prior_cumulative_txn_qty,
    CAST(30.0 AS DECIMAL(3,1)) AS prior_cumulative_ref_ord_sched_qty
  UNION ALL
  SELECT
    CAST('2' AS STRING),
    CAST(-10.0 AS DECIMAL(3,1)),
    CAST(80.0 AS DECIMAL(4,1)),
    CAST(70.0 AS DECIMAL(4,1)),
    CAST(40.0 AS DECIMAL(3,1)),
    CAST(50.0 AS DECIMAL(3,1)),
    CAST(45.0 AS DECIMAL(3,1))
  UNION ALL
  SELECT
    CAST('3' AS STRING),
    CAST(20.0 AS DECIMAL(3,1)),
    CAST(60.0 AS DECIMAL(4,1)),
    CAST(100.0 AS DECIMAL(4,1)),
    CAST(30.0 AS DECIMAL(3,1)),
    CAST(30.0 AS DECIMAL(3,1)),
    CAST(25.0 AS DECIMAL(3,1))
)

-- Happy path test data
INSERT INTO purgo_playground.purgo_playground.f_inv_movmnt_apl_qty
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
FROM base_data;

