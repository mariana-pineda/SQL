
CREATE OR REPLACE VIEW `Customer_and_Suppliers_by_City` AS
SELECT City, CompanyName, ContactName, 'Customers' AS Relationship 
FROM Customers
UNION 
SELECT City, CompanyName, ContactName, 'Suppliers' AS Relationship
FROM Suppliers;
-- ORDER BY City, CompanyName
