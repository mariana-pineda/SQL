
CREATE TABLE tpcds.promotion (
	p_promo_sk INTEGER NOT NULL, 
	p_promo_id CHAR(16) NOT NULL, 
	p_start_date_sk INTEGER, 
	p_end_date_sk INTEGER, 
	p_item_sk INTEGER, 
	p_cost NUMERIC(15, 2), 
	p_response_target INTEGER, 
	p_promo_name CHAR(50), 
	p_channel_dmail CHAR(1), 
	p_channel_email CHAR(1), 
	p_channel_catalog CHAR(1), 
	p_channel_tv CHAR(1), 
	p_channel_radio CHAR(1), 
	p_channel_press CHAR(1), 
	p_channel_event CHAR(1), 
	p_channel_demo CHAR(1), 
	p_channel_details VARCHAR(100), 
	p_purpose CHAR(15), 
	p_discount_active CHAR(1), 
	CONSTRAINT promotion_pkey PRIMARY KEY (p_promo_sk)
) DISTSTYLE ALL

