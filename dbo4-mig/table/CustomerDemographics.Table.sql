
CREATE TABLE CustomerDemographics (
  CustomerTypeID STRING NOT NULL,
  CustomerDesc STRING NULL
);

ALTER TABLE CustomerDemographics 
ADD CONSTRAINT PK_CustomerDemographics PRIMARY KEY (CustomerTypeID);
