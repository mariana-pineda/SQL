
CREATE VIEW `Sales by Catery` AS
SELECT 
    Cateries.CateryID, 
    Cateries.CateryName, 
    Products.ProductName, 
    SUM(`Order Details Extended`.ExtendedPrice) AS ProductSales
FROM  
    Cateries 
    INNER JOIN Products ON Cateries.CateryID = Products.CateryID
    INNER JOIN (Orders 
        INNER JOIN `Order Details Extended` ON Orders.OrderID = `Order Details Extended`.OrderID) 
    ON Products.ProductID = `Order Details Extended`.ProductID
WHERE 
    Orders.OrderDate BETWEEN '19970101' AND '19971231'
GROUP BY 
    Cateries.CateryID, 
    Cateries.CateryName, 
    Products.ProductName

