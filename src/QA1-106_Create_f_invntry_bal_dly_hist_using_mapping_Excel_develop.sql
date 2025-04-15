-- SQL Code for Creating and Populating f_invntry_bal_dly_hist Table in Databricks Environment

/* ---------------------------------------------------------------------------
   Configuration Setup
----------------------------------------------------------------------------*/

-- Assumption: Necessary tables and mappings are present in purgo_playground schema

/* ---------------------------------------------------------------------------
   SQL Code for Building and Populating the f_invntry_bal_dly_hist Table
----------------------------------------------------------------------------*/

CREATE OR REPLACE TABLE purgo_playground.f_invntry_bal_dly_hist (
    co_key STRING NOT NULL COMMENT 'Concatenated source_system_cd and g_company_cd',
    g_account STRING COMMENT 'Mapped from sap_master_data profit_center',
    g_assignment_type STRING NOT NULL DEFAULT 'Account' COMMENT 'Hardcoded to Account',
    g_capture_dt_yyyymmdd TIMESTAMP NOT NULL COMMENT 'Current system date',
    g_company_cd STRING NOT NULL DEFAULT '1050' COMMENT 'Hardcoded to 1050',
    g_company_currency_cd STRING NOT NULL DEFAULT 'EUR' COMMENT 'Hardcoded to EUR',
    g_dnsa_dt_yyyymmdd TIMESTAMP COMMENT 'Mapped from itemledgerentrieswopd.Expiration_Date',
    g_expiration_dt_yyyymmdd TIMESTAMP DEFAULT '9999-12-31' COMMENT 'Default to 99991231 if not represented',
    g_item_nbr STRING COMMENT 'Mapped from itemledgerentrieswopd.Item_No_',
    g_location_cd STRING COMMENT 'Mapped from itemledgerentrieswopd.Location_Code',
    g_location_status_cd STRING DEFAULT 'none' COMMENT 'Hardcoded to none',
    g_lot_effective_dt_yyyymmdd TIMESTAMP COMMENT 'Mapped from itemledgerentrieswopd.Posting_Date',
    g_lot_nbr STRING COMMENT 'Mapped from itemledgerentrieswopd.serial_no_, lot_no_',
    g_lot_status_cd STRING DEFAULT 'none' COMMENT 'Hardcoded to none',
    g_plant_cd STRING DEFAULT 'CAGER' COMMENT 'Hardcoded to CAGER',
    g_qty_allocated DECIMAL(38, 20) COMMENT 'Logic from reservation_entry quantity_base',
    g_qty_available DECIMAL(38, 20) COMMENT 'Derived logic in item_qty_on_hand.qty_on_hand',
    g_qty_financial_nettable DECIMAL(38, 20) COMMENT 'Derived logic in item_qty_on_hand.qty_on_hand',
    g_qty_in_transit DECIMAL(38, 20) DEFAULT NULL COMMENT 'Hardcoded to NULL',
    g_qty_mrp_nettable DECIMAL(38, 20) COMMENT 'Derived logic in item_qty_on_hand.qty_on_hand',
    g_qty_on_hand DECIMAL(38, 20) COMMENT 'Mapped from item_qty_on_hand.qty_on_hand',
    g_qty_shippable DECIMAL(38, 20) COMMENT 'Logic in item_qty_on_hand.qty_on_hand',
    g_source_system_cd STRING DEFAULT 'nav_ger' COMMENT 'Hardcoded to nav_ger',
    g_unit_cost_company_currency STRING COMMENT 'Mapped from Itemwopd.Standard_Cost',
    plant_key STRING COMMENT 'Concatenated source_system_cd and g_plant_cd',
    plant_location_key STRING COMMENT 'Concatenated source_system_cd, g_plant_cd, g_location_cd',
    prod_key STRING COMMENT 'Concatenated source_system_cd and g_item_nbr',
    prod_plant_key STRING COMMENT 'Concatenated source_system_cd, g_item_nbr, g_plant_cd',
    prod_plant_location_key STRING COMMENT 'Concatenated source_system_cd, g_item_nbr, g_plant_cd, g_location_cd',
    prod_plant_lot_key STRING COMMENT 'Concatenated source_system_cd, g_item_nbr, g_plant_cd, g_lot_nbr',
    prod_plant_lot_location_key STRING COMMENT 'Concatenated source_system_cd, g_item_nbr, g_plant_cd, g_lot_nbr, g_location_cd'
) USING DELTA
OPTIONS (
  comment = 'Table to store daily inventory balance history'
);

