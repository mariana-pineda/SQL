-- Test Suite for Data Standardization of delivery_dt column in f_order table

/* 
   SETUP: Define settings for the test framework 
   Ensure database and schema are addressed accurately 
*/
-- Using the database schema purgo_playground and table purgo_playground.f_order for testing
-- Prepare necessary selections and validations

-- Validate if delivery_dt is in the correct Decimal(38,0) format in yyyymmdd
WITH validation_cte AS (
  SELECT
    delivery_dt
  FROM purgo_playground.purgo_playground.f_order
  WHERE CAST(delivery_dt AS STRING) NOT REGEXP "^[0-9]{8}$"
)
-- Assert that no records exist in validation_cte for invalid delivery_dt format
SELECT COUNT(*) AS error_count FROM validation_cte;

/* 
   CONVERT: Ensure conversion from timestamp to Decimal(38,0) 
   The method of conversion ensures compliance with desired format yyyymmdd
*/
WITH conversion_cte AS (
  SELECT
    order_nbr,
    CAST(DATE_FORMAT(delivery_dt, "yyyyMMdd") AS DECIMAL(38,0)) AS converted_delivery_dt
  FROM purgo_playground.purgo_playground.f_order
  WHERE delivery_dt IS NOT NULL
)
-- Verification of correct conversion with a pseudo table conversion_cte
-- Validate that converted_delivery_dt results in expected format yyyymmdd
SELECT COUNT(*) AS conversion_error_count
FROM conversion_cte
WHERE CAST(converted_delivery_dt AS STRING) NOT REGEXP "^[0-9]{8}$";

/* 
   INTEGRATION: Handling of invalid data entries and ensuring error message logging 
*/
-- Handle invalid entries in delivery_dt (i.e., values that cannot be converted)
INSERT INTO purgo_playground.purgo_playground.dq_reports (Order_ID, Mandatory_Fields_Check, Date_Consistency_Check)
SELECT 
  CAST(order_nbr AS INT) AS Order_ID,
  "Invalid delivery_dt format" AS Mandatory_Fields_Check,
  "Fail" AS Date_Consistency_Check
FROM purgo_playground.purgo_playground.f_order
WHERE CAST(delivery_dt AS STRING) NOT REGEXP "^[0-9]{8}$";

/* 
   CLEANUP: For delta lake operations: Clean up after test execution
   Removing potentially harmful changes, keeping test environment sterile
*/
-- Cleanup any temporary testing artifacts related to validation and conversion processes

DELETE FROM purgo_playground.purgo_playground.dq_reports
WHERE Mandatory_Fields_Check = "Invalid delivery_dt format";


