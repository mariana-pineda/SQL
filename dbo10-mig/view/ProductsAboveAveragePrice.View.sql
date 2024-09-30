
CREATE OR REPLACE VIEW `Products_Above_Average_Price` AS
SELECT ProductName, UnitPrice
FROM Products
WHERE UnitPrice > (SELECT AVG(UnitPrice) FROM Products);
-- ORDER BY UnitPrice DESC
