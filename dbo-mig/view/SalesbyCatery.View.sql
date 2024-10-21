
CREATE OR REPLACE VIEW `Sales by Catery` AS
SELECT 
    Cateries.CateryID, 
    Cateries.CateryName, 
    Products.ProductName, 
    SUM(Order_Details_Extended.ExtendedPrice) AS ProductSales
FROM 
    Cateries 
INNER JOIN 
    Products 
ON 
    Cateries.CateryID = Products.CateryID
INNER JOIN 
    Orders 
ON 
    Orders.OrderID = Order_Details_Extended.OrderID
INNER JOIN 
    Order_Details_Extended 
ON 
    Products.ProductID = Order_Details_Extended.ProductID
WHERE 
    Orders.OrderDate BETWEEN '1997-01-01' AND '1997-12-31'
GROUP BY 
    Cateries.CateryID, 
    Cateries.CateryName, 
    Products.ProductName

