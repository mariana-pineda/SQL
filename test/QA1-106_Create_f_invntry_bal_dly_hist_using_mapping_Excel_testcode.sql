-- SQL Test Code for Databricks Environment

/* ---------------------------------------------------------------------------
   Configuration and Setup 
----------------------------------------------------------------------------*/

/*
Assumption: The following test script assumes the presence of necessary tables
in the purgo_playground schema and that the 'spark' object is configured.
*/

/* ---------------------------------------------------------------------------
   SQL Code for Validating the Structure and Data Integrity of purgo_playground.f_invntry_bal_dly_hist
----------------------------------------------------------------------------*/

/* Validate if the f_invntry_bal_dly_hist table creation follows defined specifications */
CREATE TABLE IF NOT EXISTS purgo_playground.f_invntry_bal_dly_hist (
    co_key STRING NOT NULL, 
    g_account STRING,
    g_assignment_type STRING NOT NULL DEFAULT 'Account',
    g_capture_dt_yyyymmdd TIMESTAMP NOT NULL,
    g_company_cd STRING NOT NULL DEFAULT '1050',
    g_company_currency_cd STRING NOT NULL DEFAULT 'EUR',
    g_dnsa_dt_yyyymmdd TIMESTAMP,
    g_expiration_dt_yyyymmdd TIMESTAMP DEFAULT '9999-12-31',
    g_item_nbr STRING,
    g_location_cd STRING,
    g_location_status_cd STRING DEFAULT 'none',
    g_lot_effective_dt_yyyymmdd TIMESTAMP,
    g_lot_nbr STRING,
    g_lot_status_cd STRING DEFAULT 'none',
    g_plant_cd STRING DEFAULT 'CAGER',
    g_qty_allocated DECIMAL(38, 20),
    g_qty_available DECIMAL(38, 20),
    g_qty_financial_nettable DECIMAL(38, 20),
    g_qty_in_transit DECIMAL(38, 20) DEFAULT NULL,
    g_qty_mrp_nettable DECIMAL(38, 20),
    g_qty_on_hand DECIMAL(38, 20),
    g_qty_shippable DECIMAL(38, 20),
    g_source_system_cd STRING DEFAULT 'nav_ger',
    g_unit_cost_company_currency STRING,
    plant_key STRING,
    plant_location_key STRING,
    prod_key STRING,
    prod_plant_key STRING,
    prod_plant_location_key STRING,
    prod_plant_lot_key STRING,
    prod_plant_lot_location_key STRING
) USING DELTA
OPTIONS (
  comment = 'Table to store daily inventory balance history'
);

/* ---------------------------------------------------------------------------
   Test for Data Type Conversion and NULL Handling
----------------------------------------------------------------------------*/

-- Test SELECT to validate proper data type mappings and NULL/Default handling
WITH cte_test_data AS (
    SELECT 
        co_key,
        g_account,
        g_assignment_type,
        g_capture_dt_yyyymmdd,
        g_company_cd,
        g_company_currency_cd,
        g_expiration_dt_yyyymmdd,
        g_item_nbr,
        g_location_cd,
        g_location_status_cd,
        g_lot_effective_dt_yyyymmdd,
        g_lot_nbr,
        g_lot_status_cd,
        g_plant_cd,
        g_qty_allocated,
        g_qty_available,
        g_qty_financial_nettable,
        g_qty_in_transit,
        g_qty_mrp_nettable,
        g_qty_on_hand,
        g_qty_shippable,
        g_source_system_cd,
        g_unit_cost_company_currency,
        plant_key,
        plant_location_key,
        prod_key,
        prod_plant_key,
        prod_plant_location_key,
        prod_plant_lot_key,
        prod_plant_lot_location_key
    FROM purgo_playground.f_invntry_bal_dly_hist
    WHERE g_capture_dt_yyyymmdd = CURRENT_DATE
    LIMIT 10
)
SELECT * FROM cte_test_data;

/* ---------------------------------------------------------------------------
   MERGE Operation Test for purgo_playground.f_invntry_bal_dly_hist
----------------------------------------------------------------------------*/

-- Perform a merge operation to validate MERGE functionality
MERGE INTO purgo_playground.f_invntry_bal_dly_hist AS target
USING (
    SELECT 
        'nav_ger105001' AS co_key, 
        'ProfitCenter1' AS g_account, 
        CURRENT_TIMESTAMP() AS g_capture_dt_yyyymmdd, 
        'Item0100' AS g_item_nbr, 
        50.0 AS g_qty_allocated, 
        100.0 AS g_qty_on_hand -- Sample test data
) AS source
ON target.co_key = source.co_key
WHEN MATCHED THEN
  UPDATE SET 
    target.g_qty_allocated = source.g_qty_allocated,
    target.g_qty_on_hand = source.g_qty_on_hand
WHEN NOT MATCHED THEN
  INSERT (co_key, g_account, g_capture_dt_yyyymmdd, g_item_nbr, g_qty_allocated, g_qty_on_hand) VALUES
  (source.co_key, source.g_account, source.g_capture_dt_yyyymmdd, source.g_item_nbr, source.g_qty_allocated, source.g_qty_on_hand);

/* ---------------------------------------------------------------------------
   Validate Data Quality and Business Rules
----------------------------------------------------------------------------*/

-- Validate specific business logic / constraints
SELECT 
    co_key, 
    COUNT(DISTINCT g_item_nbr) AS unique_items_count
FROM purgo_playground.f_invntry_bal_dly_hist
GROUP BY co_key
HAVING COUNT(DISTINCT g_item_nbr) = 0;

/* Report any constraint violation */
-- Expectation: no result implies no violations found

/* ---------------------------------------------------------------------------
   Cleanup operations to maintain test integrity
----------------------------------------------------------------------------*/

-- Delete specific test records used in validation
DELETE FROM purgo_playground.f_invntry_bal_dly_hist WHERE co_key LIKE 'nav_ger1050%';

