
CREATE TABLE Orders (
  OrderID INTEGER NOT NULL,
  CustomerID STRING,
  EmployeeID INTEGER,
  OrderDate TIMESTAMP,
  RequiredDate TIMESTAMP,
  ShippedDate TIMESTAMP,
  ShipVia INTEGER,
  Freight DECIMAL(19,4) DEFAULT 0,
  ShipName STRING,
  ShipAddress STRING,
  ShipCity STRING,
  ShipRegion STRING,
  ShipPostalCode STRING,
  ShipCountry STRING
);

ALTER TABLE Orders ADD CONSTRAINT PK_Orders PRIMARY KEY (OrderID);

ALTER TABLE Orders ADD CONSTRAINT FK_Orders_Customers FOREIGN KEY (CustomerID) REFERENCES Customers (CustomerID);

ALTER TABLE Orders ADD CONSTRAINT FK_Orders_Employees FOREIGN KEY (EmployeeID) REFERENCES Employees (EmployeeID);

ALTER TABLE Orders ADD CONSTRAINT FK_Orders_Shippers FOREIGN KEY (ShipVia) REFERENCES Shippers (ShipperID);

