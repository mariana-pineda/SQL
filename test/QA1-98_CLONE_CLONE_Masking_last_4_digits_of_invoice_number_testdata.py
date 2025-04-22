from pyspark.sql import SparkSession
from pyspark.sql.functions import col, length, substring, concat, lit
from pyspark.sql.types import StringType

spark = SparkSession.builder.appName("MaskInvoiceNumber").getOrCreate()

try:
    # Drop the clone table if it exists
    spark.sql("""
        DROP TABLE IF EXISTS purgo_databricks.purgo_playground.d_product_revenue_clone
    """)

    # Clone the original table
    spark.sql("""
        CREATE TABLE purgo_databricks.purgo_playground.d_product_revenue_clone
        AS SELECT * FROM purgo_databricks.purgo_playground.d_product_revenue
    """)

    # Read the cloned table
    df = spark.table("purgo_databricks.purgo_playground.d_product_revenue_clone")

    # Mask the last four digits of invoice_number
    df_masked = df.withColumn(
        "invoice_number",
        concat(
            substring(col("invoice_number").cast(StringType()), 1, length(col("invoice_number").cast(StringType())) - 4),
            lit("****")
        )
    )

    # Handle invoice_number with fewer than four digits by replacing entire value with '****'
    df_masked = df_masked.withColumn(
        "invoice_number",
        when(length(col("invoice_number").cast(StringType())) >= 4, col("invoice_number"))
        .otherwise(lit("****"))
    )

    # Write the masked DataFrame back to the clone table
    df_masked.write.mode("overwrite").saveAsTable("purgo_databricks.purgo_playground.d_product_revenue_clone")

except Exception as e:
    # Handle any exceptions that occur during the process
    print(f"An error occurred: {e}")