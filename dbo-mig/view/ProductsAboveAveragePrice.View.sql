
CREATE VIEW `Products Above Average Price` AS
SELECT Products.ProductName, Products.UnitPrice
FROM Products
WHERE Products.UnitPrice > (SELECT AVG(UnitPrice) FROM Products);
-- Note: The ORDER BY clause is not included in the view as views do not support ordering in Databricks.
