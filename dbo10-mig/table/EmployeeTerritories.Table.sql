
CREATE TABLE EmployeeTerritories (
  EmployeeID INT NOT NULL, 
  TerritoryID STRING NOT NULL, 
  CONSTRAINT PK_EmployeeTerritories PRIMARY KEY (EmployeeID, TerritoryID), 
  FOREIGN KEY (EmployeeID) REFERENCES Employees (EmployeeID), 
  FOREIGN KEY (TerritoryID) REFERENCES Territories (TerritoryID)
)
