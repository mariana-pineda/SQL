from pyspark.sql.functions import lit
from pyspark.sql import DataFrame

# Define the function to insert a new record into the config_master table
def insert_new_region_record(spark, s3_bucket):
    try:
        # Retrieve an existing template record from the config_master table
        existing_record_df: DataFrame = spark.sql("""
            SELECT * FROM purgo_playground.config_master WHERE src_objt_name = "Sales"
            LIMIT 1
        """)
        
        # Generate new data by replacing specific columns with new values
        new_data_df = existing_record_df.withColumn("src_objt_name", lit("ID_Sales")) \
            .withColumn("src_sys", lit("ID_Sales")) \
            .withColumn("f_format", lit("ID_MON_Sales_")) \
            .withColumn("s3_landing_path", lit(f"s3a://{s3_bucket}/landing/ID/ID_Sales/")) \
            .withColumn("s3_archive_path", lit(f"s3a://{s3_bucket}/archive/ID/ID_Sales/")) \
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

        # Append the new data back to the config_master table
        new_data_df.write \
            .format("delta") \
            .mode("append") \
            .option("mergeSchema", "true") \
            .saveAsTable("purgo_playground.config_master")

    except Exception as e:
        # Handle exceptions gracefully and log the error
        print("An error occurred while processing the data: ", str(e))

# Example call to the function with the dynamic s3_bucket value replaced as required
# insert_new_region_record(spark, "your_s3_bucket")