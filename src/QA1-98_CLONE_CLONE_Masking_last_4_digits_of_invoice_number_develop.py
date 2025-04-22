# /*
# PySpark Script to Mask the Last Four Digits of invoice_number in d_product_revenue_clone Table
# This script performs the following operations:
# 1. Drops the clone table if it exists.
# 2. Clones the original d_product_revenue table to d_product_revenue_clone.
# 3. Applies masking to the last four digits of the invoice_number column.
# 4. Validates schema consistency and handles errors gracefully.
# */

from pyspark.sql.functions import col, when, length, substring, concat, lit

try:
    # /* 
    # Drop the clone table if it exists 
    # */
    spark.sql("""
        DROP TABLE IF EXISTS purgo_databricks.purgo_playground.d_product_revenue_clone
    """)
except Exception as e:
    # /* 
    # Log error if dropping the table fails 
    # */
    raise Exception(f"Failed to drop clone table: {e}")

try:
    # /* 
    # Clone the original d_product_revenue table to d_product_revenue_clone 
    # */
    spark.sql("""
        CREATE TABLE purgo_databricks.purgo_playground.d_product_revenue_clone
        AS SELECT * FROM purgo_databricks.purgo_playground.d_product_revenue
    """)
except Exception as e:
    # /* 
    # Log error if cloning the table fails 
    # */
    raise Exception(f"Failed to clone table: {e}")

try:
    # /* 
    # Read the cloned table into a DataFrame 
    # */
    df_clone = spark.table("purgo_databricks.purgo_playground.d_product_revenue_clone")
except Exception as e:
    # /* 
    # Log error if reading the clone table fails 
    # */
    raise Exception(f"Failed to read clone table: {e}")

try:
    # /*
    # Apply masking to the last four digits of invoice_number
    # Replace last four digits with '****' if invoice_number has at least four digits
    # Otherwise, replace the entire invoice_number with '****'
    # */
    df_masked = df_clone.withColumn(
        "invoice_number",
        when(
            length(col("invoice_number").cast("string")) >= 4,
            concat(
                substring(col("invoice_number").cast("string"), 1, length(col("invoice_number").cast("string")) - 4),
                lit("****")
            )
        ).otherwise(lit("****"))
    )
except Exception as e:
    # /* 
    # Log error if masking fails 
    # */
    raise Exception(f"Failed to apply masking to invoice_number: {e}")

try:
    # /*
    # Validate that the number of columns matches the target table's schema
    # */
    original_schema = spark.table("purgo_databricks.purgo_playground.d_product_revenue_clone").schema
    masked_schema = df_masked.schema
    if len(original_schema) != len(masked_schema):
        raise Exception("Column count mismatch after masking")
    
    for orig_field, masked_field in zip(original_schema, masked_schema):
        if orig_field.name != masked_field.name or orig_field.dataType != masked_field.dataType:
            raise Exception(f"Schema mismatch on column {orig_field.name}")
except Exception as e:
    # /* 
    # Log error if schema validation fails 
    # */
    raise Exception(f"Schema validation failed: {e}")

try:
    # /* 
    # Overwrite the clone table with the masked DataFrame 
    # */
    df_masked.write.mode("overwrite").saveAsTable("purgo_databricks.purgo_playground.d_product_revenue_clone")
except Exception as e:
    # /* 
    # Log error if writing the masked DataFrame fails 
    # */
    raise Exception(f"Failed to write masked data to clone table: {e}")