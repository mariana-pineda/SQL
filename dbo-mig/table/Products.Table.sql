
CREATE TABLE Products (
    ProductID INT NOT NULL GENERATED ALWAYS AS IDENTITY,
    ProductName STRING NOT NULL,
    SupplierID INT,
    CateryID INT,
    QuantityPerUnit STRING,
    UnitPrice DECIMAL(19,4) NULL DEFAULT 0,
    UnitsInStock SMALLINT NULL DEFAULT 0,
    UnitsOnOrder SMALLINT NULL DEFAULT 0,
    ReorderLevel SMALLINT NULL DEFAULT 0,
    Discontinued BOOLEAN NOT NULL DEFAULT FALSE,
    PRIMARY KEY (ProductID),
    FOREIGN KEY (CateryID) REFERENCES Cateries (CateryID),
    FOREIGN KEY (SupplierID) REFERENCES Suppliers (SupplierID)
);
