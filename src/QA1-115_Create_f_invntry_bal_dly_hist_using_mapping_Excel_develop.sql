/* 
DDL Section: Create f_invntry_bal_dly_hist table if not exists
*/
CREATE TABLE IF NOT EXISTS purgo_databricks.purgo_playground.f_invntry_bal_dly_hist (
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
)
/* 
Using Delta Lake format
*/
USING DELTA
OPTIONS (
    "path" = "purgo_playground/f_invntry_bal_dly_hist",
    "delta.autoOptimize.optimizeWrite" = "true",
    "delta.autoOptimize.autoCompact" = "true"
);

/* 
COMMENT SECTION: Add comments to columns
*/
ALTER TABLE purgo_databricks.purgo_playground.f_invntry_bal_dly_hist
    ALTER COLUMN co_key COMMENT "Concatenate the source_system_cd and g_company_cd column value";

ALTER TABLE purgo_databricks.purgo_playground.f_invntry_bal_dly_hist
    ALTER COLUMN g_account COMMENT "100% Complete Alphanumeric";

ALTER TABLE purgo_databricks.purgo_playground.f_invntry_bal_dly_hist
    ALTER COLUMN g_assignment_type COMMENT "Default value \"Account\"";

ALTER TABLE purgo_databricks.purgo_playground.f_invntry_bal_dly_hist
    ALTER COLUMN g_capture_dt_yyyymmdd COMMENT "Will always be current date";

ALTER TABLE purgo_databricks.purgo_playground.f_invntry_bal_dly_hist
    ALTER COLUMN g_company_cd COMMENT "Hardcode as \"1050\"";

ALTER TABLE purgo_databricks.purgo_playground.f_invntry_bal_dly_hist
    ALTER COLUMN g_company_currency_cd COMMENT "Hardcode as \"EUR\"";

ALTER TABLE purgo_databricks.purgo_playground.f_invntry_bal_dly_hist
    ALTER COLUMN g_dnsa_dt_yyyymmdd COMMENT "Default value Expiration Date";

ALTER TABLE purgo_databricks.purgo_playground.f_invntry_bal_dly_hist
    ALTER COLUMN g_expiration_dt_yyyymmdd COMMENT "Default value \"99991231\"";

ALTER TABLE purgo_databricks.purgo_playground.f_invntry_bal_dly_hist
    ALTER COLUMN g_item_nbr COMMENT "Must be unique in a given system, 100% Complete Alphanumeric";

ALTER TABLE purgo_databricks.purgo_playground.f_invntry_bal_dly_hist
    ALTER COLUMN g_location_cd COMMENT "Default value \"none\", 100% Alphanumeric";

ALTER TABLE purgo_databricks.purgo_playground.f_invntry_bal_dly_hist
    ALTER COLUMN g_location_status_cd COMMENT "Hardcode as \"none\"";

ALTER TABLE purgo_databricks.purgo_playground.f_invntry_bal_dly_hist
    ALTER COLUMN g_lot_effective_dt_yyyymmdd COMMENT "Default value \"19000101\"";

ALTER TABLE purgo_databricks.purgo_playground.f_invntry_bal_dly_hist
    ALTER COLUMN g_lot_nbr COMMENT "Default value \"none\" if lot_no_ or serial_no_ contains blank space";

ALTER TABLE purgo_databricks.purgo_playground.f_invntry_bal_dly_hist
    ALTER COLUMN g_lot_status_cd COMMENT "Hardcode as \"none\"";

ALTER TABLE purgo_databricks.purgo_playground.f_invntry_bal_dly_hist
    ALTER COLUMN g_plant_cd COMMENT "Hardcode as \"CAGER\", 100% Complete Alphanumeric";

ALTER TABLE purgo_databricks.purgo_playground.f_invntry_bal_dly_hist
    ALTER COLUMN g_qty_allocated COMMENT "A subset of g_quantity_available, Decimal(10,2)";

