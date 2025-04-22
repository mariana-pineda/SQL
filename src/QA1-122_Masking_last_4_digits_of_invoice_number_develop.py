"""
Mask the last four digits of invoice_number in purgo_playground.d_product_revenue_clone
"""

from pyspark.sql.functions import col, length, when, regexp_replace

# Drop the clone table if it exists
try:
    spark.sql("""
        DROP TABLE IF EXISTS purgo_databricks.purgo_playground.d_product_revenue_clone
    """)
except Exception as e:
    # Log the error if table drop fails
    print(f"Error dropping table: {e}")

# Create a replica of the original table
try:
    spark.sql("""
        CREATE TABLE purgo_databricks.purgo_playground.d_product_revenue_clone
        AS SELECT * FROM purgo_databricks.purgo_playground.d_product_revenue
    """)
except Exception as e:
    # Log the error if table creation fails
    print(f"Error creating clone table: {e}")

# Read the clone table into a DataFrame
df = spark.table("purgo_databricks.purgo_playground.d_product_revenue_clone")

# Mask the last four digits of invoice_number
df_masked = df.withColumn(
    "invoice_number",
    when(
        col("invoice_number").isNull(),
        None
    ).when(
        length(col("invoice_number").cast("string")) < 4,
        # Assign null or handle as needed if invoice_number has fewer than four digits
        None
    ).otherwise(
        regexp_replace(col("invoice_number").cast("string"), r"(\d{4})$", "****")
    )
)

# Validate and convert data types before insertion
df_validated = df_masked.select(
    "product_id",
    "product_name",
    "product_type",
    "revenue",
    "country",
    "customer_id",
    "purchased_date",
    "invoice_date",
    "invoice_number",
    "is_returned",
    "customer_satisfaction_score",
    "product_details",
    "customer_first_purchased_date",
    "customer_first_product",
    "customer_first_revenue"
)

# Write the masked DataFrame back to the clone table
try:
    df_validated.write.mode("overwrite").saveAsTable("purgo_databricks.purgo_playground.d_product_revenue_clone")
except Exception as e:
    # Log the error if writing to table fails
    print(f"Error writing masked data to clone table: {e}")