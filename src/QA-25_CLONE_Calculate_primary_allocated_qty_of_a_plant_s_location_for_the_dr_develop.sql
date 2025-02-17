-- Define the schema for f_order table
CREATE TABLE IF NOT EXISTS purgo_playground.f_order (
  order_nbr STRING,
  order_line_nbr STRING,
  primary_qty DOUBLE,
  open_qty DOUBLE,
  shipped_qty DOUBLE,
  cancel_qty DOUBLE,
  allocated_qty DOUBLE -- Allocated_qty as a new column for storing the calculated allocated quantity
);

-- Calculate the allocated_qty using the business logic provided
MERGE INTO purgo_playground.f_order AS target
USING (
  SELECT 
    order_nbr, 
    order_line_nbr, 
    COALESCE(primary_qty, 0) + COALESCE(open_qty, 0) + COALESCE(shipped_qty, 0) + COALESCE(cancel_qty, 0) AS calculated_allocated_qty
  FROM purgo_playground.f_order
  WHERE primary_qty IS NOT NULL AND primary_qty >= 0
) AS source
ON target.order_nbr = source.order_nbr AND target.order_line_nbr = source.order_line_nbr
WHEN MATCHED THEN UPDATE SET
  target.allocated_qty = source.calculated_allocated_qty
WHEN NOT MATCHED THEN 
  INSERT (order_nbr, order_line_nbr, allocated_qty)
  VALUES (source.order_nbr, source.order_line_nbr, source.calculated_allocated_qty);

-- Data validation to ensure allocated_qty is calculated correctly
SELECT 
  order_nbr, 
  order_line_nbr, 
  CASE 
    WHEN primary_qty IS NULL THEN 'Primary quantity is required for allocated quantity calculation'
    WHEN primary_qty < 0 THEN 'Negative primary quantity is not allowed for allocated quantity calculation'
    ELSE CAST(allocated_qty AS STRING)
  END AS allocated_qty
FROM purgo_playground.f_order;

-- Optimizing the Delta table for better query performance
OPTIMIZE purgo_playground.f_order ZORDER BY (order_nbr, order_line_nbr);

-- Vacuum the table for old data cleanup
VACUUM purgo_playground.f_order RETAIN 168 HOURS;  -- Retain for 7 days
