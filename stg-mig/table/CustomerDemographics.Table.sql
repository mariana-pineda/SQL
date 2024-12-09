
CREATE TABLE CustomerDemographics (
  CustomerTypeID STRING NOT NULL,
  CustomerDesc STRING NULL
);

-- Since Databricks does not support NTEXT, it is replaced with STRING
-- Also, collation settings are not applied in Databricks
