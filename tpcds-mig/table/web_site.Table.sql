
CREATE TABLE tpcds.web_site (
  web_site_sk INT NOT NULL, 
  web_site_id CHAR(16) NOT NULL, 
  web_rec_start_date DATE, 
  web_rec_end_date DATE, 
  web_name STRING, 
  web_open_date_sk INT, 
  web_close_date_sk INT, 
  web_class STRING, 
  web_manager STRING, 
  web_mkt_id INT, 
  web_mkt_class STRING, 
  web_mkt_desc STRING, 
  web_market_manager STRING, 
  web_company_id INT, 
  web_company_name STRING, 
  web_street_number STRING, 
  web_street_name STRING, 
  web_street_type STRING, 
  web_suite_number STRING, 
  web_city STRING, 
  web_county STRING, 
  web_state STRING, 
  web_zip STRING, 
  web_country STRING, 
  web_gmt_offset DECIMAL(5, 2), 
  web_tax_percentage DECIMAL(5, 2), 
  PRIMARY KEY (web_site_sk)
) USING DELTA
