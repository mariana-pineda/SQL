
CREATE TABLE purgo_playground.d_product (
	prod_id VARCHAR(256), 
	item_nbr VARCHAR(256), 
	unit_cost DOUBLE PRECISION, 
	prod_exp_dt NUMERIC(38, 0), 
	cost_per_pkg DOUBLE PRECISION, 
	plant_add VARCHAR(256), 
	plant_loc_cd VARCHAR(256), 
	prod_line VARCHAR(256), 
	stock_type VARCHAR(256), 
	pre_prod_days DOUBLE PRECISION, 
	sellable_qty DOUBLE PRECISION, 
	prod_ordr_tracker_nbr VARCHAR(256), 
	max_order_qty VARCHAR(256), 
	flag_active VARCHAR(10), 
	crt_dt TIMESTAMP WITHOUT TIME ZONE, 
	updt_dt TIMESTAMP WITHOUT TIME ZONE
)

