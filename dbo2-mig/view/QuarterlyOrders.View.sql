
CREATE OR REPLACE VIEW `Quarterly Orders` AS
SELECT DISTINCT Customers.CustomerID, Customers.CompanyName, Customers.City, Customers.Country
FROM Customers RIGHT JOIN Orders ON Customers.CustomerID = Orders.CustomerID
WHERE Orders.OrderDate BETWEEN DATE('1997-01-01') AND DATE('1997-12-31')
