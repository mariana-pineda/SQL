from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when, current_timestamp
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, TimestampType

# Initialize Spark session
spark = SparkSession.builder \
    .appName("Test Data Generation") \
    .getOrCreate()

# Define schema for the input data
schema = StructType([
    StructField("product_id", StringType(), True),
    StructField("product_description", StringType(), True),
    StructField("dimension_1", DoubleType(), True),
    StructField("dimension_2", DoubleType(), True),
    StructField("dimension_3", DoubleType(), True)
])

# Sample data
data = [
    # Happy path test data
    ("YRDMT-6061-T6511-TB-3.7500-.3750-23.7000", "ALUM EXTRUDED ROUND TUBE - BAR - 1-Aluminum Bar - 6061-T6511-TB - 6061-T6511-TB-3.7500-.3750-23.7000", 3.75, 3.0, 0.375),
    # Edge case: Minimum dimension values
    ("YRDMT-6061-T6511-TB-0.0001-0.0001-0.0001", "ALUM EXTRUDED ROUND TUBE - BAR - 1-Aluminum Bar - 6061-T6511-TB - 6061-T6511-TB-0.0001-0.0001-0.0001", 0.0001, 0.0001, 0.0001),
    # Error case: Invalid dimension values
    ("YRDMT-6061-T6511-TB--1.0000--1.0000--1.0000", "ALUM EXTRUDED ROUND TUBE - BAR - 1-Aluminum Bar - 6061-T6511-TB - 6061-T6511-TB--1.0000--1.0000--1.0000", -1.0, -1.0, -1.0),
    # NULL handling scenario
    ("YRDMT-6061-T6511-TB-NULL-NULL-NULL", "ALUM EXTRUDED ROUND TUBE - BAR - 1-Aluminum Bar - 6061-T6511-TB - 6061-T6511-TB-NULL-NULL-NULL", None, None, None),
    # Special characters and multi-byte characters
    ("YRDMT-6061-T6511-TB-3.7500-3.7500-3.7500", "ALUM EXTRUDED ROUND TUBE - BAR - 1-Aluminum Bar - 6061-T6511-TB - 6061-T6511-TB-3.7500-3.7500-3.7500-特殊字符", 3.75, 3.75, 3.75)
]

# Create DataFrame
df = spark.createDataFrame(data, schema)

# Extract product size from description or use product_id as fallback
df = df.withColumn("product_size", 
                   when(col("product_description").rlike(r"(\d+\.\d+-\d+\.\d+-\d+\.\d+)"), 
                        col("product_description").substr(col("product_description").rlike(r"(\d+\.\d+-\d+\.\d+-\d+\.\d+)"), 0, 100))
                   .otherwise(col("product_id").substr(col("product_id").rlike(r"(\d+\.\d+-\d+\.\d+-\d+\.\d+)"), 0, 100)))

# Add timestamp column
df = df.withColumn("timestamp", current_timestamp())

# Show the DataFrame
df.show(truncate=False)

