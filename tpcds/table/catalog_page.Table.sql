
CREATE TABLE tpcds.catalog_page (
	cp_catalog_page_sk INTEGER NOT NULL, 
	cp_catalog_page_id CHAR(16) NOT NULL, 
	cp_start_date_sk INTEGER, 
	cp_end_date_sk INTEGER, 
	cp_department VARCHAR(50), 
	cp_catalog_number INTEGER, 
	cp_catalog_page_number INTEGER, 
	cp_description VARCHAR(100), 
	cp_type VARCHAR(100), 
	CONSTRAINT catalog_page_pkey PRIMARY KEY (cp_catalog_page_sk)
) DISTSTYLE ALL

