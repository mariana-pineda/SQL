
CREATE TABLE tpcds.ship_mode (
	sm_ship_mode_sk INT NOT NULL, 
	sm_ship_mode_id CHAR(16) NOT NULL, 
	sm_type STRING, 
	sm_code STRING, 
	sm_carrier STRING, 
	sm_contract STRING, 
	PRIMARY KEY (sm_ship_mode_sk)
) USING DELTA
