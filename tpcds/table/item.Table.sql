
CREATE TABLE tpcds.item (
	i_item_sk INTEGER NOT NULL, 
	i_item_id CHAR(16) NOT NULL, 
	i_rec_start_date DATE, 
	i_rec_end_date DATE, 
	i_item_desc VARCHAR(200), 
	i_current_price NUMERIC(7, 2), 
	i_wholesale_cost NUMERIC(7, 2), 
	i_brand_id INTEGER, 
	i_brand CHAR(50), 
	i_class_id INTEGER, 
	i_class CHAR(50), 
	i_category_id INTEGER, 
	i_category CHAR(50), 
	i_manufact_id INTEGER, 
	i_manufact CHAR(50), 
	i_size CHAR(20), 
	i_formulation CHAR(20), 
	i_color CHAR(20), 
	i_units CHAR(10), 
	i_container CHAR(10), 
	i_manager_id INTEGER, 
	i_product_name CHAR(50), 
	CONSTRAINT item_pkey PRIMARY KEY (i_item_sk)
) DISTSTYLE KEY DISTKEY (i_item_sk) SORTKEY (i_category)