-- Insert Data into f_invntry_bal_dly_hist Table
WITH itemledger AS (
    SELECT 
        item_no_,
        location_code,
        serial_no_,
        lot_no_,
        posting_date,
        expiration_date,
        Standard_Cost
    FROM purgo_playground.itemledgerentrieswopd
    WHERE posting_date = (
        SELECT MAX(posting_date) FROM purgo_playground.itemledgerentrieswopd
    )
),
reservation AS (
    SELECT 
        Item_No_,
        location_code,
        quantity_base
    FROM purgo_playground.reservation_entry
    WHERE reservation_status = '0' AND source_type = '37'
),
sap_master AS (
    SELECT 
        Item_No_,
        profit_center
    FROM purgo_playground.sap_master_data
),
item_qty AS (
    SELECT 
        Item_No_,
        location_code,
        qty_on_hand
    FROM purgo_playground.item_qty_on_hand
)

INSERT INTO purgo_playground.f_invntry_bal_dly_hist
SELECT 
    CONCAT("nav_ger", '1050'),
    sap.profit_center,
    'Account',
    CURRENT_TIMESTAMP(),
    '1050',
    'EUR',
    item.expiration_date,
    COALESCE(item.expiration_date, '9999-12-31'),
    item.item_no_,
    item.location_code,
    CASE WHEN item.location_code IS NOT NULL THEN item.location_code ELSE 'none' END,
    item.posting_date,
    COALESCE(
        TRIM(item.seral_no_),
        TRIM(item.lot_no_),
        'none'
    ),
    'none',
    'CAGER',
    CASE 
        WHEN res.quantity_base < 0 THEN res.quantity_base * -1 
        ELSE res.quantity_base 
    END,
    CASE WHEN item_qty.location_code IN ('HAUPT', 'GERMERING', 'LIN', 'MATRIUM') THEN item_qty.qty_on_hand ELSE NULL END,
    CASE WHEN item_qty.location_code IN ('HAUPT', 'GERMERING', 'LIN', 'MATRIUM') THEN item_qty.qty_on_hand ELSE NULL END,
    NULL,
    CASE 
        WHEN item_qty.location_code IN ('HAUPT', 'QS-WE', 'GERMERING', 'SERVICE', 'LIN', 'MATRIUM') THEN item_qty.qty_on_hand
        WHEN LEFT(RTRIM(item_qty.location_code), 3) = 'AH-' THEN item_qty.qty_on_hand
        ELSE NULL 
    END,
    item_qty.qty_on_hand,
    CASE WHEN item_qty.location_code = 'HAUPT' THEN item_qty.qty_on_hand ELSE NULL END,
    'nav_ger',
    item.Standard_Cost,
    CONCAT("nav_ger", 'CAGER'),
    CONCAT("nav_ger", 'CAGER', item.location_code),
    CONCAT("nav_ger", item.item_no_),
    CONCAT("nav_ger", item.item_no_, 'CAGER'),
    CONCAT("nav_ger", item.item_no_, 'CAGER', item.location_code),
    CONCAT("nav_ger", item.item_no_, 'CAGER', COALESCE(item.serial_no_, item.lot_no_, 'none')),
    CONCAT("nav_ger", item.item_no_, 'CAGER', COALESCE(item.serial_no_, item.lot_no_, 'none'), item.location_code)
FROM itemledger item
LEFT JOIN reservation res ON TRIM(item.item_no_) = TRIM(res.Item_No_) AND TRIM(item.location_code) = TRIM(res.location_code)
LEFT JOIN sap_master sap ON TRIM(item.item_no_) = TRIM(sap.Item_No_)
LEFT JOIN item_qty ON TRIM(item.item_no_) = TRIM(item_qty.Item_No_) AND TRIM(item.location_code) = TRIM(item_qty.location_code);

/* ---------------------------------------------------------------------------
   End of Code Block
----------------------------------------------------------------------------*/
