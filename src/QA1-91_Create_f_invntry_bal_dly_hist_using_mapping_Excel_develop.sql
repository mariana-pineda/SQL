/* SQL-based transformation logic for populating the f_invntry_bal_dly_hist table.
   This script uses Common Table Expressions (CTEs) for data transformation and insertion.
   Ensure proper handling of hardcoded values, default dates, conditional calculations, and joins.
*/

/* CTE to obtain the latest posting date for each item and location */
WITH itemledgerentries_latest AS (
  SELECT 
    Item_No_ AS item_no,
    Location_Code AS location_code,
    MAX(Posting_Date) AS latest_posting_date
  FROM purgo_databricks.purgo_playground.itemledgerentrieswopd
  GROUP BY Item_No_, Location_Code
),

/* CTE to filter reservation entries based on status and source type */
reservation_filtered AS (
  SELECT 
    Item_No_ AS item_no,
    Location_Code AS location_code,
    quantity_base
  FROM purgo_databricks.purgo_playground.reservation_entry
  WHERE reservation_status = '0' AND source_type = '37'
),

/* Data transformation CTE applying various business rules, concatenations, and filters */
transformed_data AS (
  SELECT
    'nav_ger' AS g_source_system_cd,                   -- Hardcoded source system code
    '1050' AS g_company_cd,                            -- Hardcoded company code
    'EUR' AS g_company_currency_cd,                    -- Hardcoded currency code
    CURRENT_DATE AS g_capture_dt_yyyymmdd,             -- Current date for capture date
    '99991231' AS g_expiration_dt_yyyymmdd,            -- Default expiration date
    COALESCE(item_ledger.latest_posting_date, '19000101') AS g_lot_effective_dt_yyyymmdd, -- Lot effective date
    item_ledger.item_no AS g_item_nbr,                 -- Item number from ledger entries
    item_ledger.location_code AS g_location_cd,        -- Location code from ledger entries
    'none' AS g_location_status_cd,                    -- Default location status code
    'none' AS g_lot_nbr,                               -- Default lot number
    'none' AS g_lot_status_cd,                         -- Default lot status code
    'CAGER' AS g_plant_cd,                             -- Hardcoded plant code
    CASE WHEN res.quantity_base < 0 THEN -res.quantity_base ELSE res.quantity_base END AS g_qty_allocated, -- Conditional allocation quantity
    CASE WHEN item.location_code IN ('HAUPT', 'GERMERING', 'LIN', 'MATRIUM') THEN item.qty_on_hand ELSE NULL END AS g_qty_available, -- Available quantity based on location
    CASE WHEN item.location_code IN ('HAUPT', 'QS-WE', 'GERMERING', 'SERVICE', 'LIN', 'MATRIUM') THEN item.qty_on_hand ELSE NULL END AS g_qty_mrp_nettable, -- MRP nettable quantity
    CASE WHEN item.location_code IN ('HAUPT', 'GERMERING', 'LIN', 'MATRIUM') THEN item.qty_on_hand ELSE NULL END AS g_qty_on_hand, -- On hand quantity
    CASE WHEN item.location_code = 'HAUPT' THEN item.qty_on_hand ELSE 0.0 END AS g_qty_shippable, -- Shippable quantity based on location
    NULL AS g_qty_in_transit,                          -- Transit quantity is NULL
    item.STANDARD_COST AS g_unit_cost_company_currency -- Unit cost in company currency
  FROM
    purgo_databricks.purgo_playground.item_qty_on_hand AS item
  LEFT JOIN itemledgerentries_latest AS item_ledger
    ON trim(item_ledger.item_no) = trim(item.Item_No_)
    AND trim(item_ledger.location_code) = trim(item.location_code)
  LEFT JOIN reservation_filtered AS res
    ON trim(item_ledger.item_no) = trim(res.item_no)
    AND trim(item_ledger.location_code) = trim(res.location_code)
)

/* Insert processed data into the target table */
INSERT INTO purgo_databricks.purgo_playground.f_invntry_bal_dly_hist
SELECT 
  g_source_system_cd,
  g_company_cd,
  g_company_currency_cd,
  g_capture_dt_yyyymmdd,
  g_expiration_dt_yyyymmdd,
  g_lot_effective_dt_yyyymmdd,
  g_item_nbr,
  g_location_cd,
  g_location_status_cd,
  g_lot_nbr,
  g_lot_status_cd,
  g_plant_cd,
  g_qty_allocated,
  g_qty_available,
  g_qty_mrp_nettable,
  g_qty_on_hand,
  g_qty_shippable,
  g_qty_in_transit,
  g_unit_cost_company_currency
FROM transformed_data;
