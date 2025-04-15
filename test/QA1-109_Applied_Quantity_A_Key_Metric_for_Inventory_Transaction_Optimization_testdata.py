from pyspark.sql import SparkSession
from pyspark.sql.types import StringType, DecimalType, StructType, StructField

# Create Spark session
spark = SparkSession.builder.appName("TestDataGeneration").getOrCreate()

# Define the schema for the target table
schema = StructType([
    StructField("txn_id", StringType(), True),
    StructField("ref_txn_qty", DecimalType(3, 1), True),
    StructField("cumulative_txn_qty", DecimalType(4, 1), True),
    StructField("cumulative_ref_ord_sched_qty", DecimalType(4, 1), True),
    StructField("ref_ord_sched_qty", DecimalType(3, 1), True),
    StructField("prior_cumulative_txn_qty", DecimalType(3, 1), True),
    StructField("prior_cumulative_ref_ord_sched_qty", DecimalType(3, 1), True),
    StructField("apl_qty", DecimalType(5, 1), True),
])

# Generate test data with varied scenarios

data = [
    # Happy path test data
    ("1", 50.0, 100.0, 90.0, 50.0, 40.0, 30.0, None), 
    
    # Edge cases with boundary conditions
    ("2", 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, None), # all zero values
    ("3", 999.9, 9999.9, 9999.9, 999.9, 999.9, 999.9, None), # max values
    
    # Error cases with invalid input scenarios
    ("4", -1.0, 100.0, 50.0, 25.0, 100.0, 200.0, None), # Negative ref_txn_qty with prior cumulative more than cumulative
    ("5", -20.0, 0.0, 80.0, 60.0, 60.0, 50.0, None), # Negative ref_txn_qty with zero cumulative_txn_qty
    
    # NULL handling scenarios
    ("6", None, 80.0, None, 40.0, 35.0, None, None), # NULL values in different fields
    
    # Special characters and multi-byte characters
    ("7", 20.0, 60.0, 100.0, 50.0, 30.0, 40.0, None), # Special character in txn_id
    ("8", 25.0, 70.0, 70.0, 20.0, 30.0, 25.0, None), # Normal scenario matching a condition
   
    # More diverse data points covering different potential scenarios
    ("9", 10.0, 60.0, 50.0, 30.0, 60.0, 30.0, None),
    ("10", 50.0, 120.0, 110.0, 15.0, 110.0, 100.0, None),
    ("11", 10.5, 20.5, 30.5, 10.5, 20.5, 30.5, None),
    ("12", -15.0, 35.0, 45.0, 40.0, 35.0, 20.0, None),
    ("13", None, None, None, None, None, None, None), # All NULL values
    
    # Additional testing scenarios for robustness
    ("14", 55.0, 75.0, 70.0, 60.0, 65.0, 60.0, None),
    ("15", 5.0, 0.0, 5.0, 5.0, 0.0, 5.0, None),
    ("16", -5.0, 15.0, 0.0, 20.0, 15.0, 0.0, None),
    ("17", 30.0, 60.0, 60.0, 30.0, 30.0, 30.0, None),
    ("18", 25.0, 25.0, 75.0, 25.0, 25.0, 25.0, None),
    ("19", -25.0, 75.0, 25.0, 25.0, 25.0, 75.0, None),
    ("20", None, 25.0, None, None, 25.0, None, None),
]

# Create DataFrame
df = spark.createDataFrame(data, schema)

# Show the generated test data
df.show(truncate=False)

