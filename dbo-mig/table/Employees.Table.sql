
CREATE TABLE Employees (
    EmployeeID INT NOT NULL,
    LastName STRING NOT NULL,
    FirstName STRING NOT NULL,
    Title STRING NULL,
    TitleOfCourtesy STRING NULL,
    BirthDate TIMESTAMP NULL,
    HireDate TIMESTAMP NULL,
    Address STRING NULL,
    City STRING NULL,
    Region STRING NULL,
    PostalCode STRING NULL,
    Country STRING NULL,
    HomePhone STRING NULL,
    Extension STRING NULL,
    Photo BINARY NULL,
    Notes STRING NULL,
    ReportsTo INT NULL,
    PhotoPath STRING NULL
);

ALTER TABLE Employees ADD CONSTRAINT PK_Employees PRIMARY KEY (EmployeeID);
ALTER TABLE Employees ADD CONSTRAINT FK_Employees_Employees FOREIGN KEY (ReportsTo) REFERENCES Employees (EmployeeID);
