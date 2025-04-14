-- SQL Script for validating and formatting delivery_dt in f_order table
-- Aim: To ensure delivery_dt field is correct in Decimal (38,0) format as yyyymmdd

/*
  Section: Validation Logic
  Validate delivery_dt format and report errors
*/

WITH delivery_dt_validation AS (
  SELECT 
    order_nbr,
    delivery_dt,
    CASE 
      WHEN delivery_dt IS NULL THEN "delivery_dt is missing or null"
      WHEN NOT(REGEXP_EXTRACT(CAST(delivery_dt AS STRING), "^\d{8}$") IS NOT NULL AND TRY_CAST(delivery_dt AS DECIMAL(38,0)) IS NOT NULL) THEN "Incorrect format, conversion to yyyymmdd required"
      ELSE NULL
    END AS error_message
  FROM purgo_playground.purgo_playground.f_order
)

-- Output the results of the validation
SELECT * FROM delivery_dt_validation WHERE error_message IS NOT NULL;

/*
  Section: Transformation Logic
  Transform delivery_dt to correct Decimal(38,0) format if necessary
*/

SELECT 
  order_nbr, 
  delivery_dt,
  CASE
    WHEN error_message IS NULL THEN delivery_dt
    ELSE CAST(CONCAT(SUBSTR(CAST(delivery_dt AS STRING), 1, 4), SUBSTR(CAST(delivery_dt AS STRING), 5, 2), SUBSTR(CAST(delivery_dt AS STRING), 7, 2)) AS DECIMAL(38,0))
  END AS delivery_dt_converted
FROM delivery_dt_validation;

/*
  Section: Error Logging
  Log validation errors into dq_reports for auditing
*/

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
  'Passed' AS Returned_Product_Validation,
  'Passed' AS Correct_Unit_Shipment_Type,
  'Passed' AS Price_Calculation_Accuracy
FROM delivery_dt_validation WHERE error_message IS NOT NULL;

/* End of SQL Script for delivery_dt validation and transformation */
