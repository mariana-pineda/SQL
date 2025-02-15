-- Install necessary libraries for Databricks environment
-- %pip install [library] -- Uncomment and specify library if needed

/* Schema validation for f_order table */
CREATE TABLE IF NOT EXISTS purgo_playground.f_order (
  order_nbr STRING,
  order_line_nbr STRING,
  primary_qty DOUBLE,
  open_qty DOUBLE,
  shipped_qty DOUBLE,
  cancel_qty DOUBLE
);

/* Test calculation of allocated_qty including error handling for missing or invalid data */
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

/* Cleanup the test data after validation */
DELETE FROM purgo_playground.f_order WHERE order_nbr IN ('ORD001', 'ORD002', 'ORD003', 'ORD004', 'ORD005');

