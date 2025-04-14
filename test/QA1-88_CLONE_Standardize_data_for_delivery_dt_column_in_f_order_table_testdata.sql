-- Test Data Generation for purgo_playground.f_order Table

-- Create a CTE for generating test data with diverse scenarios including happy path, edge cases, and error scenarios
WITH test_data AS (
  SELECT
    'ORD001' AS order_nbr,
    1 AS order_type,
    CAST('20240101' AS DECIMAL(38,0)) AS delivery_dt,  -- valid delivery date
    100 AS order_qty,
    CAST('20240331' AS DECIMAL(38,0)) AS sched_dt,
    CAST('20240501' AS DECIMAL(38,0)) AS expected_shipped_dt,
    CAST('20240502' AS DECIMAL(38,0)) AS actual_shipped_dt,
    'LN001' AS order_line_nbr,
    'LOC001' AS loc_tracker_id,
    '123 Main St, City, Country' AS shipping_add,
    100 AS primary_qty,
    20 AS open_qty,
    80 AS shipped_qty,
    'Normal Order' AS order_desc,
    'N' AS flag_return,
    'N' AS flag_cancel,
    NULL AS cancel_dt,  -- Handling NULL scenario
    NULL AS cancel_qty,
    CAST('2024-03-21T00:00:00.000+0000' AS TIMESTAMP) AS crt_dt,  -- valid timestamp
    CAST('2024-03-22T00:00:00.000+0000' AS TIMESTAMP) AS updt_dt
  UNION ALL
  SELECT
    'ORD002',
    2,
    CAST('20231231' AS DECIMAL(38,0)),  -- edge case: last day of the year
    50,
    CAST('20240101' AS DECIMAL(38,0)),
    CAST('20240110' AS DECIMAL(38,0)),
    CAST('20240112' AS DECIMAL(38,0)),
    'LN002',
    'LOC002',
    '456 Another St, Town, Region',
    50,
    30,
    20,
    'Special Order',
    'Y',
    'N',
    CAST('20240115' AS DECIMAL(38,0)),  -- valid cancellation date
    10,
    CAST('2023-12-31T23:59:59.999+0000' AS TIMESTAMP),  -- edge case: last second of the year
    NULL
  UNION ALL
  SELECT
    'ORD003',
    3,
    CAST('-1' AS DECIMAL(38,0)),  -- error case: negative delivery date format
    NULL AS order_qty,  -- Handling NULL scenario
    CAST('20240215' AS DECIMAL(38,0)),
    CAST('20240301' AS DECIMAL(38,0)),
    CAST('20240305' AS DECIMAL(38,0)),
    NULL AS order_line_nbr,  -- Handling NULL scenario
    'LOC003',
    '789 Boulevard, City-State, Zip',
    70,
    40,
    30,
    NULL AS order_desc,  -- Handling NULL scenario
    'N',
    'Y',
    CAST('-20240201' AS DECIMAL(38,0)),  -- error case: negative cancellation date format
    -5 AS cancel_qty,  -- error case: negative quantity
    CAST(NULL AS TIMESTAMP),  -- Handling NULL scenario
    CAST('INVALID_DATE' AS STRING)  -- error case: invalid timestamp format
)

SELECT * FROM test_data;


Notes:
- The SQL includes a Common Table Expression (CTE) named `test_data` that generates test records covering various scenarios.
- Data types used match the schema for table `purgo_playground.f_order`.
- Happy path, edge cases, and error case scenarios are included (e.g., handling of valid data, edge dates, negative values, and nulls).
- Comments explain each case scenario for clarity.