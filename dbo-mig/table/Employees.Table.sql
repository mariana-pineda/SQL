
CREATE TABLE Employees (
    EmployeeID INTEGER NOT NULL GENERATED ALWAYS AS IDENTITY, 
    LastName STRING NOT NULL, 
    FirstName STRING NOT NULL, 
    Title STRING, 
    TitleOfCourtesy STRING, 
    BirthDate TIMESTAMP, 
    HireDate TIMESTAMP, 
    Address STRING, 
    City STRING, 
    Region STRING, 
    PostalCode STRING, 
    Country STRING, 
    HomePhone STRING, 
    Extension STRING, 
    Photo BINARY, 
    Notes STRING, 
    ReportsTo INTEGER, 
    PhotoPath STRING,
    PRIMARY KEY (EmployeeID),
    FOREIGN KEY (ReportsTo) REFERENCES Employees (EmployeeID)
)
