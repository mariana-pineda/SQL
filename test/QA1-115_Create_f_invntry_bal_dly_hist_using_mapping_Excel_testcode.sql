/* 
Setup Section
*/
-- Drop target test table if exists
DROP TABLE IF EXISTS purgo_databricks.purgo_playground.f_invntry_bal_dly_hist_test;

-- Create test table with proper schema
CREATE TABLE purgo_databricks.purgo_playground.f_invntry_bal_dly_hist_test (
    co_key STRING,
    g_account STRING,
    g_assignment_type STRING,
    g_capture_dt_yyyymmdd TIMESTAMP,
    g_company_cd STRING,
    g_company_currency_cd STRING,
    g_dnsa_dt_yyyymmdd DATE,
    g_expiration_dt_yyyymmdd DATE,
    g_item_nbr STRING,
    g_location_cd STRING,
    g_location_status_cd STRING,
    g_lot_effective_dt_yyyymmdd DATE,
    g_lot_nbr STRING,
    g_lot_status_cd STRING,
    g_plant_cd STRING,
    g_qty_allocated DECIMAL(10,2),
    g_qty_available DECIMAL(10,2),
    g_qty_financial_nettable DECIMAL(10,2),
    g_qty_in_transit DECIMAL(10,2),
    g_qty_mrp_nettable DECIMAL(10,2),
    g_qty_on_hand DECIMAL(10,2),
    g_qty_shippable DECIMAL(10,2),
    g_source_system_cd STRING,
    g_unit_cost_company_currency DECIMAL(10,2),
    plant_key STRING,
    plant_location_key STRING,
    prod_key STRING,
    prod_plant_key STRING,
    prod_plant_location_key STRING,
    prod_plant_lot_key STRING,
    prod_plant_lot_location_key STRING
);

/* 
Create Error Logs Table
*/
-- Drop error_logs table if exists
DROP TABLE IF EXISTS purgo_databricks.purgo_playground.error_logs;

-- Create error_logs table for capturing test failures
CREATE TABLE purgo_databricks.purgo_playground.error_logs (
    test_name STRING,
    error_message STRING
);

