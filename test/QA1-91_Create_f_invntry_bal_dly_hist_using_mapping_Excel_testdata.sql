-- Create test data using CTEs for f_invntry_bal_dly_hist table

-- CTE to generate test data
WITH item_qty_on_hand_cte AS (
  SELECT 
    'nav_ger' AS g_source_system_cd, -- Happy path: valid hardcoded value
    '1050' AS g_company_cd,          -- Happy path: valid hardcoded value
    'EUR' AS g_company_currency_cd,  -- Happy path: valid hardcoded value
    CURRENT_DATE AS g_capture_dt_yyyymmdd, -- Happy path: using current date
    '99991231' AS g_expiration_dt_yyyymmdd, -- Edge case: default value for expiration date
    '19000101' AS g_lot_effective_dt_yyyymmdd, -- Edge case: default value for lot effective date
    'ITEM123' AS g_item_nbr, -- Happy path: valid item number
    NULL AS g_location_cd,  -- NULL scenario
    'none' AS g_location_status_cd, -- Edge case: hardcode as none
    'LOT456' AS g_lot_nbr, -- Happy path: valid lot number
    'none' AS g_lot_status_cd, -- Edge case: hardcode as none
    'CAGER' AS g_plant_cd, -- Happy path: valid plant code
    NULL AS g_qty_in_transit, -- Error case: NULL value
    CASE WHEN qty_on_hand < 0 THEN -qty_on_hand ELSE qty_on_hand END AS g_qty_allocated,
    CASE WHEN Location_Code IN ('HAUPT', 'QS-WE', 'GERMERING', 'SERVICE', 'LIN', 'MATRIUM') THEN qty_on_hand ELSE NULL END AS g_qty_mrp_nettable,
    CASE WHEN Location_Code IN ('HAUPT','GERMERING','LIN','MATRIUM') THEN qty_on_hand ELSE NULL END AS g_qty_on_hand,
    CASE WHEN Location_Code = 'HAUPT' THEN qty_on_hand ELSE 0.0 END AS g_qty_shippable,
    STANDARD_COST AS g_unit_cost_company_currency
  FROM purgo_playground.purgo_playground.item_qty_on_hand
)

-- Insert Into target table using CTE
INSERT INTO purgo_playground.purgo_playground.f_invntry_bal_dly_hist
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
FROM item_qty_on_hand_cte
WHERE trim(reservation_entry.Item_No_) = trim(item_qty_on_hand_cte.g_item_nbr)
AND trim(reservation_entry.Location_Code) = trim(item_qty_on_hand_cte.g_location_cd)


