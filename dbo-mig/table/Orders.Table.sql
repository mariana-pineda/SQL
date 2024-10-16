
CREATE TABLE Orders (
  OrderID INTEGER NOT NULL GENERATED ALWAYS AS IDENTITY,
  CustomerID STRING(5),
  EmployeeID INTEGER,
  OrderDate TIMESTAMP,
  RequiredDate TIMESTAMP,
  ShippedDate TIMESTAMP,
  ShipVia INTEGER,
  Freight DECIMAL(19, 4) DEFAULT 0,
  ShipName STRING(40),
  ShipAddress STRING(60),
  ShipCity STRING(15),
  ShipRegion STRING(15),
  ShipPostalCode STRING(10),
  ShipCountry STRING(15)
);

ALTER TABLE Orders ADD CONSTRAINT PK_Orders PRIMARY KEY (OrderID);

ALTER TABLE Orders ADD FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID);

ALTER TABLE Orders ADD FOREIGN KEY (EmployeeID) REFERENCES Employees(EmployeeID);

ALTER TABLE Orders ADD FOREIGN KEY (ShipVia) REFERENCES Shippers(ShipperID);
