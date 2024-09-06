
CREATE TABLE Territories (
    TerritoryID STRING NOT NULL, 
    TerritoryDescription STRING NOT NULL, 
    RegionID INT NOT NULL, 
    PRIMARY KEY (TerritoryID)
);

ALTER TABLE Territories
ADD CONSTRAINT FK_Territories_Region FOREIGN KEY (RegionID) REFERENCES Region (RegionID);
