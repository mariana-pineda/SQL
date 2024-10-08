
CREATE TABLE CustomerDemographics (
  CustomerTypeID STRING NOT NULL,
  CustomerDesc STRING NULL
)
USING DELTA
PARTITIONED BY (CustomerTypeID);
