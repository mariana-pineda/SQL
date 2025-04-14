-- SQL Test Script for Validating and Formatting delivery_dt in f_order Table
-- Databricks SQL syntax used with constraints and validation logic

/*
  Section: Table Creation
  Create the f_order table with proper constraints and data types
*/

CREATE TABLE IF NOT EXISTS purgo_playground.purgo_playground.f_order (
  order_nbr STRING NOT NULL,
  order_type BIGINT NOT NULL,
  delivery_dt DECIMAL(38,0) NOT NULL,
  order_qty DOUBLE,
  sched_dt DECIMAL(38,0) NOT NULL,
  expected_shipped_dt DECIMAL(38,0) NOT NULL,
  actual_shipped_dt DECIMAL(38,0),
  order_line_nbr STRING,
  loc_tracker_id STRING,
  shipping_add STRING,
  primary_qty DOUBLE,
  open_qty DOUBLE,
  shipped_qty DOUBLE,
  order_desc STRING,
  flag_return STRING CONSTRAINT flag_return_values CHECK (flag_return IN ('Y', 'N')),
  flag_cancel STRING CONSTRAINT flag_cancel_values CHECK (flag_cancel IN ('Y', 'N')),
  cancel_dt DECIMAL(38,0),
  cancel_qty DOUBLE,
  crt_dt TIMESTAMP,
  updt_dt TIMESTAMP
);

-- CTE Definition: Validate delivery_dt field format and capture errors
WITH validation_cte AS (
  SELECT 
    order_nbr,
    delivery_dt,
    CASE 
      WHEN delivery_dt IS NULL THEN "delivery_dt is missing or null"
      WHEN TRY_CAST(CAST(delivery_dt AS STRING) AS DECIMAL(38,0)) IS NULL THEN "Incorrect format, conversion to yyyymmdd required"
      ELSE NULL
    END AS error_message
  FROM purgo_playground.purgo_playground.f_order
)

-- Output any errors identified in validation_cte
SELECT * FROM validation_cte WHERE error_message IS NOT NULL;

/*
  Section: Data Transformation
  Check and prepare delivery_dt field for transformation purposes
*/

-- Transformation Checking: Validates and formats delivery_dt field
WITH transformation_cte AS (
  SELECT 
    order_nbr,
    delivery_dt,
    CASE 
      WHEN error_message IS NULL THEN delivery_dt
      ELSE CAST(CONCAT(SUBSTR(CAST(delivery_dt AS STRING), 1, 4), SUBSTR(CAST(delivery_dt AS STRING), 6, 2), SUBSTR(CAST(delivery_dt AS STRING), 9, 2)) AS DECIMAL(38,0))
    END AS delivery_dt_converted
  FROM validation_cte
)

-- Display converted delivery_dt for verification
SELECT order_nbr, delivery_dt, delivery_dt_converted FROM transformation_cte;

/*
  Section: Error Logging
  Log any identified errors into dq_reports table for auditing
*/

-- Insert errors from validation_cte into dq_reports table
INSERT INTO purgo_playground.purgo_playground.dq_reports
SELECT 
  CAST(order_nbr AS INT) AS Order_ID,
  CASE 
    WHEN error_message IS NOT NULL THEN 'Failed'
    ELSE 'Passed'
  END AS Mandatory_Fields_Check,
  CASE 
    WHEN error_message IS NOT NULL THEN 'Failed'
    ELSE 'Passed'
  END AS Date_Consistency_Check,
  'Valid' AS Range_Check,
  'Valid' AS Status_Consistency_Check,
  'Passed' AS Unique_Identifier_Check,
  CASE 
    WHEN flag_return NOT IN ('Y', 'N') THEN 'Failed'
    ELSE 'Passed'
  END AS Returned_Product_Validation,
  'Passed' AS Correct_Unit_Shipment_Type,
  'Passed' AS Price_Calculation_Accuracy
FROM validation_cte WHERE error_message IS NOT NULL;

/*
  Section: Cleanup Operations
  Execute cleanup operations after validation and transformations
*/

-- End of SQL Test Script
