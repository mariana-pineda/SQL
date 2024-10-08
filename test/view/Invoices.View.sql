
CREATE OR REPLACE VIEW Invoices AS
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
  CONCAT(Employees.FirstName, ' ', Employees.LastName) AS Salesperson, 
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
  (OrderDetails.UnitPrice * OrderDetails.Quantity * (1 - OrderDetails.Discount)) AS ExtendedPrice, 
  Orders.Freight
FROM 
  Shippers 
  INNER JOIN (
    Products 
    INNER JOIN (
      Employees 
      INNER JOIN (
        Customers 
        INNER JOIN Orders ON Customers.CustomerID = Orders.CustomerID
      ) ON Employees.EmployeeID = Orders.EmployeeID 
      INNER JOIN OrderDetails ON Orders.OrderID = OrderDetails.OrderID
    ) ON Products.ProductID = OrderDetails.ProductID
  ) ON Shippers.ShipperID = Orders.ShipVia