/* 
Insert Test Data
*/
-- Insert provided test data into test table
INSERT INTO purgo_databricks.purgo_playground.f_invntry_bal_dly_hist_test VALUES
('nav_ger1050', 'ACC12345', 'Account', '2024-04-01T12:00:00.000', '1050', 'EUR', '2024-12-31', '99991231', 'ITEM123', 'HAUPT', 'none', '1900-01-01', 'LOT67890', 'none', 'CAGER', 50.25, 100.50, 100.50, NULL, 80.00, 100.50, 100.50, 'nav_ger', 25.75, 'nav_gerCAGER', 'nav_gerCAGERHAUPT', 'nav_gerITEM123', 'nav_gerITEM123CAGER', 'nav_gerITEM123CAGERHAUPT', 'nav_gerITEM123CAGERLOT67890', 'nav_gerITEM123CAGERLOT67890HAUPT'),
('nav_ger1050', 'ACC00001', 'Account', '2024-01-01T00:00:00.000', '1050', 'EUR', '2023-01-01', '99991231', 'ITEM000', 'LIN', 'none', '1900-01-01', 'LOT00000', 'none', 'CAGER', 0.01, 0.01, 0.01, NULL, 0.01, 0.01, 0.01, 'nav_ger', 0.01, 'nav_gerCAGER', 'nav_gerCAGERLIN', 'nav_gerITEM000', 'nav_gerITEM000CAGER', 'nav_gerITEM000CAGERLIN', 'nav_gerITEM000CAGERLOT00000', 'nav_gerITEM000CAGERLOT00000LIN'),
('nav_ger1050', 'ACC99999', 'Account', '2024-12-31T23:59:59.999', '1050', 'EUR', '2024-12-31', '99991231', 'ITEM999', 'MATRIUM', 'none', '1900-01-01', 'LOT99999', 'none', 'CAGER', 99999.99, 99999.99, 99999.99, NULL, 99999.99, 99999.99, 99999.99, 'nav_ger', 99999.99, 'nav_gerCAGER', 'nav_gerCAGERMATRIUM', 'nav_gerITEM999', 'nav_gerITEM999CAGER', 'nav_gerITEM999CAGERMATRIUM', 'nav_gerITEM999CAGERLOT99999', 'nav_gerITEM999CAGERLOT99999MATRIUM'),
('nav_ger1050', NULL, 'Account', '2024-05-15T08:30:00.000', '1050', 'EUR', '2024-06-30', '99991231', 'ITEM456', 'GERMERING', 'none', '1900-01-01', 'LOT12345', 'none', 'CAGER', 25.00, 50.00, 50.00, NULL, 40.00, 50.00, 50.00, 'nav_ger', 15.50, 'nav_gerCAGER', 'nav_gerCAGERGERMERING', 'nav_gerITEM456', 'nav_gerITEM456CAGER', 'nav_gerITEM456CAGERGERMERING', 'nav_gerITEM456CAGERLOT12345', 'nav_gerITEM456CAGERLOT12345GERMERING'),
('nav_ger1050', 'ACC@#$', 'Account', '2024-07-20T14:45:00.000', '1050', 'EUR', '2024-11-30', '99991231', 'ITEM!@#', 'AH-LOC', 'none', '1900-01-01', 'LOT!@#$', 'none', 'CAGER', -10.50, 20.75, 20.75, NULL, 30.25, 20.75, 20.75, 'nav_ger', 12.50, 'nav_gerCAGER', 'nav_gerCAGERAH-LOC', 'nav_gerITEM!@#', 'nav_gerITEM!@#CAGER', 'nav_gerITEM!@#CAGERAH-LOC', 'nav_gerITEM!@#CAGERLOT!@#$', 'nav_gerITEM!@#CAGERLOT!@#$AH-LOC'),
('nav_ger1050', 'ACC测试', 'Account', '2024-08-10T09:15:00.000', '1050', 'EUR', '2024-09-30', '99991231', 'ITEM测试', 'SERVICE', 'none', '1900-01-01', 'LOT测试', 'none', 'CAGER', 75.00, 150.00, 150.00, NULL, 120.00, 150.00, 150.00, 'nav_ger', 35.75, 'nav_gerCAGER', 'nav_gerCAGERSERVICE', 'nav_gerITEM测试', 'nav_gerITEM测试CAGER', 'nav_gerITEM测试CAGERSERVICE', 'nav_gerITEM测试CAGERLOT测试', 'nav_gerITEM测试CAGERLOT测试SERVICE'),
('nav_ger1050', 'ACC_TRIM', 'Account', '2024-01-15T07:07:07.000', '1050', 'EUR', '2024-02-15', '99991231', 'ITEM_TRIM', ' AH-LOC ', 'none', '1900-01-01', 'LOT_TRIM', 'none', 'CAGER', 45.00, 90.00, 90.00, NULL, 135.00, 90.00, 90.00, 'nav_ger', 30.00, 'nav_gerCAGER', 'nav_gerCAGERAH-LOC', 'nav_gerITEM_TRIM', 'nav_gerITEM_TRIMCAGER', 'nav_gerITEM_TRIMCAGERAH-LOC', 'nav_gerITEM_TRIMCAGERLOT_TRIM', 'nav_gerITEM_TRIMCAGERLOT_TRIMAH-LOC'),
('nav_ger1050', 'ACC_DEFAULT_ASSIGN', 'Account', '2024-02-20T11:11:11.000', '1050', 'EUR', '2024-03-20', '99991231', 'ITEM_DEFAULT_ASSIGN', 'QS-WE', 'none', '1900-01-01', 'LOT_DEFAULT_ASSIGN', 'none', 'CAGER', 20.00, 40.00, 40.00, NULL, 60.00, 40.00, 40.00, 'nav_ger', 20.00, 'nav_gerCAGER', 'nav_gerCAGERQS-WE', 'nav_gerITEM_DEFAULT_ASSIGN', 'nav_gerITEM_DEFAULT_ASSIGNCAGER', 'nav_gerITEM_DEFAULT_ASSIGNCAGERQS-WE', 'nav_gerITEM_DEFAULT_ASSIGNCAGERLOT_DEFAULT_ASSIGN', 'nav_gerITEM_DEFAULT_ASSIGNCAGERLOT_DEFAULT_ASSIGNQS-WE'),
('nav_ger1050', 'ACC_VALID_CURRENCY', 'Account', '2024-10-30T06:06:06.000', '1050', 'EUR', '2024-11-30', '99991231', 'ITEM_VALID_CUR', 'HAUPT', 'none', '1900-01-01', 'LOT_VALID_CUR', 'none', 'CAGER', 110.00, 220.00, 220.00, NULL, 330.00, 220.00, 220.00, 'nav_ger', 165.00, 'nav_gerCAGER', 'nav_gerCAGERHAUPT', 'nav_gerITEM_VALID_CUR', 'nav_gerITEM_VALID_CURCAGER', 'nav_gerITEM_VALID_CURCAGERHAUPT', 'nav_gerITEM_VALID_CURCAGERLOT_VALID_CUR', 'nav_gerITEM_VALID_CURCAGERLOT_VALID_CURHAUPT');

