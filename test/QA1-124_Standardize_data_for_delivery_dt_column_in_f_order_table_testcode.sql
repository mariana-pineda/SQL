/* 
Setup and Configuration Section
Initialize the testing environment by setting the appropriate catalog and schema.
Ensure that the f_order table exists within the specified Unity Catalog and schema.
*/

/* 
Schema Validation Test
Ensure the f_order table has the correct schema, specifically that delivery_dt is DECIMAL(38,0).
*/
-- Validate schema of f_order table
SELECT 
    column_name, 
    data_type 
FROM 
    information_schema.columns 
WHERE 
    table_catalog = 'purgo_databricks' 
    AND table_schema = 'purgo_playground' 
    AND table_name = 'f_order'
    AND column_name = 'delivery_dt'
    AND data_type = 'decimal(38,0)';

-- Assertion: The above query should return exactly one record
SELECT 
    COUNT(*) AS valid_schema 
FROM (
    SELECT 
        column_name, 
        data_type 
    FROM 
        information_schema.columns 
    WHERE 
        table_catalog = 'purgo_databricks' 
        AND table_schema = 'purgo_playground' 
        AND table_name = 'f_order'
        AND column_name = 'delivery_dt'
        AND data_type = 'decimal(38,0)'
) AS schema_check;

-- Assert that valid_schema equals 1
SELECT 
    CASE 
        WHEN (SELECT COUNT(*) FROM (
                SELECT 
                    column_name, 
                    data_type 
                FROM 
                    information_schema.columns 
                WHERE 
                    table_catalog = 'purgo_databricks' 
                    AND table_schema = 'purgo_playground' 
                    AND table_name = 'f_order'
                    AND column_name = 'delivery_dt'
                    AND data_type = 'decimal(38,0)'
            ) AS schema_check) = 1 
        THEN 'Schema Validation Passed' 
        ELSE 'Schema Validation Failed' 
    END AS schema_validation_result;

/* 
Data Type Conversion Test
Check if all delivery_dt values are correctly stored as DECIMAL(38,0).
*/
-- Verify data type of delivery_dt
SELECT 
    delivery_dt, 
    CASE 
        WHEN delivery_dt IS NULL THEN 'NULL' 
        WHEN delivery_dt = CAST(delivery_dt AS DECIMAL(38,0)) THEN 'Valid Decimal' 
        ELSE 'Invalid Decimal' 
    END AS data_type_check 
FROM 
    purgo_databricks.purgo_playground.f_order;

-- Assert that there are no invalid decimals
SELECT 
    COUNT(*) AS invalid_decimals 
FROM 
    purgo_databricks.purgo_playground.f_order 
WHERE 
    delivery_dt IS NOT NULL 
    AND delivery_dt != CAST(delivery_dt AS DECIMAL(38,0));

-- Assert that invalid_decimals equals 0
SELECT 
    CASE 
        WHEN (SELECT COUNT(*) FROM purgo_databricks.purgo_playground.f_order 
              WHERE delivery_dt IS NOT NULL 
              AND delivery_dt != CAST(delivery_dt AS DECIMAL(38,0))) = 0 
        THEN 'Data Type Conversion Passed' 
        ELSE 'Data Type Conversion Failed' 
    END AS data_type_conversion_result;

/* 
Format Validation Test
Ensure that all non-null delivery_dt values follow the yyyymmdd format.
*/
-- Check format of delivery_dt
SELECT 
    delivery_dt, 
    CASE 
        WHEN delivery_dt IS NULL THEN 'NULL' 
        WHEN delivery_dt BETWEEN 10000101 AND 99991231 THEN 
            CASE 
                WHEN CAST(delivery_dt AS STRING) LIKE "________" THEN 'Valid Format' 
                ELSE 'Invalid Format' 
            END 
        ELSE 'Invalid Format' 
    END AS format_check 
FROM 
    purgo_databricks.purgo_playground.f_order;

-- Assert that there are no invalid formats
SELECT 
    COUNT(*) AS invalid_formats 
FROM 
    purgo_databricks.purgo_playground.f_order 
WHERE 
    delivery_dt IS NOT NULL 
    AND (delivery_dt < 10000101 OR delivery_dt > 99991231 
         OR CAST(delivery_dt AS STRING) NOT LIKE "________");

-- Assert that invalid_formats equals 0
SELECT 
    CASE 
        WHEN (SELECT COUNT(*) FROM purgo_databricks.purgo_playground.f_order 
              WHERE delivery_dt IS NOT NULL 
              AND (delivery_dt < 10000101 OR delivery_dt > 99991231 
                   OR CAST(delivery_dt AS STRING) NOT LIKE "________")) = 0 
        THEN 'Format Validation Passed' 
        ELSE 'Format Validation Failed' 
    END AS format_validation_result;

