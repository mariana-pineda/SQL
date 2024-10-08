
CREATE VIEW `Product Sales for 1997` AS
SELECT Cateries.CateryName, Products.ProductName, 
  SUM(CAST(("Order Details".UnitPrice * Quantity * (1 - Discount)) AS DECIMAL(18, 2))) AS ProductSales
FROM Cateries 
JOIN Products ON Cateries.CateryID = Products.CateryID
JOIN Orders 
  ON Products.ProductID = "Order Details".ProductID
JOIN `Order Details` 
  ON Orders.OrderID = "Order Details".OrderID
WHERE Orders.ShippedDate BETWEEN '1997-01-01' AND '1997-12-31'
GROUP BY Cateries.CateryName, Products.ProductName
