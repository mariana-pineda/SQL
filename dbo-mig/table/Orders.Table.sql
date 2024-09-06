
CREATE TABLE Orders (
  OrderID INTEGER NOT NULL GENERATED ALWAYS AS IDENTITY,
  CustomerID STRING COMMENT 'Matches original NCHAR(5)',
  EmployeeID INTEGER,
  OrderDate TIMESTAMP,
  RequiredDate TIMESTAMP,
  ShippedDate TIMESTAMP,
  ShipVia INTEGER,
  Freight DECIMAL(19,4) DEFAULT 0.0,
  ShipName STRING,
  ShipAddress STRING,
  ShipCity STRING,
  ShipRegion STRING,
  ShipPostalCode STRING,
  ShipCountry STRING,
  PRIMARY KEY (OrderID),
  FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID),
  FOREIGN KEY (EmployeeID) REFERENCES Employees(EmployeeID),
  FOREIGN KEY (ShipVia) REFERENCES Shippers(ShipperID)
)
