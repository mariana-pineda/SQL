
CREATE TABLE Employees (
  EmployeeID INTEGER NOT NULL GENERATED ALWAYS AS IDENTITY (START WITH 1 INCREMENT BY 1),
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
  PRIMARY KEY (EmployeeID)
);

ALTER TABLE Employees
ADD CONSTRAINT FK_Employees_ReportsTo FOREIGN KEY (ReportsTo) REFERENCES Employees (EmployeeID);