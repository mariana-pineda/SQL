-- Switch to the relevant database
USE purgo_playground;

-- SQL logic to calculate allocated_qty in the inventory stock management table 'f_order'

/*
   Calculate the allocated quantity for each order in the 'f_order' table by summing the 
   primary_qty, open_qty, shipped_qty, and cancel_qty. The results are stored in the 
   allocated_qty field.
*/

-- Create or replace temporary view to calculate allocated_qty
CREATE OR REPLACE TEMPORARY VIEW f_order_allocated AS
SELECT 
    o.order_nbr, 
    o.order_line_nbr,
    /* Calculate allocated_qty by summing primary_qty, open_qty, shipped_qty, and cancel_qty */
    COALESCE(o.primary_qty, 0) + 
    COALESCE(o.open_qty, 0) + 
    COALESCE(o.shipped_qty, 0) + 
    COALESCE(o.cancel_qty, 0) AS allocated_qty
FROM 
    purgo_playground.f_order o
JOIN 
    purgo_playground.f_inv_movmnt i
ON 
    o.order_nbr = i.txn_id
WHERE 
    o.order_nbr IS NOT NULL 
    AND o.order_line_nbr IS NOT NULL;

/*
   Perform Delta Lake operations for data versioning and optimization
   MERGE can be used to update existing records when necessary.
*/

/* Define the merge operation to update the 'allocated_qty' in the table */
MERGE INTO purgo_playground.f_order AS target
USING f_order_allocated AS source
ON 
    target.order_nbr = source.order_nbr 
    AND target.order_line_nbr = source.order_line_nbr
WHEN MATCHED THEN 
    UPDATE SET 
        target.allocated_qty = source.allocated_qty;

/*
   Data quality and validation checks for NULL values and negative quantity scenarios
   Ensure allocated_qty does not fall into invalid value ranges
*/
SELECT 
    order_nbr,
    allocated_qty,
    CASE 
        WHEN COALESCE(allocated_qty, 0) < 0 THEN 'Warning: Negative quantity detected'
        ELSE 'Pass'
    END AS Validation_Status
FROM 
    purgo_playground.f_order
WHERE 
    order_nbr IS NOT NULL;

-- If VACUUM is required, ensure correct syntax and that the command is appropriate for your environment
-- Note: Direct execution of VACUUM might not be supported in a SQL block; it usually needs to be run separately or with special permissions

-- OPTIMIZE operation can be used without triggering syntax errors if run separately
-- Uncomment and adjust the following line if necessary, and ensure permissions support this operation:
-- OPTIMIZE purgo_playground.f_order ZORDER BY (order_nbr, order_line_nbr);
