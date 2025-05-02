from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when, lit
from pyspark.sql.types import StructType, StructField, StringType, BigIntType, DoubleType, DateType

# Create Spark session
spark = SparkSession.builder.appName("TestDataGeneration").getOrCreate()

# Define schema for `d_product_revenue_clone` table
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

# Generate test data
test_data = [
    (1001, "ProductA", "Type1", 5000, "USA", "C001", None, None, "1234234534", 0, 85, "DetailsA", None, "FirstProductA", 300.0),
    (1002, "ProductB", "Type2", 10000, "CAN", "C002", None, None, "9876543210", 1, 90, "DetailsB", None, "FirstProductB", 450.5),
    (1003, "ProductC", "Type3", 1500, "MEX", "C003", None, None, "1111222233", 0, 70, "DetailsC", None, "FirstProductC", 150.75),
    (1004, "ProductD", "Type1", 2500, "USA", "C004", None, None, None, 0, 95, "DetailsD", None, "FirstProductD", 200.25),
    (1005, "ProductE", "Type2", 3000, "CAN", "C005", None, None, "", 1, 88, "DetailsE", None, "FirstProductE", 500.5),
    # Add more test data as needed
]

# Create DataFrame using test data
df = spark.createDataFrame(test_data, schema)

# Masking logic for invoice_number
df_masked = df.withColumn(
    "invoice_number",
    when(
        (col("invoice_number").isNotNull()) & (col("invoice_number").rlike(r'^\d{10}$')),
        col("invoice_number").substr(1, 6).concat(lit('****'))
    ).otherwise(col("invoice_number"))
)

# Show the masked DataFrame for verification
df_masked.show()

# Handle null or empty invoice_number
df_null_handling = df_masked.withColumn(
    "invoice_number",
    when((col("invoice_number").isNull()) | (col("invoice_number") == ""), lit(None)).otherwise(col("invoice_number"))
)

# Output the final result to verify null handling and data integrity
df_null_handling.show()

# Stop the Spark session
spark.stop()