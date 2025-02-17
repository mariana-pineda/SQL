-- Create table for storing allocated quantities calculation results
CREATE TABLE IF NOT EXISTS purgo_playground.allocated_qty_results (
  order_nbr STRING,
  order_line_nbr STRING,
  allocated_qty DOUBLE,
  crt_dt TIMESTAMP DEFAULT CURRENT_TIMESTAMP(),
  updt_dt TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
);

-- Calculate allocated_qty for inventory stock management
INSERT INTO purgo_playground.allocated_qty_results 
SELECT 
  order_nbr, 
  order_line_nbr, 
  -- Calculate allocated_qty by summing up relevant quantities
  CASE 
    WHEN primary_qty IS NULL THEN CAST(NULL AS DOUBLE)  -- Handle missing primary_qty
    WHEN primary_qty < 0 THEN CAST(NULL AS DOUBLE) -- Handle negative primary_qty
    ELSE COALESCE(primary_qty, 0) + COALESCE(open_qty, 0) + COALESCE(shipped_qty, 0) + COALESCE(cancel_qty, 0)
  END AS allocated_qty
FROM purgo_playground.f_order
WHERE EXISTS (
  SELECT 1 
  FROM purgo_playground.f_inv_movmnt
  WHERE f_order.order_nbr = f_inv_movmnt.order_nbr 
    AND f_order.order_line_nbr = f_inv_movmnt.order_line_nbr
);

-- Data quality checks to identify missing or negative primary_qty
SELECT 
  order_nbr, 
  order_line_nbr,
  'Primary quantity is required for allocated quantity calculation' AS error_message
FROM purgo_playground.f_order
WHERE primary_qty IS NULL
UNION
SELECT 
  order_nbr, 
  order_line_nbr,
  'Negative primary quantity is not allowed for allocated quantity calculation' AS error_message
FROM purgo_playground.f_order
WHERE primary_qty < 0;

-- Optimize Delta Table for performance using Z-Ordering
-- Note: This should be run on Databricks environment that supports DELTA optimization
OPTIMIZE purgo_playground.allocated_qty_results
ZORDER BY (order_nbr, order_line_nbr);

-- Schedule vacuum to maintain storage efficiency by removing old versions
-- Note: This should be run on Databricks environment that supports DELTA vacuuming
VACUUM purgo_playground.allocated_qty_results RETAIN 168 HOURS;

