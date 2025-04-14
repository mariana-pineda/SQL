-- SQL Logic to Validate delivery_dt in the f_order Table
-- Ensure delivery_dt is 100% Decimal (38,0) and in yyyymmdd format

-- Setup Validation CTE
WITH delivery_dt_validation AS (
    SELECT
        order_nbr,
        delivery_dt,
        CASE
            -- Check if delivery_dt is within valid range for yyyymmdd format
            WHEN delivery_dt BETWEEN 19000101 AND 20991231 THEN 'Valid'
            ELSE 'Invalid delivery_dt format'
        END AS validation_status
    FROM purgo_playground.f_order
)

-- Query to Select and Validate delivery_dt
-- Ensure only valid records are processed further
SELECT
    order_nbr,
    delivery_dt
FROM
    delivery_dt_validation
WHERE
    validation_status = 'Valid';

-- Cleanup operations could be added if necessary
