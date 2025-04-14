from pyspark.sql import functions as F
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, MapType

# Define schema for purgo_playground.config_master table
schema = StructType([
    StructField("config_id", IntegerType()),
    StructField("src_objt_name", StringType()),
    StructField("src_sys", StringType()),
    StructField("f_format", StringType()),
    StructField("freq", StringType()),
    StructField("loc", StringType()),
    StructField("active_flag", StringType()),
    StructField("s3_landing_path", StringType()),
    StructField("s3_archive_path", StringType()),
    StructField("s3_src_path", StringType()),
    StructField("delta_load_ts", StringType()),
    StructField("full_or_incr_load", StringType()),
    StructField("zip_file", StringType()),
    StructField("country", StringType()),
    StructField("region", StringType()),
    StructField("affiliate_group", StringType()),
    StructField("affiliate", StringType()),
    StructField("column_condition", StringType()),
    StructField("dwh_path", StringType()),
    StructField("delimiter", StringType()),
    StructField("box_id", StringType()),
    StructField("len_file", StringType()),
    StructField("outbound_ind", StringType()),
    StructField("outbound_loc", StringType()),
    StructField("source_config_id", StringType()),
    StructField("exception_report_path", StringType()),
    StructField("src_layer", StringType()),
    StructField("quote_char", StringType()),
    StructField("col_list", StringType()),
    StructField("primary_key_col", StringType()),
    StructField("email", StringType()),
    StructField("expected_dt", StringType()),
    StructField("target_table", StringType()),
    StructField("target_src_sys", StringType()),
    StructField("dynamic_dt_file_loc", StringType()),
    StructField("dt_pattern", StringType()),
    StructField("latest_file_processed", StringType()),
    StructField("delta_stg_tables", StringType()),
    StructField("stg_skip_indicator", StringType()),
    StructField("delta_stg_table_view", StringType()),
    StructField("delta_pret1_table", StringType()),
    StructField("pre_t1_skip_indicator", StringType()),
    StructField("t2_force_exclude", StringType()),
    StructField("dq_rule_name", StringType()),
    StructField("source_path", StringType()),
    StructField("pre_process_function", StringType()),
    StructField("encode_val", StringType()),
    StructField("decode_val", StringType()),
    StructField("header", StringType()),
    StructField("inferschema", StringType()),
    StructField("actual_file_name", MapType(StringType(), StringType())),
    StructField("t1_layer_flag", StringType()),
    StructField("t2_layer_flag", StringType()),
    StructField("t3_layer_flag", StringType()),
    StructField("dag_id", StringType())
])

# Generate diverse test data records
data = [
    # Happy path test data
    (101, "US_Sales", "US", "US_YTD_Sales_", None, None, "Y",
     "s3a://us_bucket/landing/US/US_Sales/", "s3a://us_bucket/archive/US/US_Sales/", None,
     None, None, None, "US", "US", "Retail", "ppd", None, None, ",", None, None,
     "N", None, None, None, "US_Layer", "'", None, None, None, None, None, None, None,
     "us_stg_sales", None, None, None, None, None, None, "/SecureFtp/-InternalX/US/IN/DATA/Sales/",
     None, None, None, "Header", "True", {'US_YTD_Sales_*': 'stg_US_wholesaler'}, "Y", "N", "N",
     "LOAD_SALES_US"),
     
    # Edge case with special characters and multi-byte characters
    (102, "CA_Sales$", "CA", "CA#YTD_Sales@", None, None, "Y",
     "s3a://ca_bucket/landing/CA/CA_Sales$/", "s3a://ca_bucket/archive/CA/CA_Sales$/", None,
     None, None, None, "CA", "CA", "Retail$", "affiliate", None, None, "|", None, None,
     "Y", None, None, None, "CA_Layer", "\"", None, None, None, None, None, None, None,
     "ca_stg_sales", None, None, None, None, None, None, "/SecureFtp/-InternalX/CA/IN/DATA/Sales/",
     None, None, None, "Header%", "True", {'CA_YTD_Sales@*': 'stg_CA_wholesaler'}, "Y", "N", "N",
     "LOAD_SALES_CA"),
    
    # Error case with invalid path and out-of-range config_id
    (9999999999, "BE_Sales", "BE", "BE_YTD_Sales_", None, None, "N",
     "invalid_path", "another_invalid_path", None,
     None, None, None, "BE", "BE", "Marketing", "affiliate", None, None, "~", None, None,
     "Y", None, None, None, "BE_Layer", "\"", None, None, None, None, None, None, None,
     "be_stg_sales", None, None, None, None, None, None, None,
     None, None, None, None, "False", {'BE_YTD_Sales_*': 'stg_BE_wholesaler'}, "N", "Y", "N",
     "LOAD_SALES_BE"),
    
    # NULL handling scenario
    (103, None, None, None, None, None, None,
     None, None, None, None, None, None, None, None, None, None, None, None, None, None,
     None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
     None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 
     None),

    # Invalid data scenario
    (104, "NL_Sales", "NL", "NL_YTD_Sales_", None, None, "N",
     "s3a://nl_bucket/landing/NL/NL_Sales/", "s3a://nl_bucket/archive/NL/NL_Sales/", None,
     None, None, "\"", "NL", "NL", "Online", "affiliate", None, None, ",", None, None,
     "N", None, None, None, "NL_Layer", "'", None, None, None, None, None, None, None,
     "nl_stg_sales", None, None, None, None, None, None, "/SecureFtp/-InternalX/NL/IN/DATA/Sales/",
     None, None, None, "Header", "False", {'': ''}, "N", "Y", "N", "LOAD_SALES_NL")
]

# Create DataFrame using the schema
df = spark.createDataFrame(data, schema)

try:
    # Insert data into the {{config_master}} table in the purgo_playground Unity Catalog
    df.write.insertInto("purgo_playground.config_master", overwrite=False)
except Exception as e:
    print("Error occurred while inserting test data:", e)