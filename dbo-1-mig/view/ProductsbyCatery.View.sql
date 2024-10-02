
CREATE OR REPLACE VIEW `Products by Catery` AS
SELECT 
  Cateries.CateryName, 
  Products.ProductName, 
  Products.QuantityPerUnit, 
  Products.UnitsInStock, 
  Products.Discontinued
FROM 
  Cateries 
JOIN 
  Products 
ON 
  Cateries.CateryID = Products.CateryID
WHERE 
  Products.Discontinued <> 1;
