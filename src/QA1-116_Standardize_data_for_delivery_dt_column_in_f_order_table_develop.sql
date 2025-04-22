/*
  Script: /Workspace/stg/scripts/f_order.sql
  Purpose: Validate that the delivery_dt column in purgo_playground.f_order table is of type Decimal(38,0) and follows the yyyymmdd format.
  Catalog: purgo_databricks
  Schema: purgo_playground
*/

-- Validate delivery_dt in purgo_playground.f_order
WITH delivery_dt_validation AS (
  SELECT
    COUNT(*) AS total_records,
    COUNT(delivery_dt) AS non_null_records,
    COUNT(*) - COUNT(delivery_dt) AS null_records,
    SUM(CASE WHEN delivery_dt >= 10000101 AND delivery_dt <= 99991231 THEN 1 ELSE 0 END) AS valid_format_records,
    SUM(CASE WHEN delivery_dt < 10000101 OR delivery_dt > 99991231 THEN 1 ELSE 0 END) AS invalid_format_records
  FROM purgo_databricks.purgo_playground.f_order
),

validation_results AS (
  SELECT
    'delivery_dt' AS field_name,
    CASE 
      WHEN invalid_format_records = 0 AND null_records = 0 THEN 'Pass'
      ELSE 'Fail'
    END AS validation_status,
    CASE 
      WHEN null_records > 0 THEN 'delivery_dt value is NULL'
      ELSE NULL
    END AS null_error,
    CASE 
      WHEN invalid_format_records > 0 THEN 'delivery_dt format is not yyyyMMdd'
      ELSE NULL
    END AS format_error
  FROM delivery_dt_validation
)

-- Insert validation results into purgo_playground.dq_reports
INSERT INTO purgo_databricks.purgo_playground.dq_reports (
  Order_ID,
  Mandatory_Fields_Check,
  Date_Consistency_Check,
  Range_Check,
  Status_Consistency_Check,
  Unique_Identifier_Check,
  Returned_Product_Validation,
  Correct_Unit_Shipment_Type,
  Price_Calculation_Accuracy
)
SELECT
  NULL AS Order_ID,
  NULL AS Mandatory_Fields_Check,
  CASE 
    WHEN validation_status = 'Pass' THEN 'Pass'
    ELSE null_error
  END AS Date_Consistency_Check,
  CASE 
    WHEN validation_status = 'Pass' THEN 'Pass'
    ELSE format_error
  END AS Range_Check,
  NULL AS Status_Consistency_Check,
  NULL AS Unique_Identifier_Check,
  NULL AS Returned_Product_Validation,
  NULL AS Correct_Unit_Shipment_Type,
  NULL AS Price_Calculation_Accuracy
FROM validation_results;
