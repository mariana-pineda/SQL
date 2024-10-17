
CREATE TABLE Suppliers (
    SupplierID INT NOT NULL GENERATED ALWAYS AS IDENTITY, 
    CompanyName STRING NOT NULL, 
    ContactName STRING NULL, 
    ContactTitle STRING NULL, 
    Address STRING NULL, 
    City STRING NULL, 
    Region STRING NULL, 
    PostalCode STRING NULL, 
    Country STRING NULL, 
    Phone STRING NULL, 
    Fax STRING NULL, 
    HomePage STRING NULL
)
USING DELTA
TBLPROPERTIES ('delta.autoOptimize.optimizeWrite' = 'true', 'delta.autoOptimize.autoCompact' = 'true');

ALTER TABLE Suppliers ADD CONSTRAINT PK_Suppliers PRIMARY KEY (SupplierID);
