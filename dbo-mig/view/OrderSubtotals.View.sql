
CREATE OR REPLACE VIEW `Order Subtotals` AS
SELECT `Order Details`.OrderID, SUM((`Order Details`.UnitPrice * Quantity * (1 - Discount))) AS Subtotal
FROM `Order Details`
GROUP BY `Order Details`.OrderID
