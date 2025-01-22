
CREATE VIEW `Order Details Extended` AS
SELECT `Order Details`.OrderID, `Order Details`.ProductID, Products.ProductName, 
    `Order Details`.UnitPrice, `Order Details`.Quantity, `Order Details`.Discount, 
    (CAST(`Order Details`.UnitPrice * Quantity * (1 - Discount) AS DOUBLE)) AS ExtendedPrice
FROM Products INNER JOIN `Order Details` ON Products.ProductID = `Order Details`.ProductID
--ORDER BY `Order Details`.OrderID
