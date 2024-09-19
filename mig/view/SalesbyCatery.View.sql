
CREATE OR REPLACE VIEW `Sales by Catery` AS
SELECT 
  Cateries.CateryID, 
  Cateries.CateryName, 
  Products.ProductName, 
  SUM(OrderDetailsExtended.ExtendedPrice) AS ProductSales
FROM 
  Cateries 
INNER JOIN 
  Products ON Cateries.CateryID = Products.CateryID
INNER JOIN 
  OrderDetailsExtended ON Products.ProductID = OrderDetailsExtended.ProductID
INNER JOIN 
  Orders ON Orders.OrderID = OrderDetailsExtended.OrderID
WHERE 
  Orders.OrderDate BETWEEN '1997-01-01' AND '1997-12-31'
GROUP BY 
  Cateries.CateryID, 
  Cateries.CateryName, 
  Products.ProductName

