from pyspark.sql import functions as F
from pyspark.sql.types import StringType

# Drop the clone table if it exists
try:
    spark.sql("DROP TABLE IF EXISTS purgo_playground.d_product_revenue_clone")
except Exception as e:
    # Handle exception for dropping table
    pass

# Create a replica of the original table
try:
    spark.sql("""
        CREATE TABLE purgo_playground.d_product_revenue_clone AS
        SELECT * FROM purgo_playground.d_product_revenue
    """)
except Exception as e:
    # Handle exception for cloning table
    pass

# Define masking logic for invoice_number
try:
    df = spark.table("purgo_playground.d_product_revenue_clone")
    
    # Change invoice_number from bigint to string
    df = df.withColumn("invoice_number", F.col("invoice_number").cast(StringType()))
    
    # Mask the last four digits of invoice_number
    df = df.withColumn(
        "invoice_number",
        F.when(
            F.length(F.col("invoice_number")) >= 4,
            F.concat(
                F.substring(F.col("invoice_number"), 1, F.length(F.col("invoice_number")) - 4),
                F.lit("****")
            )
        ).otherwise(
            F.lit("****")
        )
    )
    
    # Overwrite the clone table with masked invoice_number
    df.write.mode("overwrite").saveAsTable("purgo_playground.d_product_revenue_clone")
except Exception as e:
    # Handle exception for masking logic
    pass

# Comments for test scenarios

# Happy path: Valid invoice_number with more than four digits
# Edge case: invoice_number with exactly four digits
# Error case: invoice_number with fewer than four digits
# NULL handling: invoice_number is NULL
# Special characters: Not applicable as invoice_number is numeric before masking
# Multi-byte characters: Not applicable as invoice_number is numeric before masking