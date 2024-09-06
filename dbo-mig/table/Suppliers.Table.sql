
CREATE TABLE Suppliers (
    SupplierID INTEGER NOT NULL GENERATED ALWAYS AS IDENTITY (START WITH 1 INCREMENT BY 1), 
    CompanyName STRING(40) NOT NULL, 
    ContactName STRING(30) NULL, 
    ContactTitle STRING(30) NULL, 
    Address STRING(60) NULL, 
    City STRING(15) NULL, 
    Region STRING(15) NULL, 
    PostalCode STRING(10) NULL, 
    Country STRING(15) NULL, 
    Phone STRING(24) NULL, 
    Fax STRING(24) NULL, 
    HomePage STRING NULL, 
    CONSTRAINT PK_Suppliers PRIMARY KEY (SupplierID)
);
