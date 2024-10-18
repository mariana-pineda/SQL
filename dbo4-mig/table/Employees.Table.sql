
CREATE TABLE Employees (
  EmployeeID BIGINT NOT NULL, 
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
  ReportsTo BIGINT, 
  PhotoPath STRING
) USING DELTA;

ALTER TABLE Employees ADD CONSTRAINT PK_Employees PRIMARY KEY (EmployeeID);

ALTER TABLE Employees ADD CONSTRAINT FK_Employees_Employees FOREIGN KEY (ReportsTo) REFERENCES Employees(EmployeeID);
