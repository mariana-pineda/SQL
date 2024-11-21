
CREATE VIEW `Sales Totals by Amount` AS
SELECT `Order Subtotals`.Subtotal AS SaleAmount, Orders.OrderID, Customers.CompanyName, Orders.ShippedDate
FROM Customers
INNER JOIN 
    (Orders INNER JOIN `Order Subtotals` ON Orders.OrderID = `Order Subtotals`.OrderID)
ON Customers.CustomerID = Orders.CustomerID
WHERE (`Order Subtotals`.Subtotal > 2500) AND (Orders.ShippedDate BETWEEN '1997-01-01' AND '1997-12-31')
