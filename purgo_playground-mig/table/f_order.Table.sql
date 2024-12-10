
CREATE TABLE purgo_playground.f_order (
    order_nbr STRING, 
    order_type BIGINT, 
    delivery_dt DECIMAL(38, 0), 
    order_qty DOUBLE, 
    sched_dt DECIMAL(38, 0), 
    expected_shipped_dt DECIMAL(38, 0), 
    actual_shipped_dt DECIMAL(38, 0), 
    order_line_nbr STRING, 
    loc_tracker_id STRING, 
    shipping_add STRING, 
    primary_qty DOUBLE, 
    open_qty DOUBLE, 
    shipped_qty DOUBLE, 
    order_desc STRING, 
    flag_return STRING, 
    flag_cancel STRING, 
    cancel_dt DECIMAL(38, 0), 
    cancel_qty DOUBLE, 
    crt_dt TIMESTAMP, 
    updt_dt TIMESTAMP
)

