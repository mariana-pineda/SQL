
CREATE TABLE purgo_playground.f_item (
  item_nbr STRING,
  item_vb LONG,
  delivery_dt DECIMAL(38, 0),
  item_inv_type STRING,
  txn_nbr STRING,
  primary_qty DOUBLE,
  qty_in_hand DOUBLE,
  qty_on_hold DOUBLE,
  item_serial_nbr STRING,
  package_nbr STRING,
  crt_dt TIMESTAMP,
  updt_dt TIMESTAMP
)
