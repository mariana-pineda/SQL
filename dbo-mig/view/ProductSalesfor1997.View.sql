
CREATE VIEW `Product Sales for 1997` AS
SELECT 
    Cateries.CateryName, 
    Products.ProductName, 
    SUM(CAST("Order Details".UnitPrice * Quantity * (1 - Discount) AS DOUBLE)) AS ProductSales
FROM 
    Cateries 
    INNER JOIN Products ON Cateries.CateryID = Products.CateryID
    INNER JOIN Orders ON Orders.OrderID = "Order Details".OrderID
    INNER JOIN "Order Details" ON Products.ProductID = "Order Details".ProductID
WHERE 
    Orders.ShippedDate BETWEEN '1997-01-01' AND '1997-12-31'
GROUP BY 
    Cateries.CateryName, 
    Products.ProductName

