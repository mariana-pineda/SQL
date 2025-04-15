WITH test_data AS (
  SELECT 
    -- Happy path test data
    "ORD123456" AS order_nbr, 
    1 AS order_type, 
    20240910 AS delivery_dt, -- Valid Decimal format yyyymmdd
    10.5 AS order_qty, 
    20240915 AS sched_dt, 
    20240916 AS expected_shipped_dt, 
    20240917 AS actual_shipped_dt, 
    "LINE1234" AS order_line_nbr, 
    "LOC987654" AS loc_tracker_id, 
    "123 Main St, Anytown, USA" AS shipping_add, 
    10.5 AS primary_qty, 
    5.0 AS open_qty, 
    5.5 AS shipped_qty, 
    "Sample order description" AS order_desc, 
    "N" AS flag_return, 
    "N" AS flag_cancel, 
    20240920 AS cancel_dt, 
    0.0 AS cancel_qty, 
    "2024-03-21T00:00:00.000+0000" AS crt_dt, 
    "2024-03-25T00:00:00.000+0000" AS updt_dt
  UNION ALL
  -- Edge case: Maximum decimal value for delivery_dt
  SELECT 
    "ORD999999", 
    1, 
    99991231, 
    1.0, 
    99991230, 
    99991231, 
    99991232, 
    "LINE9999", 
    "LOC999999", 
    "456 Elm St, Somecity, USA", 
    1.0, 
    1.0, 
    0.0, 
    "Edge case order", 
    "Y", 
    "Y", 
    99991230, 
    1.0,  
    "9999-12-31T00:00:00.000+0000", 
    "9999-12-31T00:00:00.000+0000"
  UNION ALL
  -- Error case: Invalid format (string instead of decimal for delivery_dt)
  SELECT 
    "ORD543210", 
    2, 
    CAST(NULL AS BIGINT), -- Invalid - should be NULL
    2.0, 
    20240101, 
    20240102, 
    20240103, 
    "LINE4321", 
    "LOC543210", 
    "789 Oak St, Anycity, USA", 
    2.0, 
    1.0, 
    1.0, 
    "Another sample order", 
    "N", 
    "N", 
    20240105, 
    1.0,  
    "2024-05-01T00:00:00.000+0000", 
    "2024-05-05T00:00:00.000+0000"
  UNION ALL
  -- Error case: delivery_dt as NULL
  SELECT 
    "ORD654321", 
    3, 
    NULL, -- NULL handling
    3.5, 
    NULL, 
    20241212, 
    20241213, 
    "LINE5432", 
    "LOC654321", 
    "000 Anywhere St, Nomansland", 
    0.5, 
    NULL, 
    3.0, 
    "NULL delivery date test", 
    "Y", 
    "Y", 
    20241210, 
    1.0,  
    "2024-06-06T00:00:00.000+0000", 
    "2024-06-10T00:00:00.000+0000"
  UNION ALL
  -- Special characters and multi-byte characters
  SELECT 
    "ORD한글123", 
    4, 
    20240707, 
    4.0, 
    20240701, 
    20240702, 
    20240703, 
    "LINE특수123", 
    "LOC特殊5432", 
    "세계 정복 Street, Earth", 
    4.0, 
    0.0, 
    4.0, 
    "Multi-byte character test", 
    "N", 
    "N", 
    NULL, 
    NULL,
    "2024-07-07T00:00:00.000+0000", 
    "2024-07-08T00:00:00.000+0000"
)
SELECT * FROM test_data

