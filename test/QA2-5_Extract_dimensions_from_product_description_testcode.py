# Import required libraries for testing in Databricks environment
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, TimestampType
from pyspark.sql.functions import col, regexp_extract, when, current_timestamp
import unittest

# Create Spark session
spark = SparkSession.builder \
    .appName("Databricks Testing Environment") \
    .getOrCreate()

# Define the schema for the "product_desc" table
schema = StructType([
    StructField("product_id", StringType(), True),
    StructField("product_description", StringType(), True),
    StructField("dimension_1", DoubleType(), True),
    StructField("dimension_2", DoubleType(), True),
    StructField("dimension_3", DoubleType(), True)
])

# Sample test data as DataFrame
data = [
    ("YRDMT-6061-T6511-TB-3.7500-.3750-23.7000", "ALUM EXTRUDED ROUND TUBE - BAR - 1-Aluminum Bar - 6061-T6511-TB - 6061-T6511-TB-3.7500-.3750-23.7000", 3.75, 3, 0.375),
    ("YRDMT-7075-T73-TB-2.8750", "ALUMINUM EXTRUDED TUBING - BAR - 1-Aluminum Bar - 7075-T73-TB - 7075-T73-TB-2.8750", None, None, None),
    ("YRDMT-9999", "INVALID PRODUCT DESCRIPTION with no size info", None, None, None),
    ("YRDMT-6061-T6511-TB-4.5000-1.0000-104.1550", "ALUM EXTRUDED ROUND", 4.5, 1.0, 104.155)
]

# Create a DataFrame using the sample data and schema
df = spark.createDataFrame(data, schema=schema)

# Define a function to extract product size from product_description or product_id
def extract_product_size(product_id, product_description):
    # Attempt to extract size from product_description using regex pattern
    extracted_size = regexp_extract(product_description, r'(\d+\.\d+-\d+\.\d+-\d+\.\d+)', 0)
    # Fallback to extracting size from product_id if description extraction fails
    return when(col("product_description").isNull() | (extracted_size == ""), 
                regexp_extract(product_id, r'(\d+\.\d+-\d+\.\d+-\d+\.\d+|\d+\.\d+)', 0)).otherwise(extracted_size)

# Apply the function to add 'product_size' and 'timestemp' columns
df = df.withColumn("product_size", extract_product_size(col("product_id"), col("product_description"))) \
       .withColumn("timestemp", current_timestamp())

# Define unit tests
class TestProductSizeExtraction(unittest.TestCase):
    
    def test_product_size_extraction(self):
        # Validate successful extraction from description
        row = df.filter(df.product_id == "YRDMT-6061-T6511-TB-3.7500-.3750-23.7000").collect()[0]
        self.assertEqual(row.product_size, "3.7500-.3750-23.7000")

    def test_product_id_fallback(self):
        # Validate fallback extraction from product_id
        row = df.filter(df.product_id == "YRDMT-7075-T73-TB-2.8750").collect()[0]
        self.assertEqual(row.product_size, "2.8750")

    def test_invalid_description_handling(self):
        # Validate handling of invalid description with no product size
        row = df.filter(df.product_id == "YRDMT-9999").collect()[0]
        self.assertEqual(row.product_size, "")

    def test_null_handling_with_product_id(self):
        # Validate handling of null description with fallback to product_id
        row = df.filter(df.product_id == "YRDMT-6061-T6511-TB-4.5000-1.0000-104.1550").collect()[0]
        self.assertEqual(row.product_size, "4.5000-1.0000-104.1550")

# Run the tests
if __name__ == '__main__':
    unittest.main(argv=[''], verbosity=2, exit=False)
