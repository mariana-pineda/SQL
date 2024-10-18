
CREATE TABLE Orders (
    OrderID BIGINT NOT NULL GENERATED ALWAYS AS IDENTITY,
    CustomerID STRING NULL,
    EmployeeID BIGINT NULL,
    OrderDate TIMESTAMP NULL,
    RequiredDate TIMESTAMP NULL,
    ShippedDate TIMESTAMP NULL,
    ShipVia BIGINT NULL,
    Freight DECIMAL(19,4) NULL DEFAULT 0,
    ShipName STRING NULL,
    ShipAddress STRING NULL,
    ShipCity STRING NULL,
    ShipRegion STRING NULL,
    ShipPostalCode STRING NULL,
    ShipCountry STRING NULL,
    PRIMARY KEY (OrderID)
);

ALTER TABLE Orders
ADD FOREIGN KEY (CustomerID) REFERENCES Customers (CustomerID);

ALTER TABLE Orders
ADD FOREIGN KEY (EmployeeID) REFERENCES Employees (EmployeeID);

ALTER TABLE Orders
ADD FOREIGN KEY (ShipVia) REFERENCES Shippers (ShipperID);
