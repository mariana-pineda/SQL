WITH order_test_data AS (
  SELECT
    -- Happy path test data
    'ORD001' AS order_nbr, 
    1 AS order_type, 
    20240910 AS delivery_dt,  -- Valid date
    100.0 AS order_qty, 
    20240321 AS sched_dt, 
    20240401 AS expected_shipped_dt, 
    20240405 AS actual_shipped_dt, 
    'LINE001' AS order_line_nbr, 
    'LOC001' AS loc_tracker_id, 
    '123 Shipping Lane' AS shipping_add, 
    100.0 AS primary_qty, 
    0.0 AS open_qty, 
    100.0 AS shipped_qty, 
    'Standard Order' AS order_desc, 
    'N' AS flag_return, 
    'N' AS flag_cancel, 
    NULL AS cancel_dt, 
    NULL AS cancel_qty, 
    '2024-03-21T00:00:00.000+0000' AS crt_dt, 
    '2024-03-21T00:00:00.000+0000' AS updt_dt

  UNION ALL

  -- Edge case: Maximum boundary for decimal yyyymmdd
  SELECT
    'ORD002', 
    9999, 
    99991231, -- Max valid date
    0.0, 
    NULL,
    NULL, 
    NULL, 
    'LINE002', 
    'LOC002', 
    '456 Shipping Ave', 
    500.0, 
    500.0, 
    0.0, 
    'Express Delivery', 
    'Y', 
    'Y', 
    20240301, 
    50.0, 
    '2024-01-01T00:00:00.000+0000', 
    '2024-01-01T00:00:00.000+0000'

  UNION ALL

  -- Error case: Invalid delivery_dt out of range
  SELECT
    'ORD003', 
    3, 
    20241332, -- Invalid date (13th month)
    -10.0, 
    NULL, 
    NULL, 
    NULL, 
    'LINE003', 
    'LOC003', 
    '789 Shipping Blvd', 
    0.0, 
    10.0, 
    -10.0, 
    'Backordered', 
    'N', 
    'Y', 
    20240515, 
    10.0, 
    '2024-02-15T00:00:00.000+0000', 
    '2024-02-15T00:00:00.000+0000'

  UNION ALL

  -- Null handling scenario
  SELECT
    'ORD004', 
    NULL, 
    NULL, -- Null delivery_dt
    250.0, 
    NULL, 
    NULL, 
    NULL, 
    'LINE004', 
    'LOC004', 
    '234 Shipping Road', 
    250.0, 
    0.0, 
    250.0,
    'Regular Order', 
    'N', 
    'N', 
    NULL, 
    NULL, 
    '2024-04-05T00:00:00.000+0000', 
    '2024-04-05T00:00:00.000+0000'

  UNION ALL

  -- Special characters scenario
  SELECT
    'ORD005', 
    5, 
    20241020, 
    75.0, 
    NULL, 
    NULL, 
    NULL, 
    'LINE005', 
    'LOC005', 
    '890 Special St #$%', -- Special characters in address
    75.0, 
    0.0, 
    75.0, 
    'Special Characters in Desc ñáéíóú', -- Multi-byte characters
    'N', 
    'N', 
    NULL, 
    NULL, 
    '2024-05-05T00:00:00.000+0000', 
    '2024-05-05T00:00:00.000+0000'
)

SELECT * FROM order_test_data

