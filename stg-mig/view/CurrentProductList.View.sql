
CREATE OR REPLACE VIEW `Current Product List` AS
SELECT Product_List.ProductID, Product_List.ProductName
FROM Products AS Product_List
WHERE Product_List.Discontinued = 0;
-- ORDER BY clause has been commented out because views cannot have ORDER BY in Databricks
