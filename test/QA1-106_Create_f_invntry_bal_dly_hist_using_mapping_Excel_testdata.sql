-- Creating test data for purgo_playground.f_invntry_bal_dly_hist using Databricks SQL

WITH item_ledger AS (
SELECT item_no_, location_code, MAX(posting_date) AS latest_posting_date
FROM purgo_playground.itemledgerentrieswopd
GROUP BY item_no_, location_code
),

itemledgerentries AS (
SELECT ile.item_no_,
       ile.location_code,
       ile.posting_date,
       ile.serial_no_,
       ile.lot_no_,
       ile.expiration_date,
       item_ledger.latest_posting_date
FROM purgo_playground.itemledgerentrieswopd ile
JOIN item_ledger ON trim(ile.item_no_) = trim(item_ledger.item_no_)
AND trim(ile.location_code) = trim(item_ledger.location_code)
AND ile.posting_date = item_ledger.latest_posting_date
),

reservation_entries AS (
SELECT reservation_status, source_type, quantity_base, item_no_, location_code
FROM purgo_playground.reservation_entry
WHERE reservation_status = '0' AND source_type = '37'
),

items_on_hand AS (
SELECT qty_on_hand, item_no_, location_code
FROM purgo_playground.item_qty_on_hand
),

f_invntry_bal_dly_hist_test_data AS (
SELECT 
  CONCAT('nav_ger', '1050') AS co_key,
  smd.profit_center AS g_account,
  'Account' AS g_assignment_type,
  CURRENT_TIMESTAMP() AS g_capture_dt_yyyymmdd,
  '1050' AS g_company_cd,
  'EUR' AS g_company_currency_cd,
  COALESCE(ile.expiration_date, '9999-12-31') AS g_expiration_dt_yyyymmdd,
  ile.item_no_ AS g_item_nbr,
  ile.location_code AS g_location_cd,
  'none' AS g_location_status_cd,
  ile.posting_date AS g_lot_effective_dt_yyyymmdd,
  COALESCE(ile.lot_no_, ile.serial_no_, 'none') AS g_lot_nbr,
  'none' AS g_lot_status_cd,
  'CAGER' AS g_plant_cd,
  CASE WHEN re.quantity_base < 0 THEN -1 * re.quantity_base ELSE re.quantity_base END AS g_qty_allocated,
  CASE WHEN ioh.location_code IN ('HAUPT', 'GERMERING', 'LIN', 'MATRIUM') THEN ioh.qty_on_hand ELSE 0 END AS g_qty_available,
  CASE WHEN ioh.location_code IN ('HAUPT', 'GERMERING', 'LIN', 'MATRIUM') THEN ioh.qty_on_hand ELSE NULL END AS g_qty_financial_nettable,
  NULL AS g_qty_in_transit,
  CASE WHEN ioh.location_code IN ('HAUPT', 'QS-WE', 'GERMERING', 'SERVICE', 'LIN', 'MATRIUM') THEN ioh.qty_on_hand ELSE 0 END AS g_qty_mrp_nettable,
  ioh.qty_on_hand AS g_qty_on_hand,
  CASE WHEN ioh.location_code = 'HAUPT' THEN ioh.qty_on_hand ELSE NULL END AS g_qty_shippable,
  'nav_ger' AS g_source_system_cd,
  iw.Standard_Cost AS g_unit_cost_company_currency,
  CONCAT('nav_ger', 'CAGER') AS plant_key,
  CONCAT('nav_ger', 'CAGER', ile.location_code) AS plant_location_key,
  CONCAT('nav_ger', ile.item_no_) AS prod_key,
  CONCAT('nav_ger', ile.item_no_, 'CAGER') AS prod_plant_key,
  CONCAT('nav_ger', ile.item_no_, 'CAGER', ile.location_code) AS prod_plant_location_key,
  CONCAT('nav_ger', ile.item_no_, 'CAGER', ile.lot_no_) AS prod_plant_lot_key,
  CONCAT('nav_ger', ile.item_no_, 'CAGER', ile.lot_no_, ile.location_code) AS prod_plant_lot_location_key

FROM itemledgerentries ile
JOIN reservation_entries re ON trim(ile.item_no_) = trim(re.item_no_)
AND trim(ile.location_code) = trim(re.location_code)
JOIN items_on_hand ioh ON trim(ile.item_no_) = trim(ioh.item_no_)
AND trim(ile.location_code) = trim(ioh.location_code)
LEFT JOIN purgo_playground.sap_master_data smd ON trim(smd.item_no_) = trim(ile.item_no_)
LEFT JOIN purgo_playground.Itemwopd iw ON trim(iw.no_) = trim(ile.item_no_)

LIMIT 30 -- Limiting to 30 rows as required for diverse testing scenarios
)

SELECT * FROM f_invntry_bal_dly_hist_test_data;
