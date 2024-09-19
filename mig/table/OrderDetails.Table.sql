
CREATE TABLE `Order_Details` (
  OrderID INT NOT NULL,
  ProductID INT NOT NULL,
  UnitPrice DECIMAL(19,4) NOT NULL DEFAULT 0,
  Quantity SMALLINT NOT NULL DEFAULT 1,
  Discount DOUBLE NOT NULL DEFAULT 0,
  PRIMARY KEY (OrderID, ProductID)
);

ALTER TABLE `Order_Details` 
ADD CONSTRAINT FK_Order_Details_Orders FOREIGN KEY (OrderID) REFERENCES `Orders` (OrderID);

ALTER TABLE `Order_Details` 
ADD CONSTRAINT FK_Order_Details_Products FOREIGN KEY (ProductID) REFERENCES `Products` (ProductID);
