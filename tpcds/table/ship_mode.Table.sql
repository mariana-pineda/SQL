
CREATE TABLE tpcds.ship_mode (
	sm_ship_mode_sk INTEGER NOT NULL, 
	sm_ship_mode_id CHAR(16) NOT NULL, 
	sm_type CHAR(30), 
	sm_code CHAR(10), 
	sm_carrier CHAR(20), 
	sm_contract CHAR(20), 
	CONSTRAINT ship_mode_pkey PRIMARY KEY (sm_ship_mode_sk)
) DISTSTYLE ALL

