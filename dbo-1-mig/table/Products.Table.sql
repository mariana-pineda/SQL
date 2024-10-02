
CREATE TABLE Products (
    ProductID INTEGER NOT NULL GENERATED ALWAYS AS IDENTITY,
    ProductName STRING NOT NULL,
    SupplierID INTEGER,
    CateryID INTEGER,
    QuantityPerUnit STRING,
    UnitPrice DECIMAL(19,4) DEFAULT 0,
    UnitsInStock SMALLINT DEFAULT 0,
    UnitsOnOrder SMALLINT DEFAULT 0,
    ReorderLevel SMALLINT DEFAULT 0,
    Discontinued BOOLEAN NOT NULL DEFAULT false,
    PRIMARY KEY (ProductID),
    FOREIGN KEY (CateryID) REFERENCES Cateries (CateryID),
    FOREIGN KEY (SupplierID) REFERENCES Suppliers (SupplierID)
)