/* 
Test Scenarios
*/
-- Scenario: Successfully load a complete and valid record
INSERT INTO purgo_databricks.purgo_playground.error_logs (test_name, error_message)
SELECT 'Successfully load a complete and valid record', 'Failed: Record not inserted'
WHERE NOT EXISTS (
    SELECT 1 FROM purgo_databricks.purgo_playground.f_invntry_bal_dly_hist_test
    WHERE co_key = 'nav_ger1050' AND g_account = 'ACC12345'
);

-- Scenario Outline: Validate default and hardcoded field values when source data is missing
INSERT INTO purgo_databricks.purgo_playground.error_logs (test_name, error_message)
SELECT 'Validate default and hardcoded field values when source data is missing', 'Failed: Default values not set correctly'
WHERE NOT EXISTS (
    SELECT 1 FROM purgo_databricks.purgo_playground.f_invntry_bal_dly_hist_test
    WHERE g_assignment_type = 'Account' 
      AND g_company_cd = '1050' 
      AND g_company_currency_cd = 'EUR' 
      AND g_location_status_cd = 'none' 
      AND g_lot_status_cd = 'none' 
      AND g_plant_cd = 'CAGER' 
      AND g_source_system_cd = 'nav_ger' 
      AND g_qty_in_transit IS NULL
);

-- Scenario: Fail to load record with missing mandatory field g_account
INSERT INTO purgo_databricks.purgo_playground.error_logs (test_name, error_message)
SELECT 'Fail to load record with missing mandatory field g_account', 'Failed: Record with missing g_account was inserted'
WHERE EXISTS (
    SELECT 1 FROM purgo_databricks.purgo_playground.f_invntry_bal_dly_hist_test
    WHERE g_account IS NULL AND g_item_nbr = 'ITEM_MISSING_ACCOUNT'
);

-- Scenario: Validate alphanumeric constraint on g_account
INSERT INTO purgo_databricks.purgo_playground.error_logs (test_name, error_message)
SELECT 'Validate alphanumeric constraint on g_account', 'Failed: Non-alphanumeric g_account inserted'
WHERE EXISTS (
    SELECT 1 FROM purgo_databricks.purgo_playground.f_invntry_bal_dly_hist_test
    WHERE g_account RLIKE '[^a-zA-Z0-9]' AND g_item_nbr = 'ITEM!@#'
);

