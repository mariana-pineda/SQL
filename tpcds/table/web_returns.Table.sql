
CREATE TABLE tpcds.web_returns (
	wr_returned_date_sk INTEGER, 
	wr_returned_time_sk INTEGER, 
	wr_item_sk INTEGER NOT NULL, 
	wr_refunded_customer_sk INTEGER, 
	wr_refunded_cdemo_sk INTEGER, 
	wr_refunded_hdemo_sk INTEGER, 
	wr_refunded_addr_sk INTEGER, 
	wr_returning_customer_sk INTEGER, 
	wr_returning_cdemo_sk INTEGER, 
	wr_returning_hdemo_sk INTEGER, 
	wr_returning_addr_sk INTEGER, 
	wr_web_page_sk INTEGER, 
	wr_reason_sk INTEGER, 
	wr_order_number BIGINT NOT NULL, 
	wr_return_quantity INTEGER, 
	wr_return_amt NUMERIC(7, 2), 
	wr_return_tax NUMERIC(7, 2), 
	wr_return_amt_inc_tax NUMERIC(7, 2), 
	wr_fee NUMERIC(7, 2), 
	wr_return_ship_cost NUMERIC(7, 2), 
	wr_refunded_cash NUMERIC(7, 2), 
	wr_reversed_charge NUMERIC(7, 2), 
	wr_account_credit NUMERIC(7, 2), 
	wr_net_loss NUMERIC(7, 2), 
	CONSTRAINT web_returns_pkey PRIMARY KEY (wr_item_sk, wr_order_number)
) DISTSTYLE KEY DISTKEY (wr_order_number) SORTKEY (wr_returned_date_sk)

