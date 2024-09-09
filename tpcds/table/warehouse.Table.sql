
CREATE TABLE tpcds.warehouse (
	w_warehouse_sk INTEGER NOT NULL, 
	w_warehouse_id CHAR(16) NOT NULL, 
	w_warehouse_name VARCHAR(20), 
	w_warehouse_sq_ft INTEGER, 
	w_street_number CHAR(10), 
	w_street_name VARCHAR(60), 
	w_street_type CHAR(15), 
	w_suite_number CHAR(10), 
	w_city VARCHAR(60), 
	w_county VARCHAR(30), 
	w_state CHAR(2), 
	w_zip CHAR(10), 
	w_country VARCHAR(20), 
	w_gmt_offset NUMERIC(5, 2), 
	CONSTRAINT warehouse_pkey PRIMARY KEY (w_warehouse_sk)
) DISTSTYLE ALL

