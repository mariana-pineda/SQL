from pyspark.sql.functions import lit
from pyspark.sql.types import StructType, StructField, StringType

# Define schema for the config_master table
schema = StructType([
    StructField("config_id", StringType(), True),
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

try:
    # Retrieve an existing record
    existing_record_df = spark.sql("""
        SELECT * FROM purgo_playground.config_master WHERE src_objt_name = "Sales"
        """).limit(1)

    # Prepare new data by replacing columns
    new_data_df = existing_record_df.withColumn("src_objt_name", lit("ID_Sales")) \
        .withColumn("src_sys", lit("ID_Sales")) \
        .withColumn("f_format", lit("ID_MON_Sales_")) \
        .withColumn("s3_landing_path", lit("s3a://{s3_bucket}/landing/ID/ID_Sales/")) \
        .withColumn("s3_archive_path", lit("s3a://{s3_bucket}/archive/ID/ID_Sales/")) \
        .withColumn("country", lit("ID")) \
        .withColumn("region", lit("ID")) \
        .withColumn("affiliate_group", lit("ID")) \
        .withColumn("affiliate", lit("ID")) \
        .withColumn("src_layer", lit("ID_Sales")) \
        .withColumn("target_src_sys", lit("ID_Sales")) \
        .withColumn("delta_stg_tables", lit("stg_ID_sales")) \
        .withColumn("source_path", lit("/SecureFtp/-InternalX/ID/IN/DATA/Sales/")) \
        .withColumn("actual_file_name", lit('{"ID_MON_Sales_*": "stg_ID_wholesaler"}')) \
        .withColumn("dag_id", lit("LOAD_SALES_ID"))

    # Append new data back to the config_master table
    new_data_df.write \
        .format("delta") \
        .mode("append") \
        .option("mergeSchema", "true") \
        .saveAsTable("purgo_playground.config_master")

except Exception as e:
    print("An error occurred while processing the data: ", str(e))