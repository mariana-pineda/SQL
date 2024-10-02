
CREATE OR REPLACE VIEW Invoices AS
SELECT Orders.ShipName, Orders.ShipAddress, Orders.ShipCity, Orders.ShipRegion, Orders.ShipPostalCode, 
       Orders.ShipCountry, Orders.CustomerID, Customers.CompanyName AS CustomerName, Customers.Address, Customers.City, 
       Customers.Region, Customers.PostalCode, Customers.Country, 
       CONCAT(FirstName, ' ', LastName) AS Salesperson, 
       Orders.OrderID, Orders.OrderDate, Orders.RequiredDate, Orders.ShippedDate, Shippers.CompanyName AS ShipperName, 
       `Order Details`.ProductID, Products.ProductName, `Order Details`.UnitPrice, `Order Details`.Quantity, 
       `Order Details`.Discount, 
       CAST(`Order Details`.UnitPrice * Quantity * (1 - Discount) AS DECIMAL(19, 4)) AS ExtendedPrice, Orders.Freight
FROM Shippers 
INNER JOIN Orders ON Shippers.ShipperID = Orders.ShipVia
INNER JOIN Customers ON Customers.CustomerID = Orders.CustomerID
INNER JOIN Employees ON Employees.EmployeeID = Orders.EmployeeID
INNER JOIN `Order Details` ON Orders.OrderID = `Order Details`.OrderID
INNER JOIN Products ON Products.ProductID = `Order Details`.ProductID;
