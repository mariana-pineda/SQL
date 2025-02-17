-- Calculate allocated_qty and create a view for allocated quantities

/* Create or replace a view to calculate allocated_qty from f_order */
CREATE OR REPLACE VIEW purgo_playground.v_allocated_qty AS
SELECT 
  f_order.order_nbr,
  f_order.order_line_nbr,
  -- Calculate allocated_qty by summing the quantities, with error handling
  CASE
    WHEN f_order.primary_qty IS NULL THEN RAISE_ERROR('Primary quantity is required for allocated quantity calculation')
    WHEN f_order.primary_qty < 0 THEN RAISE_ERROR('Negative primary quantity is not allowed for allocated quantity calculation')
    ELSE COALESCE(f_order.primary_qty, 0) + COALESCE(f_order.open_qty, 0) + COALESCE(f_order.shipped_qty, 0) + COALESCE(f_order.cancel_qty, 0)
  END AS allocated_qty
FROM purgo_playground.f_order
WHERE EXISTS (
  -- Check if the order exists in the inventory movements table
  SELECT 1 
  FROM purgo_playground.f_inv_movmnt
  WHERE f_inv_movmnt.order_nbr = f_order.order_nbr 
    AND f_inv_movmnt.order_line_nbr = f_order.order_line_nbr
);

/* Select from the defined view to get the allocated_qty */
SELECT * FROM purgo_playground.v_allocated_qty;

/* Use Delta Lake features for updates and inserts using MERGE */
MERGE INTO purgo_playground.f_order_allocated_delta AS target
USING purgo_playground.v_allocated_qty AS source
ON target.order_nbr = source.order_nbr
  AND target.order_line_nbr = source.order_line_nbr
WHEN MATCHED THEN
  -- Update the allocated_qty if there's a match
  UPDATE SET target.allocated_qty = source.allocated_qty,
             target.updt_dt = current_timestamp()
WHEN NOT MATCHED THEN
  -- Insert new records if no match found
  INSERT (order_nbr, order_line_nbr, allocated_qty, crt_dt, updt_dt)
  VALUES (source.order_nbr, source.order_line_nbr, source.allocated_qty, current_timestamp(), current_timestamp());

/* Optimize the Delta table with Z-ordering for better performance */
OPTIMIZE purgo_playground.f_order_allocated_delta ZORDER BY (order_nbr, order_line_nbr);

/* Clean up old data in the Delta table to save storage space */
VACUUM purgo_playground.f_order_allocated_delta RETAIN 168 HOURS;

/* Insert warnings into system logs */
INSERT INTO system_logs (log_message, log_timestamp)
SELECT 'Inventory data might be outdated', current_timestamp()
WHERE NOT EXISTS (
  -- Check if the inventory data is updated recently
  SELECT 1 
  FROM purgo_playground.f_inv_movmnt 
  WHERE updt_dt > date_sub(current_timestamp(), 1)
);
