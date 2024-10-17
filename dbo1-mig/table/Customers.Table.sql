
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
  Fax STRING
);

ALTER TABLE Customers
ADD CONSTRAINT PK_Customers PRIMARY KEY (CustomerID);
