
CREATE OR REPLACE VIEW `Product Sales for 1997` AS
SELECT C.CateryName, P.ProductName, 
SUM(CAST(OD.UnitPrice * Quantity * (1 - Discount) AS DECIMAL(18, 2))) AS ProductSales
FROM Cateries C
INNER JOIN Products P ON C.CateryID = P.CateryID
INNER JOIN Orders O ON O.OrderID = OD.OrderID
INNER JOIN `Order Details` OD ON P.ProductID = OD.ProductID
WHERE O.ShippedDate BETWEEN '1997-01-01' AND '1997-12-31'
GROUP BY C.CateryName, P.ProductName

