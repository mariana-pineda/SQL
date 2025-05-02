from pyspark.sql import SparkSession
from pyspark.sql.functions import expr, col
from pyspark.sql.types import StructType, StructField, StringType, DateType, DoubleType, BigIntType

# Initialize Spark session
spark = SparkSession.builder \
    .appName("MaskInvoiceNumbers") \
    .getOrCreate()

# Define schema for the table
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

# Drop the table purgo_playground.d_product_revenue_clone if it exists
spark.sql("DROP TABLE IF EXISTS purgo_playground.d_product_revenue_clone")

# Create a replica of purgo_playground.d_product_revenue
spark.sql("CREATE TABLE purgo_playground.d_product_revenue_clone AS SELECT * FROM purgo_playground.d_product_revenue")

# Read data from purgo_playground.d_product_revenue_clone
df = spark.table("purgo_playground.d_product_revenue_clone")

# Mask the last 4 digits of the invoice_number with '****'
masked_df = df.withColumn("invoice_number", expr("concat(substring(invoice_number, 1, length(invoice_number)-4), '****')"))

# Handle invalid invoice number cases (too short, incorrect format)
def validate_invoice_number(df):
    return df.withColumn('valid_format', expr("length(invoice_number) >= 10"))

masked_df = validate_invoice_number(masked_df)
invalid_invoice_df = masked_df.filter(col('valid_format') == False)

# Display error message for invalid numbers
invalid_invoice_df.select("invoice_number").show(truncate=False)

# Show valid data
valid_invoice_df = masked_df.filter(col('valid_format') == True)
valid_invoice_df = valid_invoice_df.drop('valid_format')

# Write back the masked data to the clone table
valid_invoice_df.write.mode("overwrite").saveAsTable("purgo_playground.d_product_revenue_clone")

# Display the masked data
valid_invoice_df.show(truncate=False)

