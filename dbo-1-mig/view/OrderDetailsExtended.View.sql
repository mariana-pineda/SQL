
CREATE OR REPLACE VIEW `Order Details Extended` AS
SELECT `Order Details`.OrderID, `Order Details`.ProductID, Products.ProductName, 
    `Order Details`.UnitPrice, `Order Details`.Quantity, `Order Details`.Discount,
    (CAST((`Order Details`.UnitPrice * Quantity * (1 - Discount)) AS DECIMAL(19,4))) AS ExtendedPrice
FROM Products 
INNER JOIN `Order Details` ON Products.ProductID = `Order Details`.ProductID
