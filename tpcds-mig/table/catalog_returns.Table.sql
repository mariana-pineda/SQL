
CREATE TABLE tpcds.catalog_returns (
    cr_returned_date_sk INTEGER,
    cr_returned_time_sk INTEGER,
    cr_item_sk INTEGER NOT NULL,
    cr_refunded_customer_sk INTEGER,
    cr_refunded_cdemo_sk INTEGER,
    cr_refunded_hdemo_sk INTEGER,
    cr_refunded_addr_sk INTEGER,
    cr_returning_customer_sk INTEGER,
    cr_returning_cdemo_sk INTEGER,
    cr_returning_hdemo_sk INTEGER,
    cr_returning_addr_sk INTEGER,
    cr_call_center_sk INTEGER,
    cr_catalog_page_sk INTEGER,
    cr_ship_mode_sk INTEGER,
    cr_warehouse_sk INTEGER,
    cr_reason_sk INTEGER,
    cr_order_number BIGINT NOT NULL,
    cr_return_quantity INTEGER,
    cr_return_amount DECIMAL(7, 2),
    cr_return_tax DECIMAL(7, 2),
    cr_return_amt_inc_tax DECIMAL(7, 2),
    cr_fee DECIMAL(7, 2),
    cr_return_ship_cost DECIMAL(7, 2),
    cr_refunded_cash DECIMAL(7, 2),
    cr_reversed_charge DECIMAL(7, 2),
    cr_store_credit DECIMAL(7, 2),
    cr_net_loss DECIMAL(7, 2),
    PRIMARY KEY (cr_item_sk, cr_order_number)
) USING DELTA
OPTIONS (
    partitioned_by = ARRAY('cr_returned_date_sk')
);
