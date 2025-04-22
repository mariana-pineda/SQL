# """
# PySpark Script to Mask the Last 4 Digits of Invoice Number in purgo_playground.d_product_revenue_clone
# 
# Steps:
# 1. Drop the clone table if it exists.
# 2. Clone the original d_product_revenue table to d_product_revenue_clone.
# 3. Mask the last 4 digits of invoice_number with '*' in the clone table.
# """

from pyspark.sql.functions import col, when, concat, lit, substring, length

# /* Drop the clone table if it exists */
try:
    spark.sql("""
        DROP TABLE IF EXISTS purgo_databricks.purgo_playground.d_product_revenue_clone
    """)
except Exception as e:
    # Handle exception during drop operation
    raise RuntimeError(f"Failed to drop clone table: {e}")

# /* Clone the original d_product_revenue table */
try:
    spark.sql("""
        CREATE TABLE purgo_databricks.purgo_playground.d_product_revenue_clone
        AS SELECT * FROM purgo_databricks.purgo_playground.d_product_revenue
    """)
except Exception as e:
    # Handle exception during cloning
    raise RuntimeError(f"Failed to clone table: {e}")

# /* Read the cloned table into a DataFrame */
try:
    df_clone = spark.table("purgo_databricks.purgo_playground.d_product_revenue_clone")
except Exception as e:
    # Handle exception during table read
    raise RuntimeError(f"Failed to read clone table: {e}")

# /* Mask the last 4 digits of invoice_number */
try:
    df_masked = df_clone.withColumn(
        "invoice_number",
        when(
            (col("invoice_number").isNotNull()) & (length(col("invoice_number").cast("string")) > 4),
            concat(
                substring(col("invoice_number").cast("string"), 1, length(col("invoice_number").cast("string")) - 4),
                lit("****")
            )
        ).otherwise(col("invoice_number").cast("string"))
    )
except Exception as e:
    # Handle exception during masking
    raise RuntimeError(f"Failed to mask invoice_number: {e}")

# /* Validate the number of columns matches the original schema */
try:
    original_df = spark.table("purgo_databricks.purgo_playground.d_product_revenue")
    if len(df_masked.columns) != len(original_df.columns):
        raise ValueError("Column count mismatch after masking.")
except Exception as e:
    # Handle exception during validation
    raise RuntimeError(f"Schema validation failed: {e}")

# /* Overwrite the clone table with the masked DataFrame */
try:
    df_masked.write.mode("overwrite").saveAsTable("purgo_databricks.purgo_playground.d_product_revenue_clone")
except Exception as e:
    # Handle exception during write operation
    raise RuntimeError(f"Failed to write masked data to clone table: {e}")

# /* End of masking process */