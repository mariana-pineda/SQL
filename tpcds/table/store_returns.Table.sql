
CREATE TABLE tpcds.store_returns (
	sr_returned_date_sk INTEGER, 
	sr_return_time_sk INTEGER, 
	sr_item_sk INTEGER NOT NULL, 
	sr_customer_sk INTEGER, 
	sr_cdemo_sk INTEGER, 
	sr_hdemo_sk INTEGER, 
	sr_addr_sk INTEGER, 
	sr_store_sk INTEGER, 
	sr_reason_sk INTEGER, 
	sr_ticket_number BIGINT NOT NULL, 
	sr_return_quantity INTEGER, 
	sr_return_amt NUMERIC(7, 2), 
	sr_return_tax NUMERIC(7, 2), 
	sr_return_amt_inc_tax NUMERIC(7, 2), 
	sr_fee NUMERIC(7, 2), 
	sr_return_ship_cost NUMERIC(7, 2), 
	sr_refunded_cash NUMERIC(7, 2), 
	sr_reversed_charge NUMERIC(7, 2), 
	sr_store_credit NUMERIC(7, 2), 
	sr_net_loss NUMERIC(7, 2), 
	CONSTRAINT store_returns_pkey PRIMARY KEY (sr_item_sk, sr_ticket_number)
) DISTSTYLE KEY DISTKEY (sr_item_sk) SORTKEY (sr_returned_date_sk)

