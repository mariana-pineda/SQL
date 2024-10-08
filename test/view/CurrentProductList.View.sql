
CREATE OR REPLACE VIEW `Current Product List` AS
SELECT Product_List.ProductID, Product_List.ProductName
FROM Products AS Product_List
WHERE Product_List.Discontinued = 0;
