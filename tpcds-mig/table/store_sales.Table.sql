
CREATE TABLE tpcds.store_sales (
	ss_sold_date_sk INT, 
	ss_sold_time_sk INT, 
	ss_item_sk INT NOT NULL, 
	ss_customer_sk INT, 
	ss_cdemo_sk INT, 
	ss_hdemo_sk INT, 
	ss_addr_sk INT, 
	ss_store_sk INT, 
	ss_promo_sk INT, 
	ss_ticket_number BIGINT NOT NULL, 
	ss_quantity INT, 
	ss_wholesale_cost DECIMAL(7, 2), 
	ss_list_price DECIMAL(7, 2), 
	ss_sales_price DECIMAL(7, 2), 
	ss_ext_discount_amt DECIMAL(7, 2), 
	ss_ext_sales_price DECIMAL(7, 2), 
	ss_ext_wholesale_cost DECIMAL(7, 2), 
	ss_ext_list_price DECIMAL(7, 2), 
	ss_ext_tax DECIMAL(7, 2), 
	ss_coupon_amt DECIMAL(7, 2), 
	ss_net_paid DECIMAL(7, 2), 
	ss_net_paid_inc_tax DECIMAL(7, 2), 
	ss_net_profit DECIMAL(7, 2),
	PRIMARY KEY (ss_item_sk, ss_ticket_number)
);

CREATE INDEX idx_store_sales_sold_date ON tpcds.store_sales (ss_sold_date_sk);
