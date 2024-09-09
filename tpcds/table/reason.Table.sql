
CREATE TABLE tpcds.reason (
	r_reason_sk INTEGER NOT NULL, 
	r_reason_id CHAR(16) NOT NULL, 
	r_reason_desc CHAR(100), 
	CONSTRAINT reason_pkey PRIMARY KEY (r_reason_sk)
) DISTSTYLE ALL

