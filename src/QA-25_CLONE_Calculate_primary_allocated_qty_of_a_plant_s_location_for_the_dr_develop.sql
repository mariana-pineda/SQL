-- SQL logic to calculate allocated_qty in the inventory stock management table 'f_order'

-- Calculate allocated quantities
SELECT 
  fo.order_nbr, 
  fo.order_line_nbr, 
  -- Error handling for missing or invalid primary_qty
  CASE 
    WHEN fo.primary_qty IS NULL THEN RAISE_ERROR("Primary quantity is required for allocated quantity calculation")
    WHEN fo.primary_qty < 0 THEN RAISE_ERROR("Negative primary quantity is not allowed for allocated quantity calculation")
    -- Calculate allocated_qty by summing up relevant quantities
    ELSE COALESCE(fo.primary_qty, 0) 
        + COALESCE(fo.open_qty, 0) 
        + COALESCE(fo.shipped_qty, 0) 
        + COALESCE(fo.cancel_qty, 0)
  END AS allocated_qty
FROM purgo_playground.f_order fo
WHERE EXISTS (
  -- Ensure the corresponding entry exists in the f_inv_movmnt table
  SELECT 1 
  FROM purgo_playground.f_inv_movmnt 
  WHERE order_nbr = fo.order_nbr 
    AND order_line_nbr = fo.order_line_nbr
);

/*
  Assumptions and Logic:
  - Each entry in 'f_order' must have a corresponding entry in 'f_inv_movmnt'
  - allocated_qty is calculated as the sum of primary_qty, open_qty, shipped_qty, and cancel_qty
  - Missing or negative primary_qty raises an error
  - COALESCE function is used to handle NULL values, treating them as 0 during summation
  - Implementation logs errors appropriately in case of missing or negative quantities
  - Regular maintenance should include optimization procedures such as VACUUM and Z-ordering for Delta tables
*/
