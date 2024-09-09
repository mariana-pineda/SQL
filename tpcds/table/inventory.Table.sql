
CREATE TABLE tpcds.inventory (
	inv_date_sk INTEGER NOT NULL, 
	inv_item_sk INTEGER NOT NULL, 
	inv_warehouse_sk INTEGER NOT NULL, 
	inv_quantity_on_hand INTEGER, 
	CONSTRAINT inventory_pkey PRIMARY KEY (inv_date_sk, inv_item_sk, inv_warehouse_sk)
) DISTSTYLE KEY DISTKEY (inv_item_sk) SORTKEY (inv_date_sk)

