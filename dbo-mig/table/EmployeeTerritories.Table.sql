
CREATE TABLE EmployeeTerritories (
  EmployeeID INT NOT NULL,
  TerritoryID STRING NOT NULL,
  PRIMARY KEY (EmployeeID, TerritoryID)
) USING DELTA;

ALTER TABLE EmployeeTerritories 
ADD CONSTRAINT FK_EmployeeTerritories_Employees 
FOREIGN KEY (EmployeeID) REFERENCES Employees (EmployeeID);

ALTER TABLE EmployeeTerritories 
ADD CONSTRAINT FK_EmployeeTerritories_Territories 
FOREIGN KEY (TerritoryID) REFERENCES Territories (TerritoryID);
