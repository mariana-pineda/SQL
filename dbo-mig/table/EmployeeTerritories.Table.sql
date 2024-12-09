
CREATE TABLE EmployeeTerritories (
  EmployeeID INTEGER NOT NULL,
  TerritoryID STRING NOT NULL,
  PRIMARY KEY (EmployeeID, TerritoryID),
  FOREIGN KEY (EmployeeID) REFERENCES Employees (EmployeeID),
  FOREIGN KEY (TerritoryID) REFERENCES Territories (TerritoryID)
)