/* 
NULL Handling Test
Verify that NULL values in delivery_dt are handled appropriately.
*/
-- Check for NULL values
SELECT 
    COUNT(*) AS null_count 
FROM 
    purgo_databricks.purgo_playground.f_order 
WHERE 
    delivery_dt IS NULL;

-- Define the expected number of NULLs based on test data
SELECT 
    CASE 
        WHEN (SELECT COUNT(*) FROM purgo_databricks.purgo_playground.f_order WHERE delivery_dt IS NULL) = 1 
        THEN 'NULL Handling Passed' 
        ELSE 'NULL Handling Failed' 
    END AS null_handling_result;

/* 
Complex Type Validation Test
Since delivery_dt is a simple DECIMAL type, this test ensures no complex types are present.
*/
-- Ensure no complex types are present in the table
SELECT 
    column_name, 
    data_type 
FROM 
    information_schema.columns 
WHERE 
    table_catalog = 'purgo_databricks' 
    AND table_schema = 'purgo_playground' 
    AND table_name = 'f_order'
    AND data_type IN ('array', 'struct', 'map');

-- Assert that no complex types are found
SELECT 
    COUNT(*) AS complex_types_count 
FROM 
    information_schema.columns 
WHERE 
    table_catalog = 'purgo_databricks' 
    AND table_schema = 'purgo_playground' 
    AND table_name = 'f_order'
    AND data_type IN ('array', 'struct', 'map');

-- Assert that complex_types_count equals 0
SELECT 
    CASE 
        WHEN (SELECT COUNT(*) FROM information_schema.columns 
              WHERE table_catalog = 'purgo_databricks' 
              AND table_schema = 'purgo_playground' 
              AND table_name = 'f_order'
              AND data_type IN ('array', 'struct', 'map')) = 0 
        THEN 'Complex Type Validation Passed' 
        ELSE 'Complex Type Validation Failed' 
    END AS complex_type_validation_result;

/* 
Column Count Test
Ensure that the number of columns in the f_order table matches the target schema.
*/
-- Get the number of columns in f_order table
SELECT 
    COUNT(*) AS column_count 
FROM 
    information_schema.columns 
WHERE 
    table_catalog = 'purgo_databricks' 
    AND table_schema = 'purgo_playground' 
    AND table_name = 'f_order';

-- Define the expected number of columns
SELECT 
    CASE 
        WHEN (SELECT COUNT(*) FROM information_schema.columns 
              WHERE table_catalog = 'purgo_databricks' 
              AND table_schema = 'purgo_playground' 
              AND table_name = 'f_order') = 1 
        THEN 'Column Count Validation Passed' 
        ELSE 'Column Count Validation Failed' 
    END AS column_count_validation_result;

/* 
Data Quality Validation Test
Ensure that all records meet the data quality standards for delivery_dt.
*/
-- Identify invalid records
SELECT 
    delivery_dt 
FROM 
    purgo_databricks.purgo_playground.f_order 
WHERE 
    delivery_dt IS NOT NULL 
    AND (delivery_dt < 10000101 
         OR delivery_dt > 99991231 
         OR CAST(delivery_dt AS STRING) NOT LIKE "________");

-- Assert that there are no records with invalid delivery_dt
SELECT 
    COUNT(*) AS invalid_records_count 
FROM 
    purgo_databricks.purgo_playground.f_order 
WHERE 
    delivery_dt IS NOT NULL 
    AND (delivery_dt < 10000101 
         OR delivery_dt > 99991231 
         OR CAST(delivery_dt AS STRING) NOT LIKE "________");

-- Assert that invalid_records_count equals 0
SELECT 
    CASE 
        WHEN (SELECT COUNT(*) FROM purgo_databricks.purgo_playground.f_order 
              WHERE delivery_dt IS NOT NULL 
              AND (delivery_dt < 10000101 
                   OR delivery_dt > 99991231 
                   OR CAST(delivery_dt AS STRING) NOT LIKE "________")) = 0 
        THEN 'Data Quality Validation Passed' 
        ELSE 'Data Quality Validation Failed' 
    END AS data_quality_validation_result;

/* 
Performance Test
Measure the time taken to validate the delivery_dt column.
Note: This is a simple performance metric and can be expanded as needed.
*/
-- Capture start time
SELECT current_timestamp() AS start_time;

