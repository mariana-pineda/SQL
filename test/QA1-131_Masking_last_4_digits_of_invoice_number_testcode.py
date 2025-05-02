from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when, lit, expr
from pyspark.sql.types import StructType, StructField, StringType, BigIntType, DoubleType, DateType

# Setup Spark Session
# Assuming Spark session 'spark' is already available in the Databricks environment
# spark = SparkSession.builder.appName("MaskingInvoiceNumber").getOrCreate()

# Define schema for the table purgo_playground.d_product_revenue_clone
schema = StructType([
    StructField("product_id", BigIntType(), True),
    StructField("product_name", StringType(), True),
    StructField("product_type", StringType(), True),
    StructField("revenue", BigIntType(), True),
    StructField("country", StringType(), True),
    StructField("customer_id", StringType(), True),
    StructField("purchased_date", DateType(), True),
    StructField("invoice_date", DateType(), True),
    StructField("invoice_number", StringType(), True),
    StructField("is_returned", BigIntType(), True),
    StructField("customer_satisfaction_score", BigIntType(), True),
    StructField("product_details", StringType(), True),
    StructField("customer_first_purchased_date", DateType(), True),
    StructField("customer_first_product", StringType(), True),
    StructField("customer_first_revenue", DoubleType(), True)
])

# Load table into DataFrame
try:
    df = spark.table("purgo_playground.d_product_revenue_clone")
except Exception as e:
    # Log error if table loading fails
    print(f"Error loading table purgo_playground.d_product_revenue_clone: {e}")
    df = None

if df:
    # Masking logic for invoice_number
    df_masked = df.withColumn(
        "invoice_number",
        when(
            (col("invoice_number").isNotNull()) & (col("invoice_number").rlike(r'^\d{10}$')),
            expr("concat(substr(invoice_number, 1, 6), '****')")
        ).otherwise(col("invoice_number"))
    )

    # Handle null or empty invoice_number cases
    df_null_handling = df_masked.withColumn(
        "invoice_number",
        when((col("invoice_number").isNull()) | (col("invoice_number") == ""), lit(None)).otherwise(col("invoice_number"))
    )

    # Ensure that schema remains consistent with the target table before writing back
    assert len(df_null_handling.columns) == len(schema.fields), "Column count mismatch!"

    # Write transformed data back to the clone table
    try:
        df_null_handling.write.format("delta").mode("overwrite").saveAsTable("purgo_playground.d_product_revenue_clone")
    except Exception as e:
        print(f"Error writing masked data to clone table: {e}")

    # Stop Spark session if started locally
    # spark.stop()

