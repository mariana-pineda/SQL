
CREATE OR REPLACE VIEW `Products_by_Catery` AS
SELECT Cateries.CateryName, Products.ProductName, Products.QuantityPerUnit, Products.UnitsInStock, Products.Discontinued
FROM Cateries
INNER JOIN Products ON Cateries.CateryID = Products.CateryID
WHERE Products.Discontinued <> 1

