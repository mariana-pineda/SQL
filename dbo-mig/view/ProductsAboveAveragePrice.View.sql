
CREATE VIEW `Products_Above_Average_Price` AS
SELECT Products.ProductName, Products.UnitPrice
FROM Products
WHERE Products.UnitPrice > (SELECT AVG(UnitPrice) FROM Products)
-- ORDER BY Products.UnitPrice DESC
