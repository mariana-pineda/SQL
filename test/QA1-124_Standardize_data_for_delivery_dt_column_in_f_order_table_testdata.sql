-- Define the schema for test data
WITH test_data AS (
    SELECT CAST('20240910' AS DECIMAL(38,0)) AS delivery_dt UNION ALL -- Happy path: valid yyyymmdd
    SELECT CAST('20231231' AS DECIMAL(38,0)) UNION ALL -- Happy path: end of year
    SELECT CAST('20240101' AS DECIMAL(38,0)) UNION ALL -- Happy path: start of year
    SELECT CAST('19991231' AS DECIMAL(38,0)) UNION ALL -- Edge case: past date
    SELECT CAST('21000101' AS DECIMAL(38,0)) UNION ALL -- Edge case: future date
    SELECT CAST(NULL AS DECIMAL(38,0)) UNION ALL -- NULL handling: null value
    SELECT CAST('2024091A' AS DECIMAL(38,0)) UNION ALL -- Error case: non-numeric characters
    SELECT CAST('202409' AS DECIMAL(38,0)) UNION ALL -- Error case: incorrect length
    SELECT CAST('2024-09-10' AS DECIMAL(38,0)) UNION ALL -- Error case: invalid format with hyphens
    SELECT CAST('20241301' AS DECIMAL(38,0)) UNION ALL -- Error case: invalid month
    SELECT CAST('20240230' AS DECIMAL(38,0)) UNION ALL -- Error case: invalid day
    SELECT CAST('00000000' AS DECIMAL(38,0)) UNION ALL -- Special case: all zeros
    SELECT CAST('-20240910' AS DECIMAL(38,0)) UNION ALL -- Error case: negative value
    SELECT CAST('2024091' AS DECIMAL(38,0)) UNION ALL -- Error case: one digit short
    SELECT CAST('202409100' AS DECIMAL(38,0)) UNION ALL -- Error case: one digit extra
    SELECT CAST('2024091@' AS DECIMAL(38,0)) UNION ALL -- Error case: special character
    SELECT CAST('2024年09月10日' AS DECIMAL(38,0)) UNION ALL -- Special characters: multi-byte
    SELECT CAST(' ' AS DECIMAL(38,0)) UNION ALL -- Error case: space only
    SELECT CAST('2024/09/10' AS DECIMAL(38,0)) UNION ALL -- Error case: slashes in date
    SELECT CAST('2024*09*10' AS DECIMAL(38,0)) UNION ALL -- Error case: asterisks in date
    SELECT CAST('2024\t09\t10' AS DECIMAL(38,0)) -- Error case: tabs in date
)

-- Insert test data into the f_order table
INSERT INTO purgo_databricks.purgo_playground.f_order (delivery_dt)
SELECT delivery_dt FROM test_data;
