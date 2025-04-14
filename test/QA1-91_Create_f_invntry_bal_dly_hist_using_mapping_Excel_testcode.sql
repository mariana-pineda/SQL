/* SQL Test code for populating f_invntry_bal_dly_hist table based on the given specifications.
   Use CTEs for data transformation and insertion operations.
   Ensure proper handling of NULL values and hardcoded strings.
   Validate integration logic with joins and schema matching.
*/

-- CTE for data transformation
WITH itemledgerentries_latest AS (
  SELECT 
    Item_No_ AS item_no,
    Location_Code AS location_code,
    MAX(Posting_Date) AS latest_posting_date
  FROM purgo_databricks.purgo_playground.itemledgerentrieswopd
  GROUP BY Item_No_, Location_Code
),
reservation_filtered AS (
  SELECT 
    Item_No_ AS item_no,
    Location_Code AS location_code,
    quantity_base
  FROM purgo_databricks.purgo_playground.reservation_entry
  WHERE reservation_status = '0' AND source_type = '37'
),
transformed_data AS (
  SELECT
    'nav_ger' AS g_source_system_cd,
    '1050' AS g_company_cd,
    'EUR' AS g_company_currency_cd,
    CURRENT_DATE AS g_capture_dt_yyyymmdd,
    '99991231' AS g_expiration_dt_yyyymmdd,
    COALESCE(item_ledger.latest_posting_date, '19000101') AS g_lot_effective_dt_yyyymmdd,
    item_ledger.item_no AS g_item_nbr,
    item_ledger.location_code AS g_location_cd,
    'none' AS g_location_status_cd,
    'none' AS g_lot_nbr, -- Assuming serial_no_ mapping to 'none'
    'none' AS g_lot_status_cd,
    'CAGER' AS g_plant_cd,
    CASE WHEN res.quantity_base < 0 THEN -res.quantity_base ELSE res.quantity_base END AS g_qty_allocated,
    CASE WHEN item.location_code IN ('HAUPT', 'GERMERING', 'LIN', 'MATRIUM') THEN item.qty_on_hand ELSE NULL END AS g_qty_available,
    CASE WHEN item.location_code IN ('HAUPT', 'QS-WE', 'GERMERING', 'SERVICE', 'LIN', 'MATRIUM') THEN item.qty_on_hand ELSE NULL END AS g_qty_mrp_nettable,
    CASE WHEN item.location_code IN ('HAUPT', 'GERMERING', 'LIN', 'MATRIUM') THEN item.qty_on_hand ELSE NULL END AS g_qty_on_hand,
    CASE WHEN item.location_code = 'HAUPT' THEN item.qty_on_hand ELSE 0.0 END AS g_qty_shippable,
    NULL AS g_qty_in_transit,
    item.STANDARD_COST AS g_unit_cost_company_currency
  FROM
    purgo_databricks.purgo_playground.item_qty_on_hand AS item
  LEFT JOIN itemledgerentries_latest AS item_ledger
    ON trim(item_ledger.item_no) = trim(item.Item_No_)
    AND trim(item_ledger.location_code) = trim(item.location_code)
  LEFT JOIN reservation_filtered AS res
    ON trim(item_ledger.item_no) = trim(res.item_no)
    AND trim(item_ledger.location_code) = trim(res.location_code)
)

-- Insert into target table after validation
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
