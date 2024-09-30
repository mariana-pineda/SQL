
CREATE TABLE Orders (
  OrderID INTEGER NOT NULL,
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
  ShipCountry STRING(15),
  PRIMARY KEY (OrderID)
);

ALTER TABLE Orders ADD CONSTRAINT FK_Orders_Customers FOREIGN KEY (CustomerID) REFERENCES Customers (CustomerID);
ALTER TABLE Orders ADD CONSTRAINT FK_Orders_Employees FOREIGN KEY (EmployeeID) REFERENCES Employees (EmployeeID);
ALTER TABLE Orders ADD CONSTRAINT FK_Orders_Shippers FOREIGN KEY (ShipVia) REFERENCES Shippers (ShipperID);
