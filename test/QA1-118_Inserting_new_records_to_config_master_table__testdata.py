from pyspark.sql.types import StructType, StructField, IntegerType, StringType, TimestampType

# Define schema for config_master table
schema = StructType([
    StructField("config_id", IntegerType(), False),
    StructField("src_objt_name", StringType(), True),
    StructField("src_sys", StringType(), True),
    StructField("f_format", StringType(), True),
    StructField("freq", StringType(), True),
    StructField("loc", StringType(), True),
    StructField("active_flag", StringType(), True),
    StructField("s3_landing_path", StringType(), True),
    StructField("s3_archive_path", StringType(), True),
    StructField("s3_src_path", StringType(), True),
    StructField("delta_load_ts", StringType(), True),
    StructField("full_or_incr_load", StringType(), True),
    StructField("zip_file", StringType(), True),
    StructField("country", StringType(), True),
    StructField("region", StringType(), True),
    StructField("affiliate_group", StringType(), True),
    StructField("affiliate", StringType(), True),
    StructField("column_condition", StringType(), True),
    StructField("dwh_path", StringType(), True),
    StructField("delimiter", StringType(), True),
    StructField("box_id", StringType(), True),
    StructField("len_file", StringType(), True),
    StructField("outbound_ind", StringType(), True),
    StructField("outbound_loc", StringType(), True),
    StructField("source_config_id", StringType(), True),
    StructField("exception_report_path", StringType(), True),
    StructField("src_layer", StringType(), True),
    StructField("quote_char", StringType(), True),
    StructField("col_list", StringType(), True),
    StructField("primary_key_col", StringType(), True),
    StructField("email", StringType(), True),
    StructField("expected_dt", StringType(), True),
    StructField("target_table", StringType(), True),
    StructField("target_src_sys", StringType(), True),
    StructField("dynamic_dt_file_loc", StringType(), True),
    StructField("dt_pattern", StringType(), True),
    StructField("latest_file_processed", StringType(), True),
    StructField("delta_stg_tables", StringType(), True),
    StructField("stg_skip_indicator", StringType(), True),
    StructField("delta_stg_table_view", StringType(), True),
    StructField("delta_pret1_table", StringType(), True),
    StructField("pre_t1_skip_indicator", StringType(), True),
    StructField("t2_force_exclude", StringType(), True),
    StructField("dq_rule_name", StringType(), True),
    StructField("source_path", StringType(), True),
    StructField("pre_process_function", StringType(), True),
    StructField("encode_val", StringType(), True),
    StructField("decode_val", StringType(), True),
    StructField("header", StringType(), True),
    StructField("inferschema", StringType(), True),
    StructField("actual_file_name", StringType(), True),
    StructField("t1_layer_flag", StringType(), True),
    StructField("t2_layer_flag", StringType(), True),
    StructField("t3_layer_flag", StringType(), True),
    StructField("dag_id", StringType(), True)
])

