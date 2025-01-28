
CREATE VIEW Invoices AS
SELECT 
  Orders.ShipName, 
  Orders.ShipAddress, 
  Orders.ShipCity, 
  Orders.ShipRegion, 
  Orders.ShipPostalCode, 
  Orders.ShipCountry, 
  Orders.CustomerID, 
  Customers.CompanyName AS CustomerName, 
  Customers.Address, 
  Customers.City, 
  Customers.Region, 
  Customers.PostalCode, 
  Customers.Country, 
  CONCAT(FirstName, ' ', LastName) AS Salesperson, 
  Orders.OrderID, 
  Orders.OrderDate, 
  Orders.RequiredDate, 
  Orders.ShippedDate, 
  Shippers.CompanyName AS ShipperName, 
  OrderDetails.ProductID, 
  Products.ProductName, 
  OrderDetails.UnitPrice, 
  OrderDetails.Quantity, 
  OrderDetails.Discount, 
  (CAST(OrderDetails.UnitPrice * Quantity * (1 - Discount) AS DECIMAL(18,2))) AS ExtendedPrice, 
  Orders.Freight
FROM 
  Shippers 
  INNER JOIN Orders ON Shippers.ShipperID = Orders.ShipVia
  INNER JOIN Customers ON Customers.CustomerID = Orders.CustomerID
  INNER JOIN Employees ON Employees.EmployeeID = Orders.EmployeeID
  INNER JOIN "Order Details" AS OrderDetails ON Orders.OrderID = OrderDetails.OrderID
  INNER JOIN Products ON Products.ProductID = OrderDetails.ProductID

