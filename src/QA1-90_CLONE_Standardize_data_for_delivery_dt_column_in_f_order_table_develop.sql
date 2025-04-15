-- Validate if delivery_dt is in the correct Decimal(38,0) format in yyyymmdd
WITH validation_cte AS (
    SELECT
        delivery_dt
    FROM purgo_playground.purgo_playground.f_order
    WHERE CAST(delivery_dt AS STRING) NOT REGEXP "^[0-9]{8}$"
)
-- Assert that no records exist in validation_cte for invalid delivery_dt format
SELECT COUNT(*) AS error_count FROM validation_cte;

-- Conversion logic: Convert delivery_dt from timestamp to Decimal(38,0) formatted as yyyymmdd
WITH valid_format_cte AS (
    SELECT
        order_nbr,
        CAST(DATE_FORMAT(CAST(delivery_dt AS TIMESTAMP), "yyyyMMdd") AS DECIMAL(38,0)) AS converted_delivery_dt
    FROM purgo_playground.purgo_playground.f_order
    WHERE delivery_dt IS NOT NULL AND CAST(delivery_dt AS STRING) REGEXP "^[0-9]{8}$"
)
-- Integration step: Inserting valid records
INSERT INTO purgo_playground.purgo_playground.dq_reports (Order_ID, Mandatory_Fields_Check, Date_Consistency_Check)
SELECT 
    CAST(order_nbr AS INT) AS Order_ID,
    "Valid delivery_dt format" AS Mandatory_Fields_Check,
    "Pass" AS Date_Consistency_Check
FROM valid_format_cte;

-- Handle invalid entries in delivery_dt
INSERT INTO purgo_playground.purgo_playground.dq_reports (Order_ID, Mandatory_Fields_Check, Date_Consistency_Check)
SELECT 
    CAST(order_nbr AS INT) AS Order_ID,
    "Invalid delivery_dt format" AS Mandatory_Fields_Check,
    "Fail" AS Date_Consistency_Check
FROM purgo_playground.purgo_playground.f_order
WHERE CAST(delivery_dt AS STRING) NOT REGEXP "^[0-9]{8}$";

