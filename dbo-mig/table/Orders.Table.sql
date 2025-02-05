
CREATE TABLE Orders (
  OrderID INT GENERATED ALWAYS AS IDENTITY,
  CustomerID STRING NULL,
  EmployeeID INT NULL,
  OrderDate TIMESTAMP NULL,
  RequiredDate TIMESTAMP NULL,
  ShippedDate TIMESTAMP NULL,
  ShipVia INT NULL,
  Freight DECIMAL(19,4) NULL DEFAULT 0,
  ShipName STRING NULL,
  ShipAddress STRING NULL,
  ShipCity STRING NULL,
  ShipRegion STRING NULL,
  ShipPostalCode STRING NULL,
  ShipCountry STRING NULL
);

-- Adding PRIMARY KEY constraint
ALTER TABLE Orders ADD CONSTRAINT PK_Orders PRIMARY KEY (OrderID);

-- Adding FOREIGN KEY constraints
ALTER TABLE Orders ADD CONSTRAINT FK_Orders_Customers FOREIGN KEY (CustomerID) REFERENCES Customers (CustomerID);
ALTER TABLE Orders ADD CONSTRAINT FK_Orders_Employees FOREIGN KEY (EmployeeID) REFERENCES Employees (EmployeeID);
ALTER TABLE Orders ADD CONSTRAINT FK_Orders_Shippers FOREIGN KEY (ShipVia) REFERENCES Shippers (ShipperID);
