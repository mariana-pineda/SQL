
CREATE TABLE Orders (
  OrderID INT GENERATED ALWAYS AS IDENTITY,
  CustomerID CHAR(5),
  EmployeeID INT,
  OrderDate TIMESTAMP,
  RequiredDate TIMESTAMP,
  ShippedDate TIMESTAMP,
  ShipVia INT,
  Freight DECIMAL(19,4) DEFAULT 0,
  ShipName STRING,
  ShipAddress STRING,
  ShipCity STRING,
  ShipRegion STRING,
  ShipPostalCode STRING,
  ShipCountry STRING
);

ALTER TABLE Orders ADD CONSTRAINT PK_Orders PRIMARY KEY (OrderID);

ALTER TABLE Orders ADD CONSTRAINT FK_Orders_Customers 
FOREIGN KEY (CustomerID) REFERENCES Customers (CustomerID);

ALTER TABLE Orders ADD CONSTRAINT FK_Orders_Employees 
FOREIGN KEY (EmployeeID) REFERENCES Employees (EmployeeID);

ALTER TABLE Orders ADD CONSTRAINT FK_Orders_Shippers 
FOREIGN KEY (ShipVia) REFERENCES Shippers (ShipperID);
