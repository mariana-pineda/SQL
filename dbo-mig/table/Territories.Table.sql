
CREATE TABLE Territories (
  TerritoryID STRING NOT NULL,
  TerritoryDescription STRING NOT NULL,
  RegionID INT NOT NULL,
  PRIMARY KEY (TerritoryID)
);

ALTER TABLE Territories ADD FOREIGN KEY (RegionID) REFERENCES Region (RegionID);
