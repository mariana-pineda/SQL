-- Test Data Generation for purgo_playground.f_order

WITH test_data AS (
    SELECT 
        'ORDER001' AS order_nbr, 
        1 AS order_type, 
        CAST(20240910 AS DECIMAL(38,0)) AS delivery_dt, 
        100.0 AS order_qty, 
        CAST(20240801 AS DECIMAL(38,0)) AS sched_dt, 
        CAST(20240805 AS DECIMAL(38,0)) AS expected_shipped_dt, 
        CAST(20240804 AS DECIMAL(38,0)) AS actual_shipped_dt, 
        'LINE001' AS order_line_nbr, 
        'LOC001' AS loc_tracker_id, 
        '1234 Elm Street' AS shipping_add, 
        100.0 AS primary_qty, 
        0.0 AS open_qty, 
        100.0 AS shipped_qty, 
        'Standard Order' AS order_desc, 
        'N' AS flag_return, 
        'N' AS flag_cancel, 
        CAST(0 AS DECIMAL(38,0)) AS cancel_dt, 
        0.0 AS cancel_qty, 
        TIMESTAMP '2024-04-01T10:00:00.000+0000' AS crt_dt, 
        TIMESTAMP '2024-04-01T12:00:00.000+0000' AS updt_dt
    
    UNION ALL
    
    -- Delivery_dt with invalid format (yyyy-MM-dd)
    SELECT 
        'ORDER002', 
        2, 
        CAST('2024-09-10' AS DECIMAL(38,0)), 
        200.0, 
        CAST(20240802 AS DECIMAL(38,0)), 
        CAST(20240806 AS DECIMAL(38,0)), 
        CAST(20240805 AS DECIMAL(38,0)), 
        'LINE002', 
        'LOC002', 
        '5678 Oak Avenue', 
        200.0, 
        10.0, 
        190.0, 
        'Express Order', 
        'Y', 
        'N', 
        CAST(0 AS DECIMAL(38,0)), 
        0.0, 
        TIMESTAMP '2024-04-02T11:00:00.000+0000', 
        TIMESTAMP '2024-04-02T13:00:00.000+0000'
    
    UNION ALL
    
    -- Delivery_dt with invalid length
    SELECT 
        'ORDER003', 
        3, 
        CAST(2024091 AS DECIMAL(38,0)), 
        150.0, 
        CAST(20240803 AS DECIMAL(38,0)), 
        CAST(20240807 AS DECIMAL(38,0)), 
        CAST(20240806 AS DECIMAL(38,0)), 
        'LINE003', 
        'LOC003', 
        '9101 Pine Road', 
        150.0, 
        5.0, 
        145.0, 
        'Bulk Order', 
        'N', 
        'Y', 
        CAST(20240910 AS DECIMAL(38,0)), 
        5.0, 
        TIMESTAMP '2024-04-03T09:30:00.000+0000', 
        TIMESTAMP '2024-04-03T10:30:00.000+0000'
    
    UNION ALL
    
    -- Delivery_dt with extra digit
    SELECT 
        'ORDER004', 
        4, 
        CAST(202409100 AS DECIMAL(38,0)), 
        250.0, 
        CAST(20240804 AS DECIMAL(38,0)), 
        CAST(20240808 AS DECIMAL(38,0)), 
        CAST(20240807 AS DECIMAL(38,0)), 
        'LINE004', 
        'LOC004', 
        '🏠 2345 Maple Street', 
        250.0, 
        20.0, 
        230.0, 
        'Special Order 🚀', 
        'Y', 
        'Y', 
        CAST(20240910 AS DECIMAL(38,0)), 
        20.0, 
        TIMESTAMP '2024-04-04T14:00:00.000+0000', 
        TIMESTAMP '2024-04-04T16:00:00.000+0000'
    
    UNION ALL
    
    -- Delivery_dt as string in decimal
    SELECT 
        'ORDER005', 
        5, 
        CAST('20240910' AS DECIMAL(38,0)), 
        300.0, 
        CAST(20240805 AS DECIMAL(38,0)), 
        CAST(20240809 AS DECIMAL(38,0)), 
        CAST(20240808 AS DECIMAL(38,0)), 
        'LINE005', 
        'LOC005', 
        '6789 Birch Boulevard', 
        300.0, 
        0.0, 
        300.0, 
        'International Order', 
        'N', 
        'N', 
        CAST(0 AS DECIMAL(38,0)), 
        0.0, 
        TIMESTAMP '2024-04-05T08:45:00.000+0000', 
        TIMESTAMP '2024-04-05T09:45:00.000+0000'
    
    UNION ALL
    
    -- Delivery_dt is NULL
    SELECT 
        'ORDER006', 
        6, 
        NULL, 
        120.0, 
        CAST(20240806 AS DECIMAL(38,0)), 
        CAST(20240810 AS DECIMAL(38,0)), 
        CAST(20240809 AS DECIMAL(38,0)), 
        'LINE006', 
        'LOC006', 
        '1357 Cedar Lane', 
        120.0, 
        15.0, 
        105.0, 
        'Return Order', 
        'Y', 
        'N', 
        CAST(0 AS DECIMAL(38,0)), 
        15.0, 
        TIMESTAMP '2024-04-06T07:20:00.000+0000', 
        TIMESTAMP '2024-04-06T08:20:00.000+0000'
    
    UNION ALL
    
    -- Delivery_dt with invalid month
    SELECT 
        'ORDER007', 
        7, 
        CAST(20243101 AS DECIMAL(38,0)), 
        130.0, 
        CAST(20240807 AS DECIMAL(38,0)), 
        CAST(20240811 AS DECIMAL(38,0)), 
        CAST(20240810 AS DECIMAL(38,0)), 
        'LINE007', 
        'LOC007', 
        '2468 Spruce Street', 
        130.0, 
        10.0, 
        120.0, 
        'Invalid Month Order', 
        'N', 
        'Y', 
        CAST(20243101 AS DECIMAL(38,0)), 
        10.0, 
        TIMESTAMP '2024-04-07T10:10:00.000+0000', 
        TIMESTAMP '2024-04-07T12:10:00.000+0000'
    
    UNION ALL
    
    -- Delivery_dt with invalid day and month
    SELECT 
        'ORDER008', 
        8, 
        CAST(20240000 AS DECIMAL(38,0)), 
        140.0, 
        CAST(20240808 AS DECIMAL(38,0)), 
        CAST(20240812 AS DECIMAL(38,0)), 
        CAST(20240811 AS DECIMAL(38,0)), 
        'LINE008', 
        'LOC008', 
        '🛒 3579 Walnut Avenue', 
        140.0, 
        20.0, 
        120.0, 
        'Invalid Date Order', 
        'Y', 
        'Y', 
        CAST(20240000 AS DECIMAL(38,0)), 
        20.0, 
        TIMESTAMP '2024-04-08T13:30:00.000+0000', 
        TIMESTAMP '2024-04-08T15:30:00.000+0000'
    
    UNION ALL
    
    -- Valid delivery_dt with boundary date
    SELECT 
        'ORDER009', 
        9, 
        CAST(20240229 AS DECIMAL(38,0)), 
        160.0, 
        CAST(20240809 AS DECIMAL(38,0)), 
        CAST(20240813 AS DECIMAL(38,0)), 
        CAST(20240812 AS DECIMAL(38,0)), 
        'LINE009', 
        'LOC009', 
        '4680 Poplar Drive', 
        160.0, 
        0.0, 
        160.0, 
        'Leap Year Order', 
        'N', 
        'N', 
        CAST(0 AS DECIMAL(38,0)), 
        0.0, 
        TIMESTAMP '2024-04-09T16:45:00.000+0000', 
        TIMESTAMP '2024-04-09T18:45:00.000+0000'
    
    UNION ALL
    
    -- Delivery_dt with multi-byte characters in string fields
    SELECT 
        'ORDER010', 
        10, 
        CAST(20240910 AS DECIMAL(38,0)), 
        180.0, 
        CAST(20240810 AS DECIMAL(38,0)), 
        CAST(20240814 AS DECIMAL(38,0)), 
        CAST(20240813 AS DECIMAL(38,0)), 
        'LINE010', 
        'LOC010', 
        '🏡 5790 Cherry Blvd', 
        180.0, 
        5.0, 
        175.0, 
        'Unicode Order 🚚', 
        'Y', 
        'N', 
        CAST(0 AS DECIMAL(38,0)), 
        5.0, 
        TIMESTAMP '2024-04-10T19:00:00.000+0000', 
        TIMESTAMP '2024-04-10T21:00:00.000+0000'
    
    UNION ALL
    
    -- Additional valid records for comprehensive coverage
    SELECT 
        'ORDER011', 
        11, 
        CAST(20240315 AS DECIMAL(38,0)), 
        210.0, 
        CAST(20240811 AS DECIMAL(38,0)), 
        CAST(20240815 AS DECIMAL(38,0)), 
        CAST(20240814 AS DECIMAL(38,0)), 
        'LINE011', 
        'LOC011', 
        '6812 Willow Way', 
        210.0, 
        10.0, 
        200.0, 
        'Seasonal Order', 
        'N', 
        'Y', 
        CAST(20240315 AS DECIMAL(38,0)), 
        10.0, 
        TIMESTAMP '2024-04-11T07:15:00.000+0000', 
        TIMESTAMP '2024-04-11T09:15:00.000+0000'
    
    UNION ALL
    
    SELECT 
        'ORDER012', 
        12, 
        CAST(20240420 AS DECIMAL(38,0)), 
        220.0, 
        CAST(20240812 AS DECIMAL(38,0)), 
        CAST(20240816 AS DECIMAL(38,0)), 
        CAST(20240815 AS DECIMAL(38,0)), 
        'LINE012', 
        'LOC012', 
        '7923 Aspen Circle', 
        220.0, 
        0.0, 
        220.0, 
        'Holiday Order', 
        'Y', 
        'N', 
        CAST(0 AS DECIMAL(38,0)), 
        0.0, 
        TIMESTAMP '2024-04-12T10:25:00.000+0000', 
        TIMESTAMP '2024-04-12T12:25:00.000+0000'
    
    UNION ALL
    
    SELECT 
        'ORDER013', 
        13, 
        CAST(20240525 AS DECIMAL(38,0)), 
        230.0, 
        CAST(20240813 AS DECIMAL(38,0)), 
        CAST(20240817 AS DECIMAL(38,0)), 
        CAST(20240816 AS DECIMAL(38,0)), 
        'LINE013', 
        'LOC013', 
        '9034 Cypress Lane', 
        230.0, 
        5.0, 
        225.0, 
        'Promotional Order', 
        'N', 
        'Y', 
        CAST(20240525 AS DECIMAL(38,0)), 
        5.0, 
        TIMESTAMP '2024-04-13T13:35:00.000+0000', 
        TIMESTAMP '2024-04-13T15:35:00.000+0000'
    
    UNION ALL
    
    SELECT 
        'ORDER014', 
        14, 
        CAST(20240630 AS DECIMAL(38,0)), 
        240.0, 
        CAST(20240814 AS DECIMAL(38,0)), 
        CAST(20240818 AS DECIMAL(38,0)), 
        CAST(20240817 AS DECIMAL(38,0)), 
        'LINE014', 
        'LOC014', 
        '📦 1045 Maple Street', 
        240.0, 
        10.0, 
        230.0, 
        'Bulk Purchase Order', 
        'Y', 
        'N', 
        CAST(0 AS DECIMAL(38,0)), 
        10.0, 
        TIMESTAMP '2024-04-14T16:50:00.000+0000', 
        TIMESTAMP '2024-04-14T18:50:00.000+0000'
    
    UNION ALL
    
    SELECT 
        'ORDER015', 
        15, 
        CAST(20240705 AS DECIMAL(38,0)), 
        250.0, 
        CAST(20240815 AS DECIMAL(38,0)), 
        CAST(20240819 AS DECIMAL(38,0)), 
        CAST(20240818 AS DECIMAL(38,0)), 
        'LINE015', 
        'LOC015', 
        '1156 Pineapple Drive', 
        250.0, 
        0.0, 
        250.0, 
        'Final Order', 
        'N', 
        'N', 
        CAST(0 AS DECIMAL(38,0)), 
        0.0, 
        TIMESTAMP '2024-04-15T19:05:00.000+0000', 
        TIMESTAMP '2024-04-15T21:05:00.000+0000'
    
    UNION ALL
    
    -- Additional records to reach 20
    SELECT 
        'ORDER016', 
        16, 
        CAST(20240810 AS DECIMAL(38,0)), 
        260.0, 
        CAST(20240816 AS DECIMAL(38,0)), 
        CAST(20240820 AS DECIMAL(38,0)), 
        CAST(20240819 AS DECIMAL(38,0)), 
        'LINE016', 
        'LOC016', 
        '1267 Oakwood Blvd', 
        260.0, 
        15.0, 
        245.0, 
        'Special Handling Order', 
        'Y', 
        'Y', 
        CAST(20240810 AS DECIMAL(38,0)), 
        15.0, 
        TIMESTAMP '2024-04-16T07:30:00.000+0000', 
        TIMESTAMP '2024-04-16T09:30:00.000+0000'
    
    UNION ALL
    
    SELECT 
        'ORDER017', 
        17, 
        CAST(20240910 AS DECIMAL(38,0)), 
        270.0, 
        CAST(20240817 AS DECIMAL(38,0)), 
        CAST(20240821 AS DECIMAL(38,0)), 
        CAST(20240820 AS DECIMAL(38,0)), 
        'LINE017', 
        'LOC017', 
        '1378 Palm Street', 
        270.0, 
        5.0, 
        265.0, 
        'Urgent Order', 
        'N', 
        'Y', 
        CAST(20240910 AS DECIMAL(38,0)), 
        5.0, 
        TIMESTAMP '2024-04-17T10:40:00.000+0000', 
        TIMESTAMP '2024-04-17T12:40:00.000+0000'
    
    UNION ALL
    
    SELECT 
        'ORDER018', 
        18, 
        CAST(20241015 AS DECIMAL(38,0)), 
        280.0, 
        CAST(20240818 AS DECIMAL(38,0)), 
        CAST(20240822 AS DECIMAL(38,0)), 
        CAST(20240821 AS DECIMAL(38,0)), 
        'LINE018', 
        'LOC018', 
        '1489 Cypress Circle', 
        280.0, 
        0.0, 
        280.0, 
        'Last Minute Order', 
        'Y', 
        'N', 
        CAST(0 AS DECIMAL(38,0)), 
        0.0, 
        TIMESTAMP '2024-04-18T13:55:00.000+0000', 
        TIMESTAMP '2024-04-18T15:55:00.000+0000'
    
    UNION ALL
    
    SELECT 
        'ORDER019', 
        19, 
        CAST(20241120 AS DECIMAL(38,0)), 
        290.0, 
        CAST(20240819 AS DECIMAL(38,0)), 
        CAST(20240823 AS DECIMAL(38,0)), 
        CAST(20240822 AS DECIMAL(38,0)), 
        'LINE019', 
        'LOC019', 
        '1590 Spruce Avenue', 
        290.0, 
        10.0, 
        280.0, 
        'Overflow Order', 
        'N', 
        'Y', 
        CAST(20241120 AS DECIMAL(38,0)), 
        10.0, 
        TIMESTAMP '2024-04-19T16:10:00.000+0000', 
        TIMESTAMP '2024-04-19T18:10:00.000+0000'
    
    UNION ALL
    
    SELECT 
        'ORDER020', 
        20, 
        CAST(20241225 AS DECIMAL(38,0)), 
        300.0, 
        CAST(20240820 AS DECIMAL(38,0)), 
        CAST(20240824 AS DECIMAL(38,0)), 
        CAST(20240823 AS DECIMAL(38,0)), 
        'LINE020', 
        'LOC020', 
        '🐱‍🏍 1701 Fir Street', 
        300.0, 
        20.0, 
        280.0, 
        'Final Mega Order 🌟', 
        'Y', 
        'Y', 
        CAST(20241225 AS DECIMAL(38,0)), 
        20.0, 
        TIMESTAMP '2024-04-20T19:25:00.000+0000', 
        TIMESTAMP '2024-04-20T21:25:00.000+0000'
)

INSERT INTO purgo_playground.f_order
SELECT 
    order_nbr,
    order_type,
    delivery_dt,
    order_qty,
    sched_dt,
    expected_shipped_dt,
    actual_shipped_dt,
    order_line_nbr,
    loc_tracker_id,
    shipping_add,
    primary_qty,
    open_qty,
    shipped_qty,
    order_desc,
    flag_return,
    flag_cancel,
    cancel_dt,
    cancel_qty,
    crt_dt,
    updt_dt
FROM test_data;
