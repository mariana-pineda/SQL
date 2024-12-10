
CREATE TABLE CustomerDemographics (
  CustomerTypeID STRING NOT NULL,
  CustomerDesc STRING NULL
)
USING DELTA
TBLPROPERTIES ('delta.column.mapping.mode' = 'name')
LOCATION '/mnt/delta/CustomerDemographics';

ALTER TABLE CustomerDemographics
ADD CONSTRAINT PK_CustomerDemographics PRIMARY KEY (CustomerTypeID);
