
CREATE TABLE Shippers (
  ShipperID INT NOT NULL,
  CompanyName STRING NOT NULL,
  Phone STRING,
  PRIMARY KEY (ShipperID)
)
COMMENT 'Shippers: Table for storing shipper information'
USING DELTA
TBLPROPERTIES ('spark.databricks.delta.schema.autoMerge.enabled' = 'true');
