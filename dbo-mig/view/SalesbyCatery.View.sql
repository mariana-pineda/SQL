
CREATE VIEW `Sales by Catery` AS
SELECT C.CateryID, C.CateryName, P.ProductName, 
       SUM(ODE.ExtendedPrice) AS ProductSales
FROM Cateries C
INNER JOIN Products P ON C.CateryID = P.CateryID
INNER JOIN `Order Details Extended` ODE ON P.ProductID = ODE.ProductID
INNER JOIN Orders O ON O.OrderID = ODE.OrderID
WHERE O.OrderDate BETWEEN '1997-01-01' AND '1997-12-31'
GROUP BY C.CateryID, C.CateryName, P.ProductName
--ORDER BY P.ProductName