ALTER TABLE purgo_databricks.purgo_playground.f_invntry_bal_dly_hist
    ALTER COLUMN g_qty_available COMMENT "A subset of g_quantity_mrp_nettable based on location codes, Decimal(10,2)";

ALTER TABLE purgo_databricks.purgo_playground.f_invntry_bal_dly_hist
    ALTER COLUMN g_qty_financial_nettable COMMENT "A subset of g_quantity_on_hand with exceptions, Decimal(10,2)";

ALTER TABLE purgo_databricks.purgo_playground.f_invntry_bal_dly_hist
    ALTER COLUMN g_qty_in_transit COMMENT "Hardcoded to NULL";

ALTER TABLE purgo_databricks.purgo_playground.f_invntry_bal_dly_hist
    ALTER COLUMN g_qty_mrp_nettable COMMENT "A subset of g_quantity_on_hand based on location codes, Decimal(10,2)";

ALTER TABLE purgo_databricks.purgo_playground.f_invntry_bal_dly_hist
    ALTER COLUMN g_qty_on_hand COMMENT "100% Decimal";

ALTER TABLE purgo_databricks.purgo_playground.f_invntry_bal_dly_hist
    ALTER COLUMN g_qty_shippable COMMENT "A subset of g_quantity_available based on location code \"HAUPT\", Decimal(10,2)";

ALTER TABLE purgo_databricks.purgo_playground.f_invntry_bal_dly_hist
    ALTER COLUMN g_source_system_cd COMMENT "Hardcoded to \"nav_ger\", 100% Complete Alphanumeric";

ALTER TABLE purgo_databricks.purgo_playground.f_invntry_bal_dly_hist
    ALTER COLUMN g_unit_cost_company_currency COMMENT "Decimal(10,2)";

ALTER TABLE purgo_databricks.purgo_playground.f_invntry_bal_dly_hist
    ALTER COLUMN plant_key COMMENT "Concatenate the source_system_cd and g_plant_cd column value";

ALTER TABLE purgo_databricks.purgo_playground.f_invntry_bal_dly_hist
    ALTER COLUMN plant_location_key COMMENT "Concatenate the source_system_cd, g_plant_cd, and g_location_cd column values";

ALTER TABLE purgo_databricks.purgo_playground.f_invntry_bal_dly_hist
    ALTER COLUMN prod_key COMMENT "Concatenate the source_system_cd and g_item_nbr column values";

ALTER TABLE purgo_databricks.purgo_playground.f_invntry_bal_dly_hist
    ALTER COLUMN prod_plant_key COMMENT "Concatenate the source_system_cd, g_item_nbr, and g_plant_cd column values";

ALTER TABLE purgo_databricks.purgo_playground.f_invntry_bal_dly_hist
    ALTER COLUMN prod_plant_location_key COMMENT "Concatenate the source_system_cd, g_item_nbr, g_plant_cd, and g_location_cd column values";

ALTER TABLE purgo_databricks.purgo_playground.f_invntry_bal_dly_hist
    ALTER COLUMN prod_plant_lot_key COMMENT "Concatenate the source_system_cd, g_item_nbr, g_plant_cd, and g_lot_nbr column values";

ALTER TABLE purgo_databricks.purgo_playground.f_invntry_bal_dly_hist
    ALTER COLUMN prod_plant_lot_location_key COMMENT "Concatenate the source_system_cd, g_item_nbr, g_plant_cd, g_lot_nbr, and g_location_cd column values";

