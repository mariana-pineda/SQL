
CREATE TABLE Products (
    ProductID INT NOT NULL, 
    ProductName STRING NOT NULL, 
    SupplierID INT, 
    CateryID INT, 
    QuantityPerUnit STRING, 
    UnitPrice DECIMAL(19, 4) DEFAULT 0, 
    UnitsInStock SMALLINT DEFAULT 0, 
    UnitsOnOrder SMALLINT DEFAULT 0, 
    ReorderLevel SMALLINT DEFAULT 0, 
    Discontinued BOOLEAN NOT NULL DEFAULT FALSE, 
    PRIMARY KEY (ProductID)
);

ALTER TABLE Products 
    ADD CONSTRAINT FK_Products_Cateries FOREIGN KEY (CateryID) REFERENCES Cateries (CateryID);

ALTER TABLE Products 
    ADD CONSTRAINT FK_Products_Suppliers FOREIGN KEY (SupplierID) REFERENCES Suppliers (SupplierID);
