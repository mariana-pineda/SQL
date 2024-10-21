
CREATE OR REPLACE VIEW `Customer and Suppliers by City` AS
SELECT City, CompanyName, ContactName, 'Customers' AS Relationship 
FROM Customers
UNION 
SELECT City, CompanyName, ContactName, 'Suppliers' AS Relationship
FROM Suppliers;
