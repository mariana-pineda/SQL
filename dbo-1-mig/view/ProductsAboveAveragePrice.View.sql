
CREATE VIEW `Products Above Average Price` AS
SELECT ProductName, UnitPrice
FROM Products
WHERE UnitPrice > (SELECT AVG(UnitPrice) FROM Products)
--ORDER BY UnitPrice DESC
