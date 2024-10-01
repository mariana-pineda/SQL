
CREATE VIEW `Order Subtotals` AS
SELECT `Order Details`.OrderID, SUM(CAST((`Order Details`.UnitPrice * Quantity * (1 - Discount)) AS DECIMAL(18, 2))) AS Subtotal
FROM `Order Details`
GROUP BY `Order Details`.OrderID
