-- Create temporary view to calculate allocated quantities based on criteria
CREATE OR REPLACE TEMP VIEW allocated_qty_calc AS
SELECT 
  order_nbr, 
  order_line_nbr,
  -- Calculate allocated quantity with error handling for missing or negative primary_qty
  CASE 
    WHEN primary_qty IS NULL THEN RAISE_ERROR("Primary quantity is required for allocated quantity calculation")
    WHEN primary_qty < 0 THEN RAISE_ERROR("Negative primary quantity is not allowed for allocated quantity calculation")
    ELSE COALESCE(primary_qty, 0) + COALESCE(open_qty, 0) + COALESCE(shipped_qty, 0) + COALESCE(cancel_qty, 0)
  END AS allocated_qty
FROM 
  purgo_playground.f_order
WHERE 
  EXISTS (
    -- Ensure the order exists in the f_inv_movmnt table for integrity
    SELECT 1 
    FROM purgo_playground.f_inv_movmnt 
    WHERE order_nbr = f_order.order_nbr 
      AND order_line_nbr = f_order.order_line_nbr
  );

-- Create or replace the table to store allocated quantities
CREATE TABLE IF NOT EXISTS purgo_playground.f_order_allocated_qty (
  order_nbr STRING,
  order_line_nbr STRING,
  allocated_qty DOUBLE
);

-- Insert calculated allocated_qty into the target table
INSERT INTO purgo_playground.f_order_allocated_qty
SELECT * FROM allocated_qty_calc;

-- Optimize the table for better performance using ZORDER
OPTIMIZE purgo_playground.f_order_allocated_qty
ZORDER BY (order_nbr, order_line_nbr);

-- Optionally run vacuum to remove old versions, retaining data for 168 hours
VACUUM purgo_playground.f_order_allocated_qty RETAIN 168 HOURS;
