
CREATE TABLE Suppliers (
  SupplierID INT NOT NULL GENERATED ALWAYS AS IDENTITY,
  CompanyName STRING NOT NULL,
  ContactName STRING,
  ContactTitle STRING,
  Address STRING,
  City STRING,
  Region STRING,
  PostalCode STRING,
  Country STRING,
  Phone STRING,
  Fax STRING,
  HomePage STRING,
  PRIMARY KEY (SupplierID)
)
