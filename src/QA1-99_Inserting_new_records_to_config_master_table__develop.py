from pyspark.sql import functions as F
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, MapType, TimestampType

# Define schema for purgo_playground.config_master table
schema = StructType([
    StructField("config_id", IntegerType(), nullable=False),
    StructField("src_objt_name", StringType(), nullable=False),
    StructField("src_sys", StringType(), nullable=False),
    StructField("f_format", StringType(), nullable=False),
    StructField("freq", StringType()),
    StructField("loc", StringType()),
    StructField("active_flag", StringType()),
    StructField("s3_landing_path", StringType(), nullable=False),
    StructField("s3_archive_path", StringType(), nullable=False),
    StructField("s3_src_path", StringType()),
    StructField("delta_load_ts", TimestampType()),
    StructField("full_or_incr_load", StringType()),
    StructField("zip_file", StringType()),
    StructField("country", StringType(), nullable=False),
    StructField("region", StringType(), nullable=False),
    StructField("affiliate_group", StringType(), nullable=False),
    StructField("affiliate", StringType(), nullable=False),
    StructField("column_condition", StringType()),
    StructField("dwh_path", StringType()),
    StructField("delimiter", StringType()),
    StructField("box_id", StringType()),
    StructField("len_file", StringType()),
    StructField("outbound_ind", StringType()),
    StructField("outbound_loc", StringType()),
    StructField("source_config_id", StringType()),
    StructField("exception_report_path", StringType()),
    StructField("src_layer", StringType(), nullable=False),
    StructField("quote_char", StringType()),
    StructField("col_list", StringType()),
    StructField("primary_key_col", StringType()),
    StructField("email", StringType()),
    StructField("expected_dt", StringType()),
    StructField("target_table", StringType()),
    StructField("target_src_sys", StringType(), nullable=False),
    StructField("dynamic_dt_file_loc", StringType()),
    StructField("dt_pattern", StringType()),
    StructField("latest_file_processed", StringType()),
    StructField("delta_stg_tables", StringType(), nullable=False),
    StructField("stg_skip_indicator", StringType()),
    StructField("delta_stg_table_view", StringType()),
    StructField("delta_pret1_table", StringType()),
    StructField("pre_t1_skip_indicator", StringType()),
    StructField("t2_force_exclude", StringType()),
    StructField("dq_rule_name", StringType()),
    StructField("source_path", StringType(), nullable=False),
    StructField("pre_process_function", StringType()),
    StructField("encode_val", StringType()),
    StructField("decode_val", StringType()),
    StructField("header", StringType()),
    StructField("inferschema", StringType()),
    StructField("actual_file_name", MapType(StringType(), StringType())),
    StructField("t1_layer_flag", StringType()),
    StructField("t2_layer_flag", StringType()),
    StructField("t3_layer_flag", StringType()),
    StructField("dag_id", StringType(), nullable=False)
])

# Setup values to modify existing records for the new ID region
specified_values = {
    "src_objt_name": "ID_Sales",
    "src_sys": "ID_Sales",
    "f_format": "ID_MON_Sales_",
    "s3_landing_path": "s3a://{s3_bucket}/landing/ID/ID_Sales/",
    "s3_archive_path": "s3a://{s3_bucket}/archive/ID/ID_Sales/",
    "country": "ID",
    "region": "ID",
    "affiliate_group": "ID",
    "affiliate": "ID",
    "src_layer": "ID_Sales",
    "target_src_sys": "ID_Sales",
    "delta_stg_tables": "stg_ID_sales",
    "source_path": "/SecureFtp/-InternalX/ID/IN/DATA/Sales/",
    "actual_file_name": {"ID_MON_Sales_*": "stg_ID_wholesaler"},
    "dag_id": "LOAD_SALES_ID"
}

# Retrieve existing record for modification
config_master_df = spark.table("purgo_playground.config_master")
existing_record = config_master_df.filter(F.col("config_id") == 101).first()

if existing_record is None:
    # Log issue if no existing record is found
    print("Existing record not found for config_id 101.")
else:
    # Create new record with modified values
    new_record = {
        **{field.name: existing_record[field.name] for field in schema if field.name not in specified_values},
        **specified_values
    }

    try:
        # Convert dictionary to DataFrame
        new_df = spark.createDataFrame([new_record], schema)

        # Validate schema compatibility before inserting
        assert len(new_df.columns) == len(schema), "Schema column count mismatch"

        # Perform insertion
        new_df.write.mode("append").insertInto("purgo_playground.config_master", overwrite=False)
    except Exception as e:
        # Log any errors during insertion
        print("Error occurred while inserting new record:", e)