/* 
Data Insertion Section: Populate f_invntry_bal_dly_hist table
*/
INSERT INTO purgo_databricks.purgo_playground.f_invntry_bal_dly_hist
SELECT
    CONCAT(TRIM(il.src_sys_cd), '1050') AS co_key,
    smd.profit_center AS g_account,
    'Account' AS g_assignment_type,
    current_timestamp() AS g_capture_dt_yyyymmdd,
    '1050' AS g_company_cd,
    'EUR' AS g_company_currency_cd,
    il.expiration_date AS g_dnsa_dt_yyyymmdd,
    DATE('9999-12-31') AS g_expiration_dt_yyyymmdd,
    il.item_no_ AS g_item_nbr,
    COALESCE(TRIM(il.location_code), 'none') AS g_location_cd,
    'none' AS g_location_status_cd,
    DATE('1900-01-01') AS g_lot_effective_dt_yyyymmdd,
    CASE 
        WHEN il.lot_no_ IS NULL OR il.serial_no_ IS NULL OR il.lot_no_ LIKE '% %' OR il.serial_no_ LIKE '% %' 
        THEN 'none' 
        ELSE TRIM(il.lot_no_) 
    END AS g_lot_nbr,
    'none' AS g_lot_status_cd,
    'CAGER' AS g_plant_cd,
    CASE 
        WHEN re.quantity_base < 0 THEN ABS(re.quantity_base) 
        ELSE re.quantity_base 
    END AS g_qty_allocated,
    CASE 
        WHEN iq.location_code IN ('HAUPT', 'GERMERING', 'LIN', 'MATRIUM') 
        THEN iq.qty_on_hand 
        ELSE NULL 
    END AS g_qty_available,
    CASE 
        WHEN iq.location_code IN ('HAUPT','GERMERING','LIN','MATRIUM') 
        THEN iq.qty_on_hand 
        ELSE NULL 
    END AS g_qty_financial_nettable,
    NULL AS g_qty_in_transit,
    CASE 
        WHEN iq.location_code IN ('HAUPT','QS-WE','GERMERING','SERVICE','LIN','MATRIUM') 
             OR TRIM(iq.location_code) LIKE 'AH-%'
        THEN iq.qty_on_hand 
        ELSE NULL 
    END AS g_qty_mrp_nettable,
    iq.qty_on_hand AS g_qty_on_hand,
    CASE 
        WHEN iq.location_code = 'HAUPT' 
        THEN iq.qty_on_hand 
        ELSE NULL 
    END AS g_qty_shippable,
    'nav_ger' AS g_source_system_cd,
    iw.standard_cost AS g_unit_cost_company_currency,
    CONCAT('nav_ger', 'CAGER') AS plant_key,
    CONCAT('nav_ger', 'CAGER', COALESCE(TRIM(il.location_code), 'none')) AS plant_location_key,
    CONCAT('nav_ger', il.item_no_) AS prod_key,
    CONCAT('nav_ger', il.item_no_, 'CAGER') AS prod_plant_key,
    CONCAT('nav_ger', il.item_no_, 'CAGER', COALESCE(TRIM(il.location_code), 'none')) AS prod_plant_location_key,
    CONCAT('nav_ger', il.item_no_, 'CAGER', il.lot_no_) AS prod_plant_lot_key,
    CONCAT('nav_ger', il.item_no_, 'CAGER', il.lot_no_, COALESCE(TRIM(il.location_code), 'none')) AS prod_plant_lot_location_key
FROM
    purgo_databricks.purgo_playground.item_qty_on_hand iq
LEFT OUTER JOIN
    purgo_databricks.purgo_playground.itemledgerentrieswopd il
    ON TRIM(il.item_no_) = TRIM(iq.item_no_) AND TRIM(il.location_code) = TRIM(iq.location_code)
LEFT OUTER JOIN
    purgo_databricks.purgo_playground.sap_master_data smd
    ON TRIM(smd.item_no_) = TRIM(il.item_no_)
LEFT OUTER JOIN
    purgo_databricks.purgo_playground.reservation_entry re
    ON TRIM(re.item_no_) = TRIM(il.item_no_) AND TRIM(re.location_code) = TRIM(il.location_code)
LEFT OUTER JOIN
    purgo_databricks.purgo_playground.Itemwopd iw
    ON TRIM(iw.no_) = TRIM(iq.item_no_)
WHERE
    re.reservation_status = "0" AND re.source_type = "37";
