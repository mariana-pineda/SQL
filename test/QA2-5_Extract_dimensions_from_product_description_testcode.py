# Import necessary libraries
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when, current_timestamp, regexp_extract
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, TimestampType
import unittest

# Initialize Spark session
spark = SparkSession.builder \
    .appName("Databricks Test Suite") \
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
    ("YRDMT-6061-T6511-TB-3.7500-.3750-23.7000", "ALUM EXTRUDED ROUND TUBE - BAR - 1-Aluminum Bar - 6061-T6511-TB - 6061-T6511-TB-3.7500-.3750-23.7000", 3.75, 3.0, 0.375),
    ("YRDMT-6061-T6511-TB-0.0001-0.0001-0.0001", "ALUM EXTRUDED ROUND TUBE - BAR - 1-Aluminum Bar - 6061-T6511-TB - 6061-T6511-TB-0.0001-0.0001-0.0001", 0.0001, 0.0001, 0.0001),
    ("YRDMT-6061-T6511-TB--1.0000--1.0000--1.0000", "ALUM EXTRUDED ROUND TUBE - BAR - 1-Aluminum Bar - 6061-T6511-TB - 6061-T6511-TB--1.0000--1.0000--1.0000", -1.0, -1.0, -1.0),
    ("YRDMT-6061-T6511-TB-NULL-NULL-NULL", "ALUM EXTRUDED ROUND TUBE - BAR - 1-Aluminum Bar - 6061-T6511-TB - 6061-T6511-TB-NULL-NULL-NULL", None, None, None),
    ("YRDMT-6061-T6511-TB-3.7500-3.7500-3.7500", "ALUM EXTRUDED ROUND TUBE - BAR - 1-Aluminum Bar - 6061-T6511-TB - 6061-T6511-TB-3.7500-3.7500-3.7500-特殊字符", 3.75, 3.75, 3.75)
]

# Create DataFrame
df = spark.createDataFrame(data, schema)

# Extract product size from description or use product_id as fallback
df = df.withColumn("product_size", 
                   when(col("product_description").rlike(r"(\d+\.\d+-\d+\.\d+-\d+\.\d+)"), 
                        regexp_extract(col("product_description"), r"(\d+\.\d+-\d+\.\d+-\d+\.\d+)", 0))
                   .otherwise(regexp_extract(col("product_id"), r"(\d+\.\d+-\d+\.\d+-\d+\.\d+)", 0)))

# Add timestamp column
df = df.withColumn("timestamp", current_timestamp())

# Define test class
class TestDatabricks(unittest.TestCase):

    def test_product_size_extraction(self):
        # Test product size extraction logic
        expected_sizes = ["3.7500-.3750-23.7000", "0.0001-0.0001-0.0001", "-1.0000--1.0000--1.0000", "", "3.7500-3.7500-3.7500"]
        actual_sizes = [row['product_size'] for row in df.collect()]
        self.assertEqual(expected_sizes, actual_sizes)

    def test_null_handling(self):
        # Test NULL handling
        null_row = df.filter(col("product_id") == "YRDMT-6061-T6511-TB-NULL-NULL-NULL").collect()[0]
        self.assertIsNone(null_row['dimension_1'])
        self.assertIsNone(null_row['dimension_2'])
        self.assertIsNone(null_row['dimension_3'])

    def test_timestamp_column(self):
        # Test timestamp column existence and type
        self.assertTrue('timestamp' in df.columns)
        self.assertEqual(df.schema['timestamp'].dataType, TimestampType())

# Run tests
if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)

# Cleanup operations
spark.stop()
