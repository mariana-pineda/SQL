
CREATE TABLE tpcds.inventory (
	inv_date_sk INTEGER NOT NULL, 
	inv_item_sk INTEGER NOT NULL, 
	inv_warehouse_sk INTEGER NOT NULL, 
	inv_quantity_on_hand INTEGER, 
	PRIMARY KEY (inv_date_sk, inv_item_sk, inv_warehouse_sk)
) USING DELTA
