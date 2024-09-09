
CREATE TABLE tpcds.time_dim (
	t_time_sk INTEGER NOT NULL, 
	t_time_id CHAR(16) NOT NULL, 
	t_time INTEGER, 
	t_hour INTEGER, 
	t_minute INTEGER, 
	t_second INTEGER, 
	t_am_pm CHAR(2), 
	t_shift CHAR(20), 
	t_sub_shift CHAR(20), 
	t_meal_time CHAR(20), 
	CONSTRAINT time_dim_pkey PRIMARY KEY (t_time_sk)
) DISTSTYLE ALL

