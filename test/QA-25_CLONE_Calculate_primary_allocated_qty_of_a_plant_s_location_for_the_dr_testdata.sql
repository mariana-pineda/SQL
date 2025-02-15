-- Install necessary libraries for Databricks environment
-- %pip install [library] 

-- SQL code for test data generation in Databricks with the specified data types and conditions

-- Create a schema for test records in the f_order table
CREATE TABLE IF NOT EXISTS purgo_playground.f_order_test (
  order_nbr STRING,
  order_line_nbr STRING,
  primary_qty DOUBLE,
  open_qty DOUBLE,
  shipped_qty DOUBLE,
  cancel_qty DOUBLE,
  allocated_qty DOUBLE
);

-- Seed the f_order_test table with diverse test data
INSERT INTO purgo_playground.f_order_test (
  order_nbr, order_line_nbr, primary_qty, open_qty, shipped_qty, cancel_qty, allocated_qty
)
VALUES
  -- Happy path scenarios
  ('ORD001', '001', 100.0, 50.0, 30.0, 5.0, 185.0),
  ('ORD002', '001', 150.0, 70.0, 40.0, 10.0, 270.0),
  ('ORD003', '002', 120.0, 60.0, 20.0, 0.0, 200.0),

  -- Edge cases: boundary conditions
  ('ORD004', '003', 0.0, 0.0, 0.0, 0.0, 0.0),
  ('ORD005', '004', 999999999.99, 999999999.99, 999999999.99, 999999999.99, 3999999999.96),

  -- Error cases: invalid input scenarios
  ('ORD006', '005', NULL, 50.0, 10.0, 5.0, NULL),                      -- Missing primary_qty
  ('ORD007', '006', -50.0, 10.0, 5.0, 3.0, NULL),                     -- Negative primary_qty value
  ('ORD008', '007', 100.0, -70.0, 30.0, 10.0, NULL),                  -- Negative open_qty value

  -- NULL handling scenarios
  ('ORD009', '008', 100.0, NULL, NULL, NULL, 100.0),
  
  -- Special characters and multi-byte characters in order numbers
  ('注文A', '行001', 110.0, 40.0, 20.0, 5.0, 175.0),                 -- Japanese text
  ('ORD©', '001', 100.0, 50.0, 30.0, 5.0, 185.0),                   -- Special character ©

  -- Overlapping entries for order_nbr and order_line_nbr
  ('ORD010', '009', 110.0, 40.0, 20.0, 5.0, 175.0),
  ('ORD010', '009', 110.0, 40.0, 20.0, 5.0, 175.0),                 -- Duplicate should be handled

  -- Dependency on external inventory updates - simulated with older timestamp data
  ('ORD011', '010', 100.0, 50.0, 30.0, 5.0, 185.0);

-- Verify the inserted test data
SELECT * FROM purgo_playground.f_order_test;
