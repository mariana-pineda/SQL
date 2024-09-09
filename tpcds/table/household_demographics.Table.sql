
CREATE TABLE tpcds.household_demographics (
	hd_demo_sk INTEGER NOT NULL, 
	hd_income_band_sk INTEGER, 
	hd_buy_potential CHAR(15), 
	hd_dep_count INTEGER, 
	hd_vehicle_count INTEGER, 
	CONSTRAINT household_demographics_pkey PRIMARY KEY (hd_demo_sk)
) DISTSTYLE ALL

