-- Create CTE for test data generation with diverse scenarios
WITH TestData AS (
  SELECT 
    CAST(1 AS BIGINT) AS id,
    'Electronics' AS product_type, -- Happy path: valid category
    '2022-01-15T00:00:00.000+0000' AS purchased_date, -- Valid timestamp format
    CAST(1000.50 AS DOUBLE) AS revenue, -- Valid revenue value
    'USA' AS country, -- Valid country name

  UNION ALL

  SELECT 
    CAST(2 AS BIGINT),
    'Clothing',
    '2022-02-20T00:00:00.000+0000',
    CAST(1500.75 AS DOUBLE),
    'Canada',

  UNION ALL

  SELECT 
    CAST(NULL AS BIGINT), -- NULL handling scenario for ID
    NULL, -- NULL handling scenario for product_type
    NULL, -- NULL handling scenario for purchased_date
    NULL, -- NULL handling scenario for revenue
    NULL  -- NULL handling scenario for country
    
  UNION ALL
  
  SELECT 
    CAST(-3 AS BIGINT), -- Edge case: negative ID value (invalid)
    '', -- Special characters: empty string as invalid product_type
    'InvalidDate', -- Error case: invalid date format
    CAST(-500.25 AS DOUBLE), -- Error case: negative revenue (invalid)
    '!@#$%' -- Special characters in country name (invalid)

   UNION ALL
   
   SELECT 
     CAST(4 AS BIGINT),
     'Furniture',
     '2023-03-21T12:30:45.123+0000', 
     DECIMAL('99999.99'), 
     'UK'

   UNION ALL
   
   SELECT 
     CAST(5 AS BIGINT),
     'Books',
     TIMESTAMP('2024-03-21T14:55:35.456+0000'),
     DECIMAL('25000.99'),
     'Germany'
     
   UNION ALL
   
   SELECT 
      CAST(6 AS BIGINT),
      ARRAY('Electronics', 'Books')::ARRAY<STRING>, -- Array data type example with multi-byte characters included in the elements.
      STRUCT('2023-04-01T08:15:23.789+0000')::STRUCT<purchased_date TIMESTAMP>,  
      MAP('revenue_1',DOUBLE('3000'), 'revenue_2',DOUBLE('4000'))::MAP<STRING, DOUBLE>,
      '--'::STRING
      
)

-- Validate and convert data types ensuring schema consistency before insertion or further processing.
SELECT *
FROM TestData;
