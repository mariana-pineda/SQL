
CREATE TABLE Employees (
  EmployeeID INT NOT NULL,
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
  ReportsTo INT, 
  PhotoPath STRING
);

ALTER TABLE Employees ADD CONSTRAINT PK_Employees PRIMARY KEY (EmployeeID);

ALTER TABLE Employees ADD CONSTRAINT FK_Employees_Employees FOREIGN KEY (ReportsTo) REFERENCES Employees (EmployeeID);
