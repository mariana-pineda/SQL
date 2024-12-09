
CREATE TABLE Customers (
  CustomerID STRING NOT NULL,
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
  PRIMARY KEY (CustomerID)
)
USING DELTA;
