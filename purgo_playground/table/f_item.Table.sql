
CREATE TABLE purgo_playground.f_item (
	item_nbr VARCHAR(256), 
	item_vb BIGINT, 
	delivery_dt NUMERIC(38, 0), 
	item_inv_type VARCHAR(256), 
	txn_nbr VARCHAR(256), 
	primary_qty DOUBLE PRECISION, 
	qty_in_hand DOUBLE PRECISION, 
	qty_on_hold DOUBLE PRECISION, 
	item_serial_nbr VARCHAR(256), 
	package_nbr VARCHAR(256), 
	crt_dt TIMESTAMP WITHOUT TIME ZONE, 
	updt_dt TIMESTAMP WITHOUT TIME ZONE
)

