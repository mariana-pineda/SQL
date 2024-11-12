
CREATE TABLE purgo_playground.f_inv_movmnt (
	txn_id VARCHAR(256), 
	inv_loc VARCHAR(256), 
	financial_qty DOUBLE PRECISION, 
	net_qty DOUBLE PRECISION, 
	expired_qt NUMERIC(38, 0), 
	item_nbr VARCHAR(256), 
	unit_cost DOUBLE PRECISION, 
	um_rate DOUBLE PRECISION, 
	plant_loc_cd VARCHAR(256), 
	inv_stock_reference VARCHAR(256), 
	stock_type VARCHAR(256), 
	qty_on_hand DOUBLE PRECISION, 
	qty_shipped DOUBLE PRECISION, 
	cancel_dt NUMERIC(38, 0), 
	flag_active VARCHAR(10), 
	crt_dt TIMESTAMP WITHOUT TIME ZONE, 
	updt_dt TIMESTAMP WITHOUT TIME ZONE
)

