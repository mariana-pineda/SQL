
CREATE OR REPLACE VIEW `Sales by Catery` AS
SELECT Cateries.CateryID, Cateries.CateryName, Products.ProductName, 
	SUM(`Order Details Extended`.ExtendedPrice) AS ProductSales
FROM 	Cateries INNER JOIN 
		(Products INNER JOIN 
			(Orders INNER JOIN `Order Details Extended` ON Orders.OrderID = `Order Details Extended`.OrderID) 
		ON Products.ProductID = `Order Details Extended`.ProductID) 
	ON Cateries.CateryID = Products.CateryID
WHERE Orders.OrderDate BETWEEN '1997-01-01' AND '1997-12-31'
GROUP BY Cateries.CateryID, Cateries.CateryName, Products.ProductName
--ORDER BY Products.ProductName
