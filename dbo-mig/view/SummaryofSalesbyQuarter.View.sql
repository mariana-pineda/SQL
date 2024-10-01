
CREATE OR REPLACE VIEW `Summary_of_Sales_by_Quarter` AS
SELECT Orders.ShippedDate, Orders.OrderID, `Order_Subtotals`.Subtotal
FROM Orders INNER JOIN `Order_Subtotals` ON Orders.OrderID = `Order_Subtotals`.OrderID
WHERE Orders.ShippedDate IS NOT NULL

