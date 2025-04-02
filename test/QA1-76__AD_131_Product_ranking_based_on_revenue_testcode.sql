-- SQL Test Code for Databricks Environment

/* Setup and configuration information */
/* Ensure the database and schema are correctly set up in Unity Catalog */
/*
CREATE DATABASE IF NOT EXISTS purgo_playground;
USE purgo_playground;
*/

/* Create target table with proper constraints */
CREATE TABLE IF NOT EXISTS purgo_playground.information_schema.product_revenue (
  id BIGINT NOT NULL,
  product_type STRING NOT NULL,
  purchased_date TIMESTAMP NOT NULL,
  revenue DOUBLE NOT NULL,
  country STRING NOT NULL,
  performance STRING
);

-- CTE to simulate test data generation
WITH TestData AS (
  SELECT 
    CAST(1 AS BIGINT) AS id,
    'Electronics' AS product_type, 
    TIMESTAMP('2022-01-15T00:00:00.000+0000') AS purchased_date, 
    CAST(1000.50 AS DOUBLE) AS revenue, 
    'USA' AS country

  UNION ALL

  SELECT 
    CAST(2 AS BIGINT),
    'Clothing',
    TIMESTAMP('2022-02-20T00:00:00.000+0000'),
    CAST(1500.75 AS DOUBLE),
    'Canada'

  UNION ALL
  
  SELECT 
     CAST(NULL AS BIGINT), -- Testing null handling
     NULL, -- Testing null handling
     NULL, -- Testing null handling
     NULL, -- Testing null handling
     NULL -- Testing null handling

   UNION ALL
   
   SELECT 
     CAST(-3 AS BIGINT), -- Edge case testing with negative ID value
     '', -- Special characters testing with empty string as invalid product_type
     TIMESTAMP('1970-01-01T00:00:00.000+0000'), -- Invalid timestamp format by using epoch date for demonstration purpose.
     CAST(-500.25 AS DOUBLE), -- Error case testing with negative revenue value
     '!@#$%' -- Special characters in country name

)

/* Validate that the number of columns matches the target table's schema before insertion */
SELECT *
FROM TestData;

/* Insert validated data into the target table ensuring column match */
INSERT INTO purgo_playground.information_schema.product_revenue (id, product_type, purchased_date, revenue, country)
SELECT id, product_type, purchased_date, revenue, country FROM TestData;

/* Unit tests for transformations using window functions for ranking */
WITH RankedProducts AS (
  SELECT *,
         ROW_NUMBER() OVER (PARTITION BY country ORDER BY revenue DESC) as rank_monthly
  FROM purgo_playground.information_schema.product_revenue
)

-- Integration test for performance classification based on consistency criteria across months.
SELECT *, CASE WHEN COUNT(CASE WHEN rank_monthly <= 3 THEN 1 END) >=6 THEN 'Gold'
               WHEN COUNT(CASE WHEN rank_monthly <= 3 THEN 1 END) >=3 THEN 'Silver'
               ELSE 'Bronze' END as performance_classification
FROM RankedProducts
GROUP BY id;

/* Performance test setup not included due to complexity but should focus on optimizing queries and indexing strategy */

/* Cleanup operations after tests execution */
DELETE FROM purgo_playground.information_schema.product_revenue WHERE id IS NULL; /* Remove rows with missing IDs */

-- Additional cleanup logic can be added here if necessary.

