-- Install necessary libraries for Databricks environment
-- %pip install [library] -- Uncomment and specify library if needed

/* 
  Create table 'f_order' to store the order records 
  Ensure schema is validated with expected data types 
*/
CREATE TABLE IF NOT EXISTS purgo_playground.f_order (
  order_nbr STRING,
  order_line_nbr STRING,
  primary_qty DOUBLE,
  open_qty DOUBLE,
  shipped_qty DOUBLE,
  cancel_qty DOUBLE
);

/* 
  Calculate allocated_qty 
  - Ensure error handling for missing or negative primary_qty 
  - Use COALESCE to handle NULLs, ensuring zero is used when values are not provided 
*/
SELECT 
  order_nbr, 
  order_line_nbr, 
  CASE 
    WHEN primary_qty IS NULL THEN RAISE_ERROR('Primary quantity is required for allocated quantity calculation')
    WHEN primary_qty < 0 THEN RAISE_ERROR('Negative primary quantity is not allowed for allocated quantity calculation')
    ELSE COALESCE(primary_qty, 0) + COALESCE(open_qty, 0) + COALESCE(shipped_qty, 0) + COALESCE(cancel_qty, 0)
  END AS allocated_qty
FROM purgo_playground.f_order
WHERE EXISTS (
  SELECT 1 
  FROM purgo_playground.f_inv_movmnt 
  WHERE order_nbr = f_order.order_nbr 
    AND order_line_nbr = f_order.order_line_nbr
);

/* Consider adding partitioning or optimizing strategies here if needed */

/* 
  Cleanup test data from 'f_order' table to ensure isolation for this calculation process 
*/
DELETE FROM purgo_playground.f_order WHERE order_nbr IN ('ORD001', 'ORD002', 'ORD003', 'ORD004', 'ORD005');
