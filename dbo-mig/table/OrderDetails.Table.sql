
CREATE TABLE `Order Details` (
  `OrderID` INT NOT NULL,
  `ProductID` INT NOT NULL,
  `UnitPrice` DECIMAL(19, 4) NOT NULL DEFAULT 0,
  `Quantity` SMALLINT NOT NULL DEFAULT 1,
  `Discount` FLOAT NOT NULL DEFAULT 0,
  PRIMARY KEY (`OrderID`, `ProductID`),
  FOREIGN KEY (`OrderID`) REFERENCES `Orders`(`OrderID`),
  FOREIGN KEY (`ProductID`) REFERENCES `Products`(`ProductID`)
);
