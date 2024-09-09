
CREATE TABLE tpcds.income_band (
	ib_income_band_sk INTEGER NOT NULL, 
	ib_lower_bound INTEGER, 
	ib_upper_bound INTEGER, 
	CONSTRAINT income_band_pkey PRIMARY KEY (ib_income_band_sk)
) DISTSTYLE ALL

