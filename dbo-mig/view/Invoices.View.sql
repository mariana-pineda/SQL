
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
    CONCAT(Employees.FirstName, ' ', Employees.LastName) AS Salesperson, 
    Orders.OrderID, 
    Orders.OrderDate, 
    Orders.RequiredDate, 
    Orders.ShippedDate, 
    Shippers.CompanyName AS ShipperName, 
    Order_Details.ProductID, 
    Products.ProductName, 
    Order_Details.UnitPrice, 
    Order_Details.Quantity, 
    Order_Details.Discount, 
    CAST(Order_Details.UnitPrice * Order_Details.Quantity * (1 - Order_Details.Discount) AS DECIMAL(19, 4)) AS ExtendedPrice, 
    Orders.Freight
FROM 
    Shippers 
    INNER JOIN Orders ON Shippers.ShipperID = Orders.ShipVia
    INNER JOIN Customers ON Customers.CustomerID = Orders.CustomerID
    INNER JOIN Employees ON Employees.EmployeeID = Orders.EmployeeID
    INNER JOIN Order_Details ON Orders.OrderID = Order_Details.OrderID
    INNER JOIN Products ON Products.ProductID = Order_Details.ProductID

