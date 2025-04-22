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

-- Insert test data
INSERT INTO purgo_databricks.purgo_playground.f_invntry_bal_dly_hist_test VALUES
-- Happy path
('nav_ger1050', 'ACC12345', 'Account', '2024-04-01T12:00:00.000+0000', '1050', 'EUR', '2024-12-31', '99991231', 'ITEM123', 'HAUPT', 'none', '1900-01-01', 'LOT67890', 'none', 'CAGER', 50.25, 100.50, 100.50, NULL, 80.00, 100.50, 100.50, 'nav_ger', 25.75, 'nav_gerCAGER', 'nav_gerCAGERHAUPT', 'nav_gerITEM123', 'nav_gerITEM123CAGER', 'nav_gerITEM123CAGERHAUPT', 'nav_gerITEM123CAGERLOT67890', 'nav_gerITEM123CAGERLOT67890HAUPT'),
-- Edge case: Minimum decimal values
('nav_ger1050', 'ACC00001', 'Account', '2024-01-01T00:00:00.000+0000', '1050', 'EUR', '2023-01-01', '99991231', 'ITEM000', 'LIN', 'none', '1900-01-01', 'LOT00000', 'none', 'CAGER', 0.01, 0.01, 0.01, NULL, 0.01, 0.01, 0.01, 'nav_ger', 0.01, 'nav_gerCAGER', 'nav_gerCAGERLIN', 'nav_gerITEM000', 'nav_gerITEM000CAGER', 'nav_gerITEM000CAGERLIN', 'nav_gerITEM000CAGERLOT00000', 'nav_gerITEM000CAGERLOT00000LIN'),
-- Edge case: Maximum decimal values
('nav_ger1050', 'ACC99999', 'Account', '2024-12-31T23:59:59.999+0000', '1050', 'EUR', '2024-12-31', '99991231', 'ITEM999', 'MATRIUM', 'none', '1900-01-01', 'LOT99999', 'none', 'CAGER', 99999.99, 99999.99, 99999.99, NULL, 99999.99, 99999.99, 99999.99, 'nav_ger', 99999.99, 'nav_gerCAGER', 'nav_gerCAGERMATRIUM', 'nav_gerITEM999', 'nav_gerITEM999CAGER', 'nav_gerITEM999CAGERMATRIUM', 'nav_gerITEM999CAGERLOT99999', 'nav_gerITEM999CAGERLOT99999MATRIUM'),
-- NULL handling
('nav_ger1050', NULL, 'Account', '2024-05-15T08:30:00.000+0000', '1050', 'EUR', '2024-06-30', '99991231', 'ITEM456', 'GERMERING', 'none', '1900-01-01', 'LOT12345', 'none', 'CAGER', 25.00, 50.00, 50.00, NULL, 40.00, 50.00, 50.00, 'nav_ger', 15.50, 'nav_gerCAGER', 'nav_gerCAGERGERMERING', 'nav_gerITEM456', 'nav_gerITEM456CAGER', 'nav_gerITEM456CAGERGERMERING', 'nav_gerITEM456CAGERLOT12345', 'nav_gerITEM456CAGERLOT12345GERMERING'),
-- Special characters
('nav_ger1050', 'ACC@#$', 'Account', '2024-07-20T14:45:00.000+0000', '1050', 'EUR', '2024-11-30', '99991231', 'ITEM!@#', 'AH-LOC', 'none', '1900-01-01', 'LOT!@#$', 'none', 'CAGER', -10.50, 20.75, 20.75, NULL, 30.25, 20.75, 20.75, 'nav_ger', 12.50, 'nav_gerCAGER', 'nav_gerCAGERAH-LOC', 'nav_gerITEM!@#', 'nav_gerITEM!@#CAGER', 'nav_gerITEM!@#CAGERAH-LOC', 'nav_gerITEM!@#CAGERLOT!@#$', 'nav_gerITEM!@#CAGERLOT!@#$AH-LOC'),
-- Multi-byte characters
('nav_ger1050', 'ACC测试', 'Account', '2024-08-10T09:15:00.000+0000', '1050', 'EUR', '2024-09-30', '99991231', 'ITEM测试', 'SERVICE', 'none', '1900-01-01', 'LOT测试', 'none', 'CAGER', 75.00, 150.00, 150.00, NULL, 120.00, 150.00, 150.00, 'nav_ger', 35.75, 'nav_gerCAGER', 'nav_gerCAGERSERVICE', 'nav_gerITEM测试', 'nav_gerITEM测试CAGER', 'nav_gerITEM测试CAGERSERVICE', 'nav_gerITEM测试CAGERLOT测试', 'nav_gerITEM测试CAGERLOT测试SERVICE'),
-- Error case: Out-of-range DECIMAL
('nav_ger1050', 'ACC_OUTR', 'Account', '2024-09-05T16:20:00.000+0000', '1050', 'EUR', '2024-10-31', '99991231', 'ITEM_OUTR', 'LIN', 'none', '1900-01-01', 'LOT_OUTR', 'none', 'CAGER', 1000000.00, 2000000.00, 2000000.00, NULL, 3000000.00, 2000000.00, 2000000.00, 'nav_ger', 500000.00, 'nav_gerCAGER', 'nav_gerCAGERLIN', 'nav_gerITEM_OUTR', 'nav_gerITEM_OUTRCAGER', 'nav_gerITEM_OUTRCAGERLIN', 'nav_gerITEM_OUTRCAGERLOT_OUTR', 'nav_gerITEM_OUTRCAGERLOT_OUTRLIN'),
-- Error case: Invalid date format
('nav_ger1050', 'ACC_INVALID_DATE', 'Account', 'Invalid-Timestamp', '1050', 'EUR', '2024-13-01', '99991231', 'ITEM_INVALID_DATE', 'AH-LOC', 'none', '1900-01-01', 'LOT_INVALID', 'none', 'CAGER', 55.55, 110.11, 110.11, NULL, 88.88, 110.11, 110.11, 'nav_ger', 44.44, 'nav_gerCAGER', 'nav_gerCAGERAH-LOC', 'nav_gerITEM_INVALID_DATE', 'nav_gerITEM_INVALID_DATACAGER', 'nav_gerITEM_INVALID_DATACAGERAH-LOC', 'nav_gerITEM_INVALID_DATACAGERLOT_INVALID', 'nav_gerITEM_INVALID_DATACAGERLOT_INVALIDAH-LOC'),
-- NULL handling for g_qty_in_transit
('nav_ger1050', 'ACC_NULL_TRANSIT', 'Account', '2024-10-10T10:10:10.000+0000', '1050', 'EUR', '2024-11-10', '99991231', 'ITEM_NULL_TRANSIT', 'MATRIUM', 'none', '1900-01-01', 'LOT_NULL', 'none', 'CAGER', 60.00, 120.00, 120.00, NULL, 96.00, 120.00, 120.00, 'nav_ger', 48.00, 'nav_gerCAGER', 'nav_gerCAGERMATRIUM', 'nav_gerITEM_NULL_TRANSIT', 'nav_gerITEM_NULL_TRANSITCAGER', 'nav_gerITEM_NULL_TRANSITCAGERMATRIUM', 'nav_gerITEM_NULL_TRANSITCAGERLOT_NULL', 'nav_gerITEM_NULL_TRANSITCAGERLOT_NULLMATRIUM'),
-- Default values when source data is missing
('nav_ger1050', 'ACC_DEFAULT', 'Account', '2024-11-20T20:20:20.000+0000', '1050', 'EUR', '2024-12-20', '99991231', 'ITEM_DEFAULT', 'OTHER', 'none', '1900-01-01', 'LOT_DEFAULT', 'none', 'CAGER', 0.00, 0.00, 0.00, NULL, 0.00, 0.00, 0.00, 'nav_ger', 0.00, 'nav_gerCAGER', 'nav_gerCAGEROTHER', 'nav_gerITEM_DEFAULT', 'nav_gerITEM_DEFAULTCAGER', 'nav_gerITEM_DEFAULTCAGEROTHER', 'nav_gerITEM_DEFAULTCAGERLOT_DEFAULT', 'nav_gerITEM_DEFAULTCAGERLOT_DEFAULTOTHER'),
-- Special characters and multi-byte
('nav_ger1050', 'ACC特殊字符', 'Account', '2024-12-25T05:05:05.000+0000', '1050', 'EUR', '2024-12-31', '99991231', 'ITEM_特殊', 'AH-LOC', 'none', '1900-01-01', 'LOT_特殊', 'none', 'CAGER', 33.33, 66.66, 66.66, NULL, 99.99, 66.66, 66.66, 'nav_ger', 22.22, 'nav_gerCAGER', 'nav_gerCAGERAH-LOC', 'nav_gerITEM_特殊', 'nav_gerITEM_特殊CAGER', 'nav_gerITEM_特殊CAGERAH-LOC', 'nav_gerITEM_特殊CAGERLOT_特殊', 'nav_gerITEM_特殊CAGERLOT_特殊AH-LOC'),
-- Edge case: Trimmed location code
('nav_ger1050', 'ACC_TRIM', 'Account', '2024-01-15T07:07:07.000+0000', '1050', 'EUR', '2024-02-15', '99991231', 'ITEM_TRIM', ' AH-LOC ', 'none', '1900-01-01', 'LOT_TRIM', 'none', 'CAGER', 45.00, 90.00, 90.00, NULL, 135.00, 90.00, 90.00, 'nav_ger', 30.00, 'nav_gerCAGER', 'nav_gerCAGERAH-LOC', 'nav_gerITEM_TRIM', 'nav_gerITEM_TRIMCAGER', 'nav_gerITEM_TRIMCAGERAH-LOC', 'nav_gerITEM_TRIMCAGERLOT_TRIM', 'nav_gerITEM_TRIMCAGERLOT_TRIMAH-LOC'),
-- Default assignment type when not represented
('nav_ger1050', 'ACC_DEFAULT_ASSIGN', 'Account', '2024-02-20T11:11:11.000+0000', '1050', 'EUR', '2024-03-20', '99991231', 'ITEM_DEFAULT_ASSIGN', 'QS-WE', 'none', '1900-01-01', 'LOT_DEFAULT_ASSIGN', 'none', 'CAGER', 20.00, 40.00, 40.00, NULL, 60.00, 40.00, 40.00, 'nav_ger', 20.00, 'nav_gerCAGER', 'nav_gerCAGERQS-WE', 'nav_gerITEM_DEFAULT_ASSIGN', 'nav_gerITEM_DEFAULT_ASSIGNCAGER', 'nav_gerITEM_DEFAULT_ASSIGNCAGERQS-WE', 'nav_gerITEM_DEFAULT_ASSIGNCAGERLOT_DEFAULT_ASSIGN', 'nav_gerITEM_DEFAULT_ASSIGNCAGERLOT_DEFAULT_ASSIGNQS-WE'),
-- Invalid g_account (non-alphanumeric)
('nav_ger1050', 'ACC@@@', 'Account', '2024-03-10T13:13:13.000+0000', '1050', 'EUR', '2024-04-10', '99991231', 'ITEM_INVALID_ACCT', 'SERVICE', 'none', '1900-01-01', 'LOT_INVALID_ACCT', 'none', 'CAGER', 30.00, 60.00, 60.00, NULL, 90.00, 60.00, 60.00, 'nav_ger', 30.00, 'nav_gerCAGER', 'nav_gerCAGERSERVICE', 'nav_gerITEM_INVALID_ACCT', 'nav_gerITEM_INVALID_ACCTCAGER', 'nav_gerITEM_INVALID_ACCTCAGERSERVICE', 'nav_gerITEM_INVALID_ACCTCAGERLOT_INVALID_ACCT', 'nav_gerITEM_INVALID_ACCTCAGERLOT_INVALID_ACCTSERVICE'),
-- Derived plant_location_key
('nav_ger1050', 'ACC_DERIVED_PLANT_LOC', 'Account', '2024-04-25T17:17:17.000+0000', '1050', 'EUR', '2024-05-25', '99991231', 'ITEM_DERIVED_KEY', 'HAUPT', 'none', '1900-01-01', 'LOT_DERIVED_KEY', 'none', 'CAGER', 85.00, 170.00, 170.00, NULL, 255.00, 170.00, 170.00, 'nav_ger', 127.50, 'nav_gerCAGER', 'nav_gerCAGERHAUPT', 'nav_gerITEM_DERIVED_KEY', 'nav_gerITEM_DERIVED_KEYCAGER', 'nav_gerITEM_DERIVED_KEYCAGERHAUPT', 'nav_gerITEM_DERIVED_KEYCAGERLOT_DERIVED_KEY', 'nav_gerITEM_DERIVED_KEYCAGERLOT_DERIVED_KEYHAUPT'),
-- Duplicate record check (should be handled in validation)
('nav_ger1050', 'ACC_DUPLICATE', 'Account', '2024-05-30T19:19:19.000+0000', '1050', 'EUR', '2024-06-30', '99991231', 'ITEM_DUPLICATE', 'LIN', 'none', '1900-01-01', 'LOT_DUPLICATE', 'none', 'CAGER', 55.55, 111.11, 111.11, NULL, 166.65, 111.11, 111.11, 'nav_ger', 83.33, 'nav_gerCAGER', 'nav_gerCAGERLIN', 'nav_gerITEM_DUPLICATE', 'nav_gerITEM_DUPLICATECAGER', 'nav_gerITEM_DUPLICATECAGERLIN', 'nav_gerITEM_DUPLICATECAGERLOT_DUPLICATE', 'nav_gerITEM_DUPLICATECAGERLOT_DUPLICATELIN'),
-- Record with blank spaces in lot_no_
('nav_ger1050', 'ACC_BLANK_LOT', 'Account', '2024-06-15T21:21:21.000+0000', '1050', 'EUR', '2024-07-15', '99991231', 'ITEM_BLANK_LOT', 'AH-LOC', 'none', '1900-01-01', 'LOT 67890', 'none', 'CAGER', 65.00, 130.00, 130.00, NULL, 195.00, 130.00, 130.00, 'nav_ger', 97.50, 'nav_gerCAGER', 'nav_gerCAGERAH-LOC', 'nav_gerITEM_BLANK_LOT', 'nav_gerITEM_BLANK_LOTCAGER', 'nav_gerITEM_BLANK_LOTCAGERAH-LOC', 'nav_gerITEM_BLANK_LOTCAGERLOT 67890', 'nav_gerITEM_BLANK_LOTCAGERLOT 67890AH-LOC'),
-- Record with missing g_account (should not be inserted)
(NULL, 'ACC_MISSING', 'Account', '2024-07-05T23:23:23.000+0000', '1050', 'EUR', '2024-08-05', '99991231', 'ITEM_MISSING_ACCOUNT', 'SERVICE', 'none', '1900-01-01', 'LOT_MISSING_ACCT', 'none', 'CAGER', 70.00, 140.00, 140.00, NULL, 210.00, 140.00, 140.00, 'nav_ger', 105.00, 'nav_gerCAGER', 'nav_gerCAGERSERVICE', 'nav_gerITEM_MISSING_ACCOUNT', 'nav_gerITEM_MISSING_ACCOUNTCAGER', 'nav_gerITEM_MISSING_ACCOUNTCAGERSERVICE', 'nav_gerITEM_MISSING_ACCOUNTCAGERLOT_MISSING_ACCT', 'nav_gerITEM_MISSING_ACCOUNTCAGERLOT_MISSING_ACCTSERVICE'),
-- Record with invalid g_qty_on_hand (non-decimal)
('nav_ger1050', 'ACC_INVALID_QTY', 'Account', '2024-08-20T02:02:02.000+0000', '1050', 'EUR', '2024-09-20', '99991231', 'ITEM_INVALID_QTY', 'MATRIUM', 'none', '1900-01-01', 'LOT_INVALID_QTY', 'none', 'CAGER', 80.00, 160.00, 160.00, NULL, 240.00, 'invalid_decimal', 160.00, 'nav_ger', 120.00, 'nav_gerCAGER', 'nav_gerCAGERMATRIUM', 'nav_gerITEM_INVALID_QTY', 'nav_gerITEM_INVALID_QTYCAGER', 'nav_gerITEM_INVALID_QTYCAGERMATRIUM', 'nav_gerITEM_INVALID_QTYCAGERLOT_INVALID_QTY', 'nav_gerITEM_INVALID_QTYCAGERLOT_INVALID_QTYMATRIUM'),
-- Record with missing g_assignment_type (default to 'Account')
('nav_ger1050', 'ACC_NO_ASSIGN', NULL, '2024-09-25T04:04:04.000+0000', '1050', 'EUR', '2024-10-25', '99991231', 'ITEM_NO_ASSIGN', 'QS-WE', 'none', '1900-01-01', 'LOT_NO_ASSIGN', 'none', 'CAGER', 95.00, 190.00, 190.00, NULL, 285.00, 190.00, 190.00, 'nav_ger', 142.50, 'nav_gerCAGER', 'nav_gerCAGERQS-WE', 'nav_gerITEM_NO_ASSIGN', 'nav_gerITEM_NO_ASSIGNCAGER', 'nav_gerITEM_NO_ASSIGNCAGERQS-WE', 'nav_gerITEM_NO_ASSIGNCAGERLOT_NO_ASSIGN', 'nav_gerITEM_NO_ASSIGNCAGERLOT_NO_ASSIGNQS-WE'),
-- Record with valid ISO 4217 currency code
('nav_ger1050', 'ACC_VALID_CURRENCY', 'Account', '2024-10-30T06:06:06.000+0000', '1050', 'EUR', '2024-11-30', '99991231', 'ITEM_VALID_CUR', 'HAUPT', 'none', '1900-01-01', 'LOT_VALID_CUR', 'none', 'CAGER', 110.00, 220.00, 220.00, NULL, 330.00, 220.00, 220.00, 'nav_ger', 165.00, 'nav_gerCAGER', 'nav_gerCAGERHAUPT', 'nav_gerITEM_VALID_CUR', 'nav_gerITEM_VALID_CURCAGER', 'nav_gerITEM_VALID_CURCAGERHAUPT', 'nav_gerITEM_VALID_CURCAGERLOT_VALID_CUR', 'nav_gerITEM_VALID_CURCAGERLOT_VALID_CURHAUPT'),
-- Record with invalid currency code
('nav_ger1050', 'ACC_INVALID_CURRENCY', 'Account', '2024-11-15T08:08:08.000+0000', '1050', 'INVALID', '2024-12-15', '99991231', 'ITEM_INVALID_CUR', 'LIN', 'none', '1900-01-01', 'LOT_INVALID_CUR', 'none', 'CAGER', 120.00, 240.00, 240.00, NULL, 360.00, 240.00, 240.00, 'nav_ger', 180.00, 'nav_gerCAGER', 'nav_gerCAGERLIN', 'nav_gerITEM_INVALID_CUR', 'nav_gerITEM_INVALID_CURCAGER', 'nav_gerITEM_INVALID_CURCAGERLIN', 'nav_gerITEM_INVALID_CURCAGERLOT_INVALID_CUR', 'nav_gerITEM_INVALID_CURCAGERLOT_INVALID_CURLIN'),
-- Record with current date for g_capture_dt_yyyymmdd
('nav_ger1050', 'ACC_CURRENT_DATE', 'Account', CURRENT_TIMESTAMP(), '1050', 'EUR', '2024-07-01', '99991231', 'ITEM_CURRENT_DATE', 'SERVICE', 'none', '1900-01-01', 'LOT_CURRENT_DATE', 'none', 'CAGER', 130.00, 260.00, 260.00, NULL, 390.00, 260.00, 260.00, 'nav_ger', 195.00, 'nav_gerCAGER', 'nav_gerCAGERSERVICE', 'nav_gerITEM_CURRENT_DATE', 'nav_gerITEM_CURRENT_DATECAGER', 'nav_gerITEM_CURRENT_DATECAGERSERVICE', 'nav_gerITEM_CURRENT_DATECAGERLOT_CURRENT_DATE', 'nav_gerITEM_CURRENT_DATECAGERLOT_CURRENT_DATESERVICE'),
-- Record with multiple joins without duplication
('nav_ger1050', 'ACC_NO_DUPLICATE_JOIN', 'Account', '2024-12-05T10:10:10.000+0000', '1050', 'EUR', '2024-12-31', '99991231', 'ITEM_NO_DUP_JOIN', 'MATRIUM', 'none', '1900-01-01', 'LOT_NO_DUP_JOIN', 'none', 'CAGER', 140.00, 280.00, 280.00, NULL, 420.00, 280.00, 280.00, 'nav_ger', 210.00, 'nav_gerCAGER', 'nav_gerCAGERMATRIUM', 'nav_gerITEM_NO_DUP_JOIN', 'nav_gerITEM_NO_DUP_JOINCAGER', 'nav_gerITEM_NO_DUP_JOINCAGERMATRIUM', 'nav_gerITEM_NO_DUP_JOINCAGERLOT_NO_DUP_JOIN', 'nav_gerITEM_NO_DUP_JOINCAGERLOT_NO_DUP_JOINMATRIUM'),
-- Record to validate ISO 4217 compliance
('nav_ger1050', 'ACC_ISO_COMPLIANT', 'Account', '2024-01-20T12:12:12.000+0000', '1050', 'EUR', '2024-02-20', '99991231', 'ITEM_ISO_COMPLIANT', 'AH-LOC', 'none', '1900-01-01', 'LOT_ISO_COMPLIANT', 'none', 'CAGER', 150.00, 300.00, 300.00, NULL, 450.00, 300.00, 300.00, 'nav_ger', 225.00, 'nav_gerCAGER', 'nav_gerCAGERAH-LOC', 'nav_gerITEM_ISO_COMPLIANT', 'nav_gerITEM_ISO_COMPLIANTCAGER', 'nav_gerITEM_ISO_COMPLIANTCAGERAH-LOC', 'nav_gerITEM_ISO_COMPLIANTCAGERLOT_ISO_COMPLIANT', 'nav_gerITEM_ISO_COMPLIANTCAGERLOT_ISO_COMPLIANTAH-LOC'),
-- Record with multiple special characters
('nav_ger1050', 'ACC_MULTI_CHAR', 'Account', '2024-02-25T14:14:14.000+0000', '1050', 'EUR', '2024-03-25', '99991231', 'ITEM@#$', 'AH-LOC', 'none', '1900-01-01', 'LOT@#$', 'none', 'CAGER', 160.00, 320.00, 320.00, NULL, 480.00, 320.00, 320.00, 'nav_ger', 240.00, 'nav_gerCAGER', 'nav_gerCAGERAH-LOC', 'nav_gerITEM@#$', 'nav_gerITEM@#$$CAGER', 'nav_gerITEM@#$$CAGERAH-LOC', 'nav_gerITEM@#$$CAGERLOT@#$', 'nav_gerITEM@#$$CAGERLOT@#$$AH-LOC'),
-- Record with missing g_assignment_type and g_account
(NULL, NULL, NULL, '2024-03-30T16:16:16.000+0000', '1050', 'EUR', '2024-04-30', '99991231', 'ITEM_MISSING_BOTH', 'LIN', 'none', '1900-01-01', 'LOT_MISSING_BOTH', 'none', 'CAGER', 175.00, 350.00, 350.00, NULL, 525.00, 350.00, 350.00, 'nav_ger', 262.50, 'nav_gerCAGER', 'nav_gerCAGERLIN', 'nav_gerITEM_MISSING_BOTH', 'nav_gerITEM_MISSING_BOTHCAGER', 'nav_gerITEM_MISSING_BOTHCAGERLIN', 'nav_gerITEM_MISSING_BOTHCAGERLOT_MISSING_BOTH', 'nav_gerITEM_MISSING_BOTHCAGERLOT_MISSING_BOTHLIN'),
-- Record with complex concatenation in derived keys
('nav_ger1050', 'ACC_COMPLEX_CONCAT', 'Account', '2024-04-10T18:18:18.000+0000', '1050', 'EUR', '2024-05-10', '99991231', 'ITEM_COMPLEX', 'AH-LOC', 'none', '1900-01-01', 'LOT_COMPLEX', 'none', 'CAGER', 185.00, 370.00, 370.00, NULL, 555.00, 370.00, 370.00, 'nav_ger', 277.50, 'nav_gerCAGER', 'nav_gerCAGERAH-LOC', 'nav_gerITEM_COMPLEX', 'nav_gerITEM_COMPLEXCAGER', 'nav_gerITEM_COMPLEXCAGERAH-LOC', 'nav_gerITEM_COMPLEXCAGERLOT_COMPLEX', 'nav_gerITEM_COMPLEXCAGERLOT_COMPLEXAH-LOC');

-- Note: Records with g_account as NULL or invalid data types are expected to fail insertion or trigger error logs based on validation logic.
