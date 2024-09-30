
CREATE TABLE CustomerDemographics (
  CustomerTypeID STRING NOT NULL, 
  CustomerDesc STRING NULL
)
USING DELTA
TBLPROPERTIES (
  'delta.columnMapping.mode' = 'name'
);

ALTER TABLE CustomerDemographics
ADD CONSTRAINT PK_CustomerDemographics PRIMARY KEY (CustomerTypeID);