-- Scenario: Validate date format for g_capture_dt_yyyymmdd
INSERT INTO purgo_databricks.purgo_playground.error_logs (test_name, error_message)
SELECT 'Validate date format for g_capture_dt_yyyymmdd', 'Failed: Incorrect date format in g_capture_dt_yyyymmdd'
WHERE EXISTS (
    SELECT 1 FROM purgo_databricks.purgo_playground.f_invntry_bal_dly_hist_test
    WHERE DATE_FORMAT(g_capture_dt_yyyymmdd, 'yyyy-MM-dd') IS NULL
);

-- Scenario: Validate concatenation for plant_key
INSERT INTO purgo_databricks.purgo_playground.error_logs (test_name, error_message)
SELECT 'Validate concatenation for plant_key', 'Failed: Incorrect concatenation in plant_key'
WHERE EXISTS (
    SELECT 1 FROM purgo_databricks.purgo_playground.f_invntry_bal_dly_hist_test
    WHERE plant_key != CONCAT(g_source_system_cd, g_plant_cd)
);

-- Scenario: Validate conditional population of g_qty_allocated
INSERT INTO purgo_databricks.purgo_playground.error_logs (test_name, error_message)
SELECT 'Validate conditional population of g_qty_allocated', 'Failed: Incorrect g_qty_allocated value'
WHERE EXISTS (
    SELECT 1 FROM purgo_databricks.purgo_playground.f_invntry_bal_dly_hist_test
    WHERE g_qty_allocated != ABS(g_qty_allocated)
);

-- Scenario Outline: Validate g_qty_available based on location_code
INSERT INTO purgo_databricks.purgo_playground.error_logs (test_name, error_message)
SELECT 'Validate g_qty_available based on location_code', 'Failed: g_qty_available does not match expected value'
WHERE NOT EXISTS (
    SELECT 1 FROM purgo_databricks.purgo_playground.f_invntry_bal_dly_hist_test
    WHERE (qty_on_hand = 100.50 AND location_code = 'HAUPT' AND g_qty_available = 100.50)
       OR (qty_on_hand = 200.00 AND location_code = 'GERMERING' AND g_qty_available = 200.00)
       OR (qty_on_hand = 150.75 AND location_code = 'OTHER' AND g_qty_available IS NULL)
);

-- Scenario Outline: Validate g_qty_mrp_nettable based on location_code
INSERT INTO purgo_databricks.purgo_playground.error_logs (test_name, error_message)
SELECT 'Validate g_qty_mrp_nettable based on location_code', 'Failed: g_qty_mrp_nettable does not match expected value'
WHERE NOT EXISTS (
    SELECT 1 FROM purgo_databricks.purgo_playground.f_invntry_bal_dly_hist_test
    WHERE (qty_on_hand = 80.00 AND location_code = 'HAUPT' AND g_qty_mrp_nettable = 80.00)
       OR (qty_on_hand = 60.50 AND location_code = 'QS-WE' AND g_qty_mrp_nettable = 60.50)
       OR (qty_on_hand = 70.25 AND location_code = 'AH-LOC' AND g_qty_mrp_nettable = 70.25)
       OR (qty_on_hand = 90.00 AND location_code = 'UNKNOWN' AND g_qty_mrp_nettable IS NULL)
);

-- Scenario: Validate hardcoded value for g_source_system_cd
INSERT INTO purgo_databricks.purgo_playground.error_logs (test_name, error_message)
SELECT 'Validate hardcoded value for g_source_system_cd', 'Failed: g_source_system_cd is not hardcoded to nav_ger'
WHERE EXISTS (
    SELECT 1 FROM purgo_databricks.purgo_playground.f_invntry_bal_dly_hist_test
    WHERE g_source_system_cd != 'nav_ger'
);

-- Scenario: Validate NULL handling for g_qty_in_transit
INSERT INTO purgo_databricks.purgo_playground.error_logs (test_name, error_message)
SELECT 'Validate NULL handling for g_qty_in_transit', 'Failed: g_qty_in_transit is not NULL'
WHERE EXISTS (
    SELECT 1 FROM purgo_databricks.purgo_playground.f_invntry_bal_dly_hist_test
    WHERE g_qty_in_transit IS NOT NULL
);

