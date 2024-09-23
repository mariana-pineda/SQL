
CREATE TABLE Territories (
  TerritoryID STRING NOT NULL,
  TerritoryDescription STRING NOT NULL,
  RegionID INT NOT NULL,
  PRIMARY KEY (TerritoryID),
  FOREIGN KEY (RegionID) REFERENCES Region (RegionID)
)