-- Execute validation query
SELECT 
    COUNT(*) 
FROM 
    purgo_databricks.purgo_playground.f_order 
WHERE 
    delivery_dt IS NOT NULL 
    AND (delivery_dt < 10000101 
         OR delivery_dt > 99991231 
         OR CAST(delivery_dt AS STRING) NOT LIKE "________");

-- Capture end time
SELECT current_timestamp() AS end_time;

/* 
Delta Lake Operations Test
Validate any Delta Lake specific operations if applicable.
*/
-- Example: Check if f_order table is a Delta table
SELECT 
    CASE 
        WHEN provider = "delta" THEN "Delta Lake Table" 
        ELSE "Non-Delta Lake Table" 
    END AS table_type 
FROM 
    information_schema.tables 
WHERE 
    table_catalog = 'purgo_databricks' 
    AND table_schema = 'purgo_playground' 
    AND table_name = 'f_order';

-- Assert that f_order is a Delta Lake table
SELECT 
    CASE 
        WHEN (SELECT provider 
              FROM information_schema.tables 
              WHERE table_catalog = 'purgo_databricks' 
              AND table_schema = 'purgo_playground' 
              AND table_name = 'f_order') = "delta" 
        THEN "Delta Lake Operations Test Passed" 
        ELSE "Delta Lake Operations Test Failed" 
    END AS delta_lake_operations_test_result;

/* 
Cleanup Section
Perform any necessary cleanup operations after testing.
*/
-- Example: Remove test records if needed
-- DELETE FROM purgo_databricks.purgo_playground.f_order WHERE delivery_dt IS NOT NULL;

/* 
Test Data Insertion
Insert predefined test data into the f_order table for validation purposes.
*/
-- Define the schema for test data
WITH test_data AS (
    SELECT CAST(20240910 AS DECIMAL(38,0)) AS delivery_dt UNION ALL -- Happy path: valid yyyymmdd
    SELECT CAST(20231231 AS DECIMAL(38,0)) UNION ALL -- Happy path: end of year
    SELECT CAST(20240101 AS DECIMAL(38,0)) UNION ALL -- Happy path: start of year
    SELECT CAST(19991231 AS DECIMAL(38,0)) UNION ALL -- Edge case: past date
    SELECT CAST(21000101 AS DECIMAL(38,0)) UNION ALL -- Edge case: future date
    SELECT CAST(NULL AS DECIMAL(38,0)) UNION ALL -- NULL handling: null value
    SELECT CAST(20240910 AS DECIMAL(38,0)) UNION ALL -- Error case: non-numeric characters replaced
    SELECT CAST(20240901 AS DECIMAL(38,0)) UNION ALL -- Error case: incorrect length replaced with a valid decimal
    SELECT CAST(20240910 AS DECIMAL(38,0)) UNION ALL -- Error case: invalid format with hyphens replaced with valid decimal
    SELECT CAST(20241301 AS DECIMAL(38,0)) UNION ALL -- Error case: invalid month adjusted to a valid decimal
    SELECT CAST(20240230 AS DECIMAL(38,0)) UNION ALL -- Error case: invalid day adjusted to a valid decimal
    SELECT CAST(0 AS DECIMAL(38,0)) UNION ALL -- Special case: all zeros
    SELECT CAST(-20240910 AS DECIMAL(38,0)) UNION ALL -- Error case: negative value
    SELECT CAST(20240910 AS DECIMAL(38,0)) UNION ALL -- Error case: one digit short replaced with valid decimal
    SELECT CAST(20240910 AS DECIMAL(38,0)) UNION ALL -- Error case: one digit extra replaced with valid decimal
    SELECT CAST(20240910 AS DECIMAL(38,0)) UNION ALL -- Error case: special character replaced with valid decimal
    SELECT CAST(20240910 AS DECIMAL(38,0)) UNION ALL -- Special characters: multi-byte replaced with valid decimal
    SELECT CAST(0 AS DECIMAL(38,0)) UNION ALL -- Error case: space only replaced with valid decimal
    SELECT CAST(20240910 AS DECIMAL(38,0)) UNION ALL -- Error case: slashes in date replaced with valid decimal
    SELECT CAST(20240910 AS DECIMAL(38,0)) UNION ALL -- Error case: asterisks in date replaced with valid decimal
    SELECT CAST(20240910 AS DECIMAL(38,0)) -- Error case: tabs in date replaced with valid decimal
)

-- Insert test data into the f_order table
INSERT INTO purgo_databricks.purgo_playground.f_order (delivery_dt)
SELECT delivery_dt FROM test_data;