-- Scenario: Validate default value for g_assignment_type when not represented
INSERT INTO purgo_databricks.purgo_playground.error_logs (test_name, error_message)
SELECT 'Validate default value for g_assignment_type when not represented', 'Failed: Default value for g_assignment_type is not Account'
WHERE EXISTS (
    SELECT 1 FROM purgo_databricks.purgo_playground.f_invntry_bal_dly_hist_test
    WHERE g_assignment_type != 'Account' AND g_assignment_type IS NOT NULL
);

-- Scenario: Validate derived plant_location_key concatenation
INSERT INTO purgo_databricks.purgo_playground.error_logs (test_name, error_message)
SELECT 'Validate derived plant_location_key concatenation', 'Failed: Incorrect concatenation in plant_location_key'
WHERE EXISTS (
    SELECT 1 FROM purgo_databricks.purgo_playground.f_invntry_bal_dly_hist_test
    WHERE plant_location_key != CONCAT(g_source_system_cd, g_plant_cd, g_location_cd)
);

-- Scenario: Validate error logging for invalid data type in g_qty_on_hand
INSERT INTO purgo_databricks.purgo_playground.error_logs (test_name, error_message)
SELECT 'Validate error logging for invalid data type in g_qty_on_hand', 'Failed: Invalid g_qty_on_hand was inserted'
WHERE EXISTS (
    SELECT 1 FROM purgo_databricks.purgo_playground.f_invntry_bal_dly_hist_test
    WHERE CAST(g_qty_on_hand AS STRING) = 'invalid_decimal'
);

-- Scenario: Validate default value for g_lot_nbr when lot_no_ contains blank space
INSERT INTO purgo_databricks.purgo_playground.error_logs (test_name, error_message)
SELECT 'Validate default value for g_lot_nbr when lot_no_ contains blank space', 'Failed: g_lot_nbr was not defaulted to none'
WHERE EXISTS (
    SELECT 1 FROM purgo_databricks.purgo_playground.f_invntry_bal_dly_hist_test
    WHERE lot_no_ = 'LOT 67890' AND g_lot_nbr != 'none'
);

-- Scenario: Validate derived key prod_plant_lot_location_key
INSERT INTO purgo_databricks.purgo_playground.error_logs (test_name, error_message)
SELECT 'Validate derived key prod_plant_lot_location_key', 'Failed: Incorrect concatenation in prod_plant_lot_location_key'
WHERE EXISTS (
    SELECT 1 FROM purgo_databricks.purgo_playground.f_invntry_bal_dly_hist_test
    WHERE prod_plant_lot_location_key != CONCAT(g_source_system_cd, g_item_nbr, g_plant_cd, g_lot_nbr, g_location_cd)
);

-- Scenario: Validate date completeness for g_capture_dt_yyyymmdd
INSERT INTO purgo_databricks.purgo_playground.error_logs (test_name, error_message)
SELECT 'Validate date completeness for g_capture_dt_yyyymmdd', 'Failed: g_capture_dt_yyyymmdd is not the current date'
WHERE EXISTS (
    SELECT 1 FROM purgo_databricks.purgo_playground.f_invntry_bal_dly_hist_test
    WHERE DATE(g_capture_dt_yyyymmdd) != CURRENT_DATE()
);

-- Scenario: Validate handling of multiple joins without data duplication
INSERT INTO purgo_databricks.purgo_playground.error_logs (test_name, error_message)
SELECT 'Validate handling of multiple joins without data duplication', 'Failed: Duplicate records found in f_invntry_bal_dly_hist_test'
WHERE EXISTS (
    SELECT co_key FROM purgo_databricks.purgo_playground.f_invntry_bal_dly_hist_test
    GROUP BY co_key
    HAVING COUNT(*) > 1
);

