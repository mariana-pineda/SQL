
CREATE TABLE purgo_playground.f_inv_movmnt (
    txn_id STRING, 
    inv_loc STRING, 
    financial_qty DOUBLE, 
    net_qty DOUBLE, 
    expired_qt DECIMAL(38, 0), 
    item_nbr STRING, 
    unit_cost DOUBLE, 
    um_rate DOUBLE, 
    plant_loc_cd STRING, 
    inv_stock_reference STRING, 
    stock_type STRING, 
    qty_on_hand DOUBLE, 
    qty_shipped DOUBLE, 
    cancel_dt DECIMAL(38, 0), 
    flag_active STRING, 
    crt_dt TIMESTAMP, 
    updt_dt TIMESTAMP
)

