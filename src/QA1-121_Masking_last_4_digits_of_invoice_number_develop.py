# /*
# PySpark script to mask the last four digits of invoice_number in purgo_playground.d_product_revenue_clone table
# */

# /* Import necessary functions */
from pyspark.sql.functions import col, when, length, concat, substring, lit

# /* Step 1: Drop the clone table if it exists */
try:
    spark.sql("""
        DROP TABLE IF EXISTS purgo_databricks.purgo_playground.d_product_revenue_clone
    """)
except Exception as e:
    # /* Handle errors during table drop */
    print(f"Error dropping clone table: {e}")

# /* Step 2: Create a replica of the original table */
try:
    original_df = spark.table("purgo_databricks.purgo_playground.d_product_revenue")
    original_df.write.mode("overwrite").format("delta").saveAsTable("purgo_databricks.purgo_playground.d_product_revenue_clone")
except Exception as e:
    # /* Handle errors during table cloning */
    print(f"Error creating clone table: {e}")

# /* Step 3: Read the clone table and apply masking */
try:
    clone_df = spark.table("purgo_databricks.purgo_playground.d_product_revenue_clone")
    
    # /* Apply masking to the invoice_number column */
    masked_df = clone_df.withColumn(
        "invoice_number",
        when(
            col("invoice_number").isNull(),
            None
        ).when(
            length(col("invoice_number").cast("string")) < 4,
            lit("****")
        ).otherwise(
            concat(substring(col("invoice_number").cast("string"), 1, length(col("invoice_number").cast("string")) - 4), lit("****"))
        )
    )
    
    # /* Validate column count matches before writing */
    if len(masked_df.columns) != len(clone_df.columns):
        raise ValueError("Column count mismatch after masking")
    
    # /* Write the masked data back to the clone table */
    masked_df.write.mode("overwrite").format("delta").saveAsTable("purgo_databricks.purgo_playground.d_product_revenue_clone")
except Exception as e:
    # /* Handle errors during masking and writing */
    print(f"Error during masking process: {e}")