from pyspark.sql import SparkSession
from pyspark.sql.functions import col, regexp_replace, length, trim
from pyspark.sql.types import StringType

# Initialize Spark session
spark = SparkSession.builder.getOrCreate()

try:
    # Drop the clone table if it exists
    spark.sql("DROP TABLE IF EXISTS purgo_playground.d_product_revenue_clone")
    
    # Clone the original table to the clone table
    spark.sql("""
        CREATE TABLE purgo_playground.d_product_revenue_clone AS
        SELECT * FROM purgo_playground.d_product_revenue
    """)
    
    # Read the clone table into DataFrame
    df = spark.table("purgo_playground.d_product_revenue_clone")
    
    # Cast 'invoice_number' to string for masking
    df = df.withColumn("invoice_number_str", col("invoice_number").cast(StringType()))
    
    # Validate that 'invoice_number' has at least four characters
    invalid_invoice = df.filter(length(trim(col("invoice_number_str"))) < 4)
    if invalid_invoice.count() > 0:
        raise ValueError("Invoice number must have at least four digits")
    
    # Validate that 'invoice_number' contains only numeric characters
    non_numeric_invoice = df.filter(~col("invoice_number_str").rlike("^\d+$"))
    if non_numeric_invoice.count() > 0:
        raise ValueError("Invalid invoice number format")
    
    # Mask the last four digits of 'invoice_number' with '****'
    df_masked = df.withColumn(
        "invoice_number",
        regexp_replace(col("invoice_number_str"), r".{4}$", "****")
    ).drop("invoice_number_str")
    
    # Overwrite the clone table with the masked DataFrame
    df_masked.write.mode("overwrite").saveAsTable("purgo_playground.d_product_revenue_clone")
    
except Exception as e:
    # Handle any errors that occur during the process
    print(f"An error occurred: {e}")