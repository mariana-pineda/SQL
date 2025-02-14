-- Use the desired schema
USE purgo_playground;

-- SQL Logic to calculate allocated_qty in the inventory stock management table 'f_order'
-- Allocated quantity is calculated by summing primary_qty, open_qty, shipped_qty, and cancel_qty

-- Create or replace the view to encapsulate the logic
CREATE OR REPLACE VIEW allocated_qty_view AS
SELECT 
    o.order_nbr,
    o.order_line_nbr,
    i.txn_id,
    -- Calculate allocated_qty by summing respective quantity fields
    COALESCE(o.primary_qty, 0) + COALESCE(o.open_qty, 0) + COALESCE(o.shipped_qty, 0) + COALESCE(o.cancel_qty, 0) AS allocated_qty
FROM 
    purgo_playground.f_order o
JOIN 
    purgo_playground.f_inv_movmnt i
ON 
    o.order_nbr = i.txn_id
WHERE 
    o.order_nbr IS NOT NULL 
    AND o.order_line_nbr IS NOT NULL;

-- Enable Delta Lake features for the table
ALTER TABLE purgo_playground.f_order 
SET TBLPROPERTIES (
    "delta.autoOptimize.optimizeWrite" = true,
    "delta.autoOptimize.autoCompact" = true
);

-- Example usage of the view to fetch allocated quantities
SELECT 
    order_nbr,
    order_line_nbr,
    allocated_qty
FROM 
    allocated_qty_view;

-- Additional logic to update f_order table using Delta Lake MERGE operation for allocated quantities
MERGE INTO purgo_playground.f_order AS target
USING (
  SELECT 
    order_nbr, 
    order_line_nbr, 
    COALESCE(primary_qty, 0) + COALESCE(open_qty, 0) + COALESCE(shipped_qty, 0) + COALESCE(cancel_qty, 0) AS calculated_allocated_qty
  FROM 
    purgo_playground.f_order
) AS source
ON target.order_nbr = source.order_nbr AND target.order_line_nbr = source.order_line_nbr
WHEN MATCHED THEN
  UPDATE SET target.allocated_qty = source.calculated_allocated_qty;

-- Error handling and validation logic
-- Example: Log and handle invalid and negative quantities
SELECT 
    order_nbr,
    order_line_nbr,
    -- Check for negative quantities
    CASE 
        WHEN primary_qty < 0 OR open_qty < 0 OR shipped_qty < 0 OR cancel_qty < 0 
        THEN 'Warning: Negative quantity found'
        ELSE 'Quantity valid'
    END AS validation_status
FROM 
    purgo_playground.f_order;

-- Note: Vacuum the f_order table to remove old files and optimize performance
-- Execute this step during maintenance as needed
VACUUM purgo_playground.f_order RETAIN 168 HOURS;

-- Set up Z-ordering based on frequently queried fields
OPTIMIZE purgo_playground.f_order
ZORDER BY (order_nbr, order_line_nbr);

