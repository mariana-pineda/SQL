
CREATE OR REPLACE VIEW `Current_Product_List` AS
SELECT Product_List.ProductID, Product_List.ProductName
FROM Products AS Product_List
WHERE Product_List.Discontinued = 0;