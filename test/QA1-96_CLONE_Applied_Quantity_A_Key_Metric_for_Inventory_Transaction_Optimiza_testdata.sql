-- Test Data Generation Code using Databricks SQL

-- Define schema and create table for test data generation
CREATE TABLE purgo_playground.f_inv_movmnt_apl_qty_test (
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

-- Insert diverse test records
INSERT INTO purgo_playground.f_inv_movmnt_apl_qty_test VALUES
('1', 50.0, 100.0, 90.0, 50.0, 40.0, 30.0, 40.0, NULL),  -- Happy Path
('2', -10.0, 80.0, 70.0, 40.0, 50.0, 45.0, -10.0, NULL), -- Error Case
('3', 20.0, 60.0, 100.0, 30.0, 30.0, 25.0, 20.0, NULL),  -- Edge Case
('4', 0.0, 50.0, 45.0, 20.0, 25.0, 20.0, NULL, NULL),   -- Edge Case with zero ref_txn_qty
('5', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL), -- NULL Handling

-- Include special characters and multi-byte characters
('6', 30.0, 80.0, 75.0, 25.0, 30.0, 20.0, 25.0, '特別'), -- Multi-byte characters
('7', '25%', '45%', '50%', '30%', '25%', '20%', '30%', '@!&$'), -- Special characters
('8', -20.0, 90.0, 85.0, 50.0, 40.0, 35.0, NULL, NULL), -- Error Case with out-of-range values
('9', 100.0, NULL, 95.0, NULL, NULL, NULL, 90.0, NULL), -- Partial NULL Handling
('10', 50.0, 50.0, 50.0, 50.0, 50.0, 50.0, 50.0, 'Valid'), -- Valid data

-- Happy Path scenarios
SELECT * FROM purgo_playground.f_inv_movmnt_apl_qty_test WHERE txn_id IN ('1', '3', '10');

-- Edge Cases validation
WITH cte_edge_cases AS (
    SELECT * FROM purgo_playground.f_inv_movmnt_apl_qty_test WHERE ref_txn_qty = 0 OR apl_qty IS NULL
)
SELECT * FROM cte_edge_cases;

-- Error Case scenarios validation
WITH cte_error_cases AS (
    SELECT * FROM purgo_playground.f_inv_movmnt_apl_qty_test WHERE ref_txn_qty < 0 AND apl_qty IS NULL
)
SELECT * FROM cte_error_cases;

-- Special character handling validation
WITH cte_special_chars AS (
    SELECT * FROM purgo_playground.f_inv_movmnt_apl_qty_test WHERE apl_qty LIKE '%特%' OR apl_qty LIKE '%@!&$%'
)
SELECT * FROM cte_special_chars;

-- Validate consistency against the target table schema
INSERT INTO purgo_playground.f_inv_movmnt_apl_qty SELECT 
    txn_id,
    CAST(ref_txn_qty AS DECIMAL(3,1)),
    CAST(cumulative_txn_qty AS DECIMAL(4,1)),
    CAST(cumulative_ref_ord_sched_qty AS DECIMAL(4,1)),
    CAST(ref_ord_sched_qty AS DECIMAL(3,1)),
    CAST(prior_cumulative_txn_qty AS DECIMAL(3,1)),
    CAST(prior_cumulative_ref_ord_sched_qty AS DECIMAL(3,1)),
    CAST(apl_qty AS DECIMAL(5,1))
FROM purgo_playground.f_inv_movmnt_apl_qty_test
WHERE txn_id IS NOT NULL;
