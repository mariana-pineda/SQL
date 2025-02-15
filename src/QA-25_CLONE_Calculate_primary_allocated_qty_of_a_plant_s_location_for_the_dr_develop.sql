-- Calculate allocated_qty for inventory stock management using Databricks SQL
-- This SQL sums up specific quantities to determine the allocated stock 

-- Create the f_order table if it does not exist
CREATE TABLE IF NOT EXISTS purgo_playground.f_order (
  order_nbr STRING,
  order_line_nbr STRING,
  primary_qty DOUBLE,
  open_qty DOUBLE,
  shipped_qty DOUBLE,
  cancel_qty DOUBLE
);

-- Insert sample data into the f_order table for testing
INSERT INTO purgo_playground.f_order (order_nbr, order_line_nbr, primary_qty, open_qty, shipped_qty, cancel_qty)
VALUES 
  ('ORD001', '001', 100.0, 50.0, 30.0, 5.0),
  ('ORD002', '001', 150.0, 70.0, 40.0, 10.0),
  ('ORD003', '002', 120.0, 60.0, 20.0, 0.0),
  ('ORD004', '003', NULL, 30.0, 15.0, 5.0),  -- Represents a record with missing primary_qty
  ('ORD005', '004', -50.0, 20.0, 10.0, 15.0); -- Represents a record with negative primary_qty

-- Select the allocated quantity, handling errors and nulls
SELECT 
  order_nbr, 
  order_line_nbr, 
  CASE 
    WHEN primary_qty IS NULL THEN -1  -- Error indicator: primary quantity is required
    WHEN primary_qty < 0 THEN -1      -- Error indicator: negative primary quantity not allowed
    ELSE COALESCE(primary_qty, 0) + COALESCE(open_qty, 0) + COALESCE(shipped_qty, 0) + COALESCE(cancel_qty, 0)
  END AS allocated_qty
FROM purgo_playground.f_order
WHERE EXISTS (
  SELECT 1 
  FROM purgo_playground.f_inv_movmnt 
  WHERE order_nbr = f_order.order_nbr 
    AND order_line_nbr = f_order.order_line_nbr
);

-- Cleanup the test data after verification
DELETE FROM purgo_playground.f_order WHERE order_nbr IN ('ORD001', 'ORD002', 'ORD003', 'ORD004', 'ORD005');

-- Delta Lake Optimizations (commented for instructional use)
-- ZORDER BY can be used for optimized querying if needed
-- OPTIMIZE purgo_playground.f_order ZORDER BY (order_nbr, order_line_nbr);

-- Vacuum table for cleaning outdated entries when applicable
-- VACUUM purgo_playground.f_order RETAIN 168 HOURS;

-- Set table properties for automatic optimization
-- ALTER TABLE purgo_playground.f_order
-- SET TBLPROPERTIES (
--   'delta.autoOptimize.optimizeWrite' = 'true',
--   'delta.autoOptimize.autoCompact' = 'true'
-- );

-- Example of using a MERGE operation for Delta Lake updates
-- Uncomment to use when source data is available
-- MERGE INTO purgo_playground.f_order AS target
-- USING purgo_playground.f_source AS source
-- ON target.order_nbr = source.order_nbr AND target.order_line_nbr = source.order_line_nbr
-- WHEN MATCHED THEN
--   UPDATE SET
--     target.primary_qty = source.primary_qty,
--     target.open_qty = source.open_qty,
--     target.shipped_qty = source.shipped_qty,
--     target.cancel_qty = source.cancel_qty
-- WHEN NOT MATCHED THEN
--   INSERT (order_nbr, order_line_nbr, primary_qty, open_qty, shipped_qty, cancel_qty)
--   VALUES (source.order_nbr, source.order_line_nbr, source.primary_qty, source.open_qty, source.shipped_qty, source.cancel_qty);
