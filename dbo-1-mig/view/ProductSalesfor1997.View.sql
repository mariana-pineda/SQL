
CREATE VIEW `Product Sales for 1997` AS
SELECT Categories.CategoryName, Products.ProductName, 
SUM((CAST(`Order Details`.UnitPrice AS DECIMAL) * Quantity * (1 - Discount))) AS ProductSales
FROM Categories
INNER JOIN Products ON Categories.CategoryID = Products.CategoryID
INNER JOIN Orders ON Orders.OrderID = `Order Details`.OrderID
INNER JOIN `Order Details` ON Products.ProductID = `Order Details`.ProductID
WHERE Orders.ShippedDate BETWEEN '1997-01-01' AND '1997-12-31'
GROUP BY Categories.CategoryName, Products.ProductName
