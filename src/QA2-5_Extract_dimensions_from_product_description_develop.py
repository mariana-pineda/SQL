# Import necessary libraries
from pyspark.sql.functions import col, when, current_timestamp, regexp_extract, lit
from pyspark.sql.types import StructType, StructField, StringType, DoubleType

# Define the schema for the input data
schema = StructType([
    StructField("product_id", StringType(), True),
    StructField("product_description", StringType(), True),
    StructField("dimension_1", DoubleType(), True),
    StructField("dimension_2", DoubleType(), True),
    StructField("dimension_3", DoubleType(), True)
])

# Load the data from the CSV file into a DataFrame
df = spark.read.format("csv") \
    .option("header", "true") \
    .schema(schema) \
    .load("/path/to/product_desc (1) (1).csv")

# Extract product size from description or use product_id as fallback
df = df.withColumn("product_size", 
                   when(col("product_description").rlike(r"(\d+\.\d+-\d+\.\d+-\d+\.\d+)"), 
                        regexp_extract(col("product_description"), r"(\d+\.\d+-\d+\.\d+-\d+\.\d+)", 0))
                   .otherwise(regexp_extract(col("product_id"), r"(\d+\.\d+-\d+\.\d+-\d+\.\d+)", 0)))

# Add timestamp column
df = df.withColumn("timestamp", current_timestamp())

# Handle missing product size and log errors
df = df.withColumn("product_size", 
                   when(col("product_size") == "", lit(None).cast(StringType()))
                   .otherwise(col("product_size")))

# Log errors for missing product size
df.filter(col("product_size").isNull()).select("product_id").foreach(lambda row: print(f"Product size extraction failed for product ID: {row['product_id']}"))

# Write the DataFrame to a Delta table
df.write.format("delta") \
    .mode("overwrite") \
    .option("overwriteSchema", "true") \
    .saveAsTable("purgo_playground.d_product_revenue_bronze")

# Optimize the Delta table
spark.sql("OPTIMIZE purgo_playground.d_product_revenue_bronze ZORDER BY (product_size)")

# Vacuum the Delta table to remove old files
spark.sql("VACUUM purgo_playground.d_product_revenue_bronze RETAIN 0 HOURS")

# SQL code to create the Delta table with appropriate schema
spark.sql("""
CREATE TABLE IF NOT EXISTS purgo_playground.d_product_revenue_bronze (
    product_id STRING,
    product_description STRING,
    dimension_1 DOUBLE,
    dimension_2 DOUBLE,
    dimension_3 DOUBLE,
    product_size STRING,
    timestamp TIMESTAMP
)
USING DELTA
PARTITIONED BY (product_size)
TBLPROPERTIES (
    'delta.autoOptimize.optimizeWrite' = 'true',
    'delta.autoOptimize.autoCompact' = 'true'
)
""")
