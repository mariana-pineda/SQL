
CREATE OR REPLACE VIEW `Summary_of_Sales_by_Year` AS
SELECT Orders.ShippedDate, Orders.OrderID, `Order Subtotals`.Subtotal
FROM Orders INNER JOIN `Order Subtotals` ON Orders.OrderID = `Order Subtotals`.OrderID
WHERE Orders.ShippedDate IS NOT NULL;
