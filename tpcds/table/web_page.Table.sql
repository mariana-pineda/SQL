
CREATE TABLE tpcds.web_page (
	wp_web_page_sk INTEGER NOT NULL, 
	wp_web_page_id CHAR(16) NOT NULL, 
	wp_rec_start_date DATE, 
	wp_rec_end_date DATE, 
	wp_creation_date_sk INTEGER, 
	wp_access_date_sk INTEGER, 
	wp_autogen_flag CHAR(1), 
	wp_customer_sk INTEGER, 
	wp_url VARCHAR(100), 
	wp_type CHAR(50), 
	wp_char_count INTEGER, 
	wp_link_count INTEGER, 
	wp_image_count INTEGER, 
	wp_max_ad_count INTEGER, 
	CONSTRAINT web_page_pkey PRIMARY KEY (wp_web_page_sk)
) DISTSTYLE ALL

