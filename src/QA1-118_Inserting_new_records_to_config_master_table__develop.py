# /*
# PySpark Script to Insert a New Record into purgo_playground.config_master Table
# This script retrieves an existing record, updates specified columns with new values,
# assigns a new config_id, and appends the modified record to the config_master table.
# */

from pyspark.sql.functions import lit, max as spark_max

# /* 
# Define the ExistingConfigID and s3_bucket variables.
# Replace these values as needed.
# */
existing_config_id = 1001
s3_bucket = "my_bucket"

try:
    # /* 
    # Retrieve the existing record based on config_id
    # */
    existing_df = spark.table("purgo_playground.config_master").filter(f"config_id = {existing_config_id}")

    # /* 
    # Check if the existing record is found
    # */
    if existing_df.count() == 0:
        raise Exception(f"Record with config_id {existing_config_id} does not exist.")

    # /* 
    # Fetch the maximum config_id to generate a new unique config_id
    # */
    max_config_id = spark.table("purgo_playground.config_master").agg(spark_max("config_id").alias("max_id")).collect()[0]["max_id"]
    new_config_id = max_config_id + 1 if max_config_id else 1

    # /* 
    # Update the necessary columns with new values
    # */
    new_record_df = existing_df.withColumn("config_id", lit(new_config_id)) \
        .withColumn("src_objt_name", lit("ID_Sales")) \
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
        .withColumn("actual_file_name", lit("stg_ID_wholesaler")) \
        .withColumn("dag_id", lit("LOAD_SALES_ID"))

    # /* 
    # Ensure the number of columns matches the target table schema
    # */
    target_table_schema = spark.table("purgo_playground.config_master").schema
    new_record_schema = new_record_df.schema

    if len(target_table_schema.fields) != len(new_record_schema.fields):
        raise Exception("Column mismatch: The number of columns in the new record does not match the target table schema.")

    # /* 
    # Validate data types to ensure consistency
    # */
    for field in target_table_schema.fields:
        field_name = field.name
        field_type = field.dataType
        new_field_type = new_record_schema[field_name].dataType
        if type(field_type) != type(new_field_type):
            raise Exception(f"Data type mismatch for column '{field_name}': expected {field_type}, got {new_field_type}.")

    # /* 
    # Append the new record to the config_master table
    # */
    new_record_df.write.mode("append").saveAsTable("purgo_playground.config_master")

    # /* 
    # Log success message
    # */
    print(f"Successfully inserted new record with config_id {new_config_id} into purgo_playground.config_master.")

except Exception as e:
    # /* 
    # Handle any errors that occur during the insertion process
    # */
    print(f"Error inserting new record into purgo_playground.config_master: {e}")