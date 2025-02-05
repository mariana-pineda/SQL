
CREATE TABLE CustomerDemographics (
  CustomerTypeID STRING NOT NULL,
  CustomerDesc STRING NULL
)
USING DELTA
COMMENT 'Table with customer demographics'
TBLPROPERTIES ('primary_key_columns' = 'CustomerTypeID');
