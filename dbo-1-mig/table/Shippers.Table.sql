
CREATE TABLE Shippers (
  ShipperID INTEGER NOT NULL GENERATED ALWAYS AS IDENTITY,
  CompanyName STRING NOT NULL,
  Phone STRING
);
