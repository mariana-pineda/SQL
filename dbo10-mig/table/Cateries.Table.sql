
CREATE TABLE `Cateries` (
  `CateryID` INT NOT NULL GENERATED ALWAYS AS IDENTITY, 
  `CateryName` STRING(15) NOT NULL, 
  `Description` STRING, 
  `Picture` BINARY, 
  PRIMARY KEY (`CateryID`)
)