# Generate test data
test_data = [
    # Happy path: Valid record
    (1001, "ID_Sales", "ID_Sales", "ID_MON_Sales_", "Daily", "US", "Y",
     "s3a://my_bucket/landing/ID/ID_Sales/", "s3a://my_bucket/archive/ID/ID_Sales/",
     "/SecureFtp/-InternalX/ID/IN/DATA/Sales/", "2024-03-21T00:00:00.000+0000", "Full", "yes",
     "ID", "ID", "ID", "ID", "condition", "/dwh/path/", ",", "box123", "1000", "N", "US",
     "src_conf_1", "/exception/path/", "ID_Sales", "\"", "col1,col2", "id", "email@example.com",
     "2024-03-21", "target_table", "ID_Sales", "/dynamic/path/", "yyyy-MM-dd", "file1",
     "stg_ID_sales", "N", "view_stg", "delta_pret1", "N", "Y", "rule1",
     "/SecureFtp/-InternalX/ID/IN/DATA/Sales/", "function1", "enc", "dec",
     "header1", "true", "stg_ID_wholesaler", "N", "N", "N", "LOAD_SALES_ID"),

    # Edge case: Boundary config_id
    (2147483647, "ID_Sales", "ID_Sales", "ID_MON_Sales_", "Monthly", "EU", "Y",
     "s3a://max_bucket/landing/ID/ID_Sales/", "s3a://max_bucket/archive/ID/ID_Sales/",
     "/SecureFtp/-InternalX/ID/IN/DATA/Sales/", "2024-12-31T23:59:59.999+0000", "Incremental", "no",
     "ID_MAX", "ID", "ID", "ID", "condition_max", "/dwh/max_path/", ";", "box_max", "9999", "Y", "EU",
     "src_conf_max", "/exception/max_path/", "ID_Sales_Max", "'", "col_max1,col_max2", "id_max",
     "max_email@example.com", "2024-12-31", "target_table_max", "ID_Sales", "/dynamic/max/path/", "dd-MM-yyyy",
     "file_max", "stg_ID_sales_max", "Y", "view_stg_max", "delta_pret1_max", "Y", "Y", "rule_max",
     "/SecureFtp/-InternalX/ID/IN/DATA/Sales/", "function_max", "enc_max", "dec_max",
     "header_max", "false", "stg_ID_wholesaler_max", "Y", "Y", "Y", "LOAD_SALES_MAX"),

    # Error case: Duplicate dag_id
    (1002, "ID_Sales_Duplicate", "ID_Sales", "ID_MON_Sales_dup_", "Weekly", "CA", "Y",
     "s3a://duplicate_bucket/landing/ID/ID_Sales/", "s3a://duplicate_bucket/archive/ID/ID_Sales/",
     "/SecureFtp/-InternalX/ID/IN/DATA/Sales/", "2024-04-01T12:00:00.000+0000", "Partial", "yes",
     "ID_DUP", "ID", "ID", "ID", "condition_dup", "/dwh/dup_path/", "|", "box_dup", "500", "N", "CA",
     "src_conf_dup", "/exception/dup_path/", "ID_Sales", "`", "col_dup1,col_dup2", "id_dup",
     "dup_email@example.com", "2024-04-01", "target_table_dup", "ID_Sales", "/dynamic/dup/path/", "MM-dd-yyyy",
     "file_dup", "stg_ID_sales_dup", "N", "view_stg_dup", "delta_pret1_dup", "N", "Y", "rule_dup",
     "/SecureFtp/-InternalX/ID/IN/DATA/Sales/", "function_dup", "enc_dup", "dec_dup",
     "header_dup", "true", "stg_ID_wholesaler_dup", "N", "N", "N", "LOAD_SALES_ID"),

    # NULL handling: Some nullable fields are null
    (1003, "ID_Sales_NULL", "ID_Sales", "ID_MON_Sales_null_", "Hourly", "BE", "N",
     "s3a://null_bucket/landing/ID/ID_Sales/", "s3a://null_bucket/archive/ID/ID_Sales/",
     "/SecureFtp/-InternalX/ID/IN/DATA/Sales/", None, "Full", None,
     "ID_NULL", "ID", "ID", "ID", None, "/dwh/null_path/", None, "box_null", "0", "Y", "BE",
     "src_conf_null", None, "ID_Sales", None, None, "id_null",
     "null_email@example.com", None, "target_table_null", "ID_Sales", None, None,
     "file_null", "stg_ID_sales_null", None, "view_stg_null", "delta_pret1_null", None, "Y", "rule_null",
     "/SecureFtp/-InternalX/ID/IN/DATA/Sales/", None, None, None,
     None, "true", "stg_ID_wholesaler_null", None, None, None, "LOAD_SALES_NULL"),

    # Special characters: Multi-byte characters in string fields
    (1004, "ID_Sales_特殊字符", "ID_Sales", "ID_MON_Sales_🚀", "Yearly", "JP", "Y",
     "s3a://特殊_bucket/landing/ID/ID_Sales/", "s3a://特殊_bucket/archive/ID/ID_Sales/",
     "/SecureFtp/-InternalX/ID/IN/DATA/Sales/", "2024-05-15T08:30:00.000+0000", "Full", "yes",
     "ID_SPÉCIAL", "ID", "ID", "ID", "condition_特殊", "/dwh/特殊_path/", ",", "box_特殊", "1500", "N", "JP",
     "src_conf_特殊", "/exception/特殊_path/", "ID_Sales_特殊", "\"", "col_特殊1,col_特殊2", "id_特殊",
     "special_email@example.com", "2024-05-15", "target_table_特殊", "ID_Sales", "/dynamic/特殊/path/", "yyyy年MM月dd日",
     "file_特殊", "stg_ID_sales_特殊", "N", "view_stg_特殊", "delta_pret1_特殊", "N", "Y", "rule_特殊",
     "/SecureFtp/-InternalX/ID/IN/DATA/Sales/", "function_特殊", "enc_特殊", "dec_特殊",
     "header_特殊", "true", "stg_ID_wholesaler_特殊", "N", "N", "N", "LOAD_SALES_特殊"),

    # NULL handling: All nullable fields are null
    (1005, "ID_Sales_All_NULL", "ID_Sales", "ID_MON_Sales_all_null_", "Monthly", "AU", "N",
     "s3a://allnull_bucket/landing/ID/ID_Sales/", "s3a://allnull_bucket/archive/ID/ID_Sales/",
     "/SecureFtp/-InternalX/ID/IN/DATA/Sales/", None, "Incremental", None,
     "ID_ALL_NULL", "ID", "ID", "ID", None, "/dwh/allnull_path/", None, "box_all_null", "0", "Y", "AU",
     "src_conf_all_null", None, "ID_Sales", None, None, "id_all_null",
     "allnull_email@example.com", None, "target_table_all_null", "ID_Sales", None, None,
     "file_all_null", "stg_ID_sales_all_null", None, "view_stg_all_null", "delta_pret1_all_null", None, "Y", "rule_all_null",
     "/SecureFtp/-InternalX/ID/IN/DATA/Sales/", None, None, None,
     None, "true", "stg_ID_wholesaler_all_null", None, None, None, "LOAD_SALES_ALL_NULL"),

    # Error case: Invalid s3_landing_path format
    (1006, "ID_Sales_Invalid_S3", "ID_Sales", "ID_MON_Sales_invalid_s3_", "Daily", "FR", "Y",
     "invalid_path/landing/ID/ID_Sales/", "s3a://invalid_bucket/archive/ID/ID_Sales/",
     "/SecureFtp/-InternalX/ID/IN/DATA/Sales/", "2024-06-01T10:00:00.000+0000", "Full", "yes",
     "ID_INVALID_S3", "ID", "ID", "ID", "condition_invalid_s3", "/dwh/invalid_s3_path/", ",", "box_invalid_s3", "1000", "N", "FR",
     "src_conf_invalid_s3", "/exception/invalid_s3_path/", "ID_Sales_Invalid", "\"", "col_invalid1,col_invalid2", "id_invalid_s3",
     "invalid_s3_email@example.com", "2024-06-01", "target_table_invalid_s3", "ID_Sales", "/dynamic/invalid_s3/path/", "yyyy/MM/dd",
     "file_invalid_s3", "stg_ID_sales_invalid_s3", "N", "view_stg_invalid_s3", "delta_pret1_invalid_s3", "N", "Y", "rule_invalid_s3",
     "/SecureFtp/-InternalX/ID/IN/DATA/Sales/", "function_invalid_s3", "enc_invalid_s3", "dec_invalid_s3",
     "header_invalid_s3", "false", "stg_ID_wholesaler_invalid_s3", "N", "N", "N", "LOAD_SALES_INVALID_S3"),

    # Error case: Missing required fields
    (1007, "ID_Sales_Missing_Fields", "ID_Sales", "ID_MON_Sales_missing_fields_", "Weekly", "DE", "Y",
     "", "",  # Missing s3_landing_path and s3_archive_path
     "/SecureFtp/-InternalX/ID/IN/DATA/Sales/", "2024-07-20T14:00:00.000+0000", "Full", "yes",
     "ID_MISSING", "ID", "ID", "ID", "condition_missing", "/dwh/missing_path/", ",", "box_missing", "1000", "N", "DE",
     "src_conf_missing", "/exception/missing_path/", "ID_Sales_Missing", "\"", "col_missing1,col_missing2", "id_missing",
     "missing_email@example.com", "2024-07-20", "target_table_missing", "ID_Sales", "/dynamic/missing/path/", "dd-MM-yyyy",
     "file_missing", "stg_ID_sales_missing", "N", "view_stg_missing", "delta_pret1_missing", "N", "Y", "rule_missing",
     "/SecureFtp/-InternalX/ID/IN/DATA/Sales/", "function_missing", "enc_missing", "dec_missing",
     "header_missing", "true", "stg_ID_wholesaler_missing", "N", "N", "N", "LOAD_SALES_MISSING"),

    # Special characters: Including SQL injection-like strings
    (1008, "ID_Sales_SQL_Injection", "ID_Sales'; DROP TABLE config_master; --", "ID_MON_Sales_';--", "Daily", "IT", "Y",
     "s3a://sql_injection_bucket/landing/ID/ID_Sales/", "s3a://sql_injection_bucket/archive/ID/ID_Sales/",
     "/SecureFtp/-InternalX/ID/IN/DATA/Sales/", "2024-08-10T16:45:00.000+0000", "Full", "yes",
     "ID_SQL_INJ", "ID", "ID", "ID", "condition_sql_inj", "/dwh/sql_inj_path/", ",", "box_sql_inj", "1000", "N", "IT",
     "src_conf_sql_inj", "/exception/sql_inj_path/", "ID_Sales_SQL", "\"", "col_sql1,col_sql2", "id_sql_inj",
     "sql_inj_email@example.com", "2024-08-10", "target_table_sql_inj", "ID_Sales", "/dynamic/sql_inj/path/", "yyyy/MM/dd",
     "file_sql_inj", "stg_ID_sales_sql_inj", "N", "view_stg_sql_inj", "delta_pret1_sql_inj", "N", "Y", "rule_sql_inj",
     "/SecureFtp/-InternalX/ID/IN/DATA/Sales/", "function_sql_inj", "enc_sql_inj", "dec_sql_inj",
     "header_sql_inj", "false", "stg_ID_wholesaler_sql_inj", "N", "N", "N", "LOAD_SALES_SQL_INJ"),

    # Special characters: Emojis in string fields
    (1009, "ID_Sales_Emoji 😀", "ID_Sales", "ID_MON_Sales_🔥", "Daily", "KR", "Y",
     "s3a://emoji_bucket/landing/ID/ID_Sales/", "s3a://emoji_bucket/archive/ID/ID_Sales/",
     "/SecureFtp/-InternalX/ID/IN/DATA/Sales/", "2024-09-05T09:15:00.000+0000", "Full", "yes",
     "ID_EMOJI", "ID", "ID", "ID", "condition_emoji", "/dwh/emoji_path/", ",", "box_emoji", "1000", "N", "KR",
     "src_conf_emoji", "/exception/emoji_path/", "ID_Sales_Emoji", "\"", "col_emoji1,col_emoji2", "id_emoji",
     "emoji_email@example.com", "2024-09-05", "target_table_emoji", "ID_Sales", "/dynamic/emoji/path/", "MM/dd/yyyy",
     "file_emoji", "stg_ID_sales_emoji", "N", "view_stg_emoji", "delta_pret1_emoji", "N", "Y", "rule_emoji",
     "/SecureFtp/-InternalX/ID/IN/DATA/Sales/", "function_emoji", "enc_emoji", "dec_emoji",
     "header_emoji", "true", "stg_ID_wholesaler_emoji", "N", "N", "N", "LOAD_SALES_EMOJI"),

    # Additional records covering various scenarios
    # Happy path: Another valid record
    (1010, "ID_Sales_Other", "ID_Sales", "ID_MON_Sales_Other_", "Weekly", "UK", "Y",
     "s3a://other_bucket/landing/ID/ID_Sales/", "s3a://other_bucket/archive/ID/ID_Sales/",
     "/SecureFtp/-InternalX/ID/IN/DATA/Sales/", "2024-10-10T11:00:00.000+0000", "Incremental", "no",
     "ID_OTHER", "ID", "ID", "ID", "condition_other", "/dwh/other_path/", ",", "box_other", "2000", "Y", "UK",
     "src_conf_other", "/exception/other_path/", "ID_Sales_Other", "\"", "col_other1,col_other2", "id_other",
     "other_email@example.com", "2024-10-10", "target_table_other", "ID_Sales", "/dynamic/other/path/", "yyyy-MM-dd",
     "file_other", "stg_ID_sales_other", "Y", "view_stg_other", "delta_pret1_other", "Y", "Y", "rule_other",
     "/SecureFtp/-InternalX/ID/IN/DATA/Sales/", "function_other", "enc_other", "dec_other",
     "header_other", "true", "stg_ID_wholesaler_other", "Y", "Y", "Y", "LOAD_SALES_OTHER"),

    # Edge case: Minimum valid config_id
    (1, "ID_Sales_Min", "ID_Sales", "ID_MON_Sales_Min_", "Monthly", "SG", "Y",
     "s3a://min_bucket/landing/ID/ID_Sales/", "s3a://min_bucket/archive/ID/ID_Sales/",
     "/SecureFtp/-InternalX/ID/IN/DATA/Sales/", "2024-01-01T00:00:00.000+0000", "Full", "yes",
     "ID_MIN", "ID", "ID", "ID", "condition_min", "/dwh/min_path/", ",", "box_min", "100", "N", "SG",
     "src_conf_min", "/exception/min_path/", "ID_Sales_Min", "\"", "col_min1,col_min2", "id_min",
     "min_email@example.com", "2024-01-01", "target_table_min", "ID_Sales", "/dynamic/min/path/", "dd/MM/yyyy",
     "file_min", "stg_ID_sales_min", "N", "view_stg_min", "delta_pret1_min", "N", "Y", "rule_min",
     "/SecureFtp/-InternalX/ID/IN/DATA/Sales/", "function_min", "enc_min", "dec_min",
     "header_min", "false", "stg_ID_wholesaler_min", "N", "N", "N", "LOAD_SALES_MIN")
]

# Create DataFrame with test data
df = spark.createDataFrame(test_data, schema)

# Insert test data into config_master table with error handling
try:
    df.write.mode("append").saveAsTable("purgo_playground.config_master")
except Exception as e:
    # Handle missing or invalid data gracefully
    print(f"Error inserting test data: {e}")