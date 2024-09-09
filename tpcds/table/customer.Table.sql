
CREATE TABLE tpcds.customer (
	c_customer_sk INTEGER NOT NULL, 
	c_customer_id CHAR(16) NOT NULL, 
	c_current_cdemo_sk INTEGER, 
	c_current_hdemo_sk INTEGER, 
	c_current_addr_sk INTEGER, 
	c_first_shipto_date_sk INTEGER, 
	c_first_sales_date_sk INTEGER, 
	c_salutation CHAR(10), 
	c_first_name CHAR(20), 
	c_last_name CHAR(30), 
	c_preferred_cust_flag CHAR(1), 
	c_birth_day INTEGER, 
	c_birth_month INTEGER, 
	c_birth_year INTEGER, 
	c_birth_country VARCHAR(20), 
	c_login CHAR(13), 
	c_email_address CHAR(50), 
	c_last_review_date_sk INTEGER, 
	CONSTRAINT customer_pkey PRIMARY KEY (c_customer_sk)
) DISTSTYLE KEY DISTKEY (c_customer_sk)

