
CREATE TABLE Region (
  RegionID INT NOT NULL,
  RegionDescription STRING NOT NULL
)
USING delta
TBLPROPERTIES ('delta.columnMapping.mode' = 'name', 'delta.preserve.history' = 'true');

ALTER TABLE Region ADD CONSTRAINT pk_region PRIMARY KEY (RegionID);
