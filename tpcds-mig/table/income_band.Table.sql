
CREATE TABLE tpcds.income_band (
	ib_income_band_sk INT NOT NULL, 
	ib_lower_bound INT, 
	ib_upper_bound INT,
	PRIMARY KEY (ib_income_band_sk)
) USING DELTA
DISTRIBUTE BY (ib_income_band_sk)
