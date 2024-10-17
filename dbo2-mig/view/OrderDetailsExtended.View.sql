
CREATE OR REPLACE VIEW `Order Details Extended` AS
SELECT 
  `Order Details`.OrderID, 
  `Order Details`.ProductID, 
  Products.ProductName, 
  `Order Details`.UnitPrice, 
  `Order Details`.Quantity, 
  `Order Details`.Discount, 
  (`Order Details`.UnitPrice * `Order Details`.Quantity * (1 - `Order Details`.Discount)) AS ExtendedPrice
FROM 
  Products 
INNER JOIN 
  `Order Details` 
ON 
  Products.ProductID = `Order Details`.ProductID;
