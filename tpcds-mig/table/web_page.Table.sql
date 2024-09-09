
CREATE TABLE tpcds.web_page (
	wp_web_page_sk INT NOT NULL, 
	wp_web_page_id STRING NOT NULL, 
	wp_rec_start_date DATE, 
	wp_rec_end_date DATE, 
	wp_creation_date_sk INT, 
	wp_access_date_sk INT, 
	wp_autogen_flag STRING, 
	wp_customer_sk INT, 
	wp_url STRING, 
	wp_type STRING, 
	wp_char_count INT, 
	wp_link_count INT, 
	wp_image_count INT, 
	wp_max_ad_count INT,
	PRIMARY KEY (wp_web_page_sk)
) USING DELTA;
