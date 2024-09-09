
CREATE TABLE tpcds.item (
  i_item_sk INT NOT NULL, 
  i_item_id STRING NOT NULL, 
  i_rec_start_date DATE, 
  i_rec_end_date DATE, 
  i_item_desc STRING, 
  i_current_price DECIMAL(7, 2), 
  i_wholesale_cost DECIMAL(7, 2), 
  i_brand_id INT, 
  i_brand STRING, 
  i_class_id INT, 
  i_class STRING, 
  i_category_id INT, 
  i_category STRING, 
  i_manufact_id INT, 
  i_manufact STRING, 
  i_size STRING, 
  i_formulation STRING, 
  i_color STRING, 
  i_units STRING, 
  i_container STRING, 
  i_manager_id INT, 
  i_product_name STRING, 
  PRIMARY KEY (i_item_sk)
) USING DELTA

