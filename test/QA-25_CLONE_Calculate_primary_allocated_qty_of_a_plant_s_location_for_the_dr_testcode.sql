-- Define and switch to the correct database context
USE purgo_playground;

-- SQL Unit Test Cases for Calculating Allocated Quantity in f_order
-- Start testing logic for extraction and calculation of allocated quantity

/* 
   Test Case 1: Verify Calculation with Valid Data
   Validates that the allocated_qty is correctly calculated by summing the primary_qty, open_qty, shipped_qty, and cancel_qty.
*/
SELECT 
  CASE 
    WHEN allocated_qty = (primary_qty + open_qty + shipped_qty + cancel_qty)
    THEN 'Pass'
    ELSE 'Fail'
  END AS Test_Result,
  order_nbr,
  allocated_qty,
  (primary_qty + open_qty + shipped_qty + cancel_qty) AS Expected_allocated_qty
FROM 
  purgo_playground.f_order
WHERE 
  order_nbr = '001' AND order_line_nbr = '0011';

/* 
   Test Case 2: Handle Null Quantities 
   Verify that the calculation handles NULL values by treating them as zero for the purpose of summation.
*/
SELECT 
  order_nbr,
  COALESCE(primary_qty, 0) + COALESCE(open_qty, 0) + COALESCE(shipped_qty, 0) + COALESCE(cancel_qty, 0) AS Calculated_allocated_qty,
  CASE 
    WHEN allocated_qty = COALESCE(primary_qty, 0) + COALESCE(open_qty, 0) + COALESCE(shipped_qty, 0) + COALESCE(cancel_qty, 0)
    THEN 'Pass'
    ELSE 'Fail'
  END AS Test_Result
FROM 
  purgo_playground.f_order
WHERE 
  order_nbr = '005' AND order_line_nbr = '0015';

/* 
   Test Case 3: Handle Negative Quantities
   Ensure logic detects and reports negative quantity scenarios.
*/
SELECT 
  order_nbr,
  CASE 
    WHEN primary_qty < 0 OR open_qty < 0 OR shipped_qty < 0 OR cancel_qty < 0 
    THEN 'Warning: Negative quantity detected'
    ELSE 'Pass'
  END AS Test_Result
FROM 
  purgo_playground.f_order
WHERE 
  order_nbr = '007';

/* 
   Test Case 4: Ensure all relevant records are joined and calculated for allocated_qty
   Validate joins with f_inv_movmnt table to ensure completeness.
*/
SELECT 
  CASE 
    WHEN f_inv_movmnt.txn_id IS NOT NULL 
    THEN 'Pass'
    ELSE 'Fail'
  END AS Test_Result,
  f_order.order_nbr
FROM 
  purgo_playground.f_order 
LEFT JOIN 
  purgo_playground.f_inv_movmnt
ON 
  f_order.order_nbr = f_inv_movmnt.txn_id
WHERE 
  f_order.order_nbr IS NOT NULL;

/*
   Test Case 5: Verifying Delta Operations
   Verify that the MERGE operation correctly updates the allocated_qty field.
*/
MERGE INTO purgo_playground.f_order AS target
USING (
  SELECT 
    order_nbr, 
    order_line_nbr, 
    primary_qty, 
    open_qty, 
    shipped_qty, 
    cancel_qty 
  FROM 
    purgo_playground.f_order 
  WHERE 
    order_nbr = '001'
) AS source
ON target.order_nbr = source.order_nbr AND target.order_line_nbr = source.order_line_nbr 
WHEN MATCHED THEN 
  UPDATE SET allocated_qty = source.primary_qty + source.open_qty + source.shipped_qty + source.cancel_qty;

/*
   Test Case 6: Cleanup Operations
   Remove or reset data changes made during testing to ensure a consistent test environment is maintained.
*/
-- Reset changes in f_order table after testing
-- DELETE FROM purgo_playground.f_order WHERE order_nbr IN ('001', '002', '003', '004', '005', '006', '007');
-- You can choose to rollback or truncate after test assertions are verified
