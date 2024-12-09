
CREATE TABLE `Order Details` (
  OrderID INT NOT NULL,
  ProductID INT NOT NULL,
  UnitPrice DECIMAL(19,4) NOT NULL DEFAULT 0,
  Quantity SMALLINT NOT NULL DEFAULT 1,
  Discount FLOAT NOT NULL DEFAULT 0
);

-- Creating the primary key constraint for the table
ALTER TABLE `Order Details` ADD CONSTRAINT PK_Order_Details PRIMARY KEY (OrderID, ProductID);

-- Adding the foreign key constraints for the table
ALTER TABLE `Order Details` ADD CONSTRAINT FK_Order_Details_Orders FOREIGN KEY(OrderID) REFERENCES Orders(OrderID);
ALTER TABLE `Order Details` ADD CONSTRAINT FK_Order_Details_Products FOREIGN KEY(ProductID) REFERENCES Products(ProductID);
