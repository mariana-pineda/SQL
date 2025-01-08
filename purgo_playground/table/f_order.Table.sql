
CREATE TABLE purgo_playground.f_order (
	order_nbr VARCHAR(256), 
	order_type BIGINT, 
	delivery_dt NUMERIC(38, 0), 
	order_qty DOUBLE PRECISION, 
	sched_dt NUMERIC(38, 0), 
	expected_shipped_dt NUMERIC(38, 0), 
	actual_shipped_dt NUMERIC(38, 0), 
	order_line_nbr VARCHAR(256), 
	loc_tracker_id VARCHAR(256), 
	shipping_add VARCHAR(1024), 
	primary_qty DOUBLE PRECISION, 
	open_qty DOUBLE PRECISION, 
	shipped_qty DOUBLE PRECISION, 
	order_desc VARCHAR(1024), 
	flag_return VARCHAR(10), 
	flag_cancel VARCHAR(10), 
	cancel_dt NUMERIC(38, 0), 
	cancel_qty DOUBLE PRECISION, 
	crt_dt TIMESTAMP WITHOUT TIME ZONE, 
	updt_dt TIMESTAMP WITHOUT TIME ZONE
)

