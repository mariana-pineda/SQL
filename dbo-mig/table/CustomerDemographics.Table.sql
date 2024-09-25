
CREATE TABLE CustomerDemographics (
  CustomerTypeID STRING NOT NULL, 
  CustomerDesc STRING NULL
)
USING DELTA
OPTIONS (comment = 'Customer demographics information');

ALTER TABLE CustomerDemographics
ADD CONSTRAINT PK_CustomerDemographics PRIMARY KEY (CustomerTypeID);
