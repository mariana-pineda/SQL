
CREATE TABLE Customers (
  CustomerID CHAR(5) NOT NULL, 
  CompanyName STRING NOT NULL, 
  ContactName STRING, 
  ContactTitle STRING, 
  Address STRING, 
  City STRING, 
  Region STRING, 
  PostalCode STRING, 
  Country STRING, 
  Phone STRING, 
  Fax STRING
)
USING DELTA
OPTIONS (primaryKey = 'CustomerID')
