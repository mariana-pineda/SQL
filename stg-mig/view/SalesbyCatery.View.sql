
CREATE OR REPLACE VIEW `Sales by Catery` AS
SELECT
  Cateries.CateryID,
  Cateries.CateryName,
  Products.ProductName,
  SUM(`Order Details Extended`.ExtendedPrice) AS ProductSales
FROM
  Cateries
  INNER JOIN Products ON Cateries.CateryID = Products.CateryID
  INNER JOIN (
    SELECT
      Orders.OrderID,
      "Order Details Extended".ProductID,
      "Order Details Extended".ExtendedPrice
    FROM
      Orders
      INNER JOIN "Order Details Extended" ON Orders.OrderID = "Order Details Extended".OrderID
    WHERE
      Orders.OrderDate BETWEEN CAST('1997-01-01' AS DATE) AND CAST('1997-12-31' AS DATE)
  ) AS OrderProductDetails ON Products.ProductID = OrderProductDetails.ProductID
GROUP BY
  Cateries.CateryID,
  Cateries.CateryName,
  Products.ProductName

