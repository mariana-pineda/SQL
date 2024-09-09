
CREATE TABLE tpcds.store_sales (
	ss_sold_date_sk INTEGER, 
	ss_sold_time_sk INTEGER, 
	ss_item_sk INTEGER NOT NULL, 
	ss_customer_sk INTEGER, 
	ss_cdemo_sk INTEGER, 
	ss_hdemo_sk INTEGER, 
	ss_addr_sk INTEGER, 
	ss_store_sk INTEGER, 
	ss_promo_sk INTEGER, 
	ss_ticket_number BIGINT NOT NULL, 
	ss_quantity INTEGER, 
	ss_wholesale_cost NUMERIC(7, 2), 
	ss_list_price NUMERIC(7, 2), 
	ss_sales_price NUMERIC(7, 2), 
	ss_ext_discount_amt NUMERIC(7, 2), 
	ss_ext_sales_price NUMERIC(7, 2), 
	ss_ext_wholesale_cost NUMERIC(7, 2), 
	ss_ext_list_price NUMERIC(7, 2), 
	ss_ext_tax NUMERIC(7, 2), 
	ss_coupon_amt NUMERIC(7, 2), 
	ss_net_paid NUMERIC(7, 2), 
	ss_net_paid_inc_tax NUMERIC(7, 2), 
	ss_net_profit NUMERIC(7, 2), 
	CONSTRAINT store_sales_pkey PRIMARY KEY (ss_item_sk, ss_ticket_number)
) DISTSTYLE KEY DISTKEY (ss_item_sk) SORTKEY (ss_sold_date_sk)