-- Scenario: Validate data quality rules enforcement for alphanumeric fields
INSERT INTO purgo_databricks.purgo_playground.error_logs (test_name, error_message)
SELECT 'Validate data quality rules enforcement for alphanumeric fields', 'Failed: Non-alphanumeric characters found in alphanumeric fields'
WHERE EXISTS (
    SELECT 1 FROM purgo_databricks.purgo_playground.f_invntry_bal_dly_hist_test
    WHERE (g_account RLIKE '[^a-zA-Z0-9]')
       OR (g_item_nbr RLIKE '[^a-zA-Z0-9]')
       OR (g_location_cd RLIKE '[^a-zA-Z0-9]')
);

-- Scenario: Validate ISO 4217 compliance for g_company_currency_cd
INSERT INTO purgo_databricks.purgo_playground.error_logs (test_name, error_message)
SELECT 'Validate ISO 4217 compliance for g_company_currency_cd', 'Failed: Invalid ISO 4217 currency code in g_company_currency_cd'
WHERE EXISTS (
    SELECT 1 FROM purgo_databricks.purgo_playground.f_invntry_bal_dly_hist_test
    WHERE g_company_currency_cd NOT IN (SELECT currency_code FROM purgo_databricks.purgo_playground.iso_4217_codes)
);

-- Scenario: Validate handling of NULL values in specific fields
INSERT INTO purgo_databricks.purgo_playground.error_logs (test_name, error_message)
SELECT 'Validate handling of NULL values in specific fields', 'Failed: NULL values not handled correctly in specific fields'
WHERE EXISTS (
    SELECT 1 FROM purgo_databricks.purgo_playground.f_invntry_bal_dly_hist_test
    WHERE some_field IS NOT NULL
);

-- Scenario: Validate security compliance by restricting access to the target table
INSERT INTO purgo_databricks.purgo_playground.error_logs (test_name, error_message)
SELECT 'Validate security compliance by restricting access to the target table', 'Failed: Unauthorized access to f_invntry_bal_dly_hist_test allowed'
WHERE EXISTS (
    SELECT 1 FROM purgo_databricks.purgo_playground.permissions_audit
    WHERE table_name = 'f_invntry_bal_dly_hist_test' 
      AND user_role = 'unauthorized' 
      AND access_granted = TRUE
);

-- Scenario: Validate transformation logic for conditional quantity population
INSERT INTO purgo_databricks.purgo_playground.error_logs (test_name, error_message)
SELECT 'Validate transformation logic for conditional quantity population', 'Failed: Incorrect g_qty_available based on location_code'
WHERE EXISTS (
    SELECT 1 FROM purgo_databricks.purgo_playground.f_invntry_bal_dly_hist_test
    WHERE location_code = 'MATRIUM' AND g_qty_available != 300.00
);

-- Scenario: Validate handling of derived fields with complex concatenation
INSERT INTO purgo_databricks.purgo_playground.error_logs (test_name, error_message)
SELECT 'Validate handling of derived fields with complex concatenation', 'Failed: Derived fields have incorrect concatenation'
WHERE EXISTS (
    SELECT 1 FROM purgo_databricks.purgo_playground.f_invntry_bal_dly_hist_test
    WHERE 
        plant_key != CONCAT(g_source_system_cd, g_plant_cd) OR
        plant_location_key != CONCAT(g_source_system_cd, g_plant_cd, g_location_cd) OR
        prod_key != CONCAT(g_source_system_cd, g_item_nbr) OR
        prod_plant_key != CONCAT(g_source_system_cd, g_item_nbr, g_plant_cd) OR
        prod_plant_location_key != CONCAT(g_source_system_cd, g_item_nbr, g_plant_cd, g_location_cd) OR
        prod_plant_lot_key != CONCAT(g_source_system_cd, g_item_nbr, g_plant_cd, g_lot_nbr) OR
        prod_plant_lot_location_key != CONCAT(g_source_system_cd, g_item_nbr, g_plant_cd, g_lot_nbr, g_location_cd)
);
