-- Generate test data for the target table f_invntry_bal_dly_hist
WITH test_data AS (
    SELECT
        -- Happy path scenarios: valid data
        'source_system_1' AS source_system_name,
        'source_table_1' AS source_table_name,
        'valid_col_1' AS column_name,
        'string' AS datatype,
        12 AS length,
        'target_table_1' AS target_table_name,
        'target_col_1' AS column_name_1,
        'string' AS datatype_1,
        'UPPER(valid_col_1)' AS logic,
        
    UNION ALL
   
    -- Edge cases: boundary conditions
    SELECT
        'source_system_2' AS source_system_name,
        'source_table_2' AS source_table_name,
        'edge_col_1' AS column_name,
        'bigint' AS datatype,
        9223372036854775807 AS length, -- Max value for BIGINT
        'target_table_2' AS target_table_name,
        'target_col_2' AS column_name_1,
        'bigint' AS datatype_1,
        'edge_col_1' AS logic,

    UNION ALL

    -- Error cases: invalid input scenarios
    SELECT
        'source_system_3' AS source_system_name,
        'source_table_3' AS source_table_name,
        'error_col_1' AS column_name,
        'decimal' AS datatype,
        38 AS length,
        'target_table_3' AS target_table_name,
        'target_col_3' AS column_name_1,
        'decimal' AS datatype_1,
        NULL AS logic, -- Invalid logic scenario

    UNION ALL

    -- NULL handling scenarios
    SELECT
        'source_system_4' AS source_system_name,
        'source_table_4' AS source_table_name,
        NULL AS column_name,
        'string' AS datatype,
        0 AS length,
        'target_table_4' AS target_table_name,
        'target_col_4' AS column_name_1,
        'string' AS datatype_1,
        NULL AS logic,

    UNION ALL

    -- Special characters and multi-byte characters
    SELECT
        'source_system_5' AS source_system_name,
        'source_table_5' AS source_table_name,
        'special_col_1' AS column_name,
        'string' AS datatype,
        255 AS length,
        'target_table_5' AS target_table_name,
        'target_col_5' AS column_name_1,
        'string' AS datatype_1,
        'CONCAT(special_col_1, "!#$%^&*()")' AS logic -- Special characters scenario
)

-- Validate data consistency and prevent type mismatches
SELECT
    CASE
        WHEN datatype != datatype_1 THEN 'Datatype mismatch error'
        ELSE 'Valid datatype'
    END AS datatype_consistency,
    CASE
        WHEN column_name IS NULL THEN 'Column missing error'
        ELSE 'Column exists'
    END AS column_existence,
    *
FROM test_data

