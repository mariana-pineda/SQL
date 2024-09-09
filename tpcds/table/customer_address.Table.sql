
CREATE TABLE tpcds.customer_address (
	ca_address_sk INTEGER NOT NULL, 
	ca_address_id CHAR(16) NOT NULL, 
	ca_street_number CHAR(10), 
	ca_street_name VARCHAR(60), 
	ca_street_type CHAR(15), 
	ca_suite_number CHAR(10), 
	ca_city VARCHAR(60), 
	ca_county VARCHAR(30), 
	ca_state CHAR(2), 
	ca_zip CHAR(10), 
	ca_country VARCHAR(20), 
	ca_gmt_offset NUMERIC(5, 2), 
	ca_location_type CHAR(20), 
	CONSTRAINT customer_address_pkey PRIMARY KEY (ca_address_sk)
) DISTSTYLE KEY DISTKEY (ca_address_sk)

