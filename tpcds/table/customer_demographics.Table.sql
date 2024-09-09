
CREATE TABLE tpcds.customer_demographics (
	cd_demo_sk INTEGER NOT NULL, 
	cd_gender CHAR(1), 
	cd_marital_status CHAR(1), 
	cd_education_status CHAR(20), 
	cd_purchase_estimate INTEGER, 
	cd_credit_rating CHAR(10), 
	cd_dep_count INTEGER, 
	cd_dep_employed_count INTEGER, 
	cd_dep_college_count INTEGER, 
	CONSTRAINT customer_demographics_pkey PRIMARY KEY (cd_demo_sk)
) DISTSTYLE KEY DISTKEY (cd_demo_sk)

