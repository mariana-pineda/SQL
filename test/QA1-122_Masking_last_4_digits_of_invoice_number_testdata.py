from pyspark.sql.functions import col, when, length, regexp_replace
from pyspark.sql.types import StringType

# Drop the clone table if it exists
spark.sql("""
    DROP TABLE IF EXISTS purgo_databricks.purgo_playground.d_product_revenue_clone
""")

# Create a replica of the original table
spark.sql("""
    CREATE TABLE purgo_databricks.purgo_playground.d_product_revenue_clone
    AS SELECT * FROM purgo_databricks.purgo_playground.d_product_revenue
""")

try:
    # Read the clone table into a DataFrame
    df = spark.table("purgo_databricks.purgo_playground.d_product_revenue_clone")
    
    # Mask the last 4 digits of invoice_number
    df_masked = df.withColumn(
        "invoice_number",
        when(
            col("invoice_number").isNull(),
            # Handle NULL invoice_number
            raise_error("Invoice number cannot be null")
        ).when(
            length(col("invoice_number").cast(StringType())) < 4,
            # Handle invoice_number with fewer than four digits
            raise_error("Invoice number must have at least four digits")
        ).otherwise(
            # Mask the last four digits
            regexp_replace(col("invoice_number").cast(StringType()), r"(\d{"+str(col("invoice_number").cast(StringType()).substr(-4,4))+"})$", "****")
        )
    )
    
    # Write the masked DataFrame back to the clone table
    df_masked.write.mode("overwrite").saveAsTable("purgo_databricks.purgo_playground.d_product_revenue_clone")

except Exception as e:
    # Gracefully handle any errors during the masking process
    print(f"An error occurred during the masking process: {e}")