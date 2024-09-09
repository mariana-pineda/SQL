CREATE TABLE tpcds.catalog_page (
	cp_catalog_page_sk INT NOT NULL, 
	cp_catalog_page_id STRING NOT NULL, 
	cp_start_date_sk INT, 
	cp_end_date_sk INT, 
	cp_department STRING, 
	cp_catalog_number INT, 
	cp_catalog_page_number INT, 
	cp_description STRING, 
	cp_type STRING
)
USING DELTA;

ALTER TABLE tpcds.catalog_page ADD CONSTRAINT catalog_page_pkey PRIMARY KEY (cp_catalog_page_sk);