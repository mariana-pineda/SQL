
CREATE TABLE tpcds.reason (
    r_reason_sk INT NOT NULL, 
    r_reason_id STRING NOT NULL, 
    r_reason_desc STRING, 
    PRIMARY KEY (r_reason_sk)
) USING DELTA
