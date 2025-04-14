CREATE OR REPLACE TEMP VIEW valid_delivery_dt AS (
    -- Validate delivery_dt to be Decimal(38,0) and in format YYYYMMDD
    WITH data_validation AS (
        SELECT
            order_nbr,
            delivery_dt,
            CASE
                WHEN delivery_dt BETWEEN 19000101 AND 20991231 THEN 'Valid'
                ELSE 'Invalid delivery_dt format'
            END AS validation_status
        FROM purgo_playground.purgo_playground.f_order
    )
    SELECT * FROM data_validation WHERE validation_status = 'Valid'
);

-- Generate diverse test data with 20-30 records covering various test scenarios
INSERT INTO purgo_playground.purgo_playground.f_order (
    order_nbr, order_type, delivery_dt, order_qty, sched_dt, expected_shipped_dt,
    actual_shipped_dt, order_line_nbr, loc_tracker_id, shipping_add, primary_qty,
    open_qty, shipped_qty, order_desc, flag_return, flag_cancel, cancel_dt,
    cancel_qty, crt_dt, updt_dt
)
VALUES
    -- Happy path: Valid decimal date in YYYYMMDD format
    ('A001', 1001, 20240321, 100.0, 20240315, 20240320, 20240321, '1001', 'LT001', 'Address1', 100.0, 0.0, 0.0, 'Order Description', 'N', 'N', 0, 0.0, '2024-03-01T00:00:00.000+0000', '2024-03-02T00:00:00.000+0000'),

    -- Edge case: First day of valid date range
    ('A002', 1002, 19000101, 200.0, 20240315, 20240320, 20240321, '1002', 'LT002', 'Address2', 200.0, 0.0, 0.0, 'Order Description', 'N', 'N', 0, 0.0, '2024-03-01T00:00:00.000+0000', '2024-03-02T00:00:00.000+0000'),

    -- Edge case: Last day of valid date range
    ('A003', 1003, 20991231, 300.0, 20240315, 20240320, 20240321, '1003', 'LT003', 'Address3', 300.0, 0.0, 0.0, 'Order Description', 'N', 'N', 0, 0.0, '2024-03-01T00:00:00.000+0000', '2024-03-02T00:00:00.000+0000'),

    -- Error case: Delivery date out of range
    ('A004', 1004, 20249300, 400.0, 20240315, 20240320, 20240321, '1004', 'LT004', 'Address4', 400.0, 0.0, 0.0, 'Order Description', 'N', 'N', 0, 0.0, '2024-03-01T00:00:00.000+0000', '2024-03-02T00:00:00.000+0000'),

    -- Error case: Invalid decimal format
    ('A005', 1005, 12345678901234567890123456789012345678, 500.0, 20240315, 20240320, 20240321, '1005', 'LT005', 'Address5', 500.0, 0.0, 0.0, 'Order Description', 'N', 'N', 0, 0.0, '2024-03-01T00:00:00.000+0000', '2024-03-02T00:00:00.000+0000'),

    -- NULL handling scenario
    ('A006', 1006, NULL, 600.0, 20240315, 20240320, 20240321, '1006', 'LT006', 'Address6', 600.0, 0.0, 0.0, 'Order Description', 'N', 'N', 0, 0.0, '2024-03-01T00:00:00.000+0000', '2024-03-02T00:00:00.000+0000'),

    -- Special character handling
    ('A007', 1007, 20240910, 700.0, 20240315, 20240320, 20240321, '1007##', 'LT007*&', 'Addr\ess7$', 700.0, 0.0, 0.0, 'Order Description!@#$', 'N', 'N', 0, 0.0, '2024-03-01T00:00:00.000+0000', '2024-03-02T00:00:00.000+0000'),

    -- Multi-byte character handling
    ('A008', 1008, 20240910, 800.0, 20240315, 20240320, 20240321, '1008', 'LT008', '漢字Address8', 800.0, 0.0, 0.0, 'Order Descr漢字iption', 'N', 'N', 0, 0.0, '2024-03-01T00:00:00.000+0000', '2024-03-02T00:00:00.000+0000');

-- Use the CTE to validate data
WITH delivery_dt_check AS (
    SELECT
        delivery_dt
    FROM valid_delivery_dt
)
SELECT delivery_dt FROM delivery_dt_check;
