
CREATE OR REPLACE VIEW `Order Subtotals` AS
SELECT `Order Details`.OrderID, SUM(CAST(`Order Details`.UnitPrice * `Order Details`.Quantity * (1 - `Order Details`.Discount) AS DECIMAL(18,2))) AS Subtotal
FROM `Order Details`
GROUP BY `Order Details`.OrderID;
