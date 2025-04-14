from pyspark.sql.functions import col, lit, expr

# Define the schema for the config_master table
schema = [
    ("config_id", "int"),
    ("src_objt_name", "string"),
    ("src_sys", "string"),
    ("f_format", "string"),
    ("freq", "string"),
    ("loc", "string"),
    ("active_flag", "string"),
    ("s3_landing_path", "string"),
    ("s3_archive_path", "string"),
    ("s3_src_path", "string"),
    ("delta_load_ts", "string"),
    ("full_or_incr_load", "string"),
    ("zip_file", "string"),
    ("country", "string"),
    ("region", "string"),
    ("affiliate_group", "string"),
    ("affiliate", "string"),
    ("column_condition", "string"),
    ("dwh_path", "string"),
    ("delimiter", "string"),
    ("box_id", "string"),
    ("len_file", "string"),
    ("outbound_ind", "string"),
    ("outbound_loc", "string"),
    ("source_config_id", "string"),
    ("exception_report_path", "string"),
    ("src_layer", "string"),
    ("quote_char", "string"),
    ("col_list", "string"),
    ("primary_key_col", "string"),
    ("email", "string"),
    ("expected_dt", "string"),
    ("target_table", "string"),
    ("target_src_sys", "string"),
    ("dynamic_dt_file_loc", "string"),
    ("dt_pattern", "string"),
    ("latest_file_processed", "string"),
    ("delta_stg_tables", "string"),
    ("stg_skip_indicator", "string"),
    ("delta_stg_table_view", "string"),
    ("delta_pret1_table", "string"),
    ("pre_t1_skip_indicator", "string"),
    ("t2_force_exclude", "string"),
    ("dq_rule_name", "string"),
    ("source_path", "string"),
    ("pre_process_function", "string"),
    ("encode_val", "string"),
    ("decode_val", "string"),
    ("header", "string"),
    ("inferschema", "string"),
    ("actual_file_name", "string"),
    ("t1_layer_flag", "string"),
    ("t2_layer_flag", "string"),
    ("t3_layer_flag", "string"),
    ("dag_id", "string")
]

# Prepare test data
test_data = [
    # Happy path test data
    (101, "ID_Sales", "ID_Sales", "ID_MON_Sales_", "Daily", "US", "Y", "s3a://my_bucket/landing/ID/ID_Sales/",
     "s3a://my_bucket/archive/ID/ID_Sales/", "/path_src", "2024-03-21T00:00:00.000+0000", "Incr", "No", "ID", "ID",
     "ID", "ID", "", "dwh/path", "|", "", "", "", "", "", "", "ID_Sales", "", "", "", "", "", "", "", "", "", "",
     "stg_ID_sales", "", "", "", "", "", "/SecureFtp/-InternalX/ID/IN/DATA/Sales/", "", "", "", "", "", "", "", "",
     "", '{"ID_MON_Sales_*": "stg_ID_wholesaler"}', "", "", "", "LOAD_SALES_ID"),

    # Edge case test data
    (102, "", "", "", "Daily", "", "", "", "", "", "2024-03-21", "", "", "", "", "", "", "", "", "", "", "", "", "",
     "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""),

    # Error case test data
    (103, "OutOfRange", "InvalidSys", "ID_MON_Sales_", "Weekly", "", "N", "invalid_path", "invalid_archive", "", "timestamp",
     "LoadType", "Yes", "Wrong", "Wrong", "Wrong", "Wrong", "", "wrong/path", "", "", "", "", "", "", "", "wrong_src_layer", "", "", "", "", "", "",
     "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""),

    # NULL handling scenarios
    (104, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
     None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
     None, None, None, None, None),

    # Special characters and multi-byte characters
    (105, "Special!@#$", "Multi✓", "ID_MON_Säles_", "", "", "", "s3a://special_path/", "s3a://special_archive/",
     "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "spécial", "", "", "", "", "", "", "",
     "", "", "", "", "", "", "", "", "", "", "", "", "", "speçial_path", "", "", "", "", "", "", "", "", '{special: "value"}', "", "", "", "SPECIAL_DAG")
]

# Convert to DataFrame
config_df = spark.createDataFrame(test_data, schema=[f[0] for f in schema])

# Insert the new record into the config_master table
try:
    config_df.write.insertInto("purgo_playground.config_master", overwrite=False)
except Exception as e:
    print("Error during data insertion: ", str(e))

# Validating column count and data types (just for reference)
validation_query = """
WITH Record_Validation AS (
    SELECT *
    FROM purgo_playground.config_master
    WHERE config_id BETWEEN 101 AND 105
)

SELECT * FROM Record_Validation
"""