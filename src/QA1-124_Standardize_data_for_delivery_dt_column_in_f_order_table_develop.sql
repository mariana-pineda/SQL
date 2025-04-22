/* 
Standardize data for delivery_dt column in f_order table.
Ensures delivery_dt is Decimal(38,0) and follows yyyymmdd format.
*/

/* 
Add comment on delivery_dt column to document valid values.
*/
ALTER TABLE purgo_databricks.purgo_playground.f_order 
ALTER COLUMN delivery_dt COMMENT "Decimal(38,0). Valid format: yyyymmdd";

/* 
Validation Query: Identify records with invalid delivery_dt.
*/
WITH invalid_delivery_dt AS (
    SELECT 
        delivery_dt
    FROM 
        purgo_databricks.purgo_playground.f_order
    WHERE 
        delivery_dt IS NULL
        OR delivery_dt < 10000101
        OR delivery_dt > 99991231
        OR to_date(CAST(delivery_dt AS STRING), "yyyyMMdd") IS NULL
)
SELECT * FROM invalid_delivery_dt;
