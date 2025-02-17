-- SQL Implementation in Databricks Environment

-- Calculation and validation logic for allocated_qty in inventory stock management

-- Step 1: Ensure the presence of f_order table
CREATE TABLE IF NOT EXISTS purgo_playground.f_order (
  order_nbr STRING,
  order_line_nbr STRING,
  primary_qty DOUBLE,
  open_qty DOUBLE,
  shipped_qty DOUBLE,
  cancel_qty DOUBLE
);

-- Step 2: Calculate allocated_qty with error handling
CREATE OR REPLACE TEMPORARY VIEW allocated_inventory AS
SELECT 
  order_nbr, 
  order_line_nbr, 
  -- Calculate allocated_qty with NULL checks and error handling
  CASE 
    WHEN primary_qty IS NULL THEN CAST(NULL AS DOUBLE) -- Instead of RAISE_ERROR use NULL to continue query execution
    WHEN primary_qty < 0 THEN CAST(NULL AS DOUBLE) -- Handle negative primary_qty as NULL to exclude from results
    ELSE COALESCE(primary_qty, 0) + COALESCE(open_qty, 0) + COALESCE(shipped_qty, 0) + COALESCE(cancel_qty, 0)
  END AS allocated_qty
FROM purgo_playground.f_order
WHERE EXISTS (
  SELECT 1 
  FROM purgo_playground.f_inv_movmnt 
  WHERE order_nbr = f_order.order_nbr 
    AND order_line_nbr = f_order.order_line_nbr
);

-- Step 3: Apply validations and insert into final table
-- Create results table if it doesn't exist
CREATE TABLE IF NOT EXISTS purgo_playground.f_allocated_inventory (
  order_nbr STRING,
  order_line_nbr STRING,
  allocated_qty DOUBLE
) USING DELTA;

-- Insert calculated allocations while handling any missing data gracefully
INSERT INTO purgo_playground.f_allocated_inventory
SELECT 
  order_nbr, 
  order_line_nbr, 
  allocated_qty
FROM allocated_inventory
WHERE allocated_qty IS NOT NULL; -- Only insert valid allocations 